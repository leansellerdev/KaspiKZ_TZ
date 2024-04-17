from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd

import json

wiki_link = 'https://ru.wikipedia.org/wiki/%D0%A0%D0%B8%D0%BC%D1%81%D0%BA%D0%B0%D1%8F' \
            '_%D0%B8%D0%BC%D0%BF%D0%B5%D1%80%D0%B8%D1%8F'


# Open browser and download wiki page
def download_page(link: str):
    driver = webdriver.Chrome()
    driver.get(link)

    return driver.page_source


def parse_page():
    article_info: dict = {}

    soup = BeautifulSoup(download_page(wiki_link), 'html.parser')

    title = soup.find('span', {'class': 'mw-page-title-main'}).text.replace(' ', '')
    short_info = soup.find_all('p')[1].text.replace(' ', '')

    content = soup.find('div', {'class': 'toc'}).text.replace(' ', '')

    article_info["Название статьи"] = title
    article_info["Краткая информация"] = short_info
    article_info["Содержание"] = content

    sidebar_content = soup.find('table', {'class': 'infobox'})
    sidebar_elements = sidebar_content.find_all('tr')[8:18] + sidebar_content.find_all('tr')[23:]

    # Iterate each element in sidebar and put it in dict
    for element in sidebar_elements:

        article_info[element.findNext('th').text.replace(' ', '')] = element.findNext('td').text.replace(' ', '')

    return article_info


def write_info(info: dict):
    json_object = json.dumps(info, indent=4, ensure_ascii=False)

    with open("info.json", 'w', encoding='utf-8') as outfile:
        outfile.write(json_object)

    df = pd.DataFrame(info, index=[0])
    df.to_excel('info.xlsx')


write_info(parse_page())
