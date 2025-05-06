from datetime import datetime
import json

class Attendance:
    def __init__(self):
        self.attendance_marked = False

    #mark attendance of a student in a specific course in Professor mode
    def mark_attendance(self, student, course_id, is_present):
        self.attendance_marked = False
        if not student:
            print("Student not found!")
            return

        if course_id not in student.courses:
            print("Student not enrolled in this course!")
            return

        # Load current data
        try:
            with open('data.json', 'r') as f:
                data = json.load(f)
        except Exception as e:
            print(f"Error reading data: {e}")
            return False

        # Initialize attendance list if it doesn't exist
        if 'attendance' not in student.courses[course_id]:
            student.courses[course_id]['attendance'] = []

        date = datetime.now().strftime("%Y-%m-%d")
        attendance_record = {
            'date': date,
            'present': is_present
        }

        # Check if attendance already marked for today
        today_attendance = [record for record in student.courses[course_id]['attendance'] 
                          if record['date'] == date]
        if today_attendance:
            print(f"Attendance for {student.name} already marked for today ({date})")
            return False

        # Update student's attendance in memory and data
        student.courses[course_id]['attendance'].append(attendance_record)
        data['students'][student.student_id]['courses'][course_id]['attendance'].append(attendance_record)

        # Update course's student attendance
        if student.student_id in data['courses'][course_id]['students']:
            if 'attendance' not in data['courses'][course_id]['students'][student.student_id]:
                data['courses'][course_id]['students'][student.student_id]['attendance'] = []
            data['courses'][course_id]['students'][student.student_id]['attendance'].append(attendance_record)

        # Save updated data
        try:
            with open('data.json', 'w') as f:
                json.dump(data, f, indent=4)
            status = "present" if is_present else "absent"
            print(f"Marked {student.name} as {status} on {date}")
            self.attendance_marked = True
            return True
        except Exception as e:
            print(f"Error saving data: {e}")
            return False

    #track attendance of a student in a specific course in student mode
    def track_attendance(self, student, course_id):
        self.attendance_marked = False
        if not student:
            print("Student not found!")
            return None

        if course_id not in student.courses:
            print("Student not enrolled in this course!")
            return None

        # Load current data to get the latest attendance
        try:
            with open('data.json', 'r') as f:
                data = json.load(f)
                attendance = data['students'][student.student_id]['courses'][course_id].get('attendance', [])
        except Exception as e:
            print(f"Error reading data: {e}")
            return None

        if not attendance:
            print("No attendance records found")
            return None

        return attendance

    def get_student_attendance(self, course, student_id):
        """Get attendance records for a student in a course"""
        if student_id not in course.students:
            print(f"Student with ID {student_id} is not enrolled in this course.")
            return None

        # Load current data to get the latest attendance
        try:
            with open('data.json', 'r') as f:
                data = json.load(f)
                attendance = data['courses'][course.course_id]['students'][student_id].get('attendance', [])
        except Exception as e:
            print(f"Error reading data: {e}")
            return None

        if not attendance:
            print("No attendance records found")
            return None

        self.attendance_marked = True
        return attendance
