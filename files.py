#!/usr/bin/env python3
"""
Canvas API Course File Listing Example
"""
import requests
from canvasapi import Canvas
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
# Auth headers for direct requests


def retrieve_files(API_URL, API_KEY, course_id):
    headers = {
    "Authorization": f"Bearer {API_KEY}"
    }
    # Get the current user's ID
    user_response = requests.get(
        f"{API_URL}/api/v1/users/self",
        headers=headers
    )

    if user_response.status_code != 200:
        print(f"Error getting user information: {user_response.status_code}")
        print(user_response.text)
        return None

    user_id = user_response.json()["id"]

    try:

        # Fetch and display files from the specified course
        file_list_url = f"{API_URL}/api/v1/courses/{course_id}/files"
        file_response = requests.get(file_list_url, headers=headers)


        # Handle bad responses
        if file_response.status_code != 200:
            print(f"Failed to fetch files. Status: {file_response.status_code}")
            return

        files = file_response.json()

        if not files:
            print("No files found.")
            return

        print(f"\nFiles for Course ID {course_id}:")
        for idx, file in enumerate(files, 1):
            print(f"{idx}. {file['display_name']} (ID: {file['id']})")
            print(f"    File URL: {file['url']}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    API_URL = "https://canvas.du.edu"
    API_KEY = os.getenv("API_KEY")
    course_id = input("Enter the course ID: ")
    retrieve_files(API_URL, API_KEY, course_id)
