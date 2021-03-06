# Sets up database
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from json import dumps
from datetime import datetime, timedelta

Base = declarative_base()

# Doctor class
class Doctor(Base):
   __tablename__ = "doctor"

   id          = Column('id',String(), nullable = False, primary_key = True)  #THE ID OF THE DOCTOR CREATED BY THE SYSTEM
   FirstName   = Column('first',String(), nullable = False, default = "Mary") #THE FIRST NAME OF THE DOCTOR
   LastName    = Column('last',String(), nullable = False, default = "Allan") #THE LAST NAME OF THE DOCTOR
   profession  = Column('profession',String(), nullable = False)              #THE PROFESSION OF THE DOCTOR
   patients    = relationship("Patient", back_populates = "doctor")           #THE RELATIONSHIP BETWEEN PATIENT AND DOCTOR
   def __repr__(self): 
      return "Doctor<%s %s>" % (self.FirstName, self.LastName) 
   #Note: doctor.patients is a list(somehow). Therefore, no patients means an empty list.
   

# Patient class
class Patient(Base):
   __tablename__ = "patient"

   id                = Column('id',String(), nullable = False, primary_key = True)  #ID OF PATIENT
   FirstName         = Column('first',String(), default = "Jane")                   #FIRST NAME OF PATIENT
   LastName          = Column('last',String(), default = "Doe")                     #LAST NAME OF PATIENT
   date_of_emition   = Column('emition', DateTime, default = datetime.now())        #DATE PATIENT WAS EMITED
   doctorId          = Column('doctorId', String(), ForeignKey("doctor.id"))
   infirmity         = Column('infirmity', String(), default = None)
   medication        = Column('medication', String(), default = None)
   doctor            = relationship("Doctor", back_populates = "patients")          #WHAT DOCTOR/S THE PATIENT HAS
   def __repr__(self): 
      return "Patient<%s %s %s %s %s %s>" % (self.id, self.FirstName, self.LastName,\
                                             self.doctorId, self.infirmity, self.medication) 

#Database and our interactions with it
class Db:
   def __init__(self):
      engineName = 'sqlite:///test.db'              # Uses in-memory database
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
   def addDoctor(self, id, FirstName, LastName, profession):
      return self.session.add(Doctor(id = id, FirstName = FirstName, LastName = LastName, profession = profession))

#CREATES A DOCTOR USING THE DEFAULT NAMES
   def addDoctor_default(self, id, profession):
      return self.session.add(Doctor(id = id, profession = profession))


#SETS A DOCTOR TO A PATIENT
   def setDoctorToPatient(self, doctorId, patientId):
      doctor = self.getDoctor(doctorId)
      patient = self.getPatient(patientId)
      if doctor != None and patient != None:
         patient.doctorId = doctorId
         patient.doctor = doctor


#RETRIEVES ALL PATIENTS ASSIGNED TO A PARTICULAR DOCTOR
   def getDoctorPatients(self, doctorId):
      doctor = self.getDoctor(doctorId)
      return doctor.patients


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

#CREATES A PATIENT WITH THE GIVEN ID, FIRST NAME, AND LAST NAME
   def addPatient(self, id, FirstName, LastName):
      return self.session.add(Patient(id = id, FirstName = FirstName, LastName = LastName))

#CREATES A PATIENT USING THE DEFAULT NAMES
   def addPatient_default(self, id):
      return self.session.add(Patient(id = id))

#CREATES A PATIENT WITH THE GIVEN ID, FIRST NAME, LAST NAME, INFIRMITY, DOCTOR, AND DATE OF EMMISION
   def addPatient_all(self, id, FirstName, LastName, doctor, medication, infirmity, date_of_emition):
      patient = Patient(id=id, FirstName=FirstName, LastName=LastName, doctor=doctor,\
         medication=medication, infirmity=infirmity, date_of_emition=date_of_emition)
      return self.session.add(patient)