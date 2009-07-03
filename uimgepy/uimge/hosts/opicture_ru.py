# -*- coding: utf-8 -*-
from base_host import test_host, findall
@test_host(__name__)
class Host_o_opicture:
    host='opicture.ru'
    action = 'http://opicture.ru/upload/?api=true'
    form = {
                'preview':	'on',
                'information':'on',
                'action':'upload',
                }
    def as_file(self, _file):
        return {'type': '1' ,'file[]': _file } 
    def as_url(self, _url):
        return {'type': '2' ,'link[]': _url } 
    def thumb_size(self, _thumb_size):
        return { 'previewwidth': _thumb_size, }
    def postload(self):
        from xml.dom import minidom
        src = self.get_src()
        _xml = minidom.parseString(src)
        self.img_url = _xml.getElementsByTagName('image')[0].firstChild.data
        self.img_thumb_url =  _xml.getElementsByTagName('preview')[0].firstChild.data

        #__url = findall('showTags\(.*?\'([\d]{4}/[\d]{2}/[\d]{2}/[\d]{2}/[\d]{10,}\.[\w]{2,4})\'',  )
        #self.img_url = 'http://opicture.ru/upload/%s'% __url[0]
        #self.img_thumb_url = 'http://opicture.ru/picture/thumbs/%s.jpg'% ''.join( __url[0].split('.')[:-1])

