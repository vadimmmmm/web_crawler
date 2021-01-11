import requests
from bs4 import BeautifulSoup
from threading import Thread
from multiprocessing import Process
word= ''

def find_all_links(url: str) -> list:
    text_on_page = requests.get(url).text
    if text_on_page.find(word) == -1:
        soup = BeautifulSoup(text_on_page, 'html.parser')
        all_links = [i.get('href') for i in soup.find_all('a')]
        return all_links
    else:
        return url

def _main():
    url = 'https://www.youtube.com/'
    links = find_all_links(url)
    for link in links:
        pass


if __name__ == '__main__':
    _main()
