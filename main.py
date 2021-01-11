import requests
from bs4 import BeautifulSoup
from threading import Thread
from multiprocessing import Process
word= ''

def find_all_links(url: str) -> list:
    try:
        text_on_page = requests.get(url).text
    except:
        print('Некорректный ')
    if text_on_page.find(word) == -1:
        soup = BeautifulSoup(text_on_page, 'html.parser')
        all_links = [i.get('href') for i in soup.find_all('a')]
        return all_links
    else:
        return url

def find_word_in_links_on_pages(url:str, count=0):
    r = find_all_links(url)
    if count == 2:
        print('end')
        return
    if type(r) == str:
        return r
    else:
        for i in r:
            print(i)
            find_word_in_links_on_pages(i,count + 1)

def _main():
    url = 'https://www.youtube.com/'
    links = find_all_links(url)
    processes = []
    for link in links:
        processes.append(Process(target=find_word_in_links_on_pages, args=(link)))
    for process in processes:
        process.run()
        process.join()


if __name__ == '__main__':
    _main()
