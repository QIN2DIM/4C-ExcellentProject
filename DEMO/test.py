"""通过请求Docker-compose，获取代理IP"""

# 目标采集网站暂未出现封禁IP的反制措施，故该接口暂不开放
import requests

target = 'http://yao.qinse.top/proxy_key.txt'

resp = requests.get(target, timeout=2)

# 状态码
print(resp.status_code)

# 代理IP
print(resp.text)
