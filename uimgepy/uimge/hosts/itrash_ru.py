# -*- coding: utf-8 -*-
from base_host import test_host, findall
@test_host(__name__)
class Host_it_itrash:
    host='itrash.ru'
    action = 'http://itrash.ru/module/ib_news/ibn_processor.ajax.php?JsHttpRequest=12466100369162-form'
    form = {
            'type':'upload',
            'Submit': '',
            }

    def as_file(self, _file):
        return {'file': _file , '""':self.get_filename() }
    def postload(self ):
        _src = self.get_src()
        _regx = r'href=\\"http:\\/\\/itrash.ru\\/idb\\/(.*?)\\/o(.*?).html\\"'
        _url = findall(_regx ,_src,)[0]
        self.img_url = 'http://itrash.ru/idb/%s/o%s'%(_url)
        self.img_thumb_url = 'http://itrash.ru/idb/%s/t%s'% (_url)
