import time
import re
import requests

from selenium import webdriver
from selenium.webdriver import ChromeOptions, Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

SECONDBLOCK_ROOM_URL = 'https://2ndblock.com/room/yqDNWHh3xNLAsBO4mNEv'
PROFILE_CSS_SELECTOR = '#game-screen > div:nth-child(2) > div.css-1ewmce8.ehzashr0 > div.css-azx95j > div.css-o16ypd > div.css-f4n6xs > span'
ETHEREUM_ADDRESS_REGEX = r'^0x[a-fA-F0-9]{40}$'

CHATTING_TAB_NICKNAME_SELECTOR = 'div.css-1o1z1uf'
CHATTING_CONTENTS_TEXT_SELECTOR = 'div.css-rpu5yn.e112x67u4'
CHATTING_INPUT_SELECTOR = 'input.chatting-input'

REGISTER_WALLET_COMMAND = '/지갑등록 '

LAST_CHAT_TEXT = {}


def find_chat_elements():
    chat_list_elements = driver.find_elements(By.CSS_SELECTOR, CHATTING_TAB_NICKNAME_SELECTOR)
    return chat_list_elements


def select_chatting_tab(chat_element):
    chat_element.click()


def get_nickname_from_tab(chat_element):
    return chat_element.text


def scan_chatting_text():
    chat_contents_texts = driver.find_elements(By.CSS_SELECTOR, CHATTING_CONTENTS_TEXT_SELECTOR)
    return list(map(lambda x: x.text, chat_contents_texts))


def find_last_chat_text(chat_contents_texts):
    return chat_contents_texts[-1]


def send_chatting(message):
    chat_input = driver.find_element(By.CSS_SELECTOR, CHATTING_INPUT_SELECTOR)
    chat_input.clear()
    chat_input.send_keys(message)
    chat_input.send_keys(Keys.RETURN)


def handle_chat():
    chat_list_elements = find_chat_elements()
    for chat_element in chat_list_elements:
        nickname = get_nickname_from_tab(chat_element)
        if nickname == '전체 채팅':
            continue

        select_chatting_tab(chat_element)
        chat_contents_texts = scan_chatting_text()
        if len(chat_contents_texts) == 0:
            continue
        last_chat_text = find_last_chat_text(chat_contents_texts)

        if nickname not in LAST_CHAT_TEXT or last_chat_text != LAST_CHAT_TEXT[nickname]:
            if last_chat_text.startswith(REGISTER_WALLET_COMMAND):
                arg = last_chat_text.replace(REGISTER_WALLET_COMMAND, '')
                if re.match(ETHEREUM_ADDRESS_REGEX, arg):
                    #실제 서버로 요청을 보내는 부분
                    data = {
                        'nickname': nickname,
                        'address': arg
                    }
                    res = requests.post('http://localhost:3000/address', json=data)

                    if res.ok:
                        send_chatting('이더리움 지갑 주소 등록이 완료되었습니다.')
                    else:
                        send_chatting('대상자가 아닙니다.')
                else:
                    send_chatting('이더리움 지갑 주소를 정확하게 입력하셨는지 확인하세요.')

            LAST_CHAT_TEXT[nickname] = last_chat_text

        time.sleep(1)


if __name__ == "__main__":
    opt = ChromeOptions()
    opt.add_argument('--force-device-scale-factor=1')
    driver = webdriver.Chrome(options=opt, executable_path='./chromedriver')
    driver.get(url=SECONDBLOCK_ROOM_URL)

    WebDriverWait(driver, 3600).until(EC.presence_of_element_located((By.CSS_SELECTOR, PROFILE_CSS_SELECTOR)))
    print("로그인 감지")

    while True:
        try:
            handle_chat()
        except Exception as e:
            print('예외 발생 : ', e)
