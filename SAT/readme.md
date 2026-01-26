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

## 🛠️ Installation Instructions (Local Setup)

Follow the steps below to run the project on your local machine.

---

### ✅ Prerequisites

Make sure the following tools are installed on your system:

- **Python 3.10 or higher**  
  👉 https://www.python.org/downloads/

- **Docker**  
  👉 https://docs.docker.com/get-docker/

- **Docker Compose**  
  (Included with Docker Desktop)

- **Git**  
  👉 https://git-scm.com/downloads

Verify installation:
```bash
python --version
docker --version
docker compose version
git --version

---

## 📁 Project Structure

Student_Attendance_Tracker/
- backend/
- frontend/
- Screenshots
- docker-compose.yml
- README.md

---

## 🐳 Run Locally with Docker

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

## 🌍 Live Deployment (Render)

The project is deployed on **Render** using separate services for frontend and backend.

### 🔹 Frontend (Streamlit)
👉 **Live App URL:**  
https://student-attendance-tracker-frontend.onrender.com  

### 🔹 Backend (FastAPI)
👉 **API Base URL:**  
https://student-attendance-tracker-vimh.onrender.com  

👉 **Swagger API Docs:**  
https://student-attendance-tracker-vimh.onrender.com/docs  

---

## 👩‍💻 Author
Siva Janani R
---

