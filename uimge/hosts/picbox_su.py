# -*- coding: utf-8 -*-
import base
class Host( base.BaseHost ):
    short_key = 'pb'
    long_key = 'picbox'
    host='picbox.su'

    action = 'http://%s/upload/'%host

    form = {
            'name': 'NoName',
	    'private': '',
	    'accept': '',
            }

    def as_file(self, _file):
        return {
                'upload': _file,
                }

    def postload(self ):
        _src = self.response.body
        _url = self.findall("\[img\]http://picbox\.su/get_now/(.*?)\[/img\]" ,_src)[0]
        self.img_url = 'http://picbox.su/get_now/%s'%_url
        self.img_thumb_url = 'http://picbox.su/get_now_small/%s'%_url

if __name__ == '__main__':
    h= Host()
    h.test_file()
    h.test_url()
