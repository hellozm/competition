import requests
from bs4 import BeautifulSoup


def get_response(url):
    """
    将网站是否有备案、屏蔽以及主办单位性质，若有，则写入identification.txt并打印出来
    :param url: 想要查询的网站地址
    :return: info
    """
    full_url = "http://icp.chinaz.com/" + url
    headers = {
        'Connection': 'keep-alive',
        'Accept-Encoding': 'gzip,deflate',
        'Accept': '*/*',
        'User-Agent': 'python-requests/2.19.1',
    }
    r = requests.get(full_url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    if soup.find_all('li', 'clearfix'):  # 如果备案号以及主办单位性质存在，将两属性放在info列表并返回
        info = []
        li_1 = soup.find_all('li', 'clearfix')[1]
        info.append(li_1.find('p').text)
        li_2 = soup.find_all('li', 'bg-gray clearfix')[1]
        info.append(li_2.find('p').text)
        info[1] = info[1][:-4]
        # print(info)
        # with open('identification.txt', 'a+', encoding='utf-8') as f:
        # f.write(url+' '+' '.join(info)+'\n')
        return info
    elif soup.find_all('p', 'tc col-red fz18 YaHei pb20'):  # 如果未备案或者屏蔽
        content = soup.find_all('p', 'tc col-red fz18 YaHei pb20')[0]
        # print(content.text)
        if '未备案' in content.text:
            info = content.text
        elif '屏蔽' in content.text:
            info = content.text
        # with open('identification.txt', 'a+', encoding='utf-8') as f:
            # f.write(url+' '+info+'\n')
        return info


if __name__ == '__main__':
    get_response("http://www.6090qpg.com/")
    get_response("http://www.baidu.com/")
    get_response("http://www.taobao.com/")
