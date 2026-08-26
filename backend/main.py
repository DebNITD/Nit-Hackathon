from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
from datetime import datetime

app = FastAPI(
    title="Metrify API",
    description="Online Verification System for Weighing and Measuring Instruments",
    version="1.0"
)

# Allow our frontend to communicate with the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------
# DATABASE
# ---------------------------------------------------

def get_db():
    connection = sqlite3.connect("Database/database.db")
    connection.row_factory = sqlite3.Row
    connection.autocommit = True
    return connection


def create_tables():
    db = get_db()

    db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            role TEXT NOT NULL
        )
    """)

    db.execute("""
        CREATE TABLE IF NOT EXISTS instruments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            owner_id INTEGER NOT NULL,
            instrument_type TEXT NOT NULL,
            manufacturer TEXT,
            model TEXT,
            serial_number TEXT UNIQUE NOT NULL,
            capacity REAL,
            location TEXT,
            status TEXT DEFAULT 'REGISTERED',
            created_at TEXT
        )
    """)

    db.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            instrument_id INTEGER NOT NULL,
            owner_id INTEGER NOT NULL,
            application_type TEXT NOT NULL,
            preferred_date TEXT,
            status TEXT DEFAULT 'SUBMITTED',
            created_at TEXT
        )
    """)

    db.execute("""
        CREATE TABLE IF NOT EXISTS assignments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            application_id INTEGER NOT NULL,
            officer_id INTEGER NOT NULL,
            scheduled_date TEXT,
            status TEXT DEFAULT 'ASSIGNED'
        )
    """)

    db.execute("""
        CREATE TABLE IF NOT EXISTS verifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            application_id INTEGER NOT NULL,
            officer_id INTEGER NOT NULL,
            latitude REAL,
            longitude REAL,
            result TEXT,
            remarks TEXT,
            verification_date TEXT
        )
    """)

    db.execute("""
        CREATE TABLE IF NOT EXISTS test_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            verification_id INTEGER NOT NULL,
            standard_value REAL NOT NULL,
            observed_value REAL NOT NULL,
            permissible_error REAL NOT NULL,
            error REAL,
            result TEXT
        )
    """)

    db.close()

create_tables()


# ---------------------------------------------------
# HOME / HEALTH CHECK
# ---------------------------------------------------

@app.get("/")
def home():
    return {
        "message": "Metrify backend is running!",
        "status": "OK"
    }


# ---------------------------------------------------
# USERS
# ---------------------------------------------------

@app.post("/users")
def create_user(
    name: str,
    email: str,
    role: str
):
    db = get_db()

    cursor = db.execute(
        """
        INSERT INTO users (name, email, role)
        VALUES (?, ?, ?)
        """,
        (name, email, role.upper())
    )


    user_id = cursor.lastrowid

    db.close()

    return {
        "message": "User created successfully",
        "user_id": user_id
    }


@app.get("/users")
def get_users():
    db = get_db()

    users = db.execute(
        "SELECT * FROM users"
    ).fetchall()

    db.close()

    return [dict(user) for user in users]


# ---------------------------------------------------
# INSTRUMENTS
# ---------------------------------------------------

@app.post("/instruments")
def create_instrument(
    owner_id: int,
    instrument_type: str,
    serial_number: str,
    manufacturer: str = "",
    model: str = "",
    capacity: float = 0,
    location: str = ""
):
    db = get_db()

    try:

        cursor = db.execute(
            """
            INSERT INTO instruments
            (
                owner_id,
                instrument_type,
                manufacturer,
                model,
                serial_number,
                capacity,
                location,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                owner_id,
                instrument_type,
                manufacturer,
                model,
                serial_number,
                capacity,
                location,
                datetime.now().isoformat()
            )
        )


        instrument_id = cursor.lastrowid

        return {
            "message": "Instrument registered successfully",
            "instrument_id": instrument_id
        }

    except sqlite3.IntegrityError:
        return {
            "error": "Serial number already exists"
        }

    finally:
        db.close()


@app.get("/instruments")
def get_instruments():
    db = get_db()

    instruments = db.execute(
        "SELECT * FROM instruments"
    ).fetchall()

    db.close()

    return [dict(instrument) for instrument in instruments]


@app.get("/instruments/{instrument_id}")
def get_instrument(instrument_id: int):

    db = get_db()

    instrument = db.execute(
        "SELECT * FROM instruments WHERE id = ?",
        (instrument_id,)
    ).fetchone()

    db.close()

    if instrument is None:
        return {
            "error": "Instrument not found"
        }

    return dict(instrument)


# ---------------------------------------------------
# APPLICATIONS
# ---------------------------------------------------

@app.post("/applications")
def create_application(
    instrument_id: int,
    owner_id: int,
    application_type: str,
    preferred_date: str
):

    db = get_db()

    cursor = db.execute(
        """
        INSERT INTO applications
        (
            instrument_id,
            owner_id,
            application_type,
            preferred_date,
            created_at
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            instrument_id,
            owner_id,
            application_type,
            preferred_date,
            datetime.now().isoformat()
        )
    )


    application_id = cursor.lastrowid

    db.close()

    return {
        "message": "Verification application submitted",
        "application_id": application_id,
        "status": "SUBMITTED"
    }


