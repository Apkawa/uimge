# -*- coding: utf-8 -*-
import base
class Host( base.BaseHost ):
    dev_mode = False

    short_key = 'al'
    long_key = 'anime-last'
    host='sun.anime-last.info'
    max_file_size = 3145728 #3Mb

    action = 'http://sun.anime-last.info/basic.php'
    form = {
            'MAX_FILE_SIZE':'3145728',
            'refer':'',
            'upload':'Загрузить!',
            }

    def as_file(self, _file):
        return {'userfile': _file }
    def postload(self ):
        _src = self.response.body
        _regx = r'\[img\]http://sun.anime-last.info/images/([\w.]+?)\[/img\]'
        _url = self.findall(_regx ,_src)[0]
        self.img_url = 'http://sun.anime-last.info/images/%s'%_url
        self.img_thumb_url = 'http://sun.anime-last.info/thumbs/%s'%_url

if __name__ == '__main__':
    h= Host()
    h.test_file()
    h.test_url()
