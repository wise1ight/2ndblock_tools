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
COMMAND_SHOW_MONEY = '/소지금'
COMMAND_AUCTION_START = '/경매시작 '
COMMAND_AUCTION_STOP = '/경매종료 '
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


def handle_chat(chats):
    register_chats = list(filter(lambda x: x['content'].startswith(COMMAND_REGISTER), chats))
    handle_register_chat(register_chats)


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
    # 두 브라우저의 웹드라이버 세팅
    game_driver = webdriver.Chrome(executable_path='./chromedriver')
    game_driver.get(url='https://2ndblock.com/room/kqlm15NawUT9X1a5vOQm')
    #auction_driver = webdriver.Chrome(executable_path='chromedriver')
    #auction_driver.get('http://localhost:3000/')

    WebDriverWait(game_driver, 3600).until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, '#game-screen > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > button')))
    print("로그인 감지")

    schedule.every(1).seconds.do(scan_chat)

    while True:
        schedule.run_pending()
        time.sleep(1)



