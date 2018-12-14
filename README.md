# HospitalProject
This is a project in which my partner and I create a database that stores generated information similar to what would be seen in a hospital's database. It will use an SQLLite database to store information within 2 primary tables:
1 Doctors
2 Patients

API paths and methods:
 /patients
    GET: Returns a list of all patients currently admitted and their doctor.
    
 /<doctorId>/<patientId>:
    GET: Returns a particular patient's info (A doctor ID and patient ID must be given with the patient being assigned to that  doctor).
    DELETE: Deletes the patient (A doctor ID and patient ID must be given with the patient being assigned to that  doctor).
 
 /patient
    POST: Creates a patient with an auto-generated Id (A first name and last name must be given in request).
    
 /<patientId>
    PUT: Creates a patient with a given ID (An id of some kind must be given).
  
 /doctors
    GET: Returns a list of all the doctors and their patients and profession.
    
 /<doctorId>
    GET: Returns information on a specific doctor (A doctor ID is required).
    PUT: Creates a doctor with a given ID (An ID of some kind must be given).
    DELETE: deletes the doctor (A doctor ID must be given).
  
 /doctor
    POST: Creates a doctor with an auto-generated ID (A first name, last name, and profession must be given in request).
