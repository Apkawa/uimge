# -*- coding: utf-8 -*-
import base
class Host( base.BaseHost ):
    short_key = 'ba'
    long_key  = 'bayimg'
    host='bayimg.com'
    action = 'http://upload.%s/upload'%host
    form = {
            'code':'666',
            'tags':'guimge',
            'Submit': '',
            }

    def as_file(self, _file):
        return {'file': _file }
    def postload(self ):
        _src = self.get_src()
        _regx = r'img src="http://bayimg.com/thumb/(.+?)"'
        _url = self.findall(_regx ,_src)[0]
        self.img_url = 'http://bayimg.com/image/%s'%_url
        self.img_thumb_url = 'http://bayimg.com/thumb/%s'%_url

if __name__ == '__main__':
    h= Host()
    h.test_file()
    h.test_url()
