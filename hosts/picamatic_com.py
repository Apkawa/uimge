# -*- coding: utf-8 -*-
from base_host import *
class Host( BaseHost):
    dev_mode = True
    max_file_size = 3145728

    short_key ='pm'
    long_key = 'picamatic'
    host='picamatic.com'
    action = 'http://www.picamatic.com/'
    form = {
            'MAX_FILE_SIZE'	:'3145728',
            'upload':'',
            'Submit': '',
            }

    def as_file(self, _file):
        return {'Filedata': _file }
    def preload(self):
        import urllib
        self.action = findall('href="(http://www.picamatic.com/.*?)"', urllib.urlopen('http://www.picamatic.com/?js&schedule').read() )[0]
    def postload(self ):
        _src =  self.get_src()
        self.img_url = findall( '"js-url-direct">(http://www.picamatic.com/show/.*?)</textarea>', _src)[0]
        self.img_thumb_url = findall('&gt;&lt;img src="(http://www.picamatic.com/show/.*?)" border="0"', _src)[0]

if __name__ == '__main__':
    h= Host()
    h.test_file()
    h.test_url()
