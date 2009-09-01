# -*- coding: utf-8 -*-
import base
class __Host_ul_uloz:
    short_key = 'ul'
    long_key = 'uloz'

    host='uloz.to'
    action = 'http://up.uloz.to/ul/upload.cgi?tmp_sid=147a1d8f5aa41cd33b171a8c6b193493&user_id=0'
    form = {
            'Submit': '',
            }

    def as_file(self, _file):
        return {'upfile_0': _file }
    def thumb_size(self, _thumb_size):
        return { 'thumb_size': _thumb_size, }
    def preload(self):
        'enctype="multipart/form-data"  action="http://up.uloz.to/ul/upload.cgi?tmp_sid=147a1d8f5aa41cd33b171a8c6b193493&user_id=0"'
    def postload(self ):
        _src = self.get_src(True)
        _regx = r'example'
        _url = self.findall(_regx ,_src)[0]
        self.img_url = '%s'%_url
        self.img_thumb_url = '%s'%_url

if __name__ == '__main__':
    h= Host()
    h.test_file()
    h.test_url()
