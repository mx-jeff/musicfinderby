from src.utils import setSelenium, init_parser

from selenium.webdriver.common.by import By


def scrapper_youtube_robot(crawler_name, music):
    driver = setSelenium()
    print(f'{crawler_name} Extraindo link do video...')
    driver.get(f'https://www.youtube.com/results?search_query={music}')
    driver.implicitly_wait(220)

    html = driver.find_element(By.TAG_NAME, 'html')
    src = html.get_attribute('outerHTML')

    driver.quit()
    print(f'{crawler_name} Pagína localizada! extraindo elementos...')

    soap = init_parser(src)
    container = soap.find('div', id="contents")
    video = container.find('a', id="thumbnail")['href']

    print(f"{crawler_name} Link extraido!")
    return f"https://www.youtube.com{video}"
