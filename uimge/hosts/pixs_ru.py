# -*- coding: utf-8 -*-
import base
class Host( base.BaseHost ):
    dev_mode = False

    short_key = 'px'
    long_key = 'pixs'
    host='pixs.ru'
    max_file_size = 4*(1024*1024) #5Mb

    action = 'http://%s/redirects/upload.php'%host

    #headers = {}
    #user_agent = "string"

    form = {
            'title':'uimge',
            'private_code':'',
            'img_width':'80000',
            'img_height':'80000',
            'btn_submit':'Загрузить',
            }

    def as_file(self, _file):
        return {
                'userfile': _file,
                }

    def postload(self ):
        _src = self.response.body
        _regx = r'\[IMG\]http://img.pixs.ru/storage/([\d]/[\d]/[\d]/[\w.]+?)\.[\w]{2,4}\[/IMG\]'
        _url = self.findall(_regx ,_src)[0]
        self.img_url = 'http://img.pixs.ru/storage/%s%s'%(_url, self.get_filename(splitext=True)[1] )
        self.img_thumb_url = 'http://img.pixs.ru/thumbs/%s.jpg'%_url

if __name__ == '__main__':
    h= Host()
    h.test_file()
    h.test_url()
