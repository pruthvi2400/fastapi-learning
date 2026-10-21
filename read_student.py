from database import SessionLocal
from model import Student
from sqlalchemy import select

db = SessionLocal()

startment = select(Student)

result = db.execute(startment)

students = result.scalars().all()

for student in students:
    print(f"ID: {student.id}, Name: {student.name}, Age: {student.age}, Email: {student.email}, Course: {student.course}")      

db.close()

