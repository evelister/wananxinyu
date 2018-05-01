import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup

def get_page(i):
    url = 'http://www.vikilife.com/tag/%E6%99%9A%E5%AE%89%E5%BF%83%E8%AF%AD/page/' + str(i)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
    except RequestException:
        print('error')
        return None

def parse_page(html):
    soup = BeautifulSoup(html, 'lxml')
    details = soup.find_all('div', 'post clearfix')
    for detail in details:
        yield detail.find('a')['href']

def get_page_detail(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print('cuo wu', url)
        return None

def parse_page_detail(html):
    soup = BeautifulSoup(html, 'lxml')
    results = soup.find_all('p')
    posts = []
    for result in results:
        posts.append(result.get_text())
    for i in range(posts.count('')):
        posts.remove('')
    str1 = '欢迎关注心语公众号：晚安画报（lovepic8）'
    while str1 in posts:
        posts.remove(str1)
    return posts

def write_to_file(content):
    with open('result.txt', 'a', encoding='utf-8') as f:
        f.write((content) + '\n')
        f.close()


def main():
    for i in range(29):
        html = get_page(i)
        for url in parse_page(html):
            html = get_page_detail(url)
            if html:
                results = parse_page_detail(html)
                for i in range(len(results)):
                    print(results[i])
                    write_to_file(results[i])


if __name__ == '__main__':
    main()