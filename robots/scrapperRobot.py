from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
import os


def getLinkfromYoutube(nameOfVideo):
    #init
    global driver
    
    #options
    settings = Options()
    settings.binary_location = os.environ.get('GOOGLE_CHROME_BIN')
    settings.add_argument('--disable-dev-shm-usage')
    settings.add_argument('--headless')
    settings.add_argument('--no-sandbox')
    settings.add_experimental_option("detach", True)
    chrome_path = os.environ.get('CHROMEDRIVER_PATH') or "C:/Selenium/chromedriver.exe"

    driver = webdriver.Chrome(chrome_options=settings, executable_path=chrome_path)

    driver.get(f'https://www.youtube.com/results?search_query={nameOfVideo}')
    sleep(5)

    #click on video
    video = driver.find_element_by_xpath('//*[@id="dismissable"]')
    video.click()

    url_video = driver.current_url

    sleep(5)
    driver.close()
    
    return url_video

