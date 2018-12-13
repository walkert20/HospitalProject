from flask import Flask, request, make_response, json, url_for, abort
from db import Db   # See db.py
import json
import utils

app = Flask(__name__)
db = Db()
app.debug = True # Comment out when not testing
app.url_map.strict_slashes = False   # Allows for a trailing slash on routes

#### ERROR HANDLERS

@app.errorhandler(500)
def server_error(e):
   return make_json_response({ 'error': 'unexpected server error' }, 500)

@app.errorhandler(404)
def not_found(e):
   return make_json_response({ 'error': e.description }, 404)

@app.errorhandler(403)
def forbidden(e):
   return make_json_response({ 'error': e.description }, 403)

@app.errorhandler(400)
def client_error(e):
   return make_json_response({ 'error': e.description }, 400)
   
## Helper method for creating JSON responses
def make_json_response(content, response = 200, headers = {}):
   headers['Content-Type'] = 'application/json'
   return make_response(json.dumps(content), response, headers)
   
#### MAIN ROUTES

# Patient routes

@app.route('/patients', methods = ['GET'])
def patient_list():
    patients = db.getPatients()
    return make_json_response({
        "patients":[
        {
            "name": (patient.FirstName, patient.LastName),
            "doctor": str(patient.doctor)
        } for patient in patients
        ]
    })

@app.route('/<doctorId>/<patientId>', methods = ['GET'])
def patient_info(doctorId, patientId):
    patient = db.getPatient(patientId)
    if patient == None:
        abort(404, "Provided patient does not exist.")
    if patient.doctor == None:
        abort(404, "Patient doesn't have a doctor. One must be provided for them.")
    doctor = db.getDoctor(doctorId)
    if doctor == None:
        abort(404, "Provided doctor does not exist.")
    if patient.doctorId != doctor.id:
        abort(403, "You don't have access to this patient's file.")
    return make_json_response({
        "id":patient.id,
        "name": (patient.FirstName, patient.LastName),
        "infirmity" : patient.infirmity,
        "doctor": str(patient.doctor),
        "medication":patient.medication,
        "emition":str(patient.date_of_emition),
        })


@app.route('/patient', methods = ['POST'])
def create_patient():
    patientId = utils.makeId()
    patients = db.getPatients()
    ids = [patient.id for patient in patients]
    while patientId in ids:
        patientId = utils.makeId()
    return create_patient_with_id(patientId)

@app.route('/<patientId>', methods = ['PUT'])
def create_patient_with_id(patientId):
    patients = db.getPatients()
    ids = [patient.id for patient in patients]
    if patientId in ids:
        abort(403, "This patient already exists.")
    contents = request.get_json()
    if contents == None:
        abort(403, "You sent nothing.")
    if 'FirstName' not in contents:
        abort(403, "Must provide a first name.")
    if 'LastName' not in contents:
        abort(403, "Must include a last name.")
    FirstName = contents['FirstName']
    LastName = contents['LastName']
    db.addPatient(patientId, FirstName, LastName)
    db.commit()
    return make_json_response({'ok':'Patient was created successfully'}, 201)

@app.route('/<doctorId>/<patientId>', methods = ['DELETE'])
def delete_patient(doctorId, patientId):
    patients = db.getPatients()
    ids = [patient.id for patinet in patients]
    if patientId not in ids:
        abort(404, "There isn't a patient with this id.")
    patient = db.getPatient(patientId)
    doctor = db.getDoctor(doctorId)
    if doctor == None:
        abort(404, "Provided doctor does not exist.")
    if patient.doctorId != doctor.id:
        abort(403, "You don't have that kind of access.")
    db.deletePatient(patient)
    db.commit()
    return make_json_response({'ok':'Patient was deleted successfully'}, 204)


# Doctor routes


