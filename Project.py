import re


class Project:
    def __init__(self, title, link, date):
        self.title = title
        self.price = self.title[self.title.index('(Бюджет:'):].replace('(Бюджет: ', '').replace(')', '')
        self.title = self.title.partition('(Бюджет')[0]
        self.link = link
        self.date = re.findall(r'\d\d\s\w\w\w', date)[0] + ' ' + re.findall(r'\d\d:\d\d', date)[0]

    def set_title(self, title):
        self.title = title

    def get_title(self):
        return self.title

    def set_link(self, link):
        self.link = link

    def get_link(self):
        return self.link

    def set_date(self, date):
        self.date = date

    def get_date(self):
        return self.date

    def get_project(self):
        string = f'<a href="{self.link}">{self.title}</a>\n\n<b>{self.price}</b>\n\n{self.date}'
        return string
