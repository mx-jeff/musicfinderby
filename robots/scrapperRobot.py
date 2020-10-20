from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
import os


def getLinkfromYoutube(nameOfVideo):
    def setupWebdriver(headless):
        # options
        settings = Options()
        settings.binary_location = os.environ.get('GOOGLE_CHROME_BIN')
        settings.add_argument('--disable-dev-shm-usage')
        if headless:
            settings.add_argument('--headless')

        settings.add_argument('--no-sandbox')
        settings.add_experimental_option("detach", True)
        chrome_path = os.environ.get('CHROMEDRIVER_PATH') or "C:/Selenium/chromedriver.exe"

        return webdriver.Chrome(chrome_options=settings, executable_path=chrome_path)

    #init
    global driver

    driver = setupWebdriver(True)

    driver.get(f'https://www.youtube.com/results?search_query={nameOfVideo}')
    sleep(10)

    driver.find_element_by_xpath('//*[@id="thumbnail"]').click()
    sleep(10)

    url_video = driver.current_url

    driver.quit()
    
    return url_video

