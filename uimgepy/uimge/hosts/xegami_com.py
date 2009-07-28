# -*- coding: utf-8 -*-
from base_host import test_host, findall
#@test_host(__name__)
class Host_xe_xegami:
    host='xegami.com'
    action = 'http://%s/upload.php'%host
    form = {
            'description_a':'checked',
            'description':'uimge',
            'password':'',
            'Submit': '',
            }

    def as_file(self, _file):
        return {'upload_image': _file }
    def postload(self ):
        _src = self.get_src()
        _regx = r'img src=\"http://xegami.com/thumbs/(.+?)\"'
        _url = findall(_regx ,_src)[0]
        self.img_url = 'http://xegami.com/uploads/%s'%_url
        self.img_thumb_url = 'http://xegami.com/thumbs/%s'%_url

