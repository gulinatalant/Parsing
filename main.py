import json
from typing import List
import csv
import requests
from bs4 import BeautifulSoup, Tag



HOST = 'https://gidonline.io/'



def get_html(url: str, page=1):
    response = requests.get(url + f'/page/{page}')
    response.encoding = 'utf-8'
    if response.status_code == 200:
        return response.text
    raise Exception('сайт не отвечает')


def get_soup(html:str) ->BeautifulSoup:
    soup = BeautifulSoup(html, 'lxml')
    return soup


def get_cards_from_soup(soup: BeautifulSoup) -> List[Tag]:
    cards = soup.find_all('a',{'class': 'mainlink'})
    return cards


def get_data_from_cards(cards: List[Tag]) -> List[dict]:
    data = []
    for card in cards:
        movie = {
            'title':card.find('span').text,
            'image':HOST + card.find('img').get('src'),
            'year':card.find('div', {'class': 'mqn'}).text,
            'rating':card.find('div', {'class':'f-rate'}).find('img').get('alt'),
            'link': card.get('href'),
        }
        data.append(movie)
    return data    


def paginated_parse(page: int) -> List[dict]:
    result = []
    for page_number in range(1,page+1):
        html = get_html(HOST, page_number)
        soup = get_soup(html)
        cards = get_cards_from_soup(soup)
        data = get_data_from_cards(cards)

        result.extend(data)
    return result    




def write_to_json(data: List[dict]):
    with open('movies.json','w') as movies:
        json.dump(data, movies, indent=4, ensure_ascii=False)



def write_to_csv(data: List[dict]):
    with open('movies.csv', 'w') as movies:
        filenames = data[0].keys()
        writer = csv.DictWriter(movies, fieldnames=filenames)
        # writer = csv.DictWriter(movies, filenames=filenames)
        writer.writeheader()
        writer.writerows(data)


def main():
    data = paginated_parse(8)
    write_to_json(data)
    write_to_csv(data)





# def main():
#     data = paginated_parse(8)
#     write_to_json(data)
#     write_to_csv(data)


if __name__ == '__main__':
    main()
