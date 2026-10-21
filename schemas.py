from pydantic import BaseModel,EmailStr, ConfigDict, Field 

class StudentCreate(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    age: int = Field(ge=0)
    email: EmailStr
    department_id: int

class DepartmentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str

class StudentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    age: int | None = None
    email: str | None = None
    department: DepartmentResponse | None = None

class StudentUpdate(BaseModel):
    name: str
    age: int
    email: str
    department_id: int

class StudentPatch(BaseModel):
    name: str | None = None
    age: int | None = None
    email: str | None = None
    department_id: int | None = None

class DepartmentCreate(BaseModel):
    name: str

class DepartmentUpdate(BaseModel):
    name: str

class StudentBasicResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    age: int | None = None
    email: str | None = None

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=200)

class UserResponse(BaseModel):

    id:int
    email:EmailStr
    role:str

    model_config = ConfigDict(from_attributes=True)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class ChangePassword(BaseModel):
    current_password: str
    new_password: str = Field(min_length=8, max_length=128)