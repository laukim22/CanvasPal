import requests


def get_assignments_with_grades(api_url, api_key, course_id):
    """
    Get detailed assignment grades for a specific course.
    """
    headers = {
        "Authorization": f"Bearer {api_key}"
    }

    # Get the current user's ID
    user_response = requests.get(
        f"{api_url}/api/v1/users/self",
        headers=headers
    )

    if user_response.status_code != 200:
        print(f"Error getting user information: {user_response.status_code}")
        print(user_response.text)
        return None

    user_id = user_response.json()["id"]

    # Get all assignments for the course
    assignments_response = requests.get(
        f"{api_url}/api/v1/users/{user_id}/courses/{course_id}/assignments",
        headers=headers
    )

    if assignments_response.status_code != 200:
        print(f"Error getting assignments: {assignments_response.status_code}")
        print(assignments_response.text)
        return None

    assignments = assignments_response.json()
    assignment_results = []

    # For each assignment, get the submission with grade
    for assignment in assignments:
        assignment_id = assignment["id"]
        submission_response = requests.get(
            f"{api_url}/api/v1/courses/{course_id}/assignments/{assignment_id}/submissions/{user_id}",
            headers=headers
        )

        if submission_response.status_code != 200:
            print(f"Error getting submission for assignment {assignment_id}: {submission_response.status_code}")
            continue

        submission = submission_response.json()

        assignment_results.append({
            "assignment_id": assignment_id,
            "assignment_name": assignment["name"],
            "points_possible": assignment["points_possible"],
            "grade": submission.get("grade"),
            "score": submission.get("score")
        })

    return assignment_results


def get_assignment_groups_with_grades(api_url, api_key, course_id):
    """
    Get assignment groups with their weights and grades.
    """
    headers = {
        "Authorization": f"Bearer {api_key}"
    }

    # Get the current user's ID
    user_response = requests.get(
        f"{api_url}/api/v1/users/self",
        headers=headers
    )

    if user_response.status_code != 200:
        print(f"Error getting user information: {user_response.status_code}")
        print(user_response.text)
        return None

    user_id = user_response.json()["id"]

    # Get all assignment groups for the course
    groups_response = requests.get(
        f"{api_url}/api/v1/courses/{course_id}/assignment_groups",
        headers=headers
    )

    if groups_response.status_code != 200:
        print(f"Error getting assignment groups: {groups_response.status_code}")
        print(groups_response.text)
        return None

    groups = groups_response.json()
    group_results = []

    for group in groups:
        group_id = group["id"]

        # Get assignments in this group
        assignments_response = requests.get(
            f"{api_url}/api/v1/courses/{course_id}/assignment_groups/{group_id}/assignments",
            headers=headers
        )

        if assignments_response.status_code != 200:
            print(f"Error getting assignments for group {group_id}: {assignments_response.status_code}")
            continue

        assignments = assignments_response.json()
        assignment_grades = []

        for assignment in assignments:
            assignment_id = assignment["id"]

            # Get the submission for this assignment
            submission_response = requests.get(
                f"{api_url}/api/v1/courses/{course_id}/assignments/{assignment_id}/submissions/{user_id}",
                headers=headers
            )

            if submission_response.status_code != 200:
                print(f"Error getting submission for assignment {assignment_id}: {submission_response.status_code}")
                continue

            submission = submission_response.json()

            assignment_grades.append({
                "assignment_id": assignment_id,
                "assignment_name": assignment["name"],
                "points_possible": assignment["points_possible"],
                "grade": submission.get("grade"),
                "score": submission.get("score")
            })

        group_results.append({
            "group_id": group_id,
            "group_name": group["name"],
            "group_weight": group.get("group_weight"),
            "assignments": assignment_grades
        })

    return group_results


