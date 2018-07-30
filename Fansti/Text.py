from HTMLParser import HTMLParser
class MyHTMLParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.text = []

    def handle_data(self, data):
        self.text.append(data.decode("gbk").encode("utf8"))
try:
    import urllib2
    url = "http://www.ichemistry.cn/chemistry/{0}.htm".format("7664-93-9")
    headers = {'Content-Type': 'application/xml'}
    req = urllib2.Request(url, headers=headers)
    print(1)
    url_response = urllib2.urlopen(req)
    print(1)
    strResult = url_response.read()
    print(1)
    parser = MyHTMLParser()
    parser.feed(strResult)
    length = len(parser.text)
    print(parser.text)
except Exception as e:
    print e.message

