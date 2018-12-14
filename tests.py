from main import app, db
from utils import makeId, getHash
import utils
import json
from datetime import datetime, timedelta   #for testing

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
# Checking doctors the patient has (should be none)
assert(patient_1.doctorId is None)
assert(patient_1.doctor is None)
# Checking medications the patient has (should be none)
assert(patient_1.medication is None)
# Checking infirmities the patient has (should be none)
assert(patient_1.infirmity is None)
db.commit()


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
db.commit()


# Testing setDoctorToPatient
assert(patient_1.doctorId is None)
assert(patient_1.doctor is None)
assert(Doctor_1.patients == [])
db.setDoctorToPatient(DOCTOR_ID, PATIENT_ID)
assert(patient_1.doctorId is not None)
assert(patient_1.doctor is not None)
assert(len(Doctor_1.patients) == 1)
assert(Doctor_1.patients[0].id == PATIENT_ID)
db.commit()
# Testing getDoctorPatients
assert(Doctor_2.patients == [])
lst = db.getDoctorPatients(Doctor_2.id)
assert(len(lst) == 0)
lst = db.getDoctorPatients(Doctor_1.id)
assert(len(lst) == 1)
db.commit()
# Testing addPatient_all
patient_3 = db.getPatient(9)
assert(patient_3 == None)
lst = db.getDoctors()
doc = lst[0]
db.addPatient_all(id=9, FirstName="Kevin", LastName="Prat", doctor=doc,\
			medication="advil",infirmity="headach", date_of_emition=datetime(2018,10,6,8,0,0))
patient = db.getPatient(9)
assert(patient != None)
assert(patient.FirstName == "Kevin")
assert(patient.LastName == "Prat")
assert(patient.doctor == doc)


print("############### DB TESTS DONE ##################")


print("###############   API TESTS   ##################")

client = app.test_client()
def get_json(r):
   return json.loads(r.get_data().decode("utf-8"))

print("######  PATIENT TESTS  ######")
# testing existing patients
r = client.get('/patients')
assert(r.status_code == 200)
contents = get_json(r)
assert("patients" in contents)
assert(len(contents["patients"]) == 3) 		#Because of the already created patients

# testing create a patient with ID
r = client.put('/' + PATIENT_ID)
assert(r.status_code == 403)
r = client.put('/newPatient')
assert(r.status_code == 403)
r = client.put('/newPatient', data=json.dumps({"FirstName":"Tom"}), content_type='application/json')
assert(r.status_code == 403)
r = client.put('/newPatient', data=json.dumps({"FirstName":"Tom", "LastName":"Wilks"}), content_type='application/json')
contents = get_json(r)
assert(r.status_code == 201)

# testing create a patient without ID
r = client.post('/patient')
assert(r.status_code == 403)
r = client.post('/patient', data=json.dumps({"FirstName":"David", "LastName":"Wilks"}), content_type='application/json')
assert(r.status_code == 201)

# testing patient_info
r = client.get( '/' + DOCTOR_ID + '/oldPatient')
assert(r.status_code == 404)
r = client.get('/DoctorId/newPatient')
assert(r.status_code == 404)
db.setDoctorToPatient(Doctor_2.id, patient_2.id)
r = client.get('/' + DOCTOR_ID + '/' + patient_2.id)
assert(r.status_code == 403)
r = client.get('/' + DOCTOR_ID + '/' + PATIENT_ID)
assert(r.status_code == 200)

#Testing delete patient
r = client.get('/patients')
contents = get_json(r)
patient = contents["patients"][-1]
r = client.delete('/DoctorId/newPatient')
assert(r.status_code == 404)
r = client.delete('/DoctorId/' + patient_2.id)
assert(r.status_code == 404)
r = client.delete('/' + DOCTOR_ID + '/' + patient_2.id)
assert(r.status_code == 403)
r = client.delete('/' + DOCTOR_ID + '/' + PATIENT_ID)
assert(r.status_code == 204)


#Testing addMedication
#testing addInfirmity


print("######  DOCTOR TESTS  ######")


print("################ ALL TESTS HAVE COMPLETED ###################")