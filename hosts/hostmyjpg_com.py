# -*- coding: utf-8 -*-
import base
#@test_host(__name__)
class Host(base.BaseHost):
    short_key = 'hm'
    long_key  = 'hostmyjpg'
    host='hostmyjpg.com'
    action = 'http://www.hostmyjpg.com/'
    form = {
            'page':'upload',
            'types':'0',
            'upload':'Host Them !',
            'Submit': '',
            }

    def as_file(self, _file):
        return {'userfile0': _file }
    def postload(self ):
        _src = self.get_src()

        __url = self.findall('\[IMG\]http://img.hostmyjpg.com/(.*?)\[/IMG\]',  _src )[0]
        self.img_url = 'http://img.hostmyjpg.com/%s'%__url
        self.img_thumb_url = 'http://www.hostmyjpg.com/thumbs/%s'%__url



if __name__ == '__main__':
    h= Host()
    h.test_file()
    h.test_url()
