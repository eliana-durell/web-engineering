from flask import Flask
from flask_restful import Resource, Api
from api.routes import *
from api.management import *

app = Flask(__name__)
api = Api(app)

# Management API
api.add_resource(Init, '/manage/init') #for initializing the DB
api.add_resource(Version, '/manage/version') #for checking DB version

#Routes API
api.add_resource(User, '/users')
api.add_resource(Book, '/books')
api.add_resource(Inventory, '/inventory')
api.add_resource(History, '/history')
api.add_resource(Libraries, '/libraries')
    #rest 2
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(Checkout, '/checkout')
api.add_resource(Reserve, '/reserve')


if __name__ == '__main__':
    # rebuild_tables()
    app.run(debug=True, port=4999)