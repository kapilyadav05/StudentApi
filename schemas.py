from pydantic import BaseModel


class StudentCreate(BaseModel):
    name: str
    age: int
    course: str
    marks: float


class StudentResponse(BaseModel):
    id: int
    name: str
    age: int
    course: str
    marks: float

    class Config:
        from_attributes = True