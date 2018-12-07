from flask import Flask, request, make_response, json, url_for, abort
from db import Db   # See db.py
import json

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

@app.route('/', methods = ['GET'])
def patient_list():
	patients = db.getPatients()
	return make_json_response({
		"patients":[
		{
			"name": (patient.FirstName, patient.LastName),
			"illness" : patient.infirmity,
			"doctor(s)": patient.doctor
		} for patient in patients
		]
		})

@app.route('/<patientId>', methods = ['GET'])
def patient_info(patientId):
	pass

@app.route('/', methods = ['POST'])
def create_patient():
	pass

@app.route('/<patientId>', methods = ['PUT'])
def create_patient_with_id(patientId):
	pass

@app.route('/<patientId>', methods = ['DELETE'])
def delete_patient(patientId):
	pass


# Doctor routes

app.route('/', methods = ['GET'])
def doctor_list():
	pass

@app.route('/<doctorId>', methods = ['GET'])
def doctor_info(doctorId):
	pass

@app.route('/', methods = ['POST'])
def create_doctor():
	pass

@app.route('/<doctorId>', methods = ['PUT'])
def create_doctor_with_id(doctorId):
	pass

@app.route('/<doctorId>', methods = ['DELETE'])
def delete_doctor(doctorId):
	pass

@app.route('/<doctorId>/<patientId>', methods = ['PUT'])
def addMedication(patientId, medication):
	pass

@app.route('/<doctorId>/<patientId>', methods = ['PUT'])
def addInfirmity(patientId, infirmity):
	pass

# Starts the application
if __name__ == "__main__":
   app.run()
