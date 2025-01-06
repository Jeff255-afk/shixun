import re

# . 匹配出换行符以外的任何字符
# re.match() match 只能从头开始匹配
# res = re.match('b', 'abc123abc')
# print(res)

# \d 匹配数字
# res = re.match('\d', '123abc')
# print(res)

# \w 匹配字母、数字、下划线
# \s 匹配空白字符
# res = re.match('\w', '_123abc')
# print(res)

# + * 匹配多个字符
# + 匹配一个或多个
# res = re.match('\w+', '123abc')
# print(res)

# * 匹配零个或多个
# res = re.match('\w*', '@_123abc@123')
# print(res)

# re.search() 字符串中搜索，不一定从头开始
# res = re.search('\w+', '@_123abc@123')
# print(res)

# ? 匹配0个或一个

# [] 单个匹配， or
# res = re.match('[abc]', 'abc123')
# print(res)
#
# res = re.match('[a-zA-Z0-9]+', 'Ac123cde')
# print(res)

# ^ $开头结尾匹配
res = re.search('a\d+$', '123a1212acdq')
print(res)

# 分组 group() 取字符
res = re.search('(\d+)(\w+)', '123a1212acdq')
print(res.group(0), res.group(1), res.group(2))

# findall() 匹配所有
res = re.findall('\d+', '123a1212acdq234235676ertd')
print(res)

# 匹配范围
res = re.search('\d{2,5}', '1235678fhudesbhdkasn980348928')
print(res)
