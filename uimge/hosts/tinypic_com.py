# -*- coding: utf-8 -*-
import base
class Host(base.BaseHost):
    dev_mode = True
    max_file_size = 500000000
    short_key = 'tp'
    long_key  = 'tinypic'
    host='tinypic.com'
    action = 'http://s4.tinypic.com/upload.php'
    form = {
            'domain_lang':'en',
            'shareopt':'true',
            'description':'uimge',
            'file_type':'image',
            'dimension':'1600',
            'video-settings':'sd',
            'addresses':'',
            'MAX_FILE_SIZE': '500000000',
            'Submit': '',
            'action': 'upload'}

    '''
        UPLOAD_IDENTIFIER	622239671_1251574634
    upk	3862249602835fdd94c0dc4ec94508a5
    domain_lang	en
    action	upload
    MAX_FILE_SIZE	500000000
    shareopt	true
    the_file	filename="qr.png" Content-Type: image/png
    url	
    description	
    file_type	image
    dimension	1600
    video-settings	sd
    addresses
    '''
    def as_file(self, _file):
        return {'the_file': _file}
    def as_url(self, _url):
        return {'url':_url}
    def preload(self):
        import urllib
        uop = urllib.urlopen( 'http://%s'%self.host)

        print uop.headers.headers
        __src = uop.read()
        print __src
        __form = {
            'UPLOAD_IDENTIFIER': self.findall('name="UPLOAD_IDENTIFIER" id="uid" value="(.*?)"',__src)[0] ,
            'upk': self.findall( 'name="upk" value="(.*?)"', __src)[0],
            }
        self.action = self.findall('<form action="(http://s\d.tinypic.com/upload.php)"',__src)[0]
        self.form.update( __form)
    def postload(self):
        __src = self.response.body
        print __src
        key = dict( self.findall('name="(pic|ival)" value="(.*?)"', __src))
        key.update( {'type': self.get_filename( splitext=True )[1]})
        self.img_url = 'http://i%(ival)s.tinypic.com/%(pic)s%(type)s'%(key)
        self.img_thumb_url = 'http://i%(ival)s.tinypic.com/%(pic)s_th%(type)s'%( key)

if __name__ == '__main__':
    h= Host()
    h.test_file()
    h.test_url()
