# import requests
#
# url = 'http://www.baidu.com'
# res = requests.get(url)
# # 获取文本数据、二进制数据
# # res.encoding = 'utf-8'
# res.encoding = res.apparent_encoding
# print(res.text)


import requests

url = 'https://pics1.baidu.com/feed/3bf33a87e950352ae0354c2fe72ed2fdb2118b39.jpeg@f_auto?token=dbfe15d04053e1d5ba195a955343c67a'
res = requests.get(url)
# 获取文本数据、二进制数据
# res.encoding = 'utf-8'
res.encoding = res.apparent_encoding
with open('downloaded_image1.jpeg', 'wb') as f:
    f.write(res.content)
print(res.content)

