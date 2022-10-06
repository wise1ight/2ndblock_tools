from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

if __name__ == "__main__":
    URL = 'https://2ndblock.com/room/kqlm15NawUT9X1a5vOQm'
    driver = webdriver.Chrome(executable_path='chromedriver')
    driver.get(url=URL)

    WebDriverWait(driver, 3600).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#game-screen > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > button')))
    print("로그인 감지")