from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True, index=True)

    illness_id = Column(Integer, ForeignKey('illness.id'), nullable=True)

    sponsees = relationship('User_Family', back_populates='sponsor')
    illness = relationship('Illness')
    patient_symptoms = relationship('PatientSymptoms')


class User_Family(Base):
    __tablename__ = 'user_family'

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)

    sponsor_id = Column(Integer, ForeignKey('user.id'))

    sponsor = relationship('User', back_populates='sponsees')
    patient_symptoms = relationship('PatientSymptoms')


class Illness(Base):
    __tablename__ = 'illness'

    id = Column(Integer, primary_key=True, index=True)
    name_of_illness = Column(String, unique=True)
    type_of_illness = Column(String)
    severity = Column(String)

    symptoms = relationship(
        'IllnessSymptoms', back_populates='illness')


class IllnessSymptoms(Base):
    __tablename__ = 'symptoms'

    id = Column(Integer, primary_key=True, index=True)
    symptoms = Column(String)

    illness_id = Column(Integer, ForeignKey('illness.id'))

    illness = relationship('Illness', back_populates='symptoms')


class PatientSymptoms(Base):
    __tablename__ = 'patient_symptoms'

    id = Column(Integer, primary_key=True, index=True)
    location = Column(String)
    how_long = Column(String)
    symptoms = Column(String)

    user_id = Column(Integer, ForeignKey('user.id'))
    sponsee_id = Column(Integer, ForeignKey('user_family.id'))
