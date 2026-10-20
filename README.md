# University Subject Registration System

A command-line University Subject Registration System developed using **Python and SQLite**. The application allows users to manage student records, register students for university subjects, monitor available seats, and maintain subject registration records.

The project demonstrates Python programming, relational database management, input validation, error handling, and SQL operations.

## Features

### 1. Student Management
- Add new students with a Student ID, name, email, and programme.
- Validate Student IDs to ensure they contain numbers only.
- Check for invalid email formats.
- Prevent duplicate Student IDs and email addresses.
- View all registered students.

### 2. Subject Management
- Display available university subjects.
- View subject codes, names, credit hours, and remaining seats.
- Add new subjects with a specified class capacity.
- Prevent duplicate subject codes.

### 3. Subject Registration
- Register students for available subjects.
- Verify that a student exists before registration.
- Reject invalid subject codes.
- Prevent duplicate subject registrations.
- Prevent registration when a subject has reached maximum capacity.
- Store registration dates automatically.

### 4. Subject Withdrawal
- Allow students to drop registered subjects using their Student ID and subject code.
- Display an error if the registration does not exist.
- Update available seats automatically after withdrawal.

### 5. Registration Reports
- View subjects registered by a particular student.
- Display subject names, credit hours, and registration dates.
- Calculate total registered subjects and credit hours.
- View all student registrations.

### 6. Input Validation and Error Handling
- Validate numeric Student IDs.
- Reject empty required fields.
- Validate positive numeric inputs for credit hours and class capacity.
- Display error messages for invalid operations.
- Allow users to enter `B` to return to the main menu.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Application logic and input validation |
| SQLite | Relational database management |
| sqlite3 | Database connectivity and SQL operations |
| Python IDLE | Development and execution |

## Database Structure

The system uses three relational database tables:

**Students**
- Student ID (Primary Key)
- Name
- Email (Unique)
- Programme

**Subjects**
- Subject Code (Primary Key)
- Subject Name
- Credits
- Capacity

**Registrations**
- Student ID (Foreign Key)
- Subject Code (Foreign Key)
- Registration Date
- Composite Primary Key (Student ID, Subject Code)

Foreign key constraints maintain relationships between students, subjects, and registrations.

## How to Run

1. Install Python 3.
2. Download or clone this GitHub repository.
3. Open `Project 1.py` in Python IDLE or another Python editor.
4. Press **F5** in IDLE, or run the following command in your terminal:

```bash
python "Project 1.py"
```

5. Follow the on-screen menu to manage students and subject registrations.

The application automatically creates a local SQLite database named `university.db` when executed.

## Main Menu

```text
=======================================================
       UNIVERSITY SUBJECT REGISTRATION SYSTEM
=======================================================

1. Add Student
2. View Students
3. View Available Subjects
4. Register Subject
5. View My Registered Subjects
6. Drop Subject
7. Add New Subject
8. View All Registrations
9. Exit
```

## Example Error Messages

```text
ERROR: Student ID must contain numbers only!

ERROR: Invalid email address.

ERROR: Student ID or email already exists.

ERROR: Student ID not found!

ERROR: Invalid Subject Code!

ERROR: Already registered for this subject!

ERROR: Subject is full!

ERROR: Registration not found.

ERROR: Subject code already exists.
```

## Project Structure

```text
University-Subject-Registration-System/
├── Project 1.py
├── README.md
└── .gitignore
```

The `university.db` file is generated locally and should be excluded from GitHub when it contains student information.

## Future Improvements

- Student login and password authentication.
- Administrator and student dashboards.
- Programme-based subject eligibility.
- A graphical interface using Flask.
- Subject withdrawal confirmation.
- Semester-based subject registration.
- Timetable clash detection.
- Password recovery and account management.

## Project Status

**Functional command-line prototype** developed as an educational Python and SQLite project.

## Developer

**Ania Ahmed**

Bachelor of Information Systems (Hons), Data Analytics

Sunway University, Malaysia

