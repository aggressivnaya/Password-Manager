#from flask import Flask, request, render_template, redirect, url_for, flash
from fastapi import FastAPI, Header, Request
from validation import validate
from auth_login import access
from get_from_db import get
from update import updating_data

server = FastAPI()

'''
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
        return render_template('index.html', passwords=passwords)'''

@server.post("/login")
def login(request: Request):
    token, err = access.login(request)

    if err:
        return {"fail", 400}
    
    return {"success", 200}

@server.post("/signup") 
def signup(request: Request):
    token, err = access.signup(request)

    if err:
        return {"error", 400}
    
    return {"success", 200}
    
@server.route("/update", methods=["GET", "POST"])#TODO:split
def update(request: Request):
    access, err = validate.token(request)
    id = request.args.get('id')

    if err:
        return err
    
    updating_data.updatePassword(tokenData[0], id, request.form['content'])
    
@server.delete("/delete")
def delete(request: Request, id: int):
    access, err = validate.token(request)

    if err:
        return {"error", 400}
    
    return access
    
@server.get("/history")
def history(request: Request):
    access, err = validate.token(request)

    if err:
        return {err, 400}
    
    try:
        return get.getHistory(request)
    except:
        return 'There was an issue updating your task'
 
@server.route('/logout')
def logout():
    # Handle logout logic
    pass
    
if __name__ == "__main__":
    server.run(port=8080)