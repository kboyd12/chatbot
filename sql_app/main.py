from typing import List

from fastapi import Depends, FastAPI, HTTPException, Request
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
templates = Jinja2Templates(directory='sql_app/templates/')
app.mount("/static", StaticFiles(directory="sql_app/static"), name="static")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/')
def index(request: Request):
    return templates.TemplateResponse('index.html', context={'request': request})


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/sponsees/", response_model=schemas.User_Family)
def create_sponsee_for_user(
    user_id: int, sponsee: schemas.User_FamilyCreate, db: Session = Depends(get_db)
):
    return crud.create_user_family(db=db, sponsee=sponsee, user_id=user_id)


@app.get("/sponsees/", response_model=List[schemas.User_Family])
def all_sponsees(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    sponsees = crud.get_user_family(db, skip=skip, limit=limit)
    return sponsees


@app.get("/illnesses/", response_model=List[schemas.Illness])
def all_illnesses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    illnesses = crud.get_illnesses(db, skip=skip, limit=limit)
    return illnesses


@app.post("/illness/", response_model=schemas.Illness)
def create_illness(illness: schemas.IllnessCreate, db: Session = Depends(get_db)):
    db_illness = crud.get_illness_by_name(
        db, name_of_illness=illness.name_of_illness)
    if db_illness:
        raise HTTPException(
            status_code=400, detail="Illness already registered")
    return crud.create_illness(db=db, illness=illness)


@app.post("/illness/{illness_id}/symptoms/", response_model=schemas.IllnessSymptoms)
def create_illness_symptoms(illness_id: int, symptoms: schemas.IllnessSymptomsCreate, db: Session = Depends(get_db)):
    return crud.create_illness_symptoms(db=db, symptoms=symptoms, illness_id=illness_id)


@app.post("/users/symptoms/", response_model=schemas.PatientSymptoms)
def create_patient_symptoms(symptoms: schemas.PatientSymptomsCreate, user_id: int = None, sponsee_id: int = None, db: Session = Depends(get_db)):
    return crud.create_patient_symptoms(db, symptoms, user_id, sponsee_id)
