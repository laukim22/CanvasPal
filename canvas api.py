#!/usr/bin/env python3
"""
Canvas API Course Listing Example
"""
from canvasapi import Canvas

API_URL = "https://canvas.du.edu"
API_KEY = "1565~e2hZ6naaBDtwPW8v8vYMZfHGFTk2tVcRCKB7fGfEUvnhK8fM6aYKHhWvaYmKBFAZ"


def main():
    canvas = Canvas(API_URL, API_KEY)

    try:
        # Get the current user
        user = canvas.get_current_user()

        # Retrieve all active courses for the user
        courses = user.get_courses(enrollment_state=['active'])

        print(f"Active courses for {user.name}:")
        for i, course in enumerate(courses, 1):
            print(f"{i}. {course.name} (ID: {course.id})")
                    
            # You can access additional course properties
            if hasattr(course, 'course_code'):
                print(f"   Course Code: {course.course_code}")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()