from sqlalchemy.orm import Session
from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        email=user.email, first_name=user.first_name, last_name=user.last_name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_family(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User_Family).offset(skip).limit(limit).all()


def create_user_family(db: Session, sponsee: schemas.User_FamilyCreate, user_id: int):
    db_user_family = models.User_Family(**sponsee.dict(), sponsor_id=user_id)
    db.add(db_user_family)
    db.commit()
    db.refresh(db_user_family)
    return db_user_family

######################################################################################


def get_illness_by_name(db: Session, name_of_illness: str):
    return db.query(models.Illness).filter(models.Illness.name_of_illness == name_of_illness).first()


def create_illness(db: Session, illness: schemas.IllnessCreate):
    db_illness = models.Illness(name_of_illness=illness.name_of_illness,
                                type_of_illness=illness.type_of_illness, severity=illness.severity)
    db.add(db_illness)
    db.commit()
    db.refresh(db_illness)
    return db_illness


def get_illnesses(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Illness).offset(skip).limit(limit).all()


def create_illness_symptoms(db: Session, symptoms: schemas.IllnessSymptomsCreate, illness_id: int):
    db_ill_symp = models.IllnessSymptoms(
        symptoms=symptoms.symptoms, illness_id=illness_id)
    db.add(db_ill_symp)
    db.commit()
    db.refresh(db_ill_symp)
    return db_ill_symp


def create_patient_symptoms(db: Session, pat_symp: schemas.PatientSymptomsCreate, user_id: int = None, user_family_id: int = None):
    if user_id:
        db_pat_symp = models.PatientSymptoms(
            **pat_symp.dict(), user_id=user_id)
    elif user_family_id:
        db_pat_symp = models.PatientSymptoms(
            **pat_symp.dict(), sponsee_id=user_family_id)
    db.add(db_pat_symp)
    db.commit()
    db.refresh(db_pat_symp)
    return db_pat_symp
