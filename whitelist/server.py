from flask import Flask, request
from flask_restx import Api, Resource
from flask_cors import CORS
from werkzeug.exceptions import BadRequest

from whitelist.db import WhitelistDB

app = Flask(__name__)
CORS(app)
api = Api(app)


@api.route('/address')
class Address(Resource):
    def post(self):
        nickname = request.json.get('nickname')
        address = request.json.get('address')

        nickname_count = WhitelistDB().count_nickname(nickname)
        if nickname_count == 0:# 대상자가 아닌 경우
            raise BadRequest('You are not applicable.')
        else:
            WhitelistDB().insert_address(nickname, address)

        return {'success': True}


if __name__ == '__main__':
    app.run()
