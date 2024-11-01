from flask import Flask, jsonify, request, abort

app = Flask(__name__)

# Initial list of users
users = [
    {"ID": 1, "Name": "Alice", "Grade": "1", "Email": "alice@gmail.com"},
    {"ID": 2, "Name": "Bob", "Grade": "2", "Email": "bob@gmail.com"},
    {"ID": 3, "Name": "Justin", "Grade": "3", "Email": "justin@gmail.com"}
]

# Helper function to find user by ID
def find_user(user_id):
    return next((user for user in users if user["ID"] == user_id), None)

# GET /students - Retrieve a list of all students
@app.route('/students', methods=['GET'])
def get_students():
    return jsonify(users), 200

# GET /students/{id} - Retrieve details of a student by ID
@app.route('/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    student = find_user(student_id)
    if not student:
        abort(404, description="Student not found")
    return jsonify(student), 200

# POST /students - Add a new student
@app.route('/students', methods=['POST'])
def add_student():
    data = request.json
    if not data or 'Name' not in data or 'Grade' not in data or 'Email' not in data:
        abort(400, description="Invalid input")
    
    # Find the max ID in the current list and increment by 1 for the new student
    new_id = max(user["ID"] for user in users) + 1
    new_student = {
        "ID": new_id,
        "Name": data['Name'],
        "Grade": data['Grade'],
        "Email": data['Email']
    }
    users.append(new_student)
    return jsonify(new_student), 201

# PUT /students/{id} - Update an existing student by ID
@app.route('/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    student = find_user(student_id)
    if not student:
        abort(404, description="Student not found")
    
    data = request.json
    if 'Name' in data:
        student['Name'] = data['Name']
    if 'Grade' in data:
        student['Grade'] = data['Grade']
    if 'Email' in data:
        student['Email'] = data['Email']
    
    return jsonify(student), 200

# DELETE /students/{id} - Delete a student by ID
@app.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    student = find_user(student_id)
    if not student:
        abort(404, description="Student not found")
    
    users.remove(student)
    return '', 204

# Run the app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')