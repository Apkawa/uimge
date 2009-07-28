# -*- coding: utf-8 -*-
from base_host import test_host, findall
#@test_host(__name__)
class Host_xp_xpichost:
    host='xpichost.net'
    action = 'http://xpichost.net/upload_file.php'
    form = {
        'Submit':'Залить',
        'title':'uimge',
        'gall_id':'0'
            }

    def as_file(self, _file):
        return {'apic': _file }
    def as_url(self, _url):
        return {'url': _url}
    def thumb_size(self, _thumb_size):
        return { 'thsize': _thumb_size, }
    def postload(self ):
        _src = self.get_src()
        _regx = r'\[img\]http://xpichost.net/pic_s/(.*?).jpg\[/img\]'
        _url = findall(_regx ,_src)[0]
        self.img_url = 'http://xpichost.net/pic_b/%s%s'%(_url,self.get_filename(split=True)[1] )
        self.img_thumb_url = 'http://xpichost.net/pic_s/%s.jpg'%_url
