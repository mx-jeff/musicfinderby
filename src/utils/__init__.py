import os
from time import sleep, gmtime, strftime
import timeit
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from requests.exceptions import InvalidSchema, ConnectionError
from bs4 import BeautifulSoup
import requests


def arrendondar(numero):
    print("%.2f" % round(numero, 2))


def tempo_estimado(start):
    stop = timeit.default_timer()
    execution_time = stop - start

    print("Executando em: ", end="")
    time_formated_to_seconds = execution_time
    print(strftime("%H:%M:%S", gmtime(time_formated_to_seconds)))


def setSelenium(console=True):
    # configuração do selenium 
    chrome_options = Options()
    chrome_options.binary_location = os.environ.get('GOOGLE_CHROME_BIN')

    if console:
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
    
    # Desabilitar notificações
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_experimental_option("prefs", { 
        "profile.default_content_setting_values.notifications": 2 
    })
    # evitar detecção anti-bot
    chrome_options.add_argument("--disable-blink-features")
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_experimental_option("detach", True)
    # desabilitar o log do chrome
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
    prefs = {"profile.default_content_setting_values.notifications" : 2}
    chrome_options.add_experimental_option("prefs",prefs)
    path = os.environ.get('CHROMEDRIVER_PATH') or "./chromedriver.exe" 
    
    return webdriver.Chrome(chrome_options=chrome_options, executable_path=path, service_log_path='NUL')


def init_crawler(URL):
    try:    
        page = requests.get(URL)

        if page.status_code != 200:
            print(f'[ERRO {page.status_code}] Site indisponivel, tente novamente mais tarde')
            return
    
        return BeautifulSoup(page.content,"lxml")
    
    except InvalidSchema:
        print('Algo deu errado!')
        return 
    
    except ConnectionError:
        print('Não conseguiu se conectar na página!')
        return


def init_parser(html):
    return BeautifulSoup(html, "lxml")


def scroll(driver):
    SCROLL_PAUSE_TIME = 20

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page and increments one more second
        SCROLL_PAUSE_TIME += 1
        sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
