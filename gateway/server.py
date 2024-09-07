from flask import Flask, request, render_template, redirect, url_for, flash
from validation import validate
from auth_login import access

server = Flask(__name__)

@server.route("/login", methods=["POST"])
def login():
    token, err = access.login(request)

    if not err:
        return token
    else:
        return err

@server.route("/signup", methods=["POST"]) 
def signup():
    token, err = access.signup(request)

    if not err:
        return token
    else:
        return err
    
@server.route('/dashboard')
def dashboard():
    # Dashboard page for logged-in users
    return render_template('dashboard.html')

@server.route('/logout')
def logout():
    # Handle logout logic
    flash('Logged out successfully', 'success')
    return redirect(url_for('login'))

    
if __name__ == "__main__":
    server.run(host="0.0.0.0", port=8080)