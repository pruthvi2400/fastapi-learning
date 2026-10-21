from sqlalchemy import select
from database import SessionLocal
from model import Student

db = SessionLocal()

student_id = 101

statement = select(Student).where(Student.id == student_id)

result = db.execute(statement)

student = result.scalar_one_or_none()

if student:
    print(f"ID: {student.id}, Name: {student.name}, Age: {student.age}, Email: {student.email}, Course: {student.course}")
else:
    print(f"Student with ID {student_id} not found.")

db.close()