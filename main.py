import requests
from bs4 import BeautifulSoup
from threading import Thread
import sys
import time

WORD = 'совместимость'
MAX_DEEP = 5

def find_all_links(url: str) -> list:
    content_on_page = requests.get(url).text
    if content_on_page.find(WORD) == -1:
        soup = BeautifulSoup(content_on_page, 'html.parser')
        links = soup.find_all('a')
        res = [i.get('href') for i in links]
        for i in range(len(res) - 1, -1, -1):
            if res[i] is None:
                res.remove(res[i])
            else:
                temp = res[i].split('/')
                if temp[0] != 'https:':
                    res.remove(res[i])
        return res
    else:
        return url


def find_word_in_links_on_pages(url: str, count=2):
    result = find_all_links(url)
    if count == MAX_DEEP:
        return
    if isinstance(result, str):
        print(f'Word was find: {url}')
        return
    else:
        for i in result:
            return find_word_in_links_on_pages(i, count + 1)
        sys.exit(1)


def _main() -> None:
    url = r'https://www.tut.by/'
    links = find_all_links(url)
    if links == url:
        print(f'Word was find: {url}')
    else:
        threads = [Thread(target=find_word_in_links_on_pages, name=link, args=(link,)) for link in links]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()


if __name__ == '__main__':
    _main()
