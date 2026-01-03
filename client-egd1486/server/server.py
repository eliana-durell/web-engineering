from flask import Flask, send_from_directory
from flask_restful import Resource, Api
from flask_cors import CORS
import os

from api.swen_344_db_utils import *
from api.nutrition_api import *

app = Flask(__name__, static_folder='../egd1486-react-client4/dist')
# CORS(app) #Enable CORS on Flask server to work with Nodejs pages
api = Api(app) #api router

api.add_resource(NutritionApi,'/api/nutrition_api')

if __name__ == '__main__':
    # print("Loading db")
    # exec_sql_file('nutrition.sql')
    # print("Starting flask")
    # app.run(host='0.0.0.0', debug=True, port=5173), #starts Flask
# was port=4999 - local changed to 5173 (change also in FoodPlanner)
# run "python3 server/server.py" in parent folder then run "npm run dev" in specific client folder


    print("Starting flask")
    port = int(os.environ.get('PORT', 5173))
    app.run(host='0.0.0.0', port=port)