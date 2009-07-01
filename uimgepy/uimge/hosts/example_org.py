# -*- coding: utf-8 -*-
from base_host import test_host, findall
def test(host):
    if __name__ == '__main__':
        test_host( host)
@test
class __Host_ex_example:
    host='example.org'
    action = 'http://example.org/upload'
    form = {
            'Submit': '',
            }

    def as_file(self, _file):
        return {'image': _file }
    def as_url(self, _url):
        return {'url': _url}
    def thumb_size(self, _thumb_size):
        return { 'thumb_size': _thumb_size, }
    def postload(self ):
        _src = self.get_src()
        _regx = r'example'
        _url = findall(_regx ,_src)[0]
        self.img_url = '%s'%_url
        self.img_thumb_url = '%s'%_url
