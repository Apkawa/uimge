# -*- coding: utf-8 -*-
import base
class Host( base.BaseHost ):
    short_key = 'iu'
    long_key = 'imageup'
    host='imageup.ru'

    action = 'http://%s/'%host

    form = {
            'comment': '',
            }

    def as_file(self, _file):
        return {
                'file': _file,
                }

    def postload(self ):
        _src = self.response.body
        _url = self.findall("\[IMG\]http://www.imageup.ru/(.*?)\[/IMG\]" ,_src)[1]
	_thumb = self.findall("\[IMG\]http://www.imageup.ru/(.*?)\[/IMG\]" ,_src)[0]
        self.img_url = 'http://www.imageup.ru/%s'%_url
        self.img_thumb_url = 'http://www.imageup.ru/%s'%_thumb

if __name__ == '__main__':
    h= Host()
    h.test_file()
    h.test_url()
