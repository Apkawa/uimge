# -*- coding: utf-8 -*-
from base_host import test_host, findall
@test_host(__name__)
class Host_tp_tinypic:
    host='tinypic.com'
    action = 'http://s5.tinypic.com/upload.php'
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
    def as_file(self, _file):
        return {'the_file': _file} 
    def preload(self):
        import urllib
        __src = urllib.urlopen( 'http://%s'%self.host).read()
        __form = {
            'UPLOAD_IDENTIFIER': findall('name="UPLOAD_IDENTIFIER" id="uid" value="(.*?)"',__src)[0] ,
            'upk': findall( 'name="upk" value="(.*?)"', __src)[0],
            }
        self.form.update( __form)
    def postload(self):
        __src = self.get_src()
        key = dict( findall('name="(pic|ival|type)" value="(.*?)"', __src))
        self.img_url = 'http://i%(ival)s.tinypic.com/%(pic)s%(type)s'%(key)
        self.img_thumb_url = 'http://i%(ival)s.tinypic.com/%(pic)s_th%(type)s'%( key)
