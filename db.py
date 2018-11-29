# Sets up database
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from json import dumps

Base = declarative_base()

# Doctor class
class Doctor(Base):
   __tablename__ ="doctor"

   FirstName   = Collumn(String, nullable = False)                      #THE FIRST NAME OF THE DOCTOR
   LastName    = Collumn(String, nullable = False)                      #THE LAST NAME OF THE DOCTOR
   profession  = Collumn(String, nullable = False)                      #THE PROFESSION OF THE DOCTOR
   id          = Collumn(String, nullable = False, primary_key = True)  #THE ID OF THE DOCTOR CREATED BY THE SYSTEM
   patients    = relationship("Patient", back_populates = "doctor")     #THE RELATIONSHIP BETWEEN PAITENT AND DOCTOR
   


# Patient class
class Paitent(Base):
   __tablename__ = "patient"

   FirstName         = Collumn(String, default = "Jane")                      #FIRST NAME OF PAITENT
   LastName          = Collumn(String, default = "Doe")                       #LAST NAME OF PAITENT
   id                = Collumn(String, nullable = False, primary_key = True)  #ID OF PAITENT
   infirmnity        = Collumn(List, default = "unknown")                     #WHATS WRONG WITH THE PAINTENT
   medication        = Collumn(List, default = "unknown")                     #WHAT MEDS THE PAITENT NEEDS
   date of emition   = Collumn(DateTime.now(), nullable = False)              #DATE THE WERE EMITED
   doctor            = relationship("Doctor", back_populates = "patients")    #WHAT DOCTOR/S THE PAITENT HAS
   

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


#Methods

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
      return self.session.delete(doctor)

def addDoctor(id, first, last, profession)
   return self.session.add(Doctor(id = id, first = first, last = last, profession = profession))


# Patient methods

#GETS THE PAITENT WITH THE GIVEN ID IF ONE EXISTS
def getPaitent(self, id):
   return self.session.query(Patient)\
                 .filter_by(id = id)\
                 .one_or_none()

#GIVES BACK ALL PAITENTS
def getPaitents(self):
   return self.session.query(Patient).all()

#DELETES A GIVEN PAITENT
def deletePaitent(self, patient):
      return self.session.delete(patient)

#RETURNS A PAITENTS FIRST NAME
def paitentFirst(self)
   return self.session.query(Patient).first()

#RETURNS A PAITENTS LAST NAME
def PaitentLast(self)
   pass

#RETURNS A PAITENTS FULL NAME
def PaitnetFull(self)
   first = paitentFirst
   last = PaitentLast
   return first + last

def addPaitent(id)
   return self.session.add(Patient(id = id))


#Helper methods if needed
