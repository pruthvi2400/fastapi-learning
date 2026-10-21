from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import get_db
from model import Department, Student
from schemas import  DepartmentCreate, DepartmentResponse, DepartmentUpdate,  StudentBasicResponse

router = APIRouter()

@router.get("/", response_model=list[DepartmentResponse])
def get_departments(
    db: Session = Depends(get_db)
):
    statement = select(Department)
    result = db.execute(statement)
    departments = result.scalars().all()
    return departments

@router.post("/", response_model=DepartmentResponse)
def create_department(
    department: DepartmentCreate,
    db: Session = Depends(get_db)
):
    new_department = Department(
        name=department.name
    )

    db.add(new_department)
    db.commit()
    db.refresh(new_department)

    return new_department

@router.get("/{department_id}", response_model=DepartmentResponse)
def get_department(
    department_id: int,
    db: Session = Depends(get_db)
):
    statement = select(Department).where(
        Department.id == department_id
    )

    result = db.execute(statement)

    department = result.scalar_one_or_none()

    if department is None:
        raise HTTPException(
            status_code=404,
            detail="Department not found"
        )

    return department

@router.put("/{department_id}", response_model=DepartmentResponse)
def update_department(
    department_id: int,
    department_data: DepartmentUpdate,
    db: Session = Depends(get_db)
):
    statement = select(Department).where(
        Department.id == department_id
    )

    result = db.execute(statement)

    department = result.scalar_one_or_none()

    if department is None:
        raise HTTPException(
            status_code=404,
            detail="Department not found"
        )

    department.name = department_data.name

    db.commit()
    db.refresh(department)

    return department

@router.delete("/{department_id}")
def delete_department(
    department_id: int,
    db: Session = Depends(get_db)
):
    statement = select(Department).where(
        Department.id == department_id
    )

    result = db.execute(statement)

    department = result.scalar_one_or_none()

    if department is None:
        raise HTTPException(
            status_code=404,
            detail="Department not found"
        )

    db.delete(department)
    db.commit()

    return {
        "message": "Department deleted successfully"
    }

@router.get("/{department_id}/students",
    response_model=list[StudentBasicResponse])
def get_department_students(
    department_id: int,
    db: Session = Depends(get_db)
):
    statement = select(Student).where(
        Student.department_id == department_id
    )

    department = db.get(Department, department_id)

    if department is None:
        raise HTTPException(
            status_code=404,
            detail="Department not found"
    )

    result = db.execute(statement)

    students = result.scalars().all()

    return students