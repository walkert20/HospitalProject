from main import app, db
import json
import string
import random
from hashlib import md5

alphabet = string.ascii_uppercase + string.digits

def makeId():
   return ''.join([random.choice(alphabet) for _ in range(6)])

def getHash(password):
   return md5(password.encode('utf-8')).hexdigest()

session = db.session

PATIENT_ID = makeId()
DOCTOR_ID = makeId() 

print("################    DB TESTS   ###################")
print("######  PATIENT TESTS  ######")
# No Patients to begin with
assert(len(db.getPatients()) == 0)
# Creating a patient
db.addPatient(id = PATIENT_ID, FirstName = "Bob", LastName = "Mann")
assert(len(db.getPatients()) == 1)
assert(db.getPatients()[0].FirstName == "Bob")
assert(db.getPatients()[0].LastName == "Mann")
# Creating a patient with the default
db.addPatient(id = 1)
assert(len(db.getPatients()) == 2)
patient_1 = db.getPatient(PATIENT_ID)
assert(patient.id is not None)
assert(patient.id == PATIENT_ID)
patient_2 = db.getPatient(2)
assert patient_2.id is None
patient_2 = db.getPatient(1)
assert patient_2.FirstName == "Jane"
assert patient_2.LastName == "Doe"
assert(db.getPatients()[0] is patient_1)
db.commit()
# Deleting a patient
db.deletePatient(patient_1)
patient = db.getPatient(PATIENT_ID)
assert(patient is None)
# Re-creating the patient for further testing (No actual humans were harmed in the making
# of these tests.)
patient_1 = db.addPatient(id = PATIENT_ID, first = "Bob", last = "Mann")


print("######  DOCTOR TESTS  ######")


# No Doctors to begin with
assert(len(db.getDoctors()) == 0)
# Creating a Doctor
db.addDoctor(id = DOCTOR_ID, first = "Jane", last = "Doe")
assert(len(db.getDoctors()) == 1)
assert(db.getDoctors()[0].FirstName == "Jane")
assert(db.getDoctors()[0].LastName == "Doe")
# Creating a Doctor with the default
db.addDoctor(id = 1)
assert(len(db.getDoctors()) == 2)
Doctor_1 = db.getDoctor(DOCTOR_ID)
assert(Doctor.id is not None)
assert(Doctor.id == Doctor_ID)
Doctor_2 = db.getDoctor(2)
assert Doctor_2.id is None
Doctor_2 = db.getDoctor(1)
assert(Doctor_2.FirstName == "Mary")
assert(Doctor_2.LastName == "Allan")
assert(db.getDoctors()[0] is Doctor_1)
db.commit()
# Deleting a Doctor
db.deleteDoctor(Doctor_1)
Doctor = db.getDoctor(DOCTOR_ID)
assert(Doctor is None)
# Re-creating the Doctor for further testing (No actual humans were harmed in the making
# of these tests.)
Doctor_1 = db.addPatient(id = DOCTOR_ID, first = "Jane", last = "Doe")


print("################ DB TESTS DONE ###################")


print("################   API TESTS   ###################")

print("######  PATIENT TESTS  ######")


print("######  DOCTOR TESTS  ######")


print("################ ALL TESTS HAVE COMPLETED ###################")