import time
import requests
from bs4 import BeautifulSoup


class Parser:
    def __init__(self, headers, link, category_id):
        self.link = link
        self.headers = headers
        self.category_id = str(category_id)
        self.extension = 'Проекты на FL.ru (Все проекты: Разработка сайтов)'
        self.result = ''

    def set_extension(self, extension):
        if extension != 'Все категории':
            self.extension = f'Проекты на FL.ru (Все проекты: {extension})'
            return

        self.extension = f'Проекты на FL.ru (Все проекты)'

    def get_extension(self):
        return self.extension

    def set_category_id(self, category_id):
        self.category_id = str(category_id)

    def get_category_id(self):
        return self.category_id

    def make_dict(self, title='', date='', link=''):
        dictionary = {'title': title, 'date': date, 'link': link}
        return dictionary

    def get_titles(self):
        titles = []

        for item in self.result:
            titles.append(item.get('title'))

        return titles

    def get_page(self):
        response = ''
        try:
            session = requests.Session()
            session.headers = self.headers
            response = session.get(url=(self.link + self.category_id))
            decoded_response = response.content.decode('utf-8')

            if response.status_code == 200:
                return decoded_response
            else:
                raise Exception(f'Error in page receiving!\n{response}')

        except Exception:
            raise Exception(f'Error in page receiving!\n{response}')

    def get_content(self, page):
        xml = BeautifulSoup(page, 'xml')
        return xml

    def parse_category(self):
        try:
            content = self.get_content(self.get_page())

            titles = content.find_all('title')
            links = content.find_all('guid')
            dates = content.find_all('pubDate')
        except Exception:
            raise Exception(f'Error in page parsing!')
        formatted_titles = []
        link_list = []
        dates_list = []

        pair_list = []

        for link in links:
            link_list.append(link.text)

        for date in dates:
            dates_list.append(date.text)

        for title in titles:
            if title.text.lower() != self.extension.lower():
                formatted_titles.append(title.text.replace(' &#8381;', 'P'))

        if len(formatted_titles) == len(link_list):
            for i in range(len(formatted_titles)):
                pair_list.append(self.make_dict(formatted_titles[i], dates_list[i], link_list[i]))

        elif len(formatted_titles) != len(link_list):

            if len(formatted_titles) > len(link_list):
                for i in range(len(link_list)):
                    pair_list.append(self.make_dict(formatted_titles[i], dates_list[i], link_list[i]))

            elif len(formatted_titles) < len(link_list):
                for i in range(len(formatted_titles)):
                    pair_list.append(self.make_dict(formatted_titles[i], dates_list[i], link_list[i]))

        else:
            pair_list.append(self.make_dict('err0r', time.strftime("%H:%M:%S", time.localtime()), 'err0r'))
            raise Exception(f'Error in dict compilation!')

        self.result = pair_list
        return pair_list
