import csv

from selenium import webdriver
from selenium.webdriver.common.by import By
import time


def write_data_in_csv(title, date, link):
    with open('news.csv', 'a', newline='', encoding='utf-8') as f:
        fieldnames = ['title', 'date', 'link']
        writer = csv.DictWriter(f, fieldnames=fieldnames)

        # Проверка, если файл пустой, то записываем заголовок
        if f.tell() == 0:
            writer.writeheader()

        writer.writerow({'title': title, 'date': date, 'link': link})


def check_uniqueness(link):
    with open('news.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if link in row.values():
                return False

        return True


def parse_html_page(url: str):
    driver = webdriver.Chrome()
    driver.get(url)

    news_blocks = driver.find_elements(By.CLASS_NAME, "no-style")

    for block in news_blocks:
        block_link = block.get_attribute('href')
        block_text = block.text.split('\n')

        if not check_uniqueness(block_link):
            continue

        if block_text[0] == 'Top':
            write_data_in_csv(block_text[1], block_text[2], block_link)
            continue

        write_data_in_csv(block_text[0], block_text[1], block_link)


while True:
    time.sleep(1)
    parse_html_page('https://announcements.bybit.com/en-US/?category=&page=1')