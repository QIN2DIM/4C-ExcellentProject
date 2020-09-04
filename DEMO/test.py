import requests
import tempfile
import os
from fake_useragent import UserAgent

target = 'http://yao.qinse.top/proxy_key.txt'

res = requests.get(target, )

print(res.text)