from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS
import json
from waitress import serve
import datetime
import requests
import re

app=Flask(__name__)
cors = CORS(app)

@app.route("/",methods=['GET'])
def test():
    json = {}
    json["message"]="Server running ..."
    return jsonify(json)

##JWT ----->
from flask_jwt_extended import create_access_token, verify_jwt_in_request
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
app.config["JWT_SECRET_KEY"]="super-secret" #Cambiar por el que se conveniente
jwt = JWTManager(app)

@app.route("/login", methods = ['POST'])
def create_token():
    data = request.get_json()
    headers = {"Content-Type": "application/json; charset=utf-8"}
    url = dataConfig["url-backend-asset"] + '/usuario/validar'
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        user = response.json()
        expires = datetime.timedelta(seconds=60 * 60 * 24)
        access_token = create_access_token(identity=user, expires_delta=expires)
        return jsonify({"token": access_token, "user_id": user["_id"]})
    else:
        return jsonify({"msg": "Bad username or password"}), 401


@app.before_request
def before_request_callback():
    excludeRoutes = ["/login"]
    if excludeRoutes.__contains__(request.path):
        pass
    elif verify_jwt_in_request():
        usuario = get_jwt_identity()
        #print(usuario)

@app.route("/modelo", methods=['POST'])
def callModel():
    data = request.get_json()
    headers = {"Content-Type": "application/json; charset=utf-8"}
    url = dataConfig["url-backend-asset"] + '/modelo'
    response = requests.post(url, headers= headers, json= data)
    json = response.json()
    return jsonify(json)

@app.route("/resultado/year/<string:year>", methods = ['POST'])
def createResult(year):
    user = get_jwt_identity()
    data = request.get_json()
    headers = {"Content-Type": "application/json; charset=utf-8"}
    url = dataConfig["url-backend-asset"] + '/resultado/user/'+user["_id"]+'/year/'+year
    response = requests.post(url, headers=headers, json= data)
    json = response.json()
    return jsonify(json)




def loadFileConfig():
    with open('config.json') as f:
        data = json.load(f)
    return data


if __name__=='__main__':
    dataConfig = loadFileConfig()
    print("Server running : "+"http://"+dataConfig["url-backend"]+":" +
    str(dataConfig["port"]))
    serve(app,host=dataConfig["url-backend"],port=dataConfig["port"])

