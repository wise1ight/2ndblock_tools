from selenium import webdriver
from selenium.webdriver import ActionChains, ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from graphical import GraphicalLocator


def detect_object():
    print('test')

if __name__ == "__main__":
    URL = 'https://2ndblock.com/room/kqlm15NawUT9X1a5vOQm'
    opt = ChromeOptions()
    opt.add_argument('--force-device-scale-factor=1')
    driver = webdriver.Chrome(options=opt, executable_path='../chromedriver')
    driver.get(url=URL)

    WebDriverWait(driver, 3600).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#game-screen > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > button')))
    print("로그인 감지")

    block_button = driver.find_element(By.CSS_SELECTOR, '#game-screen > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > button')
    block_button.click()

    driver.implicitly_wait(3)

    img_check = GraphicalLocator("img/B.png")
    img_check.find_me(driver)
    print(f"{img_check.threshold['shape']} {img_check.threshold['histogram']}")
    is_found = True if img_check.threshold['shape'] >= 0.8 and \
                       img_check.threshold['histogram'] >= 0.4 else False

    if is_found:
        action = ActionChains(driver)
        print(f"x : {img_check.center_x}, y : {img_check.center_y}")
        action.move_by_offset(img_check.center_x, img_check.center_y)
        action.click()
        action.perform()

        delete_button = driver.find_element(By.CSS_SELECTOR, 'div.in-game-button.editor.red')
        delete_button.click()