@app.get("/applications")
def get_applications():

    db = get_db()

    applications = db.execute(
        """
        SELECT *
        FROM applications
        ORDER BY id DESC
        """
    ).fetchall()

    db.close()

    return [dict(application) for application in applications]


@app.get("/applications/{application_id}")
def get_application(application_id: int):

    db = get_db()

    application = db.execute(
        """
        SELECT *
        FROM applications
        WHERE id = ?
        """,
        (application_id,)
    ).fetchone()

    db.close()

    if application is None:
        return {
            "error": "Application not found"
        }

    return dict(application)


# ---------------------------------------------------
# OFFICER ASSIGNMENT
# ---------------------------------------------------

@app.post("/assignments")
def assign_officer(
    application_id: int,
    officer_id: int,
    scheduled_date: str
):

    db = get_db()

    cursor = db.execute(
        """
        INSERT INTO assignments
        (
            application_id,
            officer_id,
            scheduled_date
        )
        VALUES (?, ?, ?)
        """,
        (
            application_id,
            officer_id,
            scheduled_date
        )
    )

    # Update application status
    db.execute(
        """
        UPDATE applications
        SET status = 'ASSIGNED'
        WHERE id = ?
        """,
        (application_id,)
    )


    assignment_id = cursor.lastrowid

    db.close()

    return {
        "message": "Officer assigned successfully",
        "assignment_id": assignment_id
    }


@app.get("/assignments")
def get_assignments():

    db = get_db()

    assignments = db.execute(
        "SELECT * FROM assignments"
    ).fetchall()

    db.close()

    return [dict(assignment) for assignment in assignments]


# ---------------------------------------------------
# VERIFICATION
# ---------------------------------------------------

@app.post("/verifications")
def create_verification(
    application_id: int,
    officer_id: int,
    latitude: float = 0,
    longitude: float = 0,
    remarks: str = ""
):

    db = get_db()

    cursor = db.execute(
        """
        INSERT INTO verifications
        (
            application_id,
            officer_id,
            latitude,
            longitude,
            remarks,
            verification_date
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            application_id,
            officer_id,
            latitude,
            longitude,
            remarks,
            datetime.now().isoformat()
        )
    )

    # Update application status
    db.execute(
        """
        UPDATE applications
        SET status = 'VERIFICATION_PENDING'
        WHERE id = ?
        """,
        (application_id,)
    )


    verification_id = cursor.lastrowid

    db.close()

    return {
        "message": "Verification created",
        "verification_id": verification_id
    }


# ---------------------------------------------------
# TEST READING + AUTOMATIC CALCULATION
# ---------------------------------------------------

@app.post("/verifications/{verification_id}/tests")
def add_test_result(
    verification_id: int,
    standard_value: float,
    observed_value: float,
    permissible_error: float
):

    error = observed_value - standard_value

    if abs(error) <= permissible_error:
        result = "PASS"
    else:
        result = "FAIL"

    db = get_db()

    cursor = db.execute(
        """
        INSERT INTO test_results
        (
            verification_id,
            standard_value,
            observed_value,
            permissible_error,
            error,
            result
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            verification_id,
            standard_value,
            observed_value,
            permissible_error,
            error,
            result
        )
    )

    test_id = cursor.lastrowid

    db.close()

    return {
        "test_id": test_id,
        "standard_value": standard_value,
        "observed_value": observed_value,
        "error": error,
        "permissible_error": permissible_error,
        "result": result
    }


# ---------------------------------------------------
# COMPLETE VERIFICATION
# ---------------------------------------------------

@app.post("/verifications/{verification_id}/complete")
def complete_verification(verification_id: int):

    db = get_db()

    tests = db.execute(
        """
        SELECT *
        FROM test_results
        WHERE verification_id = ?
        """,
        (verification_id,)
    ).fetchall()

    if not tests:
        db.close()

        return {
            "error": "No test results found"
        }

    # Verification passes only if every test passes
    final_result = "PASS"

    for test in tests:
        if test["result"] == "FAIL":
            final_result = "FAIL"

    db.execute(
        """
        UPDATE verifications
        SET result = ?
        WHERE id = ?
        """,
        (final_result, verification_id)
    )

    # Find the application
    verification = db.execute(
        """
        SELECT application_id
        FROM verifications
        WHERE id = ?
        """,
        (verification_id,)
    ).fetchone()

    if verification:
        db.execute(
            """
            UPDATE applications
            SET status = ?
            WHERE id = ?
            """,
            (
                "VERIFIED" if final_result == "PASS" else "REJECTED",
                verification["application_id"]
            )
        )

    db.close()

    return {
        "verification_id": verification_id,
        "final_result": final_result,
        "message": "Verification completed"
    }


# ---------------------------------------------------
# VIEW VERIFICATION
# ---------------------------------------------------

@app.get("/verifications/{verification_id}")
def get_verification(verification_id: int):

    db = get_db()

    verification = db.execute(
        """
        SELECT *
        FROM verifications
        WHERE id = ?
        """,
        (verification_id,)
    ).fetchone()

    if verification is None:
        db.close()

        return {
            "error": "Verification not found"
        }

    tests = db.execute(
        """
        SELECT *
        FROM test_results
        WHERE verification_id = ?
        """,
        (verification_id,)
    ).fetchall()

    db.close()

    return {
        "verification": dict(verification),
        "test_results": [dict(test) for test in tests]
    }