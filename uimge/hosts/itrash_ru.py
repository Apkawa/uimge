# -*- coding: utf-8 -*-
import base
#TODO FIX
class Host(base.BaseHost):
    short_key = 'it'
    long_key  = 'itrash'
    host='itrash.ru'
    '''
    action = 'http://itrash.ru/module/ib_news/ibn_processor.ajax.php?JsHttpRequest=12466100369162-form'
    form = {
            'type':'upload',
            'Submit': '',
            }
    '''
    action = 'http://itrash.ru/loader/cmd.php'
    form ={
            'command':'send',
            'client_code':'iTL10',
            'passkey':'',
            }

    def as_file(self, _file):
        return {'file': _file , '""':self.get_filename() }

    def postload(self ):
        _src = self.response.body
        _regx = r'<item_path>db/([\w]+?)/</item_path>[\s]+<item_image>([\w.]+?)</item_image>'
        _url = self.findall(_regx ,_src,)[0]
        self.img_url = 'http://itrash.ru/idb/%s/o%s'%(_url)
        self.img_thumb_url = 'http://itrash.ru/idb/%s/t%s'% (_url)



if __name__ == '__main__':
    h= Host()
    h.test_file()
    h.test_url()
