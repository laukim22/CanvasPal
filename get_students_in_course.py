import requests
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("API_KEY")
COURSE_ID = "COURSE_ID"
BASE_URL = 'https://canvas.du.edu/api/v1/'

headers = {
        'Authorization': f'Bearer {API_KEY}'
    }

def get_students_in_course(COURSE_ID: str)->list:
    """
    Takes the course ID as a string,
    returns a list of the students in the course.
    """
    
    url = f'{BASE_URL}courses/{COURSE_ID}/students'

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        # Convert JSON response into a Python dictionary
        data = response.json()
        
        students =[] #instantiate list of students

        # Access the 'name' field
        for item in data:
            name = item['name']
            # print(f'{name}')
            students.append(name)
        
        # print(f"These are the students in your course: {students}")
    else:
        return ImportError(f"Failed to retrieve data. Status code: {response.status_code}") #idk if right error

    return students

print(get_students_in_course(COURSE_ID))