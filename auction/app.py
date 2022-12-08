import requests
from flask import Flask, request
from flask_restx import Api, Resource
from flask_cors import CORS
from werkzeug.exceptions import BadRequest

INITIAL_USER_MONEY = 1000000

app = Flask(__name__)
CORS(app)
api = Api(app)

auction_status = {
    'isProgress': False,
    'edition': None,
    'lowLimitBidPrice': 0,
    'highestBidPrice': 0,
    'highestBidNickname': None,
    'editionNum': 1,
}
edition_num = 0
editions = {}
user_money = {}


@api.route('/init')
class Initial(Resource):
    def get(self):
        global editions
        res = requests.get('https://ccx.upbit.com/nx/v1/members/f5c50355-c14e-4c95-8420-d4ea14b46f9c/editions?states=FOR_SALE&states=NOT_FOR_SALE&size=60')
        res_json = res.json()
        items = res_json['items']

        for item in items:
            uuid = item['product']['uuid']
            editionNumber = item['editionNumber']
            if uuid in editions and editions[uuid]['editionNumber'] < editionNumber:
                continue
            editions[uuid] = item

        editions = list(editions.values())
        auction_status['edition'] = editions[0]
        return editions


@api.route('/auction')
class Auction(Resource):
    def get(self):
        global auction_status
        return auction_status

    def post(self):
        global auction_status

        if auction_status['isProgress']:
            raise BadRequest('Progressing')

        lowLimitBidPrice = int(request.json.get('lowLimitBidPrice'))

        auction_status['isProgress'] = True
        auction_status['lowLimitBidPrice'] = lowLimitBidPrice
        auction_status['highestBidPrice'] = 0
        auction_status['highestBidNickname'] = None

        return auction_status

    def put(self):
        global auction_status
        global user_money

        if not auction_status['isProgress']:
            raise BadRequest('Not Progressing Auction')

        nickname = request.json.get('nickname')
        bidPrice = int(request.json.get('bidPrice'))

        if user_money[nickname]['amount'] < bidPrice:
            raise BadRequest('Amount is not enough')

        if auction_status['lowLimitBidPrice'] >= bidPrice:
            raise BadRequest('Bid Price is Small than limit')

        if auction_status['highestBidPrice'] >= bidPrice:
            raise BadRequest('Bid Price is Small than Current Price')

        auction_status['highestBidPrice'] = bidPrice
        auction_status['highestBidNickname'] = nickname

        return auction_status

    def delete(self):
        global auction_status
        global edition_num
        global editions

        if not auction_status['isProgress']:
            raise BadRequest('Not Progressing Auction')

        auction_status['isProgress'] = False
        nickname = auction_status['highestBidNickname']
        if nickname is not None:
            user_money[nickname]['amount'] = user_money[nickname]['amount'] - auction_status['highestBidPrice']
        editions[edition_num]['highestBidNickname'] = nickname
        editions[edition_num]['highestBidPrice'] = auction_status['highestBidPrice']

        return auction_status


@api.route('/auction/next')
class AuctionNext(Resource):
    def post(self):
        global auction_status
        global edition_num
        global editions

        if auction_status['isProgress']:
            raise BadRequest('Progressing')

        if 'highestBidPrice' not in editions[edition_num]:
            raise BadRequest('Not Closed Auction')

        edition_num = edition_num + 1
        auction_status['edition'] = editions[edition_num]
        auction_status['editionNum'] = edition_num

        return auction_status


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
