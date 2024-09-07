from flask import Flask, request, render_template, redirect, url_for, flash
from requestHandler import LoginRequestHandler, PasswordRequestHandler
import database as db

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # For session management

# Initialize the database
database = db.Database()

# Create an instance of the login request handler
login_handler = LoginRequestHandler(database)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        # Handle login logic
        request_info = RequestInfo(Request.LOGIN.value, f"{email},{password}")
        result = login_handler.handleRequest(request_info)
        if result.requestId == Response.LOGIN.value:
            flash('Login successful', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Login failed: ' + result.response, 'danger')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        name = request.form['name']
        # Handle signup logic
        request_info = RequestInfo(Request.SIGNUP.value, f"{email},{password},{name}")
        result = login_handler.handleRequest(request_info)
        if result.requestId == Response.SIGNUP.value:
            flash('Signup successful', 'success')
            return redirect(url_for('login'))
        else:
            flash('Signup failed: ' + result.response, 'danger')
            return redirect(url_for('signup'))
    return render_template('signup.html')

@app.route('/dashboard')
def dashboard():
    # Dashboard page for logged-in users
    return render_template('dashboard.html')

@app.route('/logout')
def logout():
    # Handle logout logic
    flash('Logged out successfully', 'success')
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)




'''
Explanation:
Flask Routes:

/: Home route.
/login: Handles both GET (display login form) and POST (process login).
/signup: Handles both GET (display signup form) and POST (process signup).
/dashboard: The dashboard for logged-in users.
/logout: Route to handle user logout.
Request Handlers:

Uses LoginRequestHandler to process login and signup requests.
Displays appropriate success or failure messages using Flask's flash function.
Run the Flask App:
Save the code in app.py.
'''