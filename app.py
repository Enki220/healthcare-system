from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask app
app = Flask(__name__)

# Set up the database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///patients.db'  # SQLite database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking

# Initialize the database
db = SQLAlchemy(app)

# Create the Patient model
class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    condition = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"<Patient {self.name}, Age {self.age}, Condition {self.condition}>"

# Home route
@app.route('/')
def home():
    return "Flask is working!"

# Route to add a patient
@app.route('/add_patient', methods=['POST'])
def add_patient():
    patient_data = request.get_json()
    new_patient = Patient(
        name=patient_data['name'],
        age=patient_data['age'],
        condition=patient_data['condition']
    )
    db.session.add(new_patient)
    db.session.commit()
    return jsonify({"message": "Patient added successfully", "patient": {
        "id": new_patient.id,
        "name": new_patient.name,
        "age": new_patient.age,
        "condition": new_patient.condition
    }}), 201

# Route to get all patients
@app.route('/patients', methods=['GET'])
def get_patients():
    patients = Patient.query.all()  # Retrieve all patients from the database
    patients_list = []
    for patient in patients:
        patients_list.append({
            "id": patient.id,
            "name": patient.name,
            "age": patient.age,
            "condition": patient.condition
        })
    return jsonify({"patients": patients_list})

# Route to get a specific patient by ID
@app.route('/patient/<int:id>', methods=['GET'])
def get_patient(id):
    patient = Patient.query.get(id)  # Retrieve a specific patient
    if patient is None:
        return jsonify({"message": "Patient not found"}), 404
    return jsonify({
        "id": patient.id,
        "name": patient.name,
        "age": patient.age,
        "condition": patient.condition
    })

# Route to delete a patient by ID
@app.route('/delete_patient/<int:id>', methods=['DELETE'])
def delete_patient(id):
    patient = Patient.query.get(id)
    if patient is None:
        return jsonify({"message": "Patient not found"}), 404
    db.session.delete(patient)
    db.session.commit()
    return jsonify({"message": "Patient deleted successfully"}), 200

if __name__ == "__main__":
    # Create all tables (if not already created)
    with app.app_context():
        db.create_all()
    
    # Run the app
    app.run(debug=True)
