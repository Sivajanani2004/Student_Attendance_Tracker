from fastapi import FastAPI
from routes.route import router

app = FastAPI(Title = 'Student_Attendance_Tracker')

app.include_router(router)