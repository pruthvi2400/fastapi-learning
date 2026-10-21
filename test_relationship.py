from database import SessionLocal
from model import Student

db = SessionLocal()

student = db.get(Student, 1)

print("Student:", student.name)
print("Department ID:", student.department_id)
print("Department:", student.department.name)

db.close()