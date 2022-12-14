import time

import requests
import schedule

from selenium import webdriver
from selenium.webdriver import ChromeOptions, Keys, ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import numpy as np

from ticker.graphical import GraphicalLocator

SECONDBLOCK_ROOM_URL = 'https://2ndblock.com/room/kqlm15NawUT9X1a5vOQm'
UPBIT_TICKER_URL = 'https://api.upbit.com/v1/ticker?markets=KRW-BTC'
BINANCE_TICKER_URL = 'https://www.binance.com/api/v3/ticker/price?symbol=BTCUSDT'

PROFILE_CSS_SELECTOR = '#game-screen > div:nth-child(2) > div.css-1ewmce8.ehzashr0 > div.css-azx95j > div.css-o16ypd > div.css-f4n6xs > span'
BLOCK_EDITOR_SELECTOR = '#game-screen > div:nth-child(2) > div.css-1ewmce8.ehzashr0 > div.css-70qvj9 > div.css-1k38fl6 > button:nth-child(1)'
BLOCK_EDITOR_TAB_SELECTOR = 'div.css-1hfmw46.effezff0 > ul > li:nth-child(3) > a'
BLOCK_EDITOR_UP_SELECTOR = '#up > div'
BLOCK_EDITOR_CONFIRM_SELECTOR = '#confirm > div'
BLOCK_EDITOR_DELETE_SELECTOR = '#delete > div'
BLOCK_EDITOR_COMPLETE_SELECTOR = '#game-screen > div.css-13o7eu2.e1d2ojxm0 > div > div.footer > button > div'
BLOCK_ITEM_SELECTORS = {
    '1': '.css-1qgw649',
    '2': '.css-121if3b',
    '3': '.css-13gpr2l',
    '4': '.css-1e2gx2t',
    '5': '.css-4rae8q',
    '6': '.css-1daydhm',
    '7': '.css-un6tel',
    '8': '.css-97e978',
    '9': '.css-hk5sa6',
    '0': '.css-15rw0xp'
}
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
old_ticker_str = ' ' * 20


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


