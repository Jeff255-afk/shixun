import requests

# 图片的URL
image_url = "https://pics1.baidu.com/feed/3bf33a87e950352ae0354c2fe72ed2fdb2118b39.jpeg@f_auto?token=dbfe15d04053e1d5ba195a955343c67a"

# 发起GET请求获取图片数据
response = requests.get(image_url)

# 检查请求是否成功
if response.status_code == 200:
    # 使用合适的内容类型来确定文件扩展名
    content_type = response.headers.get('content-type')

    # 写入文件，'wb' 表示以二进制格式写入
    with open('downloaded_image.jpeg', 'wb') as image_file:
        image_file.write(response.content)

    print("图片下载成功")
else:
    print(f"下载失败，状态码: {response.status_code}")