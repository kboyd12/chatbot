from typing import List, Optional

from pydantic import BaseModel, EmailStr


class PatientSymptomsBase(BaseModel):
    location: str
    how_long: str
    symptoms: str


class PatientSymptomsCreate(PatientSymptomsBase):
    pass


class PatientSymptoms(PatientSymptomsBase):
    id: int
    user_id: Optional[int]
    sponsee_id: Optional[int]

    class Config:
        orm_mode = True


class IllnessSymptomsBase(BaseModel):
    symptoms: str


class IllnessSymptomsCreate(IllnessSymptomsBase):
    pass


class IllnessSymptoms(IllnessSymptomsBase):
    id: int
    illness_id: int

    class Config:
        orm_mode = True


class IllnessBase(BaseModel):
    name_of_illness: str
    type_of_illness: str
    severity: str


class IllnessCreate(IllnessBase):
    pass


class Illness(IllnessBase):
    id: int
    symptoms: List[IllnessSymptoms] = []

    class Config:
        orm_mode = True


class User_FamilyBase(BaseModel):
    first_name: str
    last_name: str


class User_FamilyCreate(User_FamilyBase):
    pass


class User_Family(User_FamilyBase):
    id: int
    sponsor_id: int

    patient_symptoms: List[PatientSymptoms] = []

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int

    sponsees: List[User_Family] = []
    patient_symptoms: List[PatientSymptoms] = []

    class Config:
        orm_mode = True
