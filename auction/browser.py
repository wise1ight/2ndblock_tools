import time

import schedule
import requests

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


COMMAND_REGISTER = '/등록'
COMMAND_BID = '/입찰 '
COMMAND_AUCTION_START = '/경매시작 '
COMMAND_AUCTION_STOP = '/경매종료'
COMMAND_AUCTION_NEXT = '/다음경매'

game_driver = None
auction_driver = None


def handle_register_chat(chats):
    for chat in chats:
        data = {
            'nickname': chat['nickname']
        }
        res = requests.post('http://localhost:8000/money', json=data)
        if res.ok and 'amount' in res.json():
            chat_input = game_driver.find_element(By.CSS_SELECTOR, 'div.Chatting-module__chatting-input--KBvdr > input')
            chat_input.clear()
            chat_input.send_keys(f"{data['nickname']}님이 등록하셨습니다. 현재 보유금액은 {res.json()['amount']:,} HD 입니다.")
            chat_input.send_keys(Keys.RETURN)


def handle_bid_chat(chats):
    for chat in chats:
        data = {
            'nickname': chat['nickname'],
            'bidPrice': chat['content'].replace(COMMAND_BID, '')
        }
        res = requests.put('http://localhost:8000/auction', json=data)
        if res.ok and 'highestBidNickname' in res.json():
            chat_input = game_driver.find_element(By.CSS_SELECTOR, 'div.Chatting-module__chatting-input--KBvdr > input')
            chat_input.clear()
            chat_input.send_keys(f"{res.json()['highestBidNickname']}님이 {res.json()['highestBidPrice']:,} HD에 입찰!")
            chat_input.send_keys(Keys.RETURN)


def handle_auction_start(chats):
    for chat in chats:
        data = {
            'lowLimitBidPrice': chat['content'].replace(COMMAND_AUCTION_START, '')
        }
        res = requests.post('http://localhost:8000/auction', json=data)
        if res.ok and 'isProgress' in res.json() and res.json()['isProgress']:
            chat_input = game_driver.find_element(By.CSS_SELECTOR, 'div.Chatting-module__chatting-input--KBvdr > input')
            chat_input.clear()
            chat_input.send_keys(f"경매를 시작합니다!")
            chat_input.send_keys(Keys.RETURN)


def handle_auction_stop(chats):
    for _ in chats:
        res = requests.delete('http://localhost:8000/auction')
        if res.ok and 'isProgress' in res.json() and not res.json()['isProgress']:
            highestBidPrice = res.json()['highestBidPrice']
            highestBidNickname = res.json()['highestBidNickname']

            chat_input = game_driver.find_element(By.CSS_SELECTOR, 'div.Chatting-module__chatting-input--KBvdr > input')
            chat_input.clear()
            if highestBidNickname is not None:
                chat_input.send_keys(f"{highestBidNickname}님에게 낙찰되었습니다! 축하드립니다! 낙찰가는 {highestBidPrice:,} HD 입니다.")
            else:
                chat_input.send_keys("이 경매는 유찰되었습니다.")
            chat_input.send_keys(Keys.RETURN)


def handle_auction_next(chats):
    for _ in chats:
        res = requests.post('http://localhost:8000/auction/next')
        if res.ok and 'edition' in res.json():
            edition = res.json()['edition']
            creator = edition['product']['contract']['creator']['title']
            title = edition['product']['title']

            chat_input = game_driver.find_element(By.CSS_SELECTOR, 'div.Chatting-module__chatting-input--KBvdr > input')
            chat_input.clear()
            chat_input.send_keys(f"이번 작품은 {creator} 작가님의 '{title}' 입니다.")
            chat_input.send_keys(Keys.RETURN)


def handle_chat(chats):
    register_chats = list(filter(lambda x: x['content'].startswith(COMMAND_REGISTER), chats))
    handle_register_chat(register_chats)
    bid_chats = list(filter(lambda x: x['content'].startswith(COMMAND_BID), chats))
    handle_bid_chat(bid_chats)
    auction_start_chats = list(filter(lambda x: x['content'].startswith(COMMAND_AUCTION_START) and x['admin'], chats))
    handle_auction_start(auction_start_chats)
    auction_stop_chats = list(filter(lambda x: x['content'].startswith(COMMAND_AUCTION_STOP) and x['admin'], chats))
    handle_auction_stop(auction_stop_chats)
    auction_next_chats = list(filter(lambda x: x['content'].startswith(COMMAND_AUCTION_NEXT) and x['admin'], chats))
    handle_auction_next(auction_next_chats)


def scan_chat():
    try:
        chat_elements = game_driver.find_elements(By.CSS_SELECTOR, '.css-7bwuzs')
        chats = list(map(lambda x: {
            'nickname': x.find_element(By.CSS_SELECTOR, '.e1vvw3651').text,
            'time': x.find_element(By.CSS_SELECTOR, '.e1vvw3652').text,
            'content': x.find_element(By.CSS_SELECTOR, '.e1vvw3650').text,
            'admin': len(x.find_elements(By.CSS_SELECTOR, '.css-14kaac3')) == 1
        }, chat_elements))

        handle_chat(chats)
    except Exception as e:
        print(str(e))


if __name__ == "__main__":
    game_driver = webdriver.Chrome(executable_path='../chromedriver')
    game_driver.get(url='https://2ndblock.com/room/kqlm15NawUT9X1a5vOQm')

    WebDriverWait(game_driver, 3600).until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, '#game-screen > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > button')))
    print("로그인 감지")

    schedule.every(1).seconds.do(scan_chat)

    while True:
        schedule.run_pending()
        time.sleep(1)



