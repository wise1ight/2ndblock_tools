import time
import schedule

from selenium import webdriver
from selenium.webdriver import ChromeOptions, Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

SECONDBLOCK_ROOM_URL = 'https://2ndblock.com/room/kqlm15NawUT9X1a5vOQm'
PROFILE_CSS_SELECTOR = '#game-screen > div:nth-child(2) > div.css-1ewmce8.ehzashr0 > div.css-azx95j > div.css-o16ypd > div.css-f4n6xs > span'

CHATTING_ELEMENT_SELECTOR = '.css-7bwuzs'
CHATTING_NICKNAME_SELECTOR = '.e112x67u3'
CHATTING_TIME_SELECTOR = '.e112x67u2'
CHATTING_CONTENT_SELECTOR = '.e112x67u4'
CHATTING_ADMIN_SELECTOR = '.css-14kaac3'
CHATTING_INPUT_SELECTOR = 'input.chatting-input'

COMMAND_CHART_CHANGE_MARKET = '/종목변경 '

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


def handle_chat():
    try:
        chats = find_chat()
        new_chats = list(filter(lambda x: f"{x['nickname']}-{x['time']}-{x['content']}" not in LAST_CHAT_TEXT, chats))

        for chat in new_chats:
            if chat['content'].startswith(COMMAND_CHART_CHANGE_MARKET):
                handle_chart_change_market(chat)

            LAST_CHAT_TEXT.add(f"{chat['nickname']}-{chat['time']}-{chat['content']}")

            print(chat)

    except Exception as e:
        print('예외 발생 : ', e)


if __name__ == "__main__":
    opt = ChromeOptions()
    opt.add_argument('--force-device-scale-factor=1')
    block_driver = webdriver.Chrome(options=opt, executable_path='./chromedriver')
    chart_driver = webdriver.Chrome(options=opt, executable_path='./chromedriver')
    block_driver.get(url=SECONDBLOCK_ROOM_URL)

    WebDriverWait(block_driver, 3600).until(EC.presence_of_element_located((By.CSS_SELECTOR, PROFILE_CSS_SELECTOR)))
    print("로그인 감지")

    schedule.every(1).seconds.do(handle_chat)

    while True:
        schedule.run_pending()
        time.sleep(1)