def refresh_ticker(btc_price, usdt_price):
    global old_ticker_str

    editor_button = block_driver.find_element(By.CSS_SELECTOR, BLOCK_EDITOR_SELECTOR)
    editor_button.click()
    editor_tab = block_driver.find_element(By.CSS_SELECTOR, BLOCK_EDITOR_TAB_SELECTOR)
    editor_tab.click()

    # Anchor 이미지를 찾아 좌표계산
    b_locator, u_locator, bottom_locator = GraphicalLocator("ticker/img/B.png"), GraphicalLocator("ticker/img/U.png"), GraphicalLocator("ticker/img/bottom.png")
    b_locator.find_me(block_driver)
    u_locator.find_me(block_driver)
    bottom_locator.find_me(block_driver)

    is_found = True if b_locator.threshold['shape'] >= 0.8 and \
                       b_locator.threshold['histogram'] >= 0.4 and \
                       u_locator.threshold['shape'] >= 0.8 and \
                       u_locator.threshold['histogram'] >= 0.4 and \
                       bottom_locator.threshold['shape'] >= 0.8 and \
                       bottom_locator.threshold['histogram'] >= 0.4 else False

    print(b_locator.center_x, b_locator.center_y, u_locator.center_x, u_locator.center_y)

    if is_found:
        # 이미지 중심 좌표로 canvas 다룰 영역 계산
        coefficients = np.polyfit([b_locator.center_x, u_locator.center_x], [b_locator.center_y, u_locator.center_y], 1)
        polynomial = np.poly1d(coefficients)

        x_axis = np.linspace(b_locator.center_x, u_locator.center_x, 13)#제일 처음 'B'와 13번째의 'U'간 티커들 x축 좌표 구하기
        right_x_pos = x_axis[0] + (x_axis[1] - x_axis[0]) * 19#마지막 티커의 x축 좌표 구하기
        x_axis = np.linspace(b_locator.center_x, right_x_pos, 20)#x축 좌표
        top_y_axis = polynomial(x_axis)#상단 y축 좌표
        bottom_y_axis = np.array(list(map(lambda x: x + (bottom_locator.center_y - b_locator.center_y), top_y_axis)))#하단 y축 좌표

        ticker_str = ' ' * 3 + str(btc_price) + ' ' * 5 + str(usdt_price)

        action = ActionChains(block_driver)

        for i in range(20):
            if ticker_str[i] == old_ticker_str[i]:
                continue

            print(int(x_axis[i]), int(top_y_axis[i]))

            # 상단의 기존 오브젝트 제거
            action.reset_actions()
            action.move_by_offset(int(x_axis[i]), int(top_y_axis[i]))
            action.click()
            action.perform()

            # 삭제
            WebDriverWait(block_driver, 3600).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, BLOCK_EDITOR_DELETE_SELECTOR)))
            delete_button = block_driver.find_element(By.CSS_SELECTOR, BLOCK_EDITOR_DELETE_SELECTOR)
            delete_button.click()
            time.sleep(1)

            # 아이템 선택
            target_item = block_driver.find_element(By.CSS_SELECTOR, BLOCK_ITEM_SELECTORS[ticker_str[i]])
            target_item.click()
            time.sleep(1)

            # 하단에 오브젝트 배치
            action.reset_actions()
            action.move_by_offset(int(x_axis[i]), int(bottom_y_axis[i]))
            action.click()
            action.perform()

            # 오브젝트 상단으로 이동
            WebDriverWait(block_driver, 3600).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, BLOCK_EDITOR_UP_SELECTOR)))
            up_button = block_driver.find_element(By.CSS_SELECTOR, BLOCK_EDITOR_UP_SELECTOR)
            for _ in range(26):
                up_button.click()

            # 확인
            WebDriverWait(block_driver, 3600).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, BLOCK_EDITOR_CONFIRM_SELECTOR)))
            confirm_button = block_driver.find_element(By.CSS_SELECTOR, BLOCK_EDITOR_CONFIRM_SELECTOR)
            confirm_button.click()

            # 아이템 선택 해제
            target_item = block_driver.find_element(By.CSS_SELECTOR, BLOCK_ITEM_SELECTORS[ticker_str[i]])
            target_item.click()

            time.sleep(2)

        old_ticker_str = ticker_str

    complete_button = block_driver.find_element(By.CSS_SELECTOR, BLOCK_EDITOR_COMPLETE_SELECTOR)
    complete_button.click()


def handle_ticker():
    try:
        upbit_res = requests.get(UPBIT_TICKER_URL)
        binance_res = requests.get(BINANCE_TICKER_URL)

        if upbit_res.ok and binance_res.ok:
            btckrw_price = upbit_res.json()[0]['trade_price']
            btcusdt_price = float(binance_res.json()['price'])
            usdt_price = round(btckrw_price / btcusdt_price)

            refresh_ticker(btckrw_price, usdt_price)

    except Exception as e:
        print('예외 발생 : ', e)


if __name__ == "__main__":
    opt = ChromeOptions()
    opt.add_argument('--force-device-scale-factor=1')
    opt.add_argument('--window-size=3840,2160')
    opt.add_experimental_option("excludeSwitches", ['enable-automation'])
    block_driver = webdriver.Chrome(options=opt, executable_path='./chromedriver')
    chart_driver = webdriver.Chrome(executable_path='./chromedriver')
    block_driver.get(url=SECONDBLOCK_ROOM_URL)

    WebDriverWait(block_driver, 3600).until(EC.presence_of_element_located((By.CSS_SELECTOR, PROFILE_CSS_SELECTOR)))
    print("로그인 감지")

    schedule.every(1).seconds.do(handle_chat)
    schedule.every(10).seconds.do(handle_ticker)

    while True:
        schedule.run_pending()
        time.sleep(1)
