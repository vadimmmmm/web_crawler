import requests
from bs4 import BeautifulSoup
from threading import Thread
from multiprocessing import Process
import time

word = 'latest'
MAX_DEEP = 5


def find_all_links(url: str) -> list:
    content_on_page = requests.get(url).text
    if content_on_page.find(word) == -1:
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


def _main():
    url = r'https://www.youtube.com/'
    links = find_all_links(url)
    if links == url:
        print(f'Word was find: {url}')
    else:
        all_proccesses = [Thread(target=find_word_in_links_on_pages, name=link, args=(link,)) for link in links]
        for i in all_proccesses:
            i.start()
        for i in all_proccesses:
            i.join()


if __name__ == '__main__':
    start = time.time()
    _main()
    print(f'time: {time.time() - start}')
