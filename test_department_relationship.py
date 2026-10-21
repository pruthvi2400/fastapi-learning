from sqlalchemy import select
from sqlalchemy.orm import selectinload

from database import SessionLocal
from model import Department

db = SessionLocal()

statement = select(Department).where(
    Department.id == 1
).options(
    selectinload(Department.students)
)

result = db.execute(statement)

department = result.scalar_one()

print("Department:", department.name)

print("Now accessing students...")

for student in department.students:
    print(student.name)

db.close()
