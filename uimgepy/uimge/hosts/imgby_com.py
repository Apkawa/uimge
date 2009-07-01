# -*- coding: utf-8 -*-
from base_host import test_host, findall
def test(host):
    if __name__ == '__main__':
        test_host( host)
@test
class Host_ib_imgby:
    host='imgby.com'
    action = 'http://%s/'%host
    form = {
            'remota':'',
            'resize':'',
            'x':'49',
            'y':'21',
            'Submit': '',
            }

    def as_file(self, _file):
        return {'fileup': _file }
    def postload(self ):
        _src = self.get_src()
        _regx = r'\[img\]http://imgby.com/thumbs/(.+?)\[/img\]'
        _url = findall(_regx ,_src)[0]
        self.img_url = 'http://imgby.com/%s'%_url
        self.img_thumb_url = 'http://imgby.com/thumbs/%s'%_url


