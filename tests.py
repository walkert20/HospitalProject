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
db.addPatient_default(id = 1)
assert(len(db.getPatients()) == 2)
patient_1 = db.getPatient(PATIENT_ID)
assert(patient_1.id is not None)
assert(patient_1.id == PATIENT_ID)
assert(patient_1.FirstName == "Bob")
patient_2 = db.getPatient(2)
assert patient_2 is None
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
db.addPatient(id = PATIENT_ID, FirstName = "Bob", LastName = "Mann")
patient_1 = db.getPatient(PATIENT_ID)
# Checking doctors the patient has
assert(patient_1.doctorId is None)
assert(patient_1.doctor is None)
# Checking medications the patient has
assert(patient_1.medication is None)
# Checking infirmities the patient has
assert(patient_1.infirmity is None)



print("######  DOCTOR TESTS  ######")


# No Doctors to begin with
assert(len(db.getDoctors()) == 0)
# Creating a Doctor
db.addDoctor(id = DOCTOR_ID, FirstName = "Jane", LastName = "Doe", profession = "Surgen")
assert(len(db.getDoctors()) == 1)
assert(db.getDoctors()[0].FirstName == "Jane")
assert(db.getDoctors()[0].LastName == "Doe")
# Creating a Doctor with the default
db.addDoctor_default(id = 1, profession = "nurse")
assert(len(db.getDoctors()) == 2)
Doctor_1 = db.getDoctor(DOCTOR_ID)
assert(Doctor_1.id is not None)
assert(Doctor_1.id == DOCTOR_ID)
assert(Doctor_1.FirstName == "Jane")
Doctor_2 = db.getDoctor(2)
assert Doctor_2 is None
Doctor_2 = db.getDoctor(1)
assert(Doctor_2.FirstName == "Mary")
assert(Doctor_2.LastName == "Allan")
assert(db.getDoctors()[0] is Doctor_1)
db.commit()
# Deleting a Doctor
db.deleteDoctor(Doctor_1)
Doctor = db.getDoctor(DOCTOR_ID)
assert(Doctor is None)
# Re-creating the doctor for further testing
db.addDoctor(id = DOCTOR_ID, FirstName = "Jane", LastName = "Doe", profession = "Surgeon")
Doctor_1 = db.getDoctor(DOCTOR_ID)
# Checking for the patients this doctor has
assert(Doctor_1.patients == [])

print("################ DB TESTS DONE ###################")


print("################   API TESTS   ###################")

client = app.test_client()
def get_json(r):
   return json.loads(r.get_data().decode("utf-8"))

print("######  PATIENT TESTS  ######")


print("######  DOCTOR TESTS  ######")


print("################ ALL TESTS HAVE COMPLETED ###################")