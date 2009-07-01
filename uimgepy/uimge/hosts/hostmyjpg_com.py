# -*- coding: utf-8 -*-
from base_host import test_host, findall
@test_host(__name__)
class Host_hm_hostmyjpg:
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

        __url = findall('\[IMG\]http://img.hostmyjpg.com/(.*?)\[/IMG\]',  _src )[0]
        self.img_url = 'http://img.hostmyjpg.com/%s'%__url
        self.img_thumb_url = 'http://www.hostmyjpg.com/thumbs/%s'%__url
