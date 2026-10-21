from fastapi import FastAPI
from routers import students, departments, auth
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(
    students.router,
    prefix="/students",
    tags=["Students"]
)

app.include_router(
    departments.router,
    prefix="/departments",
    tags=["Departments"]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)