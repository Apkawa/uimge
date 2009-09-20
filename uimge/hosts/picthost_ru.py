# -*- coding: utf-8 -*-
import base
class Host:
    dev_mode = True
    short_key = 'p'
    long_key  = 'picthost'
    host='picthost.ru'
    action = 'http://picthost.ru/upload.php'
    form = {'private_upload': '1', 'upload': '"Upload Images"', }
    def as_file(self, _file):
        return {'userfile[]': _file}
    def as_url(self, _url):
        action = 'http://picthost.ru/upload.php?url=1'
        return {'userfile[]': _url}
    def postload(self):
        src = self.response.body
        print src
        url=self.findall('\<a href=\"viewer.php\?file=(.*?)\"',  src)

        t = 'http://picthost.ru/images/'
        tumburl=url[0].split('.')
        tumburl[-2] += '_thumb'
        tumburl = '.'.join(tumburl)
        self.img_url = t+url[0]
        self.img_thumb_url = t+tumburl



if __name__ == '__main__':
    h= Host()
    h.test_file()
    h.test_url()
