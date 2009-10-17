# -*- coding: utf-8 -*-
import base
class Host( base.BaseHost ):
    short_key = 'r'
    long_key  = 'radikal'
    key = { 'short':'r','long':'radikal' }

    host = 'radikal.ru'
    #action = 'http://www.radikal.ru/action.aspx' 
    #action = 'http://www.radikal.ru/fotodesktop/PostImgH.ashx' 
    action = ''
    form = {
                'CP': 'yes',
                'Submit': '',
                'upload': 'yes'
                }
    def as_file(self, _file):
        self.url = False
        self.action = 'http://www.radikal.ru/fotodesktop/PostImgH.ashx'
        return {'F': _file }
    def as_url(self, _url):
        self.url = True
        self.action = 'http://www.radikal.ru/action.aspx'
        return {'URLF': _url }
    def thumb_size(self, _thumb_size):
        return { 'VM': _thumb_size, }

    def postload(self):
        _src = self.response.body
        if self.url:
            __url = self.findall('\[IMG\](http://.*.radikal.ru.*)\[/IMG\]', _src )
            self.img_url = __url[0]
            self.img_thumb_url =  __url[1]
        else:
            from xml.dom import minidom
            from xml.parsers.expat import ExpatError

            try:
                _xml = minidom.parseString( _src )
            except ExpatError:
                self.error()

            self.img_url = _xml.getElementsByTagName('rurl')[0].firstChild.data
            self.img_thumb_url =  _xml.getElementsByTagName('rurlt')[0].firstChild.data

if __name__ == '__main__':
    h= Host()
    h.test_file()
    h.test_url()
