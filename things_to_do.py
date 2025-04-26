#!/usr/bin/env python3
"""
Canvas Things To Do Tool

Lists all upcoming assignments and events from Canvas.
"""
from canvasapi import Canvas
import sys
from datetime import datetime
import re

API_URL = "https://canvas.du.edu"
API_TOKEN = "YOUR_API_TOKEN"


def get_upcoming_assignments(days_filter=None, course_filter=None):
    """
    Get upcoming assignments from Canvas

    Args:
        days_filter: Only show assignments due within this many days
        course_filter: Only show assignments from specific course ID

    Returns:
        List of processed assignment data
    """
    canvas = Canvas(API_URL, API_TOKEN)

    try:
        print("Fetching your upcoming Canvas events...")
        events = canvas.get_upcoming_events()

        if not events:
            return []

        # Process the events
        assignment_data = []
        course_cache = {}  # Cache for course objects

        for event in events:
            # Extract event details
            title = event.get('title', 'Unnamed Event')

            # Handle date formatting
            start_at = event.get('start_at', None)
            if start_at:
                try:
                    start_date = datetime.strptime(start_at, "%Y-%m-%dT%H:%M:%SZ")
                    formatted_date = start_date.strftime("%Y-%m-%d %H:%M")
                    days_until = (start_date - datetime.now()).days

                    # Skip if outside the days filter
                    if days_filter is not None and days_until > days_filter:
                        continue

                    if days_until == 0:
                        due_status = "Today!"
                    elif days_until == 1:
                        due_status = "Tomorrow!"
                    elif days_until > 1:
                        due_status = f"In {days_until} days"
                    else:
                        due_status = "Overdue!"
                except (ValueError, TypeError):
                    formatted_date = "Unknown date"
                    due_status = ""
            else:
                formatted_date = "No due date"
                due_status = ""

            # Extract course information
            context_code = event.get('context_code', '')
            course_name = "Unknown Course"
            course_id = None

            if context_code.startswith('course_'):
                course_id = context_code.split('_')[1]

                # Skip if not matching course filter
                if course_filter and str(course_filter) != course_id:
                    continue

                # Use cached course object if available, otherwise fetch it
                if course_id in course_cache:
                    course_obj = course_cache[course_id]
                else:
                    try:
                        course_obj = canvas.get_course(course_id)
                        course_cache[course_id] = course_obj
                    except Exception:
                        course_obj = None

                if course_obj:
                    course_name = getattr(course_obj, 'name',
                                          getattr(course_obj, 'course_code', f"Course {course_id}"))
                else:
                    course_name = f"Course {course_id}"

            # Get HTML URL if available
            html_url = event.get('html_url', '')

            # Try to extract assignment ID from URL if it's an assignment URL
            assignment_id = None
            if html_url and '/assignments/' in html_url:
                try:
                    # Look for assignment ID pattern in URL
                    match = re.search(r'/assignments/(\d+)', html_url)
                    if match:
                        assignment_id = match.group(1)
                except:
                    assignment_id = None

            # Store assignment metadata
            assignment_info = {
                'id': assignment_id,
                'course_id': course_id,
                'title': title,
                'due_date': formatted_date,
                'due_status': due_status,
                'course_name': course_name,
                'html_url': html_url
            }
            assignment_data.append(assignment_info)

        # Sort by date
        assignment_data.sort(key=lambda x: x['due_date'])

        return assignment_data

    except Exception as e:
        print(f"Error retrieving upcoming events: {e}", file=sys.stderr)
        return []
