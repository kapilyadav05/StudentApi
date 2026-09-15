from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from model import Student
from schemas import StudentCreate, StudentResponse


# Create database table
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Student API",
    description="Student CRUD API using FastAPI and PostgreSQL",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "Student API is running successfully"
    }




# CREATE STUDENT

@app.post("/students", response_model=StudentResponse)
def create_student(
    student: StudentCreate,
    db: Session = Depends(get_db)
):

    new_student = Student(
        name=student.name,
        age=student.age,
        course=student.course,
        marks=student.marks
    )

    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return new_student


# GET ALL STUDENTS

@app.get("/students", response_model=list[StudentResponse])
def get_students(db: Session = Depends(get_db)):

    students = db.query(Student).all()

    return students



# GET STUDENT BY ID

@app.get("/students/{student_id}", response_model=StudentResponse)
def get_student(
    student_id: int,
    db: Session = Depends(get_db)
):

    student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return student


# UPDATE STUDENT

@app.put("/students/{student_id}", response_model=StudentResponse)
def update_student(
    student_id: int,
    student_data: StudentCreate,
    db: Session = Depends(get_db)
):

    student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    student.name = student_data.name
    student.age = student_data.age
    student.course = student_data.course
    student.marks = student_data.marks

    db.commit()
    db.refresh(student)

    return student


# =========================
# DELETE STUDENT
# =========================

@app.delete("/students/{student_id}")
def delete_student(
    student_id: int,
    db: Session = Depends(get_db)
):

    student = db.query(Student).filter(
        Student.id == student_id
    ).first()

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