import time

from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

SECONDBLOCK_ROOM_URL = 'https://2ndblock.com/room/yqDNWHh3xNLAsBO4mNEv'
PROFILE_CSS_SELECTOR = '#game-screen > div:nth-child(2) > div.css-1ewmce8.ehzashr0 > div.css-azx95j > div.css-o16ypd > div.css-f4n6xs > span'

CHATTING_TAB_NICKNAME_SELECTOR = 'div.css-1o1z1uf'
CHATTING_CONTENTS_TEXT_SELECTOR = 'div.css-rpu5yn.e112x67u4'

LAST_CHAT_TEXT = {

}


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
            print(last_chat_text)
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
        handle_chat()

