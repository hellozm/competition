import re
import requests
import analyze_web
from bs4 import BeautifulSoup


class Spider:
    def __init__(self, url):
        self.url = url
        self.base_url = 'http://pinggu.zx110.org/checkWebsite.do'
        self.headers = {
            'Connection': 'keep-alive',
            'Accept-Encoding': 'gzip,deflate',
            'Accept': '*/*',
            'User-Agent': 'python-requests/2.19.1',
        }
        self.feature = []
        self.flag = True
        self.html = self.get_response()

    def get_response(self):
        data = {
            'lt': 1,
            'wd': self.url
        }
        try:
            r = requests.post(self.base_url, data=data, headers=self.headers)
            if r.status_code == 200:
                return r.text
            else:
                return ''
        except :
            self.flag = False
            return ''

    def get_main_info(self):
        """
        获取网页主体信息中的备案号（0|1）以及主办单位性质（无：0，个人：1，企业：2，政府：3）
        :return:
        """
        if self.flag:
            html = self.html
            soup = BeautifulSoup(html, 'html.parser')
            if soup.find('div', id='tablist_1_0'):
                tablist = soup.find('div', id='tablist_1_0')
                if tablist.find_all('tr'):  # 如果该网站有主体信息（备案号、主办单位性质）
                    tr = tablist.find_all('tr')
                    for each_tr in tr:
                        if each_tr.text:
                            if '网站备案' in each_tr.text:
                                self.feature.append("1")
                                # print(each_tr.text)
                            if '主办单位性质' in each_tr.text:
                                td = each_tr.find_all('td')
                                character = td[1].text
                                if character == '个人':
                                    self.feature.append('1')
                                elif character == '企业':
                                    self.feature.append('2')
                                else:
                                    self.feature.append('3')
                else:  # 没有主体信息（备案号、主办单位性质），则向查询备案号的网站查询
                    info = analyze_web.get_response(self.url)
                    if '未备案' in info:
                        self.feature.append('0')
                        self.feature.append('0')
                    elif '失败' in info:
                        self.feature.append('0')
                        self.feature.append('0')
                    elif '屏蔽' in info:
                        self.feature.append('1')
                        self.feature.append('1')
                    else:
                        self.feature.append('1')
                        character = info[0]
                        if character == '个人':
                            self.feature.append('1')
                        elif character == '企业':
                            self.feature.append('2')
                        else:
                            self.feature.append('3')
                    # print(info)
                # print(self.feature)

            else:
                self.feature.append('0')
                self.feature.append('0')
                print(self.url + '不存在！------------')
        else:
            self.feature.append('error!')
            self.feature.append('error!')

    def get_ip_location(self):
        """
        获取网址ip所在地（未知：0，国外：1，国内：2）
        :return:
        """
        try:
            response = requests.get('http://ip.bczs.net/' + self.url, headers=self.headers)
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            if soup.find_all('div', 'well'):
                div = soup.find_all('div', 'well')[0]
                code = div.find_all('code')
                area = code[2].text
                if '中国' in area:
                    self.feature.append('2')
                elif '未知' in area:
                    self.feature.append('0')
                else:
                    self.feature.append('1')
            else:
                self.feature.append('1')
        except:
            self.feature.append('error!')

    def get_qualification_info(self):
        """
        获取网页中资质信息中的证书，有一个加一分
        :return: 证书名以及数量
        """
        if self.flag:
            html = self.html
            soup = BeautifulSoup(html, 'html.parser')
            if soup.find('div', id='tablist_1_1'):
                tablist = soup.find('div', id='tablist_1_1')
                if tablist.find_all('div', 'pg-result-content'):
                    divs = tablist.find_all('div', 'pg-result-content')
                    count = len(divs)
                    self.feature.append(str(count))
                    for div in divs:
                        h3 = div.find('h3')
                        # print(h3.text)
                else:
                    self.feature.append('0')
        else:
            self.feature.append('error!')

    def get_site_loopholes_info(self):
        """
        获取网站漏洞数量(高危，严重，警告，轻微)
        :return:
        """
        if self.flag:
            html = self.html
            soup = BeautifulSoup(html, 'html.parser')
            if soup.find('div', id='tablist_1_2'):
                tablist = soup.find('div', id='tablist_1_2')
                if tablist.find_all('li'):
                    for each_li in tablist.find_all('li'):
                        number = each_li.text.strip()[-4]
                        self.feature.append(str(number))
                elif tablist.find_all('div', 'pg-box-nothing')[0].text == '安全检测失败!':
                    self.feature.append('0')
                    self.feature.append('0')
                    self.feature.append('0')
                    self.feature.append('0')
                else:
                    self.feature.append('10')
                    self.feature.append('10')
                    self.feature.append('10')
                    self.feature.append('10')
        else:
            self.feature.append('error!')
            self.feature.append('error!')
            self.feature.append('error!')
            self.feature.append('error!')

    def get_site_label(self):
        if self.flag:
            html = self.html
            soup = BeautifulSoup(html, 'html.parser')
            if soup.find('span', 'site-txt ok'):
                label = soup.find('span', 'site-txt ok').text
                self.feature.append('1')
                # print(label)
            elif soup.find('span', 'site-txt ok bad'):
                label = soup.find('span', 'site-txt ok bad').text
                self.feature.append('0')
                # print(label)
            elif soup.find('span', 'site-txt ok general'):
                label = soup.find('span', 'site-txt ok general').text
                self.feature.append('0')
        else:
            self.feature.append('error!')

    def write_feature(self):
        with open('feature.txt', 'a+', encoding='utf-8') as f:
            f.write(','.join(self.feature) + '\n')


if __name__ == '__main__':

    with open('urls.txt') as f:
        for line in f:
            url = line.rstrip().split('//')[1].split(':')[0]
            print(url)
            s = Spider(url)
            s.get_main_info()
            s.get_ip_location()
            s.get_qualification_info()
            s.get_site_loopholes_info()
            s.get_site_label()
            s.write_feature()
    '''
    s = Spider('hunantv.com')
    s.get_main_info()
    s.get_ip_location()
    s.get_qualification_info()
    s.get_site_loopholes_info()
    s.get_site_label()
    s.write_feature()
    '''