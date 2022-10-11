from flask import Flask, request
from flask_restx import Api, Resource
from werkzeug.exceptions import BadRequest

INITIAL_USER_MONEY = 1000000

app = Flask(__name__)
api = Api(app)

user_money = {}


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


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
