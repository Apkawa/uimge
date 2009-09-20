# -*- coding: utf-8 -*-
import base
#@test_host(__name__)

class Host( base.BaseHost ):
    short_key = 'u'
    long_key  = 'funkyimg'
    host='funkyimg.com'
    action = 'http://funkyimg.com/up.php'
    form = {
            'addInfo': 'on',
            'maxId': '2',
            'maxNumber': '2',
            'upload': '"Upload Images"',
            }
    def as_file(self, _file):
        return {
                'uptype': 'file',
                'file_1':_file,}
    def as_url(self, _url):
        return {
                'uptype': 'url',
                'url':'',
                'url_1':_url,
                }
    def postload(self):
        __url=self.findall('\[IMG\](http://funkyimg.com/.*)\[/IMG\]\[/URL\]', self.response.body )
        __url.reverse()
        self.img_url= __url[0]
        self.img_thumb_url = __url[1]



if __name__ == '__main__':
    h= Host()
    h.test_file()
    h.test_url()
