# 📊 Student Attendance Tracker

A full-stack **Student Attendance Management System** built using **FastAPI**, **Streamlit**, and **Docker**.  
This application supports role-based access for **Admin** and **Teacher** users.

---

## 🚀 Features

### 👥 User Roles

**Admin**
- Manage students (Add / Edit / Delete)
- Manage teachers (View / Delete)
- Assign & unassign students to teachers
- View all attendance reports
- Update student attendance

**Teacher**
- View assigned students
- Mark attendance (Present / Absent)
- Update attendance for assigned students only
- View attendance reports for their students

---

## 🔐 Authentication
- Login and Signup
- Password hashing
- JWT token-based authentication

---

## 🛠️ Tech Stack
- Backend: FastAPI, SQLAlchemy
- Frontend: Streamlit
- Database: SQLite
- Authentication: JWT
- Containerization: Docker & Docker Compose

---

## 📁 Project Structure

Student_Attendance_Tracker/
- backend/
- frontend/
- docker-compose.yml
- README.md

---

## 🛠️ Installation Instructions

### Prerequisites
- Python 3.10+
- Docker
- Docker Compose
- Git

---

## 🐳 Run Using Docker

### Step 1: Clone Repository
```bash
git clone <your-repository-url>
cd Student_Attendance_Tracker
```

### Step 2: Build and Run
```bash
docker compose up --build
```

### Step 3: Open in Browser
- Frontend: http://localhost:8501
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Stop Containers
```bash
docker compose down
```

---

## 👩‍💻 Author
Siva Janani R

---

## 📄 License
This project is for educational purposes only.