def calculate_weighted_average(groups):
    """
    Calculate the weighted average grade based on assignment groups and their weights.
    """
    total_weight = 0
    weighted_score_sum = 0
    group_details = []

    for group in groups:
        weight = group.get('group_weight', 0) or 0
        assignments = group.get('assignments', [])

        total_points = 0
        earned_points = 0
        graded_assignments = 0  # Track how many assignments have grades

        for assignment in assignments:
            points_possible = assignment.get('points_possible')
            score = assignment.get('score')
            # Only include assignments that have been graded
            if points_possible is not None and score is not None:
                total_points += points_possible
                earned_points += score
                graded_assignments += 1

        if total_points > 0:
            group_average = earned_points / total_points
            group_percentage = group_average * 100

            # Only apply weight if the group has graded assignments
            if graded_assignments > 0:
                weighted_score_sum += group_average * weight
                total_weight += weight
        else:
            group_average = 0
            group_percentage = 0

        group_details.append({
            'name': group.get('group_name'),
            'weight': weight,
            'average': group_average,
            'percentage': group_percentage,
            'contribution': group_average * weight,
            'graded_assignments': graded_assignments
        })

    if total_weight > 0:
        weighted_average = weighted_score_sum / total_weight
    else:
        weighted_average = 0

    return {
        'weighted_average': weighted_average,
        'weighted_percentage': weighted_average * 100,
        'group_details': group_details
    }


def main():
    API_URL = "https://canvas.du.edu"
    API_KEY = "YOUR_API_KEY"

    # Get the course ID from user input
    course_id = input("Enter the course ID: ")

    print("\n--- CANVAS GRADE REPORT ---")
    print(f"Course ID: {course_id}")

    print("\n--- Detailed Assignment Information ---")
    assignments = get_assignments_with_grades(API_URL, API_KEY, course_id)
    if assignments:
        for assignment in assignments:
            print(f"Assignment: {assignment['assignment_name']}")
            print(f"  Points Possible: {assignment['points_possible']}")
            print(f"  Grade: {assignment['grade']}")
            print(f"  Score: {assignment['score']}")
            print()

    print("\n--- Assignment Groups Information ---")
    groups = get_assignment_groups_with_grades(API_URL, API_KEY, course_id)
    if groups:
        for group in groups:
            print(f"Group: {group['group_name']} (Weight: {group['group_weight']}%)")
            completed_assignments = 0
            total_assignments = len(group['assignments'])

            for assignment in group['assignments']:
                score_display = assignment['score'] if assignment['score'] is not None else "Not graded"
                print(f"  - {assignment['assignment_name']}: {score_display}/{assignment['points_possible']}")
                if assignment['score'] is not None:
                    completed_assignments += 1

            completion_percentage = (completed_assignments / total_assignments * 100) if total_assignments > 0 else 0
            print(
                f"  Completion: {completed_assignments}/{total_assignments} assignments ({completion_percentage:.1f}%)")
            print()

        # Calculate and display weighted average
        grade_calculation = calculate_weighted_average(groups)

        print("\n--- FINAL GRADE CALCULATION ---")
        print(f"Current Weighted Average: {grade_calculation['weighted_percentage']:.2f}%")
        print("\nBreakdown by Assignment Group:")
        for group in grade_calculation['group_details']:
            if group['graded_assignments'] > 0:
                print(f"  {group['name']} ({group['weight']}% of total):")
                print(f"    Group Average: {group['percentage']:.2f}%")
                print(f"    Contribution to Final Grade: {group['contribution']:.2f} points")
            else:
                print(f"  {group['name']} ({group['weight']}% of total): No graded assignments yet")
        print()

        letter_grade = determine_letter_grade(grade_calculation['weighted_percentage'])
        print(f"Current Letter Grade Equivalent: {letter_grade}")


def determine_letter_grade(percentage):
    """
    Convert percentage to letter grade based on standard grading scale.
    """
    if percentage >= 93:
        return "A"
    elif percentage >= 90:
        return "A-"
    elif percentage >= 87:
        return "B+"
    elif percentage >= 83:
        return "B"
    elif percentage >= 80:
        return "B-"
    elif percentage >= 77:
        return "C+"
    elif percentage >= 73:
        return "C"
    elif percentage >= 70:
        return "C-"
    elif percentage >= 67:
        return "D+"
    elif percentage >= 63:
        return "D"
    elif percentage >= 60:
        return "D-"
    else:
        return "F"


if __name__ == "__main__":
    main()
