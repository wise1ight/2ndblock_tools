import requests
from flask import Flask, request
from flask_restx import Api, Resource
from werkzeug.exceptions import BadRequest

INITIAL_USER_MONEY = 1000000

app = Flask(__name__)
api = Api(app)

editions = {}
user_money = {}


@api.route('/init')
class Initial(Resource):
    def get(self):
        res = requests.get('https://ccx.upbit.com/nx/v1/members/f5c50355-c14e-4c95-8420-d4ea14b46f9c/editions?states=FOR_SALE&states=NOT_FOR_SALE&size=60')
        res_json = res.json()
        items = res_json['items']

        for item in items:
            uuid = item['product']['uuid']
            editionNumber = item['editionNumber']
            if uuid in editions and editions[uuid]['editionNumber'] < editionNumber:
                continue
            editions[uuid] = item

        return editions


@api.route('/money')
class Money(Resource):
    def get(self):  # 모든 유저 잔고 조회
        global user_money
        return user_money

    def post(self):  # 개별 유저의 잔고 생성
        global user_money

        nickname = request.json.get('nickname')
        if nickname in user_money:
            raise BadRequest('Already Exist Nickname')

        user_money[nickname] = {
            'amount': INITIAL_USER_MONEY
        }

        return user_money[nickname]


if __name__ == '__main__':
    app.run()
