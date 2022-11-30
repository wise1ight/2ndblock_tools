import time

import schedule

from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

driver = None
chart_driver = None


def chat():
    try:
        chat_elements = driver.find_elements(By.CSS_SELECTOR, '.e1vvw3650')
        last_chats = list(map(lambda x: x.text, chat_elements))
        filtered_chats = list(filter(lambda x: x.startswith('/종목변경 '), last_chats))
        if len(filtered_chats) > 0:
            target = filtered_chats[-1].split('/종목변경 ')[1]
            new_base_symbol = target.split('/')[0].upper()
            new_quote_symbol = target.split('/')[1].upper()

            chart_url = f'https://upbit.com/exchange?code=CRIX.UPBIT.{new_quote_symbol}-{new_base_symbol}'
            if chart_url != chart_driver.current_url:
                chart_driver.get(url=chart_url)
    except:
        print('woops ')


if __name__ == "__main__":
    URL = 'https://2ndblock.com/room/kqlm15NawUT9X1a5vOQm'
    opt = ChromeOptions()
    opt.add_argument('--force-device-scale-factor=1')
    driver = webdriver.Chrome(options=opt, executable_path='./chromedriver')
    chart_driver = webdriver.Chrome(options=opt, executable_path='./chromedriver')
    driver.get(url=URL)

    WebDriverWait(driver, 3600).until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, '#game-screen > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > button')))
    print("로그인 감지")

    schedule.every(10).seconds.do(chat)

    while True:
        schedule.run_pending()
        time.sleep(1)

