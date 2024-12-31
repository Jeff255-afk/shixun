import requests
from bs4 import BeautifulSoup

url = 'http://www.baidu.com'
res = requests.get(url)

res.encoding = res.apparent_encoding

html = res.text
# html xml解析
soup = BeautifulSoup(html, 'html.parser')
# print(soup.prettify())
# print(soup.title.string)
# print(soup.find_all('div', {'class': 'head_wrapper'}))

alist = list()
temp = soup.find_all('a')
print(temp)
for a in temp:
    # print(a['href'])
    alist.append(a['href'])
print(alist)
