#!/usr/bin/env python3
"""
Canvas Assignment Description Tool

Fetches and displays the detailed description of a Canvas assignment.
"""
from canvasapi import Canvas
import sys
import re

# Try to import HTML parser libraries for better description rendering
try:
    from html.parser import HTMLParser
    from html import unescape

    HAS_HTML_PARSER = True
except ImportError:
    HAS_HTML_PARSER = False

API_URL = "https://canvas.du.edu"
API_TOKEN = "YOUR_API_TOKEN"


def strip_html_tags(html_text):
    """Remove HTML tags from a string and clean up whitespace"""
    if not html_text:
        return ""

    if HAS_HTML_PARSER:
        text = unescape(html_text)
        # Simple tag removal
        text = re.sub(r'<[^>]+>', ' ', text)
    else:
        # Basic regex-based approach as fallback
        text = html_text
        text = re.sub(r'<[^>]+>', ' ', text)

    # Clean up whitespace
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def get_assignment_description(course_id, assignment_id):
    """
    Fetches and returns an assignment description

    Args:
        course_id: The Canvas course ID
        assignment_id: The Canvas assignment ID

    Returns:
        Tuple of (assignment_object, formatted_description)
    """
    try:
        canvas = Canvas(API_URL, API_TOKEN)
        course = canvas.get_course(course_id)
        assignment = course.get_assignment(assignment_id)

        # Get raw description
        description = getattr(assignment, 'description', None)

        # Format the description
        if description:
            if '<' not in description and '>' not in description:
                formatted_description = description
            else:
                formatted_description = strip_html_tags(description)
        else:
            formatted_description = "No description available for this assignment."

        return {
            "assignment_name": assignment.name,
            "due_date": getattr(assignment, 'due_at', 'No due date'),
            "points": getattr(assignment, 'points_possible', 'Not specified'),
            "description": formatted_description,
            "url": getattr(assignment, 'html_url', None)
        }
    except Exception as e:
        print(f"Error fetching assignment: {e}", file=sys.stderr)
        return None
