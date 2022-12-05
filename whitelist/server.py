from flask import Flask, request
from flask_restx import Api, Resource
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
api = Api(app)


@api.route('/address')
class Address(Resource):
    def post(self):
        nickname = request.json.get('nickname')
        address = request.json.get('address')

        return {'success': True}


if __name__ == '__main__':
    app.run()
