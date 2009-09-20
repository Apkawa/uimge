# -*- coding: utf-8 -*-
import base
class Host(base.BaseHost):
    short_key = 'ib'
    long_key  = 'imgby'
    host='imgby.com'
    action = 'http://%s/'%host
    form = {
            'remota':'',
            'resize':'',
            'x':'147',
            'y':'48',
            'Submit': '',
            }

    def as_file(self, _file):
        return {'fileup': _file }
    def postload(self ):
        _src = self.response.body
        _regx = r'\[img\]http://imgby.com/thumbs/(.+?)\[/img\]'
        _url = self.findall(_regx ,_src)[0]
        self.img_url = 'http://imgby.com/%s'%_url
        self.img_thumb_url = 'http://imgby.com/thumbs/%s'%_url





if __name__ == '__main__':
    h= Host()
    h.test_file()
    h.test_url()
