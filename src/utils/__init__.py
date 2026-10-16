import os
import sys
import requests
import timeit
import logging

from bs4 import BeautifulSoup
from time import sleep, gmtime, strftime
from dotenv import load_dotenv
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from requests.exceptions import InvalidSchema, ConnectionError

from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.chrome.service import Service


def arrendondar(numero):
    print("%.2f" % round(numero, 2))


def tempo_estimado(start):
    stop = timeit.default_timer()
    execution_time = stop - start

    print("Executando em: ", end="")
    time_formated_to_seconds = execution_time
    print(strftime("%H:%M:%S", gmtime(time_formated_to_seconds)))


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


def log(msg):
    today = datetime.now()

    date_time = today.strftime("%d/%m/%Y %H:%M:%S")

    with open('log.txt', 'a') as log:
        log.writelines(f"{date_time} - {msg}\n")


def choose_driver(driver_name:str):
    if driver_name == "chrome":
        return ChromeDriverManager().install()
    elif driver_name == "firefox":
        return GeckoDriverManager().install()
    elif driver_name == "edge":
        return EdgeChromiumDriverManager().install()
    else:
        return ChromeDriverManager().install()


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)


def setSelenium(headless:bool=True, rotate_useragent:bool=False, remote_webdriver:bool=True, driver_name:str="chrome", profile:bool=False, profile_name:str="default") -> webdriver.Chrome :
    """
    Set Selenium Webdriver
    args: 
        - headless: bool, True if you want to run the browser in headless mode
        - rotate_useragent: bool, True if you want to rotate the useragent
        - remote_webdriver: bool, True if you want to download and use the remote webdriver
        - driver_name: str, the name of the driver you want to use
        - profile_name: str, the name of the profile
        - profile:bool, True if you want to use profiles

    returns:
        - webdriver: Selenium Webdriver instance
    """


    chrome_options = Options()
    load_dotenv()

    if headless:
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
 
    chrome_options.add_argument(f'user-agent=Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36')
    chrome_options.add_argument("--disable-blink-features")
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_experimental_option("detach", True)
    # desabilitar o log do chrome
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
    prefs = {"profile.default_content_setting_values.notifications": 2}
    chrome_options.add_experimental_option("prefs", prefs)

    if profile:
        dir_path = os.getcwd()
        profile = os.path.join(f"{dir_path}/{profile_name}", "profile", "wpp")
        chrome_options.add_argument(f'user-data-dir={profile}')

    if remote_webdriver:
        path = choose_driver(driver_name)

    else:
        path = os.getenv('CHROMEDRIVER_PATH')

    return webdriver.Chrome(options=chrome_options, service=Service(executable_path=resource_path(path), log_path='NUL'))


def init_log(filesave:bool=False, filename:str="debug.log", level=logging.INFO, **kwargs) -> None:
    
    """setup a configured custom log handler

    parameters:
        - filename (str): log filename
        - filesave (bool): if save to file or not (default:False)
        - level (logging): log leve (default:logging.INFO)

    returns:
        None
    """

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
     
    # create console handler and set level to info
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s", datefmt='%d/%m/%Y %H:%M:%S')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    if kwargs.get("error_sep") and filesave:
        # create error file handler and set level to error
        handler = logging.FileHandler(os.path.join("error.log"),"w", encoding=None, delay="true")
        handler.setLevel(logging.ERROR)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s", datefmt='%d/%m/%Y %H:%M:%S')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
   
    if filesave:
        # create debug file handler and set level to debug
        handler = logging.FileHandler(os.path.join(filename),"w")
        handler.setLevel(level)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s", datefmt='%d/%m/%Y %H:%M:%S')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
