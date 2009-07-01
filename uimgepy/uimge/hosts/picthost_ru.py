# -*- coding: utf-8 -*-
from base_host import test_host, findall
@test_host(__name__)
class Host_p_picthost:
    host='picthost.ru'
    action = 'http://picthost.ru/upload.php'
    form = {'private_upload': '1', 'upload': '"Upload Images"', }
    def as_file(self, _file):
        return {'userfile[]': _file}
    def as_url(self, _url):
        action = 'http://picthost.ru/upload.php?url=1'
        return {'userfile[]': _url}
    def postload(self):
        url=findall('\<a href=\"viewer.php\?file=(.*?)\"', self.get_src() )

        t = 'http://picthost.ru/images/'
        tumburl=url[0].split('.')
        tumburl[-2] += '_thumb'
        tumburl = '.'.join(tumburl)
        self.img_url = t+url[0]
        self.img_thumb_url = t+tumburl
