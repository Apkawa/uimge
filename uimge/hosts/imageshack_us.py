# -*- coding: utf-8 -*-
import base
class Host(base.BaseHost):
    short_key ='k'
    long_key = 'imageshack'

    host='imageshack.us'
    action = 'http://imageshack.us/'
    form = {
            'uploadtype': 'on',
            'Submit':'"host it!"'
            }
    max_file_size = 13145728 #13 Mb

    def as_file(self,_file):
        return {'fileupload': _file }
#    def as_url(self,_file):
#        action = 'http://www.imageshack.us/transload.php'
#        return {'url': _file }
    def postload(self):
        _src = self.response.body
        url=self.findall('value=\"(http://img.[\d]+?.imageshack.us/img[\d]+?/.*?/.*?)\"', _src )
        tumburl=url[0].split('.')
        tumburl.insert(-1,'th')
        self.img_url = url[0]
        self.img_thumb_url = '.'.join(tumburl)

if __name__ == '__main__':
    h= Host()
    h.test_file()
    h.test_url()
