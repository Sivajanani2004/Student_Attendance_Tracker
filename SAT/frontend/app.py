import streamlit as st
import requests,re
import pandas as pd
import os


BASE_URL = os.getenv("BACKEND_URL","http://127.0.0.1:8000")
st.write("BASE_URL =", BASE_URL)
st.set_page_config(page_title= "Student Attendance Tracker",page_icon="📊")


# SESSION STATE 
if "page" not in st.session_state:
    st.session_state.page = "login"
    st.session_state.login = False
    st.session_state.token = None
    st.session_state.role = None
    st.session_state.user = None


def check_password_strength(password: str):
    if len(password) < 8:
        return "Weak", "Password must be at least 8 characters"
    if not re.search(r"[A-Z]", password):
        return "Weak", "Add at least one uppercase letter"
    if not re.search(r"[a-z]", password):
        return "Weak", "Add at least one lowercase letter"
    if not re.search(r"[0-9]", password):
        return "Weak", "Add at least one number"
    if not re.search(r"[!@#$%^&*()_+=\-]", password):
        return "Weak", "Add at least one special character"
    
    return "Strong", "Strong password"

# Wakeup backend
def wake_backend():
    try:
        requests.get(f"{BASE_URL}/docs", timeout=10)
    except:
        pass

# SIGNUP PAGE