@app.route('/doctors', methods = ['GET'])
def doctor_list():
    doctors = db.getDoctors()
    return make_json_response({
        "doctors":[
        {
            "name": (doctor.FirstName, doctor.LastName),
            "profession":(doctor.profession),
            "patients":(doctor.patients)
        } for doctor in doctors
        ]
        })

@app.route('/<doctorId>', methods = ['GET'])
def doctor_info(doctorId):
	doctor = db.getDoctor(doctorId)
	return make_json_response({
		"doctor": {
			"name": (docotr.FirstName, doctor.LastName),
			"profession":(doctor.profession),
			"patients":(doctor.patients)
		}
		})

@app.route('/doctor', methods = ['POST'])
def create_doctor():
    doctorId = utils.makeId()
    doctors = db.getDoctors()
    ids = [docotr.id for docotr in doctors]
    while doctorId in ids:
        doctorId = utils.makeId()
    return create_doctor_with_id(doctorId)

@app.route('/<doctorId>', methods = ['PUT'])
def create_doctor_with_id(doctorId):
    doctors = db.getDoctors()
    ids = [doctor.id for doctor in doctors]
    if doctorId in ids:
        abort(403, "This doctor already exists.")
    contents = request.get_json()
    if contents == None:
        abort(403, "You sent nothing.")
    if 'FirstName' not in contents:
        abort(403, "Must provide a first name.")
    if 'LastName' not in contents:
        abort(403, "Must include a last name.")
    if 'profession' not in contents:
        abort(403, "Must include a profession")
    FirstName = contents['FirstName']
    LastName = contents['LastName']
    profession = contents['profession']
    db.addDoctor(doctorId, FirstName, LastName, profession)
    db.commit()
    return make_json_response({'ok':'Doctor was created successfully'}, 201)

@app.route('/<doctorId>', methods = ['DELETE'])
def delete_doctor(doctorId):
    doctors = db.getDoctor()
    ids = [doctor.id for doctor in doctors]
    if doctorId not in ids:
        abort(404, "There isn't a doctor with this id.")
    patient = db.getDoctor(patientId)
    doctor = db.getPatient(doctorId)
    if patient == None:
        abort(404, "Provided patient does not exist.")
    if doctor.patientId != patient.id:
        abort(403, "You don't have that kind of access.")
    db.deleteDoctor(patient)
    db.commit()
    return make_json_response({'ok':'Doctor was deleted successfully'}, 204)


@app.route('/<doctorId>/<patientId>/<medication>', methods = ['POST'])
def addMedication(doctorId, patientId, medication):
    patient = db.getPatient(patientId)
    if patient == None:
        abort(404, "Provided patient does not exist.")
    doctor = db.getDoctor(doctorId)
    if doctor == None:
        abort(404, "Provided doctor does not exist.")
    if patient.doctorId != doctor.id:
        abort(403, "You don't have that kind of access.")

    patientInfo = patient_info(doctorId, patientId)
    delete_patient(doctorId, patientId)
    db.addPatient(patientId, patientInfo['name'][0], patientInfo['name'][1],\
                  patientInfo['infirmity'], patientInfo['doctor'], medication,\
                  patientInfo['emition'])
    db.commit()

@app.route('/<doctorId>/<patientId>/<infirmity>', methods = ['POST'])
def addInfirmity(doctorId, patientId, infirmity):
    patient = db.getPatient(patientId)
    if patient == None:
        abort(404, "Provided patient does not exist.")
    doctor = db.getDoctor(doctorId)
    if doctor == None:
        abort(404, "Provided doctor does not exist.")
    if patient.doctorId != doctor.id:
        abort(403, "You don't have that kind of access.")

    patientInfo = patient_info(doctorId, patientId)
    delete_patient(doctorId, patientId)
    db.addPatient(patientId, patientInfo['name'][0], patientInfo['name'][1],\
                  infirmity, patientInfo['doctor'], patientInfo['medication'],\
                  patientInfo['emition'])
    db.commit()


# Starts the application
if __name__ == "__main__":
   app.run()
