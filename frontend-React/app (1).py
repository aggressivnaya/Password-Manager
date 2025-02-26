from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
import os

app = Flask(__name__)
CORS(app)

# In a real application, use a secure secret key and store it properly
app.config['SECRET_KEY'] = 'your-secret-key'

# In-memory storage (replace with a database in a real application)
users = []
passwords = []
groups = []

def token_required(f):
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        except:
            return jsonify({'message': 'Token is invalid!'}), 401
        return f(*args, **kwargs)
    return decorated

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = {
        'id': len(users) + 1,
        'username': data['username'],
        'password': hashed_password
    }
    users.append(new_user)
    return jsonify({'message': 'Registered successfully'}), 201

@app.route('/api/login', methods=['POST'])
def login():
    auth = request.json
    user = next((u for u in users if u['username'] == auth['username']), None)
    if not user or not check_password_hash(user['password'], auth['password']):
        return jsonify({'message': 'Invalid credentials'}), 401
    token = jwt.encode({
        'user_id': user['id'],
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }, app.config['SECRET_KEY'], algorithm="HS256")
    return jsonify({'token': token})

@app.route('/api/passwords', methods=['GET', 'POST'])
@token_required
def handle_passwords():
    if request.method == 'GET':
        return jsonify(passwords)
    elif request.method == 'POST':
        new_password = request.json
        passwords.append(new_password)
        return jsonify(new_password), 201

@app.route('/api/groups', methods=['GET', 'POST'])
@token_required
def handle_groups():
    if request.method == 'GET':
        return jsonify(groups)
    elif request.method == 'POST':
        new_group = request.json
        groups.append(new_group)
        return jsonify(new_group), 201

@app.route('/api/groups/<int:group_id>/passwords', methods=['GET', 'POST'])
@token_required
def handle_group_passwords(group_id):
    group = next((g for g in groups if g['id'] == group_id), None)
    if not group:
        return jsonify({"error": "Group not found"}), 404

    if request.method == 'GET':
        return jsonify(group.get('passwords', []))
    elif request.method == 'POST':
        new_password = request.json
        if 'passwords' not in group:
            group['passwords'] = []
        group['passwords'].append(new_password)
        return jsonify(new_password), 201

if __name__ == '__main__':
    app.run(debug=True)

