from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from services.content import (register_user,login_user,create_student,assign_student,fetch_assigned_students,unassign_student,mark_attendance,attendance_report,update_attendance,
                              get_all_users,get_all_students,get_teachers,update_student,delete_student,update_teacher,delete_teacher,
                              student_wise_report,month_wise_report)
from models.schema import (CreateUsers,CreateStudents,Login,AssignStudent,MarkAttendance,UpdateAttendance,
                           UpdateStudent,UpdateTeacher)
from database.db import SessionLocal
from auths.auth import decode_token

router = APIRouter()
auth = OAuth2PasswordBearer(tokenUrl="login")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@router.post("/register")
def register(data: CreateUsers, db: Session = Depends(get_db)):
    return register_user(data, db)


@router.post("/login")
def login(data: Login, db: Session = Depends(get_db)):
    return login_user(data.email, data.password, db)


#  ADMIN : STUDENTS 

@router.post("/admin/student")
def add_student(data: CreateStudents,db: Session = Depends(get_db),token_data=Depends(decode_token)):
    return create_student(data, token_data, db)


@router.put("/admin/student/{std_id}")
def edit_student(std_id: int,data: UpdateStudent,db: Session = Depends(get_db),token_data=Depends(decode_token)):
    return update_student(std_id, data, token_data, db)


@router.delete("/admin/student/{std_id}")
def remove_student(std_id: int,db: Session = Depends(get_db),token_data=Depends(decode_token)):
    return delete_student(std_id, token_data, db)


@router.get("/admin/students")
def view_students(db: Session = Depends(get_db),token_data=Depends(decode_token)):
    return get_all_students(token_data, db)


#  ADMIN : TEACHERS 

@router.get("/admin/users")
def view_users(db: Session = Depends(get_db),token_data=Depends(decode_token)):
    return get_all_users(token_data, db)


@router.put("/admin/teacher/{user_id}")
def edit_teacher(user_id: int,data: UpdateTeacher,db: Session = Depends(get_db),token_data=Depends(decode_token)):
    return update_teacher(user_id, data, token_data, db)


@router.delete("/admin/teacher/{user_id}")
def remove_teacher(user_id: int,db: Session = Depends(get_db),token_data=Depends(decode_token)):
    return delete_teacher(user_id, token_data, db)


@router.get("/teachers")
def list_teachers(db: Session = Depends(get_db)):
    return get_teachers(db)


#  ASSIGN STUDENTS 

@router.post("/admin/assign")
def assign(data: AssignStudent,db: Session = Depends(get_db),token_data=Depends(decode_token)):
    return assign_student(data, token_data, db)

@router.delete("/admin/unassign")
def unassign(teacher_id: int,student_id: int,db: Session = Depends(get_db),token_data=Depends(decode_token)):
    return unassign_student(teacher_id, student_id, token_data, db)


# TEACHER 

@router.get("/teacher/students")
def my_students(db: Session = Depends(get_db),token_data=Depends(decode_token)):
    return fetch_assigned_students(token_data, db)


@router.post("/teacher/attendance")
def attendance(data: MarkAttendance,db: Session = Depends(get_db),token_data=Depends(decode_token)):
    return mark_attendance(db, data, token_data)


@router.put("/teacher/attendance")
def update_attendance_route(data: UpdateAttendance,db: Session = Depends(get_db),token_data=Depends(decode_token)):
    return update_attendance(data, token_data, db)


#  REPORTS 

@router.get("/attendance/report")
def report(db: Session = Depends(get_db),token_data=Depends(decode_token)):
    return attendance_report(token_data, db)


@router.get("/admin/report/student-wise")
def student_report(db: Session = Depends(get_db),token_data=Depends(decode_token)):
    return student_wise_report(token_data, db)


@router.get("/admin/report/month-wise")
def monthly_report(db: Session = Depends(get_db),token_data=Depends(decode_token)):
    return month_wise_report(token_data, db)


@router.put("/admin/attendance")
def admin_update_attendance(data: UpdateAttendance,db: Session = Depends(get_db),token_data=Depends(decode_token)):
    return update_attendance(data, token_data, db)