from database import SessionLocal
from model import Student

db = SessionLocal()

student = Student(
    id=103,
    name="Rajut",
    age=21,
    email="rajut@gmail.com",
    course="AI & DS"
)

db.add(student)

db.commit()

print("Student inserted successfully!")

db.refresh(student)

db.close()
print("Student ID:", student.id)
