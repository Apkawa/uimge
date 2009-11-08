# -*- coding: utf-8 -*-
import base
class Host( base.BaseHost ):
    dev_mode = False

    short_key = 'xt'
    long_key = 'xtupload'
    host='xtupload.com'
#    max_file_size =  #5Mb



    action = 'http://www.xtupload.com/new/upload.php'
    form = {
            'private':'private',
            'Submit': '',
            }

    def as_file(self, _file):
        return {
                'typ':'s',
                'f_single': _file,
                'cap_single':self.filename}
    def postload(self ):
        req = self.response.body
        req = self.findall(r'(http://www.xtupload.com/new/.+?)">', req)[0]
        self.get_html( req)
        _src = self.response.body
        _regx = r'\[img\]http://www.xtupload.com/new/thumb-([\w.]+?)\[/img\]'
        _url = self.findall(_regx ,_src)[0]
        self.img_url = 'http://www.xtupload.com/new/image-%s'%_url
        self.img_thumb_url = 'http://www.xtupload.com/new/thumb-%s'%_url

if __name__ == '__main__':
    h= Host()
    h.test_file()
    h.test_url()
