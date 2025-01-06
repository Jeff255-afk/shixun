import requests

url = 'https://httpbin.org/get'

res = requests.get(url)
proxies = {
    'http': 'http://127.0.0.1:33210'
}
print(res.json())