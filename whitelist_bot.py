from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

SECONDBLOCK_ROOM_URL = 'https://2ndblock.com/room/kqlm15NawUT9X1a5vOQm'
PROFILE_CSS_SELECTOR = '#game-screen > div:nth-child(2) > div.css-1ewmce8.ehzashr0 > div.css-azx95j > div.css-o16ypd > div.css-f4n6xs > span'

CHATTING_LIST_SELECTOR = 'div.css-n1fm3w'
CHATTING_TAB_NICKNAME_SELECTOR = 'div.css-1o1z1uf'
CHATTING_CONTENTS_TEXT_SELECTOR = 'div.css-rpu5yn.e112x67u4'
CHATTING_ALL_CHAT_SELECTOR = 'div.todo-game-focus.Chatting_chat-user-scroll__GmCv_ > div:first-child'


if __name__ == "__main__":
    opt = ChromeOptions()
    opt.add_argument('--force-device-scale-factor=1')
    driver = webdriver.Chrome(options=opt, executable_path='./chromedriver')
    driver.get(url=SECONDBLOCK_ROOM_URL)

    WebDriverWait(driver, 3600).until(EC.presence_of_element_located((By.CSS_SELECTOR, PROFILE_CSS_SELECTOR)))
    print("로그인 감지")


