# -*- coding: utf-8 -*-
from base_host import test_host, findall
#@test_host(__name__)
class Host_k_imageshack:
    host='imageshack.us'
    action = 'http://imageshack.us/'
    form = {'uploadtype': 'on', 'Submit':'"host it!"'}
    def __init__(self):
        self.ihost={\
           'host':'imageshack.us', \
           'post':'/', \
           'cookie':''\
           }
    def as_file(self,_file):
        return {'fileupload': _file }
    def postload(self):
        url=findall('value=\"(http://img.[\d]+?.imageshack.us/img[\d]+?/.*?/.*?)\"', self.get_src() )
        tumburl=url[0].split('.')
        tumburl.insert(-1,'th')
        self.img_url = url[0]
        self.img_thumb_url = '.'.join(tumburl)
