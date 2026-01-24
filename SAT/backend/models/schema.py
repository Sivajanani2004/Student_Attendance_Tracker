from pydantic import BaseModel, EmailStr
from datetime import date



class CreateUsers(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str


class Login(BaseModel):
    email: EmailStr
    password: str


# STUDENTS 

class CreateStudents(BaseModel):
    name: str
    roll_number: str
    std_class: int


class UpdateStudent(BaseModel):
    name: str
    roll_number: str
    std_class: int


#  TEACHERS 

class UpdateTeacher(BaseModel):
    name: str
    email: EmailStr


#  ASSIGN STUDENTS

class AssignStudent(BaseModel):
    teacher_id: int
    student_id: int


# ATTENDANCE 

class MarkAttendance(BaseModel):
    student_id: int
    date: date
    status: bool


class UpdateAttendance(BaseModel):
    student_id: int
    date: date
    status: bool


#  REPORTS 

class StudentWiseReport(BaseModel):
    student_id: int
    total_days: int
    present_days: int
    absent_days: int
    present_percent: float


class MonthWiseReport(BaseModel):
    month: str
    total_days: int
    present: int
    absent: int
    present_percent: float
