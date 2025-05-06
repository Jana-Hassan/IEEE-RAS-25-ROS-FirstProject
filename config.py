import os

# File paths
DATA_FILE = 'data.json'

# College settings
COLLEGES = {
    'Engineering': '00',
    'Computer Science': '01',
    'Medicine': '02',
    'Business': '03'
}

# Department settings
DEPARTMENTS = {
    'Engineering': {
        'Mechatronics': 'm00',
        'Mechanical': 'me00',
        'Electrical': 'el00',
        'Civil': 'ce00'
    },
    'Computer Science': {
        'Computer Science': 'cs01',
        'Information Technology': 'it01'
    },
    'Medicine': {
        'General Medicine': 'gm02',
        'Pharmacy': 'ph02',
        'Dentistry': 'dt02',
        'Nursing': 'nr02'
    },
    'Business': {
        'Business Administration': 'ba03',
        'Accounting': 'ac03',
        'Finance': 'fi03',
        'Marketing': 'mk03'
    }
}

# Course settings
COURSE_LEVELS = ['1', '2', '3', '4']
MAX_COURSES = 7

# Course IDs by Department
COURSE_IDS = {
    "Information Technology": {
        "it1": "Introduction to Programming",
        "it2": "Web Development",
        "it3": "Database Systems",
        "it4": "Network Security",
        "cs1": "Machine Learning",
        "cs2": "Artificial Intelligence",
        "cs3": "Operating Systems",
        "cs4": "Computer Networks"
    },
    "Mechatronics": {
        "mt1": "Introduction to Robotics",
        "mt2": "Control Systems",
        "mt3": "Industrial Automation",
        "mt4": "Embedded Systems"
    },
    "General Medicine": {
        "gm1": "Anatomy",
        "gm2": "Physiology",
        "gm3": "Pathology",
        "gm4": "Clinical Skills"
    },
    "Marketing": {
        "mk1": "Marketing Principles",
        "mk2": "Consumer Behavior",
        "mk3": "Digital Marketing",
        "mk4": "Brand Management"
    }
}

# Grade settings
GRADE_SCALE = {
    "A+": 4.0, "A": 4.0, "A-": 3.7,
    "B+": 3.3, "B": 3.0, "B-": 2.7,
    "C+": 2.3, "C": 2.0, "C-": 1.7,
    "D+": 1.3, "D": 1.0, "F": 0.0
}

# Menu options
MAIN_MENU = {
    "1": "Student Interface",
    "2": "Professor Interface",
    "3": "Admin Interface",
    "0": "Exit"
}

STUDENT_MENU = {
    "1": "Register for Course",
    "2": "View Grades",
    "3": "View Attendance",
    "4": "Calculate GPA",
    "0": "Back to Main Menu"
}

PROFESSOR_MENU = {
    "1": "Assign Grade",
    "2": "Mark Attendance",
    "3": "View Course Students",
    "0": "Back to Main Menu"
}

ADMIN_MENU = {
    "1": "Add Student",
    "2": "Add Professor",
    "3": "Add Course",
    "4": "Remove Student",
    "5": "Remove Professor",
    "6": "Remove Course",
    "0": "Back to Main Menu"
}