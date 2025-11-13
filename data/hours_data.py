import sqlite3
import os
import time
from enum import Enum
HOURS_DB_PATH = os.getenv("HOURS_DB_PATH")
PENDING_DB_PATH = os.getenv("PENDING_DB_PATH")

class Status(Enum):
    Approved = 0
    Rejected = 1
    Pending = 2

class DbContext:
    hours_conn: sqlite3.Connection
    pending_conn: sqlite3.Connection
    def __init__(self):
        if HOURS_DB_PATH == None or PENDING_DB_PATH == None:
            exit(-1)
        else:
            self.hours_conn = sqlite3.connect(HOURS_DB_PATH)
            self.pending_conn = sqlite3.connect(PENDING_DB_PATH)
    
    def close(self):
        self.hours_conn.close()
        self.pending_conn.close()

    def get_pending_submission(self, id: int):
        cursor = self.pending_conn.execute(f"SELECT * FROM pending_submissions WHERE rowid={id}")
        submission = Submission(cursor.fetchone())
        cursor.close()
        return submission
        
    def get_approved_submission(self, id: int):
        cursor = self.hours_conn.execute(f"SELECT * FROM pending_submissions WHERE rowid={id}")
        submission = Submission(cursor.fetchone())
        cursor.close()
        return submission
        
    def insert_new_sub(self, submission: Submission):
        cursor = self.pending_conn.execute("INSERT INTO pending_submissions VALUES(:student_email, :start_time, :num_qtr_hours, :supervisor_email, :location, :organization, :service_type, :status)")
    
    def submit(self, approved: bool, id: int):
        if not approved:
            pass
        cursor = self.pending_conn.cursor()
        

        

class Submission:
    id: int #Primary key for locating within whichever database it may be in
    student_email: str
    start_time: int #The time they started, expressed as unix timestamp
    num_qtr_hours: int #Number of quarter-hours completed
    supervisor_email: str#Email of the supervisor (MUST be a whitelisted address)
    location: str #The place where they did service
    organization: str #Service organization they worked with
    service_type: str #Hours class (Ignatian, Work Grant, Other, Etc.) also allows for default 
    status: Status #Pending vs. complete
    def __init__(self, row: tuple):
        """
        Initialize from an SQLite row tuple with the following order:
        (id, student_email, start_time, num_qtr_hours, supervisor_email,
         location, organization, service_type, status)
        """
        # All values may not be none, making this initializer safe
        values = list(row)

        raw_id = values[0]
        self.id = int(raw_id)

        self.student_email = values[1]

        raw_start = values[2]
        self.start_time = int(raw_start)

        raw_qtrs = values[3]
        self.num_qtr_hours = int(raw_qtrs)

        self.supervisor_email = values[4]
        self.location = values[5]
        self.organization = values[6]
        self.service_type = values[7]

        self.status = Status(values[8])
        
    def into_named(self) -> dict:
        return {
            "student_email": self.student_email,
            "start_time": self.start_time,
            "num_qtr_hours": self.num_qtr_hours,
            "supervisor_email": self.supervisor_email,
            "location": self.location,
            "organization": self.organization,
            "service_type": self.service_type,
            "status": self.status.value
        }

#multiple ways to submit:
'''
- using generated code
    -supervisor may generate code attaching service metadata to db, students can log with code
-supervisor may log hours for students
-students may request to log hours from specific supervisor

'''
