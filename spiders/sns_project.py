import os

import requests
from bs4 import BeautifulSoup

from config import SPIDER_HEADERS, ROOT_DIR_DATABASE


class SnsProjSpider(object):

    def __init__(self):
        self.sch_211 = 'http://www.eol.cn/e_html/gk/gxmdold/211.shtml'
        self.sch_985 = 'http://daxue.eol.cn/985.shtml'

    @staticmethod
    def handle_html(url):
        res = requests.get(url, headers=SPIDER_HEADERS)
        res.encoding = res.apparent_encoding
        return res.text

    @staticmethod
    def parse_html(html):
        soup = BeautifulSoup(html, 'html.parser')
        return soup

    def get_school_211(self) -> list:
        """
        抓取211 工程院校名单
        :return:
        """
        # //td[@align='center']//span
        html = self.handle_html(self.sch_211)
        soup = self.parse_html(html)

        sns = soup.find_all('td', attrs={'align': 'center'})
        sns_list = list()
        for sn in sns:
            try:
                msg = sn.find('span').text
                if '大学' in msg or '学院' in msg:
                    sns_list.append(msg)
            except AttributeError:
                pass
        return sns_list

    def get_school_985(self) -> list:
        """
        抓取985 工程院校名单
        :return:
        """
        html = self.handle_html(self.sch_985)
        soup = self.parse_html(html)
        sns = soup.find_all('td')
        sns_list = list()
        for sn in sns:
            try:
                msg = sn.find('a').text
                if '大学' in msg or '学院' in msg:
                    sns_list.append(msg)
            except AttributeError:
                pass
        return sns_list


def checker_of_fileExit(file_name):
    ck_path = os.path.exists(file_name)
    if ck_path:
        with open(file_name, 'r', encoding='utf-8') as f:
            return [i.strip() for i in f.readlines()]
    else:
        if '211' in file_name:
            return SnsProjSpider().get_school_211()
        elif '985' in file_name:
            return SnsProjSpider().get_school_985()


def get_211():
    return checker_of_fileExit(ROOT_DIR_DATABASE + '/tpd/get_school_211.txt')


def get_985():
    return checker_of_fileExit(ROOT_DIR_DATABASE + '/tpd/get_school_985.txt')
