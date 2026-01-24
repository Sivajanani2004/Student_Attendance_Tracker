from sqlalchemy.orm import Session
from models.table_schema import Users,Students,Attendance,TeacherStudentMap
from passlib.hash import argon2
from auths.auth import create_access_token
from fastapi import HTTPException
from sqlalchemy import func


def register_user(data, db):
    existing_user = db.query(Users).filter(Users.email == data.email).first()
    if existing_user:
        raise HTTPException(status_code=400,detail="User already exists. Please login.")
    user = Users(name=data.name,email=data.email,
                password=argon2.hash(data.password),role=data.role)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": "User registered successfully"}

def login_user(email: str, password: str,db:Session):  
    user = db.query(Users).filter(Users.email == email).first()
    
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username")

    if not argon2.verify(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid password")

    
    token = create_access_token({"user_id": user.user_id,"role":user.role})
    return {"message": "Login Successfully", "access_token": token,"role":user.role.lower(),"name":user.name}


def create_student(data,token_data,db: Session):
    if token_data["role"] != "admin":
        raise HTTPException(403, "Only admin can create students")
    student = Students(name=data.name,roll_number = data.roll_number,std_class = data.std_class)
    db.add(student)
    db.commit()
    db.refresh(student)
    return student


def update_student(std_id: int, data, token_data, db: Session):
    if token_data["role"] != "admin":
        raise HTTPException(403, "Only admin can update students")

    student = db.query(Students).filter(Students.std_id == std_id).first()
    if not student:
        raise HTTPException(404, "Student not found")

    student.name = data.name
    student.roll_number = data.roll_number
    student.std_class = data.std_class
    db.commit()
    return {"message": "Student updated successfully"}


def delete_student(std_id: int, token_data, db: Session):
    if token_data["role"] != "admin":
        raise HTTPException(403, "Only admin can delete students")

    student = db.query(Students).filter(Students.std_id == std_id).first()
    if not student:
        raise HTTPException(404, "Student not found")

    db.delete(student)
    db.commit()
    return {"message": "Student deleted successfully"}


def get_all_students(token_data, db: Session):
    if token_data["role"] != "admin":
        raise HTTPException(403, "Only admin can view students")

    students = db.query(Students).all()
    return [
        {
            "std_id": s.std_id,
            "name": s.name,
            "roll_number": s.roll_number,
            "std_class": s.std_class
        }
        for s in students]



def get_all_users(token_data, db):
    if token_data["role"] != "admin":
        raise HTTPException(403, "Only admin can view users")
    users = db.query(Users).all()
    return [
        {
            "user_id": u.user_id,
            "name": u.name,
            "email": u.email,
            "role": u.role
        }
        for u in users]


def update_teacher(user_id: int, data, token_data, db: Session):
    if token_data["role"] != "admin":
        raise HTTPException(403, "Only admin can update teachers")

    teacher = db.query(Users).filter(Users.user_id == user_id,Users.role == "teacher").first()
    if not teacher:
        raise HTTPException(404, "Teacher not found")

    teacher.name = data.name
    teacher.email = data.email
    db.commit()
    return {"message": "Teacher updated successfully"}


def delete_teacher(user_id: int, token_data, db: Session):
    if token_data["role"] != "admin":
        raise HTTPException(403, "Only admin can delete teachers")
    teacher = db.query(Users).filter(
        Users.user_id == user_id,
        Users.role == "teacher").first()

    if not teacher:
        raise HTTPException(404, "Teacher not found")
    db.delete(teacher)
    db.commit()
    return {"message": "Teacher deleted successfully"}


def get_teachers(db: Session):
    teachers = db.query(Users).filter(Users.role == "teacher").all()
    return [{"user_id": t.user_id, "name": t.name}
            for t in teachers]


def assign_student(data, token_data, db: Session):
    if token_data["role"] != "admin":
        raise HTTPException(403, "Only admin can assign students")
    existing = db.query(TeacherStudentMap).filter(TeacherStudentMap.teacher_id == data.teacher_id,
                                                  TeacherStudentMap.student_id == data.student_id).first()
    if existing:
        raise HTTPException(400, "Student already assigned to this teacher")
    mapping = TeacherStudentMap(teacher_id=data.teacher_id,    student_id=data.student_id)
    db.add(mapping)
    db.commit()
    return {"message": "Student assigned successfully"}



def fetch_assigned_students(token_data, db: Session):
    if token_data["role"] != "teacher":
        raise HTTPException(403, "Only teacher can view students")

    students = db.query(Students).join(TeacherStudentMap,TeacherStudentMap.student_id == Students.std_id).filter(
                                       TeacherStudentMap.teacher_id == token_data["user_id"]).all()
    return [
        {
            "std_id": s.std_id,
            "name": s.name,
            "roll_number": s.roll_number,
            "std_class": s.std_class
        }
        for s in students]


def unassign_student(teacher_id: int, student_id: int, token_data, db: Session):
    if token_data["role"] != "admin":
        raise HTTPException(403, "Only admin can unassign students")

    mapping = db.query(TeacherStudentMap).filter(
        TeacherStudentMap.teacher_id == teacher_id,
        TeacherStudentMap.student_id == student_id
    ).first()

    if not mapping:
        raise HTTPException(404, "Assignment not found")

    db.delete(mapping)
    db.commit()

    return {"message": "Student unassigned successfully"}



def mark_attendance(db: Session, data, token_data):
    if token_data["role"] != "teacher":
        raise HTTPException(403, "Only teacher can mark attendance")

    mapping = db.query(TeacherStudentMap).filter(
        TeacherStudentMap.teacher_id == token_data["user_id"],
        TeacherStudentMap.student_id == data.student_id).first()

    if not mapping:
        raise HTTPException(403, "Student not assigned to you")

    exists = db.query(Attendance).filter(Attendance.student_id == data.student_id,
                                         Attendance.date == data.date).first()
    if exists:
        raise HTTPException(400, "Attendance already marked")

    attendance = Attendance(
        student_id=data.student_id,
        date=data.date,
        status=data.status,
        marked_by_teacher=token_data["user_id"])
    db.add(attendance)
    db.commit()
    return {"message": "Attendance marked successfully"}


def update_attendance(data, token_data, db: Session):
    attendance = db.query(Attendance).filter(
        Attendance.student_id == data.student_id,
        Attendance.date == data.date).first()

    if not attendance:
        raise HTTPException(404, "Attendance not found")

    if token_data["role"] == "teacher":
        if attendance.marked_by_teacher != token_data["user_id"]:
            raise HTTPException(403, "You can update only your attendance")

    attendance.status = data.status
    db.commit()

    return {"message": "Attendance updated successfully"}



def attendance_report(token_data, db: Session):
    if token_data["role"] == "admin":
        return db.query(Attendance).all()
    return db.query(Attendance).join(TeacherStudentMap, TeacherStudentMap.student_id == Attendance.student_id) \
        .filter(TeacherStudentMap.teacher_id == token_data["user_id"]).all()


def student_wise_report(token_data, db: Session):
    if token_data["role"] != "admin":
        raise HTTPException(403, "Only admin")

    result = db.query(
        Attendance.student_id,func.count(Attendance.id).label("total_days"),
        func.sum(func.case((Attendance.status == True, 1), else_=0)).label("present_days")).group_by(Attendance.student_id).all()

    return [
        {
            "student_id": r.student_id,
            "total_days": r.total_days,
            "present_days": r.present_days,
            "absent_days": r.total_days - r.present_days,
            "present_percent": round((r.present_days / r.total_days) * 100, 2)
        }
        for r in result
    ]


def month_wise_report(token_data, db: Session):
    if token_data["role"] != "admin":
        raise HTTPException(403, "Only admin")

    result = db.query(func.strftime('%Y-%m', Attendance.date).label("month"),func.count(Attendance.id).label("total"),
        func.sum(func.case((Attendance.status == True, 1), else_=0)).label("present")).group_by("month").all()

    return [
        {
            "month": r.month,
            "total_days": r.total,
            "present": r.present,
            "absent": r.total - r.present,
            "present_percent": round((r.present / r.total) * 100, 2)
        }
        for r in result
    ]



