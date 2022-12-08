import time

import requests
import schedule

from selenium import webdriver
from selenium.webdriver import ChromeOptions, Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

SECONDBLOCK_ROOM_URL = 'https://2ndblock.com/room/kqlm15NawUT9X1a5vOQm'
UPBIT_TICKER_URL = 'https://api.upbit.com/v1/ticker?markets=KRW-BTC'
BINANCE_TICKER_URL = 'https://www.binance.com/api/v3/ticker/price?symbol=BTCUSDT'

PROFILE_CSS_SELECTOR = '#game-screen > div:nth-child(2) > div.css-1ewmce8.ehzashr0 > div.css-azx95j > div.css-o16ypd > div.css-f4n6xs > span'
CHATTING_ELEMENT_SELECTOR = '.css-7bwuzs'
CHATTING_NICKNAME_SELECTOR = '.e112x67u3'
CHATTING_TIME_SELECTOR = '.e112x67u2'
CHATTING_CONTENT_SELECTOR = '.e112x67u4'
CHATTING_ADMIN_SELECTOR = '.css-14kaac3'
CHATTING_INPUT_SELECTOR = 'input.chatting-input'

COMMAND_CHART_CHANGE_MARKET = '/종목변경 '
COMMAND_AUCTION_REGISTER = '/등록'
COMMAND_AUCTION_BID = '/입찰 '
COMMAND_AUCTION_START = '/경매시작 '
COMMAND_AUCTION_STOP = '/경매종료'
COMMAND_AUCTION_NEXT = '/다음경매'

LAST_CHAT_TEXT = set()


def find_chat():
    chat_elements = block_driver.find_elements(By.CSS_SELECTOR, CHATTING_ELEMENT_SELECTOR)
    chats = list(map(lambda x: {
        'nickname': x.find_element(By.CSS_SELECTOR, CHATTING_NICKNAME_SELECTOR).text,
        'time': x.find_element(By.CSS_SELECTOR, CHATTING_TIME_SELECTOR).text,
        'content': x.find_element(By.CSS_SELECTOR, CHATTING_CONTENT_SELECTOR).text,
        'admin': len(x.find_elements(By.CSS_SELECTOR, CHATTING_ADMIN_SELECTOR)) == 1
    }, chat_elements))
    return chats


def send_chatting(message):
    chat_input = block_driver.find_element(By.CSS_SELECTOR, CHATTING_INPUT_SELECTOR)
    chat_input.clear()
    chat_input.send_keys(message)
    chat_input.send_keys(Keys.RETURN)


def handle_chart_change_market(chat):
    target = chat['content'].replace(COMMAND_CHART_CHANGE_MARKET, '')
    new_base_symbol = target.split('/')[0].upper()
    new_quote_symbol = target.split('/')[1].upper()

    chart_url = f'https://upbit.com/exchange?code=CRIX.UPBIT.{new_quote_symbol}-{new_base_symbol}'
    if chart_url != chart_driver.current_url:
        chart_driver.get(url=chart_url)


def handle_auction_register(chat):
    data = {
        'nickname': chat['nickname']
    }
    res = requests.post('http://localhost:8000/money', json=data)
    if res.ok and 'amount' in res.json():
        send_chatting(f"{data['nickname']}님이 등록하셨습니다. 현재 보유금액은 {res.json()['amount']:,} HD 입니다.")


def handle_auction_bid(chat):
    data = {
        'nickname': chat['nickname'],
        'bidPrice': chat['content'].replace(COMMAND_AUCTION_BID, '')
    }
    res = requests.put('http://localhost:8000/auction', json=data)
    if res.ok and 'highestBidNickname' in res.json():
        send_chatting(f"{res.json()['highestBidNickname']}님이 {res.json()['highestBidPrice']:,} HD에 입찰!")


def handle_auction_start(chat):
    data = {
        'lowLimitBidPrice': chat['content'].replace(COMMAND_AUCTION_START, '')
    }
    res = requests.post('http://localhost:8000/auction', json=data)
    if res.ok and 'isProgress' in res.json() and res.json()['isProgress']:
        send_chatting(f"경매를 시작합니다!")


def handle_auction_stop(chat):
    res = requests.delete('http://localhost:8000/auction')
    if res.ok and 'isProgress' in res.json() and not res.json()['isProgress']:
        highestBidPrice = res.json()['highestBidPrice']
        highestBidNickname = res.json()['highestBidNickname']

        if highestBidNickname is not None:
            send_chatting(f"{highestBidNickname}님에게 낙찰되었습니다! 축하드립니다! 낙찰가는 {highestBidPrice:,} HD 입니다.")
        else:
            send_chatting("이 경매는 유찰되었습니다.")


def handle_auction_next(chat):
    res = requests.post('http://localhost:8000/auction/next')
    if res.ok and 'edition' in res.json():
        edition = res.json()['edition']
        creator = edition['product']['contract']['creator']['title']
        title = edition['product']['title']

        send_chatting(f"이번 작품은 {creator} 작가님의 '{title}' 입니다.")


def handle_chat():
    try:
        chats = find_chat()
        new_chats = list(filter(lambda x: f"{x['nickname']}-{x['time']}-{x['content']}" not in LAST_CHAT_TEXT, chats))

        for chat in new_chats:
            if chat['content'].startswith(COMMAND_CHART_CHANGE_MARKET):
                handle_chart_change_market(chat)
            elif chat['content'].startswith(COMMAND_AUCTION_REGISTER):
                handle_auction_register(chat)
            elif chat['content'].startswith(COMMAND_AUCTION_BID):
                handle_auction_bid(chat)
            elif chat['content'].startswith(COMMAND_AUCTION_START) and chat['admin']:
                handle_auction_start(chat)
            elif chat['content'].startswith(COMMAND_AUCTION_STOP) and chat['admin']:
                handle_auction_stop(chat)
            elif chat['content'].startswith(COMMAND_AUCTION_NEXT) and chat['admin']:
                handle_auction_next(chat)

            LAST_CHAT_TEXT.add(f"{chat['nickname']}-{chat['time']}-{chat['content']}")

            print(chat)

    except Exception as e:
        print('예외 발생 : ', e)


def fetch_ticker():
    upbit_res = requests.get(UPBIT_TICKER_URL)
    binance_res = requests.get(BINANCE_TICKER_URL)

    if upbit_res.ok and binance_res.ok:
        btckrw_price = upbit_res.json()[0]['trade_price']
        btcusdt_price = float(binance_res.json()['price'])
        usdt_price = round(btckrw_price / btcusdt_price)
        print(f"{btckrw_price}, {usdt_price}")


if __name__ == "__main__":
    opt = ChromeOptions()
    opt.add_argument('--force-device-scale-factor=1')
    block_driver = webdriver.Chrome(options=opt, executable_path='./chromedriver')
    chart_driver = webdriver.Chrome(options=opt, executable_path='./chromedriver')
    block_driver.get(url=SECONDBLOCK_ROOM_URL)

    WebDriverWait(block_driver, 3600).until(EC.presence_of_element_located((By.CSS_SELECTOR, PROFILE_CSS_SELECTOR)))
    print("로그인 감지")

    schedule.every(1).seconds.do(handle_chat)
    schedule.every(5).seconds.do(fetch_ticker)

    while True:
        schedule.run_pending()
        time.sleep(1)
