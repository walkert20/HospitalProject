# Sets up database
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from json import dumps
from datetime import datetime, timedelta

Base = declarative_base()

# Doctor class
class Doctor(Base):
   __tablename__ ="doctor"

   id          = Column('id',String(), nullable = False, primary_key = True)  #THE ID OF THE DOCTOR CREATED BY THE SYSTEM
   FirstName   = Column('first',String(), nullable = False, default = "Mary")                   #THE FIRST NAME OF THE DOCTOR
   LastName    = Column('last',String(), nullable = False, default = "Allan")                    #THE LAST NAME OF THE DOCTOR
   profession  = Column('profession',String(), nullable = False)              #THE PROFESSION OF THE DOCTOR
   
   patients    = relationship("Patient", back_populates = "doctor")            #THE RELATIONSHIP BETWEEN PATIENT AND DOCTOR
   

# Patient class
class Patient(Base):
   __tablename__ = "patient"

   id                = Column('id',String(), nullable = False, primary_key = True)                  #ID OF PATIENT
   FirstName         = Column('first',String(), default = "Jane")                                   #FIRST NAME OF PATIENT
   LastName          = Column('last',String(), default = "Doe")                                     #LAST NAME OF PATIENT
   date_of_emition   = Column('emition', DateTime, default = datetime.now())                        #DATE PATIENT WAS EMITED
   
   infirmity         = relationship("Infirmity", back_populates = "illness")                        #WHAT'S WRONG WITH THE PAINTENT
   medication        = relationship("Medication", back_populates = "meds")                          #WHAT MEDICATIONS THE PATIENT HAS
   doctor            = relationship("Doctor", back_populates = "patients")                          #WHAT DOCTOR/S THE PATIENT HAS

# Medication class
class Medication(Base):
    __tablename__ = "Meds"

    id        = Column('id',String(), nullable = False, primary_key = True)    #ID OF MEDICATION
    name      = Column('name',String(), nullable = False)                      #NAME OF THE MEDICATION
    
    meds      = relationship("Patient", back_populates = "medication")          #PATIENTS THAT HAVE THIS MEDICATION

# Infirmity class
class Infirmity(Base):
    __tablename__ = "illness"
    id       = Column('id',String(), nullable = False, primary_key = True)    #ID OF INFIRMITY
    name     = Column('name',String(), nullable = False)                      #NAME OF INFIRMITY
    
    illness  = relationship("Patient", back_populates = "infirmity")           #PATIENTS WHO HAVE THIS INFIRMITY

#Database and our interactions with it
class Db:
   def __init__(self):
      engineName = 'sqlite:///test.db'   # Uses in-memory database
      self.engine = create_engine(engineName)
      self.metadata = Base.metadata
      self.metadata.bind = self.engine
      self.metadata.drop_all(bind=self.engine)
      self.metadata.create_all(bind=self.engine)
      Session = sessionmaker(bind=self.engine)
      self.session = Session()

   def commit(self):
      self.session.commit()

   def rollback(self):
      self.session.rollback()


#METHODS

# Doctor methods

#GETS THE DOCTOR WITH THE GIVEN ID IF ONE EXISTS
   def getDoctor(self, id):
      return self.session.query(Doctor)\
                 .filter_by(id = id)\
                 .one_or_none()

#GIVES BACK ALL DOCTORS
   def getDoctors(self):
      return self.session.query(Doctor).all()

#DELETES A GIVEN DOCTOR
   def deleteDoctor(self, doctor):
      self.session.delete(doctor)

#CREATES A DOCTOR WITH THE GIVEN ID, FIRST NAME, LAST NAME, AND THEIR PROFESSION
   def addDoctor(self, id, first, last, profession):
      return self.session.add(Doctor(id = id, first = first, last = last, profession = profession))


# Patient methods

#GETS THE PATIENT WITH THE GIVEN ID IF ONE EXISTS
   def getPatient(self, id):
      return self.session.query(Patient)\
                 .filter_by(id = id)\
                 .one_or_none()

#GIVES BACK ALL PATIENTS
   def getPatients(self):
      return self.session.query(Patient).all()

#DELETES A GIVEN PATIENT
   def deletePatient(self, patient):
      self.session.delete(patient)

#CREATEs A PATIENT WITH THE GIVEN ID, FIRST NAME, AND LAST NAME
   def addPatient(self, id, first, last):
      return self.session.add(Patient(id = id, first = first, last = last))

# Medication methods

#CREATES A MEDICATION WITH THE GIVEN ID AND NAME
   def addMedication(self, id, name):
      medication = Medication(id = id, name = name)
      return self.session.add(medication)

#RETRIEVES THE MEDICATION WITH THE GIVEN ID IF ONE EXISTS
   def getMedication(self, id):
      return self.session.query(Medication).filter_by(id = id)\
           .one_or_none()

#DELETES THE GIVEN MEDICATION
   def removeMedication(self, medication):
      self.session.delete(medication)

# Infirmity methods

#CREATE AN INFIRMITY WITH THE GIVEN ID AND NAME
   def addInfirmity(self, id, name):
      infirmity = Infirmity(id = id, name = name)
      return self.session.add(infirmity)

#RETRIEVES THE INFRIMITY WITH THE GIVEN ID IF ONE EXISTS
   def getInfirmity(self, id):
      return self.session.query(Infirmity).filter_by(id = id)\
           .one_or_none()

#DELETES THE GIVEN INFIRMITY
   def removeInfirmity(self, infirmity):
      self.session.delete(infirmity)