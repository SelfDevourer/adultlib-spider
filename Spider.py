from pyquery import PyQuery as pq


class Spider:

    def get_basic_url(self):
        return self.basic_url

    def __init__(self, basic_url):
        self.basic_url = basic_url

    def getdoc(self, url=None, path=None):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'}
        if url is not None:
            doc = pq(url=url, headers=headers)
        else:
            doc = pq(url=self.basic_url + path, headers=headers)
        return doc

    def get_page_count(self, url=None):
        if url is None:
            url = self.basic_url
        doc = self.getdoc(url=url)
        if doc('#next'):
            link = doc('.pagination-lg li:last').prev().find('a')
            return int(self.get_page_count(self.basic_url + "page/" + link.text()))
        else:
            link = doc('.pagination-lg li:last').find('a')
            return int(link.text())
