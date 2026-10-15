
import sqlite3

# ==========================================
# UNIVERSITY SUBJECT REGISTRATION SYSTEM
# ==========================================

DATABASE = "university.db"


# ==========================================
# DATABASE CONNECTION
# ==========================================

def connect_db():
    conn = sqlite3.connect(DATABASE)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


# ==========================================
# CREATE DATABASE TABLES
# ==========================================

def setup_database():
    with connect_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS students (
                student_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                programme TEXT NOT NULL
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS subjects (
                subject_code TEXT PRIMARY KEY,
                subject_name TEXT NOT NULL,
                credits INTEGER NOT NULL,
                capacity INTEGER NOT NULL
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS registrations (
                student_id TEXT NOT NULL,
                subject_code TEXT NOT NULL,
                registration_date TIMESTAMP
                    DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (student_id, subject_code),
                FOREIGN KEY (student_id)
                    REFERENCES students(student_id),
                FOREIGN KEY (subject_code)
                    REFERENCES subjects(subject_code)
            )
        """)

        subjects = [
            ("CSC101", "Introduction to Python", 3, 30),
            ("DBS201", "Database Management", 3, 25),
            ("STA210", "Business Statistics", 3, 35),
            ("WEB220", "Web Development", 3, 30),
            ("DSC301", "Data Analytics", 4, 25),
            ("AI310", "Artificial Intelligence", 4, 20),
            ("NET205", "Computer Networking", 3, 30),
            ("SYS210", "Systems Analysis and Design", 3, 30)
        ]

        conn.executemany("""
            INSERT OR IGNORE INTO subjects
            (subject_code, subject_name, credits, capacity)
            VALUES (?, ?, ?, ?)
        """, subjects)


# ==========================================
# INPUT AND BACK OPTION
# ==========================================

class BackToMenu(Exception):
    pass


def get_input(message):
    value = input(message + " (B = Back): ").strip()

    if value.upper() == "B":
        raise BackToMenu

    return value


def get_student_id():
    while True:
        student_id = get_input("Enter Student ID")

        if not student_id:
            print("ERROR: Student ID cannot be empty.")
        elif not student_id.isascii() or not student_id.isdigit():
            print("ERROR: Student ID must contain numbers only!")
            print("Example: 24131682")
        else:
            return student_id


def get_positive_number(message):
    while True:
        value = get_input(message)

        try:
            number = int(value)

            if number <= 0:
                print("ERROR: Enter a number greater than zero.")
            else:
                return number

        except ValueError:
            print("ERROR: Please enter a valid number.")


def get_required_input(message):
    while True:
        value = get_input(message)

        if value:
            return value

        print("ERROR: This field cannot be empty.")


# ==========================================
# ADD STUDENT
# ==========================================

def add_student():
    print("\n--- ADD NEW STUDENT ---")

    student_id = get_student_id()
    name = get_required_input("Full Name")
    email = get_required_input("Email")
    programme = get_required_input("Programme")

    if "@" not in email or "." not in email.split("@")[-1]:
        print("ERROR: Invalid email address.")
        return

    try:
        with connect_db() as conn:
            conn.execute("""
                INSERT INTO students
                (student_id, name, email, programme)
                VALUES (?, ?, ?, ?)
            """, (student_id, name, email, programme))

        print("\nSUCCESS: Student added successfully!")

    except sqlite3.IntegrityError:
        print("\nERROR: Student ID or email already exists.")


# ==========================================
# VIEW STUDENTS
# ==========================================

def view_students():
    with connect_db() as conn:
        students = conn.execute("""
            SELECT student_id, name, email, programme
            FROM students
            ORDER BY name
        """).fetchall()

    print("\n--- STUDENT LIST ---")

    if not students:
        print("No students found.")
        return

    for student in students:
        print("-" * 45)
        print(f"Student ID : {student[0]}")
        print(f"Name       : {student[1]}")
        print(f"Email      : {student[2]}")
        print(f"Programme  : {student[3]}")


# ==========================================
# VIEW AVAILABLE SUBJECTS
# ==========================================

def view_subjects():
    with connect_db() as conn:
        subjects = conn.execute("""
            SELECT s.subject_code, s.subject_name,
                   s.credits, s.capacity,
                   COUNT(r.student_id) AS enrolled
            FROM subjects s
            LEFT JOIN registrations r
                ON s.subject_code = r.subject_code
            GROUP BY s.subject_code
            ORDER BY s.subject_code
        """).fetchall()

    print("\n--- AVAILABLE SUBJECTS ---")
    print(f"{'Code':<10} {'Subject':<32} {'Credits':<8} {'Seats':<8}")
    print("-" * 65)

    for code, name, credits, capacity, enrolled in subjects:
        seats = capacity - enrolled
        print(f"{code:<10} {name:<32} {credits:<8} {seats:<8}")


# ==========================================
# REGISTER SUBJECT
# ==========================================

def register_subject():
    print("\n--- SUBJECT REGISTRATION ---")

    student_id = get_student_id()
    subject_code = get_required_input("Subject Code").upper()

    with connect_db() as conn:
        student = conn.execute("""
            SELECT student_id FROM students
            WHERE student_id = ?
        """, (student_id,)).fetchone()

        if not student:
            print("\nERROR: Student ID not found!")
            print("Please add the student first.")
            return

        subject = conn.execute("""
            SELECT capacity FROM subjects
            WHERE subject_code = ?
        """, (subject_code,)).fetchone()

        if not subject:
            print("\nERROR: Invalid Subject Code!")
            print("Please select a subject from the list.")
            return

        existing = conn.execute("""
            SELECT 1 FROM registrations
            WHERE student_id = ? AND subject_code = ?
        """, (student_id, subject_code)).fetchone()

        if existing:
            print("\nERROR: Already registered for this subject!")
            return

        enrolled = conn.execute("""
            SELECT COUNT(*) FROM registrations
            WHERE subject_code = ?
        """, (subject_code,)).fetchone()[0]

        if enrolled >= subject[0]:
            print("\nERROR: Subject is full!")
            print("No seats are currently available.")
            return

        conn.execute("""
            INSERT INTO registrations
            (student_id, subject_code)
            VALUES (?, ?)
        """, (student_id, subject_code))

    print("\nSUCCESS: Subject registered successfully!")


# ==========================================
# VIEW REGISTERED SUBJECTS
# ==========================================

def view_registrations():
    print("\n--- MY REGISTERED SUBJECTS ---")

    student_id = get_student_id()

    with connect_db() as conn:
        student = conn.execute("""
            SELECT name FROM students
            WHERE student_id = ?
        """, (student_id,)).fetchone()

        if not student:
            print("ERROR: Student ID not found.")
            return

        subjects = conn.execute("""
            SELECT s.subject_code, s.subject_name,
                   s.credits, r.registration_date
            FROM registrations r
            JOIN subjects s
                ON r.subject_code = s.subject_code
            WHERE r.student_id = ?
            ORDER BY s.subject_code
        """, (student_id,)).fetchall()

    print(f"\nStudent: {student[0]}")
    print("-" * 45)

    if not subjects:
        print("No subjects registered.")
        return

    total_credits = 0

    for code, name, credits, date in subjects:
        print(f"\nSubject: {code} - {name}")
        print(f"Credits: {credits}")
        print(f"Registered on: {date}")
        total_credits += credits

    print("\n" + "-" * 45)
    print(f"Total Registered Subjects: {len(subjects)}")
    print(f"Total Credits: {total_credits}")


# ==========================================
# DROP SUBJECT
# ==========================================

def drop_subject():
    print("\n--- DROP SUBJECT ---")

    student_id = get_student_id()
    subject_code = get_required_input("Subject Code").upper()

    with connect_db() as conn:
        result = conn.execute("""
            DELETE FROM registrations
            WHERE student_id = ? AND subject_code = ?
        """, (student_id, subject_code))

        deleted = result.rowcount

    if deleted:
        print("\nSUCCESS: Subject dropped successfully!")
    else:
        print("\nERROR: Registration not found.")


# ==========================================
# ADD NEW SUBJECT
# ==========================================

def add_subject():
    print("\n--- ADD NEW SUBJECT ---")

    code = get_required_input("Subject Code").upper()
    name = get_required_input("Subject Name")
    credits = get_positive_number("Credit Hours")
    capacity = get_positive_number("Class Capacity")

    try:
        with connect_db() as conn:
            conn.execute("""
                INSERT INTO subjects
                (subject_code, subject_name, credits, capacity)
                VALUES (?, ?, ?, ?)
            """, (code, name, credits, capacity))

        print("\nSUCCESS: Subject added successfully!")

    except sqlite3.IntegrityError:
        print("\nERROR: Subject code already exists.")


# ==========================================
# VIEW ALL REGISTRATIONS
# ==========================================

def all_registrations():
    with connect_db() as conn:
        records = conn.execute("""
            SELECT st.student_id, st.name,
                   s.subject_code, s.subject_name,
                   r.registration_date
            FROM registrations r
            JOIN students st
                ON r.student_id = st.student_id
            JOIN subjects s
                ON r.subject_code = s.subject_code
            ORDER BY st.name
        """).fetchall()

    print("\n--- ALL REGISTRATIONS ---")

    if not records:
        print("No registrations found.")
        return

    for student_id, name, code, subject, date in records:
        print("-" * 50)
        print(f"Student ID : {student_id}")
        print(f"Student    : {name}")
        print(f"Subject    : {code} - {subject}")
        print(f"Date       : {date}")


# ==========================================
# MAIN MENU
# ==========================================

def main():
    setup_database()

    while True:
        print("\n" + "=" * 55)
        print("       UNIVERSITY SUBJECT REGISTRATION SYSTEM")
        print("=" * 55)

        print("1. Add Student")
        print("2. View Students")
        print("3. View Available Subjects")
        print("4. Register Subject")
        print("5. View My Registered Subjects")
        print("6. Drop Subject")
        print("7. Add New Subject")
        print("8. View All Registrations")
        print("9. Exit")

        choice = input("\nEnter your choice (1-9): ").strip()

        actions = {
            "1": add_student,
            "2": view_students,
            "3": view_subjects,
            "4": register_subject,
            "5": view_registrations,
            "6": drop_subject,
            "7": add_subject,
            "8": all_registrations
        }

        if choice == "9":
            print("\nThank you for using UniReg!")
            break

        elif choice in actions:
            try:
                actions[choice]()

            except BackToMenu:
                print("\nReturning to Main Menu...")

        else:
            print("\nERROR: Invalid choice! Please select 1-9.")


# ==========================================
# START APPLICATION
# ==========================================

if __name__ == "__main__":
    main()

