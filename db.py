# Sets up database
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from json import dumps

Base = declarative_base()

# Doctor class
class Doctor(Base):
   __tablename__ ="doctor"

   id          = Collumn('id',String(), nullable = False, primary_key = True)  #THE ID OF THE DOCTOR CREATED BY THE SYSTEM
   FirstName   = Collumn('first',String(), nullable = False)   				   #THE FIRST NAME OF THE DOCTOR
   LastName    = Collumn('last',String(), nullable = False)                    #THE LAST NAME OF THE DOCTOR
   profession  = Collumn('profession',String(), nullable = False)              #THE PROFESSION OF THE DOCTOR
   patients    = relationship("Patient", back_populates = "doctor")     	   #THE RELATIONSHIP BETWEEN PATIENT AND DOCTOR
   


# Patient class
class Patient(Base):
   __tablename__ = "patient"

   id                = Collumn('id',String(), nullable = False, primary_key = True)  				#ID OF PATIENT
   FirstName         = Collumn('first',String(), default = "Jane")                      			#FIRST NAME OF PATIENT
   LastName          = Collumn('last',String(), default = "Doe")                       				#LAST NAME OF PATIENT
   date of emition   = Collumn('emition',DateTime.now(), nullable = False, default = datetime.now())#DATE PATIENT WAS EMITED
   infirmity         = relationship("Infirmity", back_populates = "illness")                    	#WHAT'S WRONG WITH THE PAINTENT
   medication        = relationship("Medication", back_populates = "meds")                     		#WHAT MEDICATIONS THE PATIENT HAS
   doctor            = relationship("Doctor", back_populates = "patients")    						#WHAT DOCTOR/S THE PATIENT HAS

# Medication class
class Medication(Base):
	__tablename__ = "Meds"

	id        = Collumn('id',String(), nullable = False, primary_key = True)  	#ID OF MEDICATION
	name 	  = Collumn('name',String(), nullable = False)  					#NAME OF THE MEDICATION
	meds      = relationship("Patient", back_populates = "medication")			#PATIENTS THAT HAVE THIS MEDICATION

# Infirmity class
class Infirmity(Base):
	__tablename__ = "illness"
	id 		 = Collumn('id',String(), nullable = False, primary_key = True)    #ID OF INFIRMITY
	name 	 = Collumn('name',String(), nullable = False)  					   #NAME OF INFIRMITY
	illness  = relationship("Patient", back_populates = "infirmity")		   #PATIENTS WHO HAVE THIS INFIRMITY

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
    self.session.delete(doctor)

#CREATES A DOCTOR WITH THE GIVEN FIRST NAME, LAST NAME, AND THEIR PROFESSION
def addDoctor(id, first, last, profession)
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
      return self.session.delete(patient)

#RETURNS A PATIENTS FIRST NAME
def patientFirst(self)
   return self.session.query(Patient).first()

#RETURNS A PATIENTS LAST NAME
def PatientLast(self)
   return self.session.query(Patient).last()

#RETURNS A PATIENTS FULL NAME
def PatientFull(self)
   first = patientFirst
   last = PatientLast
   return first + last

def addPatient(id)
   return self.session.add(Patient(id = id))

#Helper methods if needed

def addMed(self, )