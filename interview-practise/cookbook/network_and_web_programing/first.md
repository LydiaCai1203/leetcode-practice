# 作为客户端与HTTP服务交互

### 一、urllib

```python
from urllib import request, parse

url_get = 'http://httpbin.org/get'
url_post = 'http://httpbin.org/post'

headers = {
    'User-agent' : 'none/ofyourbusiness',
    'Spam' : 'Eggs'
}

parms = {
    'name1': 'value1',
    'name2': 'value2',
}

def get():
    querystring = parse.urlencode(parms)
    u = request.urlopen(url + '?' + querystring, headers=headers)
    resp = u.read()
    print(resp)

def post():
    querystring = parse.urlencode(parms)
    u = request.urlopen(url, querystring.encode('ascii'),headers=headers)
    resp = u.read()
    print(resp)

```



##### 二、requests

```python
import requests

resp = requests.head('http://www.python.org/index.html')

status = resp.status_code
last_modified = resp.headers['last-modified']
content_type = resp.headers['content-type']
content_length = resp.headers['content-length']

# ------------------------
resp = requests.get('http://pypi.python.org/pypi?:action=login',
                    auth=('user','password'))

# ------------------------                    
resp1 = requests.get(url)
# Second requests with cookies received on first requests
resp2 = requests.get(url, cookies=resp1.cookies)

# ------------------------
import requests
url = 'http://httpbin.org/post'
files = { 'file': ('data.csv', open('data.csv', 'rb')) }

r = requests.post(url, files=files)
```

##### 最后

+ urllib 仅仅能发出 GET 和 POST 请求。

+ 使用 http.client 可以实现 HEAD 请求或是其它。

+ 如果请求设计proxy、auth、cookies，还是建议使用requests

```python
from http.client import HTTPConnection


c = HTTPConnection('www.python.org', 80)
c.request('HEAD', '/index.html')
resp = c.getresponse()

print('status', resp.status)
for name, value in resp.getheaders():
    print(name, value)
```

+ 最后在进行网络请求交互的时候可以现在 http://httpbin.org/get 上进行实验交互，这个站点会接收和发出请求，然后以 JSON 的形式将信息传回来。


























































































