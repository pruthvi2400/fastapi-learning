from fastapi import APIRouter, Depends, HTTPException,Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import get_db
from model import Student,User, Department
from schemas import StudentCreate, StudentResponse, StudentUpdate, StudentPatch
from model import User
from security import get_current_admin,get_current_user

from sqlalchemy.exc import IntegrityError

router = APIRouter()


# CREATE
@router.post("/", response_model=StudentResponse)
def create_student(
    student: StudentCreate,
    db: Session = Depends(get_db)
):
    new_student = Student(
        name=student.name,
        age=student.age,
        email=student.email,
        department_id=student.department_id
    )

    db.add(new_student)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Student with this email already exists"
        )
    db.refresh(new_student)

    return new_student


# READ ALL
@router.get("/", response_model=list[StudentResponse])
def get_students(
    skip : int = Query(0, ge=0),
    limit : int = Query(10, ge=1, le=100),
    name: str | None = None,
    department_id: int | None = None,
    sort_by: str | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    statement = select(Student)

    statement = select(Student).offset(skip).limit(limit)

    sort_columns = {
    "id": Student.id,
    "name": Student.name,
    "age": Student.age,
    }

    if sort_by:
        column = sort_columns.get(sort_by)

        if column is None:
            raise HTTPException(
                status_code=400,
                detail="Invalid sort_by. Use id, name, or age.",
        )

    if department_id is not None:
        department = (
            db.query(Department)
            .filter(Department.id == student.department_id)
            .first()
    )

        if department is None:
            raise HTTPException(
                status_code=404,
                detail="Department not found",
            )

        statement = statement.where(
            Student.department_id == department_id
        )

    statement = statement.order_by(column)

    if name :
        statement = statement.where(Student.name==name)

    if department_id:
        statement = statement.where(Student.department_id == department_id)

    if sort_by == "age":
        statement = statement.order_by(Student.age)

    elif sort_by == "name":
        statement = statement.order_by(Student.name)

    result = db.execute(statement)

    students = result.scalars().all()

    return students


# READ ONE
@router.get("/{student_id}", response_model=StudentResponse)
def get_student(
    student_id: int,
    db: Session = Depends(get_db)
):
    statement = select(Student).where(Student.id == student_id)

    result = db.execute(statement)

    student = result.scalar_one_or_none()

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return student


# UPDATE - PUT
@router.put("/{student_id}", response_model=StudentResponse)
def update_student(
    student_id: int,
    student_data: StudentUpdate,
    db: Session = Depends(get_db)
):
    statement = select(Student).where(Student.id == student_id)

    result = db.execute(statement)

    student = result.scalar_one_or_none()

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    student.name = student_data.name
    student.age = student_data.age
    student.email = student_data.email
    student.department_id = student_data.department_id

    db.commit()
    db.refresh(student)

    return student


# PARTIAL UPDATE - PATCH
@router.patch("/{student_id}", response_model=StudentResponse)
def patch_student(
    student_id: int,
    student_patch: StudentPatch,
    db: Session = Depends(get_db)
):
    statement = select(Student).where(Student.id == student_id)

    result = db.execute(statement)

    student = result.scalar_one_or_none()

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    update_data = student_patch.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(student, field, value)

    db.commit()
    db.refresh(student)

    return student


# DELETE
@router.delete("/{student_id}")
def delete_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    statement = select(Student).where(Student.id == student_id)

    result = db.execute(statement)

    student = result.scalar_one_or_none()

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    db.delete(student)
    db.commit()

    return {
        "message": "Student deleted successfully"
    }