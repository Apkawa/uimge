# -*- coding: utf-8 -*-
from base_host import *
class Host(BaseHost):
    max_file_size = 2097152
    short_key = 'sp'
    long_key  = 'savepic'
    host='savepic.ru'
    action = 'http://savepic.ru/search.php'
    form = {'MAX_FILE_SIZE': '2097152',
             'email': '',
             'flip': '0',
             'font1': 'comic_bold',
             'font2': '20',
             'mini': '300x225',
             'note': '',
             'orient': 'h',
             'rotate': '00',
             'size1': '1',
             'size2': '800x600',
             'subm2': '\xc3\x8e\xc3\xb2\xc3\xaf\xc3\xb0\xc3\xa0\xc3\xa2\xc3\xa8\xc3\xb2\xc3\xbc'}
    def as_file(self, _file):
        return {'file':_file}

    def postload(self):
        reurl = findall('\"/([\d]+?).htm\"', self.get_src() )[0]
        ext ='png'#self.get_filename().split('.')[-1].lower()
        url,tmb = 'http://savepic.ru/%s.%s'%(reurl,ext),'http://savepic.ru/%sm.%s'%(reurl,ext)
        self.img_url = url
        self.img_thumb_url = tmb



if __name__ == '__main__':
    h= Host()
    h.test_file()
    h.test_url()
