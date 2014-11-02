#-*- coding: utf-8 -*-

from flask import request, Flask, jsonify, render_template
import requests
import config
from decimal import Decimal
YO_API_TOKEN = config.DEVKEY

app = Flask(__name__)
userList = []

class User():
    def __init__(self, name="", lat=0, lon=0):
        self.name = name
        self.lat = lat
        self.lon = lon

#  user = User(username, Decimal(latitude), Decimal(longitude))
def toUserList():
    f = open ("DATA.txt", 'r')
    for line in f:
        split = line.split()
        userList.append(User(split[0],Decimal(split[1]),Decimal(split[2])))
    return userList

@app.route('/getUsers')
def getUsers():
    return jsonify(userList)

@app.route('/')
def index():
    return render_template('index.html')



@app.route("/yo/")
def yo():
    # extract and parse query parameters
    username = request.args.get('username')
    # get location and split it
    location = request.args.get('location')
    split = location.split(";")
    latitude = split [0]
    longitude = split[1]

    f = open ('DATA.txt', 'a')
    print (username + " " + latitude + " " + longitude, file=f)
    userList.append(User(username, Decimal(latitude), Decimal(longitude)))
    # Yo the result back to the user
    requests.post("http://api.justyo.co/yo/", data={'api_token': YO_API_TOKEN, 'username': username, 'link': 'GOOGLEMAPSLINK'})

    return 'OK'


if __name__ == "__main__":
    app.debug = True
    toUserList()
    app.run(host="0.0.0.0", port=5000)
