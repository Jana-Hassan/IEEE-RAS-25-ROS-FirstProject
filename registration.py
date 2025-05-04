# registration

from course_data import course_db  # Import or call function course

def register_course(student, course_id):
    if course_id not in course_db:
        print("Invalid course.")
        return

    required_level = course_db[course_id]
    if student.level < required_level:
        print(f"Cannot register for {course_id}. It requires level {required_level}.")
        return

    if len(student.courses) >= 7:
        print("Course limit reached. Max is 7.")
        return

    if course_id in student.courses:
        print(f"Already registered in {course_id}.")
    else:
        student.courses.append(course_id)
        print(f"Course {course_id} registered successfully.")