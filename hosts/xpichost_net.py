# -*- coding: utf-8 -*-
import base
class Host(base.BaseHost):
    dev_mode = False
    short_key = 'xp'
    long_key  = 'xpichost'
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
        _src = self.response.body
        _regx = r'\[img\]http://xpichost.net/pic_s/(.*?).jpg\[/img\]'
        _url = self.findall(_regx ,_src)[0]
        filename = self.get_filename(splitext=True)[1]
        self.img_url = 'http://xpichost.net/pic_b/%s%s'%(_url, filename )
        self.img_thumb_url = 'http://xpichost.net/pic_s/%s.jpg'%_url

if __name__ == '__main__':
    h= Host()
    h.test_file()
    h.test_url()

