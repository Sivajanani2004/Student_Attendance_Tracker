from sqlalchemy.orm import declarative_base
from sqlalchemy import (Column,Integer,String,Boolean,Date,
                        ForeignKey,UniqueConstraint)
from database.db import engine

Base = declarative_base()


class Users(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)


class Students(Base):
    __tablename__ = "students"
    std_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    roll_number = Column(String, unique=True, nullable=False)
    std_class = Column(Integer, nullable=False)


class TeacherStudentMap(Base):
    __tablename__ = "teacher_student_map"
    id = Column(Integer, primary_key=True)
    teacher_id = Column(Integer,ForeignKey("users.user_id", ondelete="CASCADE"),nullable=False)
    student_id = Column(Integer,ForeignKey("students.std_id", ondelete="CASCADE"),nullable=False)

    __table_args__ = (UniqueConstraint("teacher_id","student_id",name="unique_teacher_student"),)


class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer,ForeignKey("students.std_id", ondelete="CASCADE"),nullable=False)
    date = Column(Date, nullable=False)
    status = Column(Boolean, nullable=False)
    marked_by_teacher = Column(Integer,ForeignKey("users.user_id", ondelete="CASCADE"),nullable=False)

    __table_args__ = ( UniqueConstraint("student_id","date",name="unique_student_date"),)


Base.metadata.create_all(bind=engine)
