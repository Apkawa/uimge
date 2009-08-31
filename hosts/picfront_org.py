# -*- coding: utf-8 -*-
from base_host import *
class Host(BaseHost):
    short_key = 'pf'
    long_key  = 'picfront'
    host='picfront.org'
    action = 'http://www12.picfront.org/index.php'
    form = {
'SID':'038523eb60ad58d45fc5223130ccc406',
'HOST_WWW':'0',
'HOST_END':'org',
'UPLOAD_IDENTIFIER':'13379733361246536683',
'x':'30',
'y':'23',
'resize_x':'',
'resize_y':'',
'branding_image':'filename="" Content-Type: application/octet-stream',
'branding_urlimage':'',
'branding_text':'',
'rotate':'',
'mirror':'',
'colormode_do':'1',
'camerashakestep':'1',
'folder':'0',
'urlimage':'',
            'thumbbar':'1',
            'Submit': '',
            }

    def as_file(self, _file):
        return {'file_0': _file }
   # def as_url(self, _url):
  #      return {
    #        'file_0':'filename="" Content-Type: application/octet-stream',
 #           'urluploadfile_0': _url}
    def postload(self ):
        _src = self.get_geturl()
        _regx = r'http://picfront.org/uploaded.php\?images=(.*)'
        _url = findall(_regx ,_src)[0]
        self.img_url = 'http://www12.picfront.org/picture/%s/img/%s'%(_url, self.get_filename() )
        self.img_thumb_url = 'http://www12.picfront.org/picture/%s/thb/%s'%(_url, self.get_filename() )



if __name__ == '__main__':
    h= Host()
    h.test_file()
    h.test_url()
