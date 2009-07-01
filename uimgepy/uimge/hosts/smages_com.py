# -*- coding: utf-8 -*-
from base_host import test_host, findall
class Host_s_smages:
    host='smages.com'
    action = 'http://smages.com/upload'
    form = {'Submit': ''}

    def as_file(self, _file):
        return {'img': _file }
    def postload(self ):
        __url = findall('src=\'http://smages.com/i/(.*?).([\w]{2,4})\'', self.get_src() )[0]
        self.img_url = 'http://smages.com/i/%s.%s'%(__url[0], __url[1])
        self.img_thumb_url = 'http://smages.com/t/%s.jpg'%__url[0]
if __name__ == '__main__':
    test_host( Host_r_radikal )
