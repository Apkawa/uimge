# -*- coding: utf-8 -*-
import base
#@test_host(__name__)
class Host(base.BaseHost):
    short_key = 'om'
    long_key  = 'omploader'
    host='ompldr.org'
    action = 'http://%s/upload'%host
    form = {
            'submit': '',
            }

    def as_file(self, _file):
        return { 'file1': _file }
    #def as_url(self, _url):
    #    return { 'url1': _url }
    def postload(self ):
        _src = self.response.body
        __url = self.findall('\[img\]http://ompldr.org/t(.*?)\[/img\]',  _src )[0]
        self.img_url = 'http://ompldr.org/v%s'%__url
        self.img_thumb_url = 'http://ompldr.org/t%s'%__url



if __name__ == '__main__':
    h= Host()
    h.test_file()
    h.test_url()
