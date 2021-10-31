import requests
from bs4 import BeautifulSoup
from config import *
import csv

def all_pagination():
    s = requests.get(url=URL, headers=HEADERS, cookies=COOKIES).text
    soup = BeautifulSoup(s, 'lxml')
    item = soup.find_all('span', class_='pagination-item-JJq_j')
    pages = item[-2]
    pages = pages.get_text(strip=True)
    pages = int(pages)
    return pages

def get_html(url):
    s = requests.get(url=url, headers=HEADERS, cookies=COOKIES)
    return s.text

def get_content(html):
    list_content =[]
    soup = BeautifulSoup(html, 'lxml')
    items = soup.find_all('div', class_='iva-item-root-Nj_hb photo-slider-slider-_PvpN iva-item-list-H_dpX iva-item-redesign-nV4C4 iva-item-responsive-gIKjW items-item-My3ih items-listItem-Gd1jN js-catalog-item-enum')
    for item in items:
        list_content.append({
            'title': item.find('a', class_='link-link-MbQDP link-design-default-_nSbv title-root-j7cja iva-item-title-_qCwt title-listRedesign-XHq38 title-root_maxHeight-SXHes').get('title'),
            'link': 'https://avito.ru' + item.find('a', class_='link-link-MbQDP link-design-default-_nSbv title-root-j7cja iva-item-title-_qCwt title-listRedesign-XHq38 title-root_maxHeight-SXHes').get('href'),
            'price': item.find('span', class_='price-price-BQkOZ').find_next('meta').find_next('meta').get('content'),
            'place': item.find('div', class_='iva-item-developmentNameStep-n46gZ').find_next('span').get_text(strip=True),
            'discription': item.find('div', class_='iva-item-descriptionStep-QGE8Y').find_next('div').get_text(strip=True),
        })
    return list_content

def get_pagination(html):
    pass

def save(lst):
    with open('homes.csv', 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(
            ['Название', 'Ссылка', 'Цена', 'Местоположение', 'Описание'])
        for i in lst:
            writer.writerow(
                [i['title'], i['link'], i['price'], i['place'], i['discription']]
            )

def main():
    URL = 'https://www.avito.ru/moskva/doma_dachi_kottedzhi?p=1'
    list_all_content = []
    all_pagin = all_pagination()
    try:
        for i in range(2, all_pagin + 1):
            html = get_html(URL)
            list_all_content.extend(get_content(html))
            URL = f'https://www.avito.ru/moskva/doma_dachi_kottedzhi?p={i}'
            print(f'Парсинг {i} страницы!')
        save(list_all_content)
    except Exception:
        print('Ошибка, сохранение файла!')
        save(list_all_content)


if __name__ == '__main__':
    main()
