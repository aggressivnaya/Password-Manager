from flask import Flask, request, render_template, redirect, url_for, flash
from validation import validate
from auth_login import access
from get_from_db import get
from update import updating_data

server = Flask(__name__)

@server.route('/', methods=['POST', 'GET'])
def index():
    access, err = validate.token(request)

    if err:
        return err
    
    tokenData = request.headers["Authorization"]

    #in the same index page we see passwords and adding them
    if request.method == 'POST':
        try:
            password = request.form['content']
            updating_data.addPassword(tokenData, password)
            return redirect('/')
        except:
            return 'There was an issue adding your task'
    else:
        passwords = get.getPasswords(tokenData)
        return render_template('index.html', passwords=passwords)

@server.route("/login", methods=["POST"])
def login():
    token, err = access.login(request)

    if err:
        return "fail", 400
    
    #tokenData = request.headers["Authorization"].split(' ')[1]
    #return token
    #render_template('index.html')
    return "success", 200
    #return err
    #redirect(url_for('login'))

@server.route("/signup", methods=["POST"]) 
def signup():
    token, err = access.signup(request)

    if err:
        #return token
        #return render_template('index.html')
        return "error", 400
        #return err
       # return redirect(url_for('signup'))

    #tokenData = request.headers["Authorization"].split(' ')[1]
    return "success", 200
    
@server.route("/update", methods=["GET", "POST"])
def update():
    access, err = validate.token(request)
    id = request.args.get('id')

    if err:
        return err
    
    #tokenData = request.headers["Authorization"].split(' ')[1]
    #currPass = get.getPasswordById(id)

    if request.method == 'POST':
        try:
            #updating_data.updatePassword(tokenData[0], id, request.form['content'])
            return redirect('/')
        except:
            return 'There was an issue updating your task'
    else:
        return render_template('update.html', password=currPass)
    
@server.route("/delete")
def delete():
    access, err = validate.token(request)
    id = request.args.get('id')

    if err:
        return access, 400
    
    

    try:
        
        return redirect('/')
    except:
        return 'There was an issue updating your task'
    
@server.route("/history", methods=["GET"])
def history():
    access, err = validate.token(request)

    if err:
        return access, 400
    
    #tokenData = request.headers["Authorization"].split(' ')[1]

    try:
        get.getHistory(tokenData[0])
        return redirect('/')
    except:
        return 'There was an issue updating your task'
 
@server.route('/logout')
def logout():
    # Handle logout logic
    flash('Logged out successfully', 'success')
    return redirect(url_for('login'))
    
if __name__ == "__main__":
    server.run(port=8080)