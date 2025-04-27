import requests
from dotenv import load_dotenv
import os
from canvasapi import Canvas

load_dotenv()

API_KEY = os.getenv("API_KEY")
COURSE_ID = "190476"
BASE_URL = 'https://canvas.du.edu'

def get_people_in_course(COURSE_ID: str)->list:
    """
    Takes the course ID as a string,
    returns a list of the students in the course.
    """
    canvas = Canvas(BASE_URL, API_KEY)

    course = canvas.get_course(COURSE_ID)
    students = course.get_users(enrollment_type=["student"])
    tas = course.get_users(enrollment_type=["ta"])
    professors = course.get_users(enrollment_type=["teacher"])


    for student in students:
        print(f"{student}: Student")
    for ta in tas:
        print(f"{ta}: TA")
    for professor in professors:
        print(f"{professor}: Professor")

get_people_in_course(COURSE_ID)