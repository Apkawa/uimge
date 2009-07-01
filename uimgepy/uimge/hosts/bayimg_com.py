# -*- coding: utf-8 -*-
from base_host import test_host, findall
def test(host):
    if __name__ == '__main__':
        test_host( host)
@test
class Host_ba_bayimg:
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
        _url = findall(_regx ,_src)[0]
        self.img_url = 'http://bayimg.com/image/%s'%_url
        self.img_thumb_url = 'http://bayimg.com/thumb/%s'%_url