def signup_page():
    st.header("📝 Sign Up")

    name = st.text_input("User Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    role = st.selectbox("Role", ["admin", "teacher"])

    if password:
        strength, msg = check_password_strength(password)
        if strength == "Weak":
            st.warning(msg)
        else:
            st.success(msg)

    col1, col2 = st.columns([2, 1])

    with col1:
        create_clicked = st.button("Create Account")

    with col2:
        if st.button("🔐 Already have an account? Login"):
            st.session_state.page = "login"
            st.rerun()

   
    if create_clicked:
        strength, _ = check_password_strength(password)
        if strength == "Weak":
            st.error("Please use a stronger password before creating account.")
            return
        
        payload = {"name": name,"email": email,"password": password,"role": role}
        res = requests.post(f"{BASE_URL}/register", json=payload)
        if res.status_code == 200:
            st.success("Account created successfully. Please login.")
            st.session_state.page = "login"
            st.rerun()
        else:
            error_msg = res.json().get("detail", "Something went wrong")
            st.error(error_msg)


# LOGIN PAGE

def login_page():
    st.header("🔐 Login Page")

    email = st.text_input("Enter Email")
    password = st.text_input("Enter Password", type="password")
    col1, col2 = st.columns([2,1])

    with col1:
        login_clicked = st.button("🔓 Login")

    with col2:
        if st.button("📝 New user? Sign up"):
            st.session_state.page = "signup"
            st.rerun()

    if login_clicked:
        payload = {"email": email, "password": password}
        response = requests.post(f"{BASE_URL}/login", json=payload,timeout=15)

        if response.status_code == 200:
            data = response.json()
            st.session_state.login = True
            st.session_state.user = data["name"]
            st.session_state.role = data["role"].lower()
            st.session_state.token = data["access_token"]
            st.session_state.page = "dashboard"
            st.success("Login successful")
            st.rerun()
        else:
            st.error("Invalid credentials")

#  DASHBOARD 

def dashboard():
    headers = {"Authorization": f"Bearer {st.session_state.token}"}
    if st.session_state.role == "admin":
        st.header(f"🛡️ Welcome to Admin Panel, {st.session_state.user}")
    else:
        st.header(f"👩‍🏫 Welcome to Staff Page, {st.session_state.user}")

# ADMIN

    if st.session_state.role == "admin":
        menu = st.sidebar.selectbox("🛠 Admin Menu",["🎒 Manage Students", "🔗 Assign Students", "📅 Attendance Reports", "🗂 View Users"])

        if menu == "🎒 Manage Students":
            st.subheader("🎒 Manage Students")
            name = st.text_input("Student Name")
            roll = st.text_input("Roll Number")
            cls = st.number_input("Class", min_value=1)

            if st.button("➕ Add Student"):
                payload = {"name": name, "roll_number": roll, "std_class": cls}
                res = requests.post(f"{BASE_URL}/admin/student",json=payload,headers=headers)
                if res.status_code == 200:
                    st.success("Student added successfully")
                else:
                    st.error(res.text)

        if menu == "🔗 Assign Students":
            st.subheader("🔗 Assign / Unassign Students")
            users = requests.get(f"{BASE_URL}/admin/users", headers=headers).json()
            teachers = {u["name"]: u["user_id"] for u in users if u["role"] == "teacher"}
            students = requests.get(f"{BASE_URL}/admin/students", headers=headers).json()
            students_map = {f"{s['name']} (Class {s['std_class']})": s["std_id"]
                            for s in students}

            teacher_name = st.selectbox("Select Teacher", teachers.keys())
            student_name = st.selectbox("Select Student", students_map.keys())
            col1, col2 = st.columns([2,1])
            with col1:
                if st.button("✅ Assign"):
                    payload = {"teacher_id": teachers[teacher_name],"student_id": students_map[student_name]}
                    res = requests.post(f"{BASE_URL}/admin/assign", json=payload, headers=headers)
                    if res.status_code == 200:
                        st.success("Student assigned successfully")
                    else:
                        st.error(res.text)
            with col2:
                if st.button("❌ Unassign"):
                    res = requests.delete(
                        f"{BASE_URL}/admin/unassign",
                        params={
                            "teacher_id": teachers[teacher_name],
                            "student_id": students_map[student_name]},headers=headers)
                    if res.status_code == 200:
                        st.success("Student unassigned successfully")
                        st.rerun()
                    else:
                        st.error(res.text)
                    
        if menu == "📅 Attendance Reports":
            st.subheader("📅 Attendance Reports")
            res = requests.get(f"{BASE_URL}/attendance/report", headers=headers)

            if res.status_code != 200:
                st.error("Unable to fetch report")
                return

            data = res.json()
            if not data:
                st.info("Attendance is not submitted yet.")
                return

            teachers = requests.get(f"{BASE_URL}/teachers", headers=headers).json()
            students = requests.get(f"{BASE_URL}/admin/students", headers=headers).json()

            teacher_map = {t["user_id"]: f'{t["name"]} - ID: {t["user_id"]}'
                           for t in teachers}
            student_map = {f'{s["name"]} (ID: {s["std_id"]})': s["std_id"]
                           for s in students}

            df = pd.DataFrame(data)

            df["status"] = df["status"].apply(lambda x: "Present" if x else "Absent")
            df["marked_by_teacher"] = df["marked_by_teacher"].map(teacher_map)
            df["student_name"] = df["student_id"].map({s["std_id"]: f'{s["name"]} (ID {s["std_id"]})' for s in students})
            st.table(df[["student_name", "date", "status", "marked_by_teacher"]])

            st.subheader("Update Attendance")
            student_id = st.selectbox("Student ID", df["student_id"].unique())
            date = st.selectbox("Date", df[df["student_id"] == student_id]["date"].unique())
            status = st.selectbox("Status", ["Present", "Absent"])
         
            if st.button("Update Attendance"):
                payload = {"student_id": student_id,"date": date,"status": status == "Present"}
                update_res = requests.put(f"{BASE_URL}/admin/attendance",json=payload,headers=headers)
                if update_res.status_code == 200:
                    st.success("Attendance updated successfully")
                    st.rerun()
                else:
                    st.error(update_res.text)

        if menu == "🗂 View Users":
            st.subheader("🗂 View Users")
            res = requests.get(f"{BASE_URL}/admin/users", headers=headers)

            if res.status_code == 200:
                users = res.json()

                if not users:
                    st.info("No users found.")
                else:
                    st.table(users)

                    st.subheader("Remove Teacher / User")

                    user_map = {f'{u["name"]} ({u["role"]}) - ID {u["user_id"]}': u["user_id"]
                                for u in users if u["role"] == "teacher"}
                    selected_user = st.selectbox("Select Teacher to Remove",user_map.keys())
                    col1, col2 = st.columns([2, 1])
                    with col2:
                        if st.button("Remove Teacher"):
                            user_id = user_map[selected_user]
                            res = requests.delete(f"{BASE_URL}/admin/teacher/{user_id}",headers=headers)
                            if res.status_code == 200:
                                st.success("Teacher deleted successfully")
                                st.rerun()
                            else:
                                st.error(res.text)

        with st.sidebar:
            if st.button("🚪 Logout"):
                st.session_state.clear()
                st.rerun()

# TEACHER 

    elif st.session_state.role == "teacher":
        menu = st.sidebar.selectbox("Teacher Menu",["👩‍🎓 My Students", "✍️ Mark Attendance", "📅 Attendance Reports"])

        if menu == "👩‍🎓 My Students":
            st.subheader("My Students")
            res = requests.get(f"{BASE_URL}/teacher/students", headers=headers)
            if res.status_code == 200:
                data = res.json()
                if not data:
                    st.info("No students assigned yet.")
                else:
                    df = pd.DataFrame(data)
                    st.table(df)

        if menu == "✍️ Mark Attendance":
            st.subheader("Mark Attendance")
            res = requests.get(f"{BASE_URL}/teacher/students", headers=headers)
            if res.status_code != 200:
                st.error("Unable to load assigned students")
                return
            students = res.json()
            if not students:
                st.info("No students assigned to you.")
                return

            student_map = {f'{s["std_id"]} - {s["name"]}': s["std_id"] for s in students}
            selected_student = st.selectbox("Select Student",student_map.keys())
            student_id = student_map[selected_student]
            date = st.date_input("Date")
            status = st.selectbox("Status", ["Present", "Absent"])

            if st.button("Submit Attendance"):
                payload = {"student_id": student_id,"date": str(date),"status": True if status == "Present" else False}
                res = requests.post(f"{BASE_URL}/teacher/attendance",json=payload,headers=headers)
                if res.status_code == 200:
                    st.success("Attendance marked successfully")
                else:
                    st.error(res.json().get("detail", "Failed to mark attendance"))

        if menu == "📅 Attendance Reports":
            st.subheader("Attendance Reports")
            res = requests.get(f"{BASE_URL}/attendance/report", headers=headers)

            if res.status_code != 200:
                st.error("Unable to fetch report")
                return

            data = res.json()
            if not data:
                st.info("Attendance is not submitted yet.")
                return

            teachers = requests.get(f"{BASE_URL}/teachers", headers=headers).json()
            teacher_map = {t["user_id"]: f'{t["name"]} (ID: {t["user_id"]})' for t in teachers}

            df = pd.DataFrame(data) 
            df["status"] = df["status"].apply(lambda x: "Present" if x else "Absent")
            df["marked_by_teacher"] = df["marked_by_teacher"].map(teacher_map)     
            st.table(df[["student_id", "date", "status", "marked_by_teacher"]])

            st.subheader("🛠 Update Attendance")
            student_id = st.selectbox("Student ID", df["student_id"].unique())
            date = st.selectbox("Date", df[df["student_id"] == student_id]["date"].unique())
            status = st.selectbox("Status", ["Present", "Absent"])

            if st.button("Update Attendance"):
                payload = {"student_id": student_id,  "date": date,"status": status == "Present"}
                update_res = requests.put(f"{BASE_URL}/teacher/attendance", json=payload, headers=headers)

                if update_res.status_code == 200:
                    st.success("Attendance updated successfully")
                    st.rerun()
                else:
                    st.error(update_res.text)

        with st.sidebar:
            if st.button("🚪 Logout"):
                st.session_state.clear()
                st.rerun()

# MAIN
if st.session_state.page == "login":
    login_page()
elif st.session_state.page == "signup":
    signup_page()
else:
    dashboard()
