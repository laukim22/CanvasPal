from datetime import datetime, timezone
from canvasapi import Canvas

API_URL = "https://canvas.du.edu"
API_TOKEN = "Your Token"

from datetime import datetime, timezone
from canvasapi import Canvas

def get_unsubmitted_due_assignments(course_id: int):
    """
    Fetch only unsubmitted assignments for a course, compute time until due,
    and return them sorted by due date.

    :param canvas: Authenticated Canvas object
    :param course_id: ID of the course to inspect
    :return: List of dicts with keys: id, name, due_at, days_until, status, html_url
    """
    canvas = Canvas(API_URL, API_TOKEN)
    
    # 1. Retrieve the course
    course = canvas.get_course(course_id)  # GET /api/v1/courses/:course_id :contentReference[oaicite:2]{index=2}

    # 2. List only assignments not yet submitted
    assignments = course.get_assignments(bucket='unsubmitted', include=['submission'])  
    # ‘bucket’ filters by submission status; ‘unsubmitted’ returns only missing assignments :contentReference[oaicite:3]{index=3} :contentReference[oaicite:4]{index=4}

    now = datetime.now(timezone.utc)
    due_list = []

    for asg in assignments:
        due_str = asg.due_at  # ISO 8601 timestamp or None :contentReference[oaicite:5]{index=5}
        if not due_str:
            # Skip undated assignments
            continue

        # Parse ISO 8601 “Z”-terminated UTC string into datetime
        # Python 3.11+: datetime.fromisoformat handles the 'Z' suffix; for earlier versions, strip 'Z' :contentReference[oaicite:6]{index=6}
        try:
            if due_str.endswith('Z'):
                due_dt = datetime.fromisoformat(due_str.replace('Z', '+00:00'))
            else:
                due_dt = datetime.fromisoformat(due_str)
        except ValueError:
            # Fallback to strptime if necessary :contentReference[oaicite:7]{index=7}
            due_dt = datetime.strptime(due_str, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)

        delta = due_dt - now
        days = delta.days

        if delta.total_seconds() < 0:
            status = "Overdue!"
        elif days == 0:
            status = "Today!"
        elif days == 1:
            status = "Tomorrow!"
        else:
            status = f"In {days} days"

        due_list.append([
            asg.name,
            status,
            asg.html_url,
            due_str
        ])

    # Sort by due-date string (ISO 8601 sorts lexically by date) :contentReference[oaicite:8]{index=8}
    due_list.sort(key=lambda x: x[3])
    
    print ((f"\nFound {len(due_list)} unsubmitted assignments:"))
    print()

    print(f"{'Assignment':<16} {'Due':<12}")
    print("-" * 110)
    for assignments in due_list:
        print(f"{assignments[0]:<16} \t {assignments[1]:<12}")
        print(f"Link: {assignments[2]}")

