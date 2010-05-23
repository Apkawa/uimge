# -*- coding: utf-8 -*-
import base
class Host(base.BaseHost):
    short_key ='k'
    long_key = 'imageshack'

    host='imageshack.us'
    action = 'http://post.imageshack.us/'
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
        '''
        http://img413.imageshack.us/img413/2970/20281668.th.png
        [IMG]http://img571.imageshack.us/img571/2408/40074625.png[/IMG][/URL]
        '''
        url=self.findall('\]\[IMG\](http://img.[\d]+?.imageshack.us/img[\d]+?/.*?/.*?)\[/IMG\]\[/URL\]', _src )
        tumburl=url[0].split('.')
        tumburl.insert(-1,'th')
        self.img_url = url[0]
        self.img_thumb_url = '.'.join(tumburl)

if __name__ == '__main__':
    h= Host()
    h.test_file()
    h.test_url()
