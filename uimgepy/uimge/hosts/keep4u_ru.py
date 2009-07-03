# -*- coding: utf-8 -*-
from base_host import test_host, findall
@test_host(__name__)
class Host_k4_keep4u:
    host='keep4u.ru'
    action = 'http://keep4u.ru/'
    form = {
            'disable_effects':'on',
            'preview':'yes',
            'sbmt':'',
            'Submit': '',
            }
    def as_file(self, _file):
        return {'pfile': _file }
    def thumb_size(self, _thumb_size):
        return { 'preview_size': _thumb_size, }
    def postload(self ):
        _src =  self.get_src()
        _url = findall( 'value=\"\[img\]http://keep4u.ru/imgs/b/(.*?)\[/img\]\"', _src)[0]
        self.img_url = 'http://keep4u.ru/imgs/b/%s'%_url
        self.img_thumb_url = 'http://keep4u.ru/imgs/s/%s'%_url 

