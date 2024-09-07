from flask import Flask, request, render_template, redirect, url_for, flash
from validation import validate
from auth_login import access
import database as db

server = Flask(__name__)

@server.route('/', methods=['POST', 'GET'])
def index():
    access, err = validate.token(request)

    if err:
        return err
    
    tokenData = access.split('.')

    #in the same index page we see passwords and adding them
    if request.method == 'POST':
        try:
            password = request.form['content']
            db.Database().addPassword(tokenData[0], password)
            return redirect('/')
        except:
            return 'There was an issue adding your task'
    else:
        passwords = db.Database().getPasswords(tokenData[0])
        return render_template('index1.html', passwords=passwords)

@server.route("/login", methods=["POST"])
def login():
    token, err = access.login(request)

    if not err:
        #return token
        render_template('index1.html')
    else:
        #return err
        redirect(url_for('login'))

@server.route("/signup", methods=["POST"]) 
def signup():
    token, err = access.signup(request)

    if not err:
        #return token
        return render_template('index1.html')
    else:
        #return err
        return redirect(url_for('signup'))
    
@server.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
    access, err = validate.token(request)

    if err:
        return err
    
    tokenData = access.split('.')
    currPass = db.Database().findPasswordById(id)

    if request.method == 'POST':
        try:
            db.Database().updatePassword(tokenData[0], id, request.form['content'])
            return redirect('/')
        except:
            return 'There was an issue updating your task'
    else:
        return render_template('updare.html', password=currPass)
    
@server.route("/delete/<int:id>")
def delete(id):
    access, err = validate.token(request)

    if err:
        return err
    
    tokenData = access.split('.')

    try:
        currPass = db.Database().findPasswordById(id)
        db.Database().deletePassword(tokenData[0], currPass)
        return redirect('/')
    except:
        return 'There was an issue updating your task'
 
@server.route('/logout')
def logout():
    # Handle logout logic
    flash('Logged out successfully', 'success')
    return redirect(url_for('login'))
    
if __name__ == "__main__":
    server.run(host="0.0.0.0", port=8080)