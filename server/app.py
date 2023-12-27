# -*- coding: utf-8 -*-
from unicodedata import name
from flask import Flask
from flask_cors import CORS
from CONSTS import HOST,PORT,CORS_ORIGINS
from operators.db import initialize_db
  
from routers.registration import registration_api
from routers.add_activity import add_activity
from routers.biusiness import register_business
from routers.get_activity import get_activities
from routers.login import login
from routers.Volunteer_matchmaking import create_match


app = Flask(__name__)
CORS(app, resources={ r'/*': { 'origins': CORS_ORIGINS } })
app.register_blueprint(registration_api)
# app.register_business_blueprint(register_business)
# app.register_blueprint(add_activity)
# app.register_blueprint(get_activities)
# app.register_blueprint(registration_api)
# app.register_blueprint(registration_api)

initialize_db()









@app.route('/')
def route_default():
    return 'Welcome'


if __name__=="__main__":
    app.run(host=HOST,port=PORT)

