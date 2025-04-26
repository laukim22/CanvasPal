from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from canvasapi import Canvas

API_URL   = "https://canvas.du.edu"
API_TOKEN = "your token"

def get_todo_list():
    """
    Fetch unsubmitted assignments across all of the current user's courses,
    compute time until due, and return them sorted by due date.
    """
    canvas = Canvas(API_URL, API_TOKEN)
    user   = canvas.get_current_user()    
    current_courses = user.get_favorite_courses()           

    mtn_zone = ZoneInfo("America/Denver")
    now = datetime.now(timezone.utc)             
    due_list = []

    for course in current_courses:
        # Only assignments not yet submitted
        assignments = course.get_assignments(
            bucket='unsubmitted',                
            include=['submission']               
        )

        for asg in assignments:  
            due_str = asg.due_at                 
            if not due_str:
                continue

            try:
                if due_str.endswith('Z'):
                    due_dt = datetime.fromisoformat(due_str.replace('Z', '+00:00'))
                else:
                    due_dt = datetime.fromisoformat(due_str)
            except ValueError:
                due_dt = datetime.strptime(due_str, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)

            due_dt = due_dt.astimezone(mtn_zone)
            # and overwrite due_str with a nicely formatted MTN timestamp
            due_str = due_dt.strftime("%Y-%m-%d %H:%M %Z")

            delta = due_dt - now
            days  = delta.days

            if delta.total_seconds() < 0:
                status = "Overdue!"
            elif days == 0:
                status = "Today!"
            elif days == 1:
                status = "Tomorrow!"
            else:
                status = f"In {days} days"

            due_list.append({
                "course":    course.name,
                "id":        asg.id,
                "name":      asg.name,
                "due_at":    due_str,
                "days":      days,
                "status":    status,
                "html_url":  asg.html_url
            })
    
    due_list.sort(key=lambda x: x["due_at"])
    
    print(f"\nFound {len(due_list)} unsubmitted assignments:\n")
    print(f"{'Course':<30} {'Assignment':<40} {'Due':<20} {'Status':<10}")
    print("-" * 110)
    for a in due_list:
        print(f"{a['course']:<30} {a['name']:<40} {a['due_at']:<20} {a['status']:<10}")
        print(f"  Link: {a['html_url']}")

get_todo_list()