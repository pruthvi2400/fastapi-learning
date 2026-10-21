from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from sqlalchemy import Column, Integer, String
import sqlalchemy as sa
from sqlalchemy import CheckConstraint, ForeignKey,DateTime
from datetime import datetime



class Base(DeclarativeBase):
    pass

class Student(Base):
    __tablename__="students"
    id:Mapped[int]=mapped_column(primary_key=True)
    name: Mapped[str]=mapped_column()
    age: Mapped[int] = mapped_column(CheckConstraint("age >= 0"),)
    email: Mapped[str] = mapped_column(unique=True)
    phone_number: Mapped[str | None] = mapped_column(
    nullable=True)
    city: Mapped[str | None] = mapped_column(sa.String(100), nullable=True)

    department_id: Mapped[int] = mapped_column(
        ForeignKey("departments.id")
    )

    department: Mapped["Department"] = relationship(
        back_populates="students"
    )

    __table_args__ = (
    CheckConstraint("age >= 0", name="check_student_age_nonnegative"),
)

class Department(Base):
    __tablename__ = "departments"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()

    students: Mapped[list["Student"]] = relationship(
         back_populates="department"
    )

class User(Base):
    __tablename__ = "users"

    id :Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(255), unique=True, index=True
    )
    hashed_password: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(
        String(20), default="user"
    )


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id: Mapped[int] = mapped_column(primary_key=True)
    token: Mapped[str] = mapped_column(String(500), unique=True, index=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
    revoked: Mapped[bool] = mapped_column(default=False, nullable=False)

