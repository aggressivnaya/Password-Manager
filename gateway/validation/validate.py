import os, requests

#this checking if the authorization in the header exist 
#also if the token is right
def token(request):
    if not "Authorization" in request.headers:
        return "missing credentials", 401

    token = request.headers["Authorization"]

    if not token:
        return "missing credentials", 401

    response = requests.post(
        f"http://{os.environ.get('AUTH_SVC_ADDRESS')}/validate",#TODO: insert value to AUTH_SVC_ADDRESS
        headers={"Authorization": token},
    )

    if response.status_code == 200:
        return response.text, response.status_code
    else:
        return None, 400