import requests
import re
from bs4 import BeautifulSoup


class LinkQueue:
    def __init__(self):
        self.visited = []
        self.unvisited = []

    def get_visited_url(self):
        return self.visited

    def remove_visited_url(self, url):
        self.visited.remove(url)


class Spider:
    """
    爬取页面里面的url（少重复）
    """
    def __init__(self, url):
        self.url = url
        self.headers = {
                'Connection': 'keep-alive',
                'Accept-Encoding': 'gzip,deflate',
                'Accept': '*/*',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0',
            }
        self.flag = True
        try:
            self.r = requests.get(self.url, headers=self.headers, timeout=5)
        except requests.exceptions.ConnectTimeout:
            self.flag = False
            print("connection_timeout------"+self.url)
        except requests.exceptions.ConnectionError:
            self.flag = False
            print("connection_error-----"+self.url)
        except requests.exceptions.ReadTimeout:
            self.flag = False
            print("timeout------"+self.url)

    def get_url(self):
        if self.url.split('.')[-2] not in queue.visited:
            queue.visited.append(self.url.split('.')[-2])
        queue.unvisited.remove(self.url)
        # print(queue.visited)
        if self.flag and self.r.status_code == 200:
            soup = BeautifulSoup(self.r.text, 'html.parser')
            suburl = set()
            for label in soup.find_all("a"):
                if label.get('href') and re.match('http.*', label.get('href')):
                    normal_url = spider.normalization(label.get('href'))
                    if len(normal_url.split('.')) == 3 and normal_url.split('.')[-2] not in queue.visited:
                        # print(normal_url)
                        queue.visited.append(normal_url.split('.')[-2])
                        suburl.add(normal_url)
            for s in suburl:
                if len(queue.unvisited) < 600:
                    queue.unvisited.append(s)
                    with open('urls.txt', 'a+', encoding='utf-8') as f:
                        # print(s)
                        f.write(s+'\n')
                else:
                    queue.unvisited.clear()
            suburl.clear()

    def normalization(self, link):
        split_link = link.split('/')
        first_url = '/'.join(split_link[:3])
        normal_url = first_url.split('?')[0]
        return normal_url


if __name__ == "__main__":

    with open('different_urls', 'r', encoding='utf-8') as f:
        for line in f:
            start_url = line
            queue = LinkQueue()
            print(line)
            queue.unvisited.append(start_url)
            i = 0
            for url in queue.unvisited:
                spider = Spider(url)
                spider.get_url()

    '''
    start_url = "http://www.jiangsu.gov.cn/"
    queue = LinkQueue()
    queue.unvisited.append(start_url)
    for url in queue.unvisited:
        spider = Spider(url)
        spider.get_url()
    '''
