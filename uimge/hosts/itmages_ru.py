# -*- coding: utf-8 -*-
import base
#@test_host(__name__)
class Host(base.BaseHost):
    #TODO fix CSRF
    dev_mode = True
    short_key = 'im'
    long_key  = 'itmages'
    host='itmages.ru'
    action = 'http://%s/add'%host
    form = {
            'submit': '',
            }

    def as_file(self, _file):
        return {'img': _file }

    def preload(self):
        resp = self.get_html('http://%s'%self.host)
        print resp.body
        token = self.findall(r'value="(\w+)" name="token"', resp.body)[0]
        print token

    def postload(self):
        _src = self.response.body
        __url = self.findall('\[img\]http://itmages.ru/src/view/(.*?)\[/img\]',  _src )[0]
        self.img_url = 'http://itmages.ru/src/view/%s'%__url
        self.img_thumb_url = 'http://itmages.ru/src/preview/%s'%__url



if __name__ == '__main__':
    h= Host()
    h.test_file()
    h.test_url()
