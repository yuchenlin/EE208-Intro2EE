import urlparse


url1  = 'http://123123.com/asd'

url2  = 'gf1.html'

url = urlparse.urljoin(url1,url2)
print url