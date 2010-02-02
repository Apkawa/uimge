# -*- coding: utf-8 -*-
import base
class Host(base.BaseHost):
    dev_mode = True
    short_key = 'xe'
    long_key  = 'xegami'
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
        _src = self.response.body
        _regx = r'img src=\"http://xegami.com/thumbs/(.+?)\"'
        _url = self.findall(_regx ,_src)[0]
        self.img_url = 'http://xegami.com/uploads/%s'%_url
        self.img_thumb_url = 'http://xegami.com/thumbs/%s'%_url




if __name__ == '__main__':
    h= Host()
    h.test_file()
    h.test_url()
