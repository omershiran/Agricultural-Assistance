# -*- coding: utf-8 -*-
from unicodedata import name
from flask import Flask
from flask_cors import CORS
from CONSTS import HOST,PORT,CORS_ORIGINS
from operators.db import initialize_db, get_activity

from routers.registration import registration_api
from server.operators.insert_fake_data import insert_random_activities_no_faker_fixed_v2
from server.routers.add_activity import add_activity_api
from server.routers.get_activity import activities_api

app = Flask(__name__)
CORS(app, resources={ r'/*': { 'origins': CORS_ORIGINS } })
app.register_blueprint(add_activity_api)
app.register_blueprint(activities_api)

initialize_db()
insert_random_activities_no_faker_fixed_v2()









@app.route('/')
def route_default():
    return 'Welcome'


if __name__=="__main__":
    app.run(host=HOST,port=PORT)

