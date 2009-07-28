# -*- coding: utf-8 -*-
from base_host import test_host, findall
#@test_host(__name__)
class Host_i_ipicture:
    host='ipicture.ru'
    action = 'http://ipicture.ru/Upload/'
    form = {
            'thumb_resize_on':'on',
            'ramka_off':'on',
            'ignorAllCheck':'on',
            'submit':'"Загрузить"',
            }
    '''
    POST /api HTTP/1.1
User-Agent: iPicture ImageUploader
Accept: text/html
Content-Type: multipart/form-data; boundary=995997794
Host: ipicture.ru
Content-Length: 830394
Expect: 100-continue
Connection: Keep-Alive


    '''
    def as_file(self, _file):
        #self.action = 'http://ipicture.ru/api/'
        return {
            'uploadtype':'1',
            'method':'file',
            'file':'upload',
            'userfile': _file
            }
    def as_url(self, _url):
            return {
            'uploadtype':'2',
            'method':'url',
            'userurl[]': _url
            }
    def thumb_size(self, _thumb_size):
        return {'thumb_resize':_thumb_size,}
    def postload(self):
        from urllib import urlopen
        __reurl=findall('(http://.*.html)', self.get_headers()[-1])
        __url=findall('\[IMG\](http://.*)\[\/IMG\]', urlopen(__reurl[0]).read())
        self.img_url= __url[0]
        self.img_thumb_url = __url[2]
        '''
        else:
            _src = self.get_src()
            print _src
            self.img_url, self.img_thumb_url = findall('<(?:image|thumb)path>(.*?)</(?:image|thumb)path>', _src )
        '''



