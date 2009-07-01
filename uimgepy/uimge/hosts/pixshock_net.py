# -*- coding: utf-8 -*-
from base_host import test_host, findall
@test_host(__name__)
class __Host_ex_example:
    host='pixshock.net'
    action = 'http://%s/upfile.html'%host
    form = {
            'MAX_FILE_SIZE':'10000000',
            'title1':'uimge',
            'smallsize1':'640',
            'catname':'1',
            'Submit': '',
            }

    def as_file(self, _file):
        return {'apic1': _file }
    def as_url(self, _url):
        return {'apic1': _url}
    def thumb_size(self, _thumb_size):
        return { 'size1': _thumb_size, }
    def postload(self ):
        _src = self.get_src()
#http://www.pixshock.net/pic_b/280a9fb689f39a13f1c3217e6634a486.png
        _regx = r'\[img\]http://www.pixshock.net/pic_b/(.*)\[/img\]'
        _url = findall(_regx ,_src)[0]
        self.img_url = 'http://www.pixshock.net/pic_b/%s'%_url
        self.img_thumb_url = 'http://www.pixshock.net/pic_b/%s'%_url
