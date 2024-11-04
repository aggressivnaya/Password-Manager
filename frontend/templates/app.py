from flask import Flask, render_template, request, redirect, jsonify

app = Flask(__name__)

# Sample data (Replace this with actual DB integration)
users = {"test@example.com": {"password": "12345", "private_passwords": ["Google", "Facebook"], "groups": ["Group1"]}}
groups = {"Group1": [{"name": "SharedPassword1"}, {"name": "SharedPassword2"}]}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    if email in users and users[email]['password'] == password:
        return redirect('/dashboard')
    return "Login Failed", 401

@app.route('/signup', methods=['POST'])
def signup_post():
    email = request.form['email']
    password = request.form['password']
    users[email] = {"password": password, "private_passwords": [], "groups": []}
    return redirect('/')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/getPrivatePasswords', methods=['GET'])
def get_private_passwords():
    # Assuming user is logged in, hardcoded example for test@example.com
    return jsonify(users["test@example.com"]["private_passwords"])

@app.route('/getGroups', methods=['GET'])
def get_groups():
    return jsonify(users["test@example.com"]["groups"])

@app.route('/getSharedPasswords', methods=['GET'])
def get_shared_passwords():
    group_id = request.args.get('groupId')
    return jsonify(groups.get(group_id, []))

@app.route('/logout')
def logout():
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
