import requests

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:32.0) Gecko/20100101 Firefox/32.0"}
# r = requests.head("http://www.baidu.com", headers=headers)
r = requests.head("http://www.qq.com", headers=headers)
print(r.headers)
# {'Cache-Control': 'private, no-cache, no-store, proxy-revalidate, no-transform', 'Connection': 'keep-alive', 'Content-Type': 'text/html', 'Date': 'Fri, 11 Jun 2021 17:27:53 GMT', 'Last-Modified': 'Mon, 13 Jun 2016 02:50:21 GMT', 'Pragma': 'no-cache', 'Server': 'bfe/1.0.8.18'}
# {'Cache-Control': 'private, no-cache, no-store, proxy-revalidate, no-transform', 'Content-Encoding': 'gzip', 'Content-Type': 'text/html', 'Date': 'Fri, 11 Jun 2021 17:30:49 GMT', 'Last-Modified': 'Mon, 13 Jun 2016 02:50:26 GMT', 'Pragma': 'no-cache', 'Server': 'bfe/1.0.8.18', 'Connection': 'keep-alive'}
# {'Server': 'ias/1.3.5.6_1.17.3', 'Date': 'Fri, 11 Jun 2021 17:31:19 GMT', 'Content-Type': 'text/html', 'Content-Length': '151', 'Location': 'https://www.qq.com/', 'Connection': 'keep-alive'}
