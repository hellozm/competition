import requests
from bs4 import BeautifulSoup


def get_base_info(url):
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
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0',
    }
    r = requests.get(full_url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    if soup.find_all('li', 'clearfix'):  # 如果网站基本信息存在
        info = []
        sponsor_name = soup.find_all('li', 'clearfix')[0].find('p').text
        sponsor_feature = soup.find_all('li', 'clearfix')[1].find('p').text
        sponsor_license = soup.find_all('li', 'clearfix')[2].find('p').text
        web_name = soup.find_all('li', 'clearfix')[3].find('p').text
        info.append(sponsor_name[:-10])
        info.append(sponsor_feature)
        info.append(sponsor_license[:-4])
        info.append(web_name)
        # print(info)
        return info
    elif soup.find_all('p', 'tc col-red fz18 YaHei pb20'):  # 如果未备案或者屏蔽
        content = soup.find_all('p', 'tc col-red fz18 YaHei pb20')[0]
        print(content.text)
        if '未备案' in content.text:
            info = content.text
        elif '屏蔽' in content.text:
            info = content.text
        else:
            info = '查询失败'
        return info
    else:
        info = '404'
        return info


if __name__ == '__main__':
    get_base_info("http://www.wx359.cn/")
    get_base_info("http://www.baidu.com/")
    get_base_info("http://www.taobao.com/")
