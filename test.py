import urllib.parse
url = 'https://s.weibo.com/weibo?q=%E5%B0%8F%E6%97%A5%E6%9C%AC&typeall=1&suball=1&timescope=custom%3A2023-12-01-0%3A2023-12-02-23&Refer=g&page=1'
decoded_url = urllib.parse.unquote(url)
print(decoded_url)