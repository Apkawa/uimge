# -*- coding: utf-8 -*-
import base
import json
import urllib

class Host(base.BaseHost):
    max_file_size = 10485760
    short_key = 'pu'
    long_key  = 'pikucha'
    host='pikucha.ru'
    action = 'http://pikucha.ru/api?object=image&action=upload'


    #cookie = 'SID=5237d3ed3061bee49511681fb9d7a1cb'
    form = {
            'MAX_FILE_SIZE':'10485760',
            'album':'',
            'album_name':'',
            'description':'',
            'description_value':'uimge',
            'thumbnail_dimension':'180',
            'thumbnail_size':'0',
            'thumbnail_text':'',
            'rotate':'',
            #'json_tag':'1',
            'Submit': '',
            }

    def as_file(self, _file):
        return {
                'files[]': _file 
                }
    def preload(self):
        cookie = urllib.urlopen('http://%s/api?object=user&action=create'%self.host).headers['set-cookie']
        self.cookie = cookie

    def postload(self):
        _src = self.response.body
        result = json.loads(_src)
        d = result[0]
        self.img_url = d[u'url_direct']
        self.img_thumb_url = d[u'url_thumbnail']



if __name__ == '__main__':
    h= Host()
    h.test_file()
    h.test_url()
