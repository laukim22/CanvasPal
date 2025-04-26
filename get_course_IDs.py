#!/usr/bin/env python3
"""
Canvas API Course Listing Example
"""
from canvasapi import Canvas

from dotenv import load_dotenv
import os

load_dotenv() # chatgpt gave me this ok

API_URL = "https://canvas.du.edu"
API_KEY = os.getenv("API_KEY")


def get_course_IDs():
    canvas = Canvas(API_URL, API_KEY)

    try:
        # Get the current user
        user = canvas.get_current_user()

        # Retrieve all active courses for the user
        courses = user.get_favorite_courses()

        for course in courses:
            print(f"{course.name} (ID: {course.id})")


    except Exception as e:
        print(f"Error: {e}")

get_course_IDs()

