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

def retrieve_files(course_id: int):
    canvas = Canvas(API_URL, API_KEY)

    try:
        # Get the current user
        user = canvas.get_current_user()       

            
        # You can access additional course properties
        files = user.get_files()  # Get files for the first course

        for i, file in enumerate(files, 1):
            print(f"{i}. {file} (ID: {file.id})")
            print(f"   File URL: {file.url}")
            

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    course_id = 184658
    retrieve_files(course_id)

