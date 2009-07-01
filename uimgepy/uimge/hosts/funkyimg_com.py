# -*- coding: utf-8 -*-
from base_host import test_host, findall

class Host_u_funkyimg:
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
        __url=findall('\[IMG\](http://funkyimg.com/.*)\[/IMG\]\[/URL\]', self.get_src() )
        __url.reverse()
        self.img_url= __url[0]
        self.img_thumb_url = __url[1]



if __name__ == '__main__':
    test_host( Host_r_radikal )
