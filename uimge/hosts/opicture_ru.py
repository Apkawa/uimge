# -*- coding: utf-8 -*-
import base
class Host(base.BaseHost):
    dev_mode = True
    short_key = 'o'
    long_key  = 'opicture'
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
        src = self.response.body
        _xml = minidom.parseString(src)
        self.img_url = _xml.getElementsByTagName('image')[0].firstChild.data
        self.img_thumb_url =  _xml.getElementsByTagName('preview')[0].firstChild.data

        #__url = self.findall('showTags\(.*?\'([\d]{4}/[\d]{2}/[\d]{2}/[\d]{2}/[\d]{10,}\.[\w]{2,4})\'',  )
        #self.img_url = 'http://opicture.ru/upload/%s'% __url[0]
        #self.img_thumb_url = 'http://opicture.ru/picture/thumbs/%s.jpg'% ''.join( __url[0].split('.')[:-1])




if __name__ == '__main__':
    h= Host()
    h.test_file()
    h.test_url()
