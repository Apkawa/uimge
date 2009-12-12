# -*- coding: utf-8 -*-
import base
class Host( base.BaseHost ):
    dev_mode = False

    short_key = 'c2n'
    long_key = 'clip2net'
    host='clip2net.com'
#    max_file_size = 5*(1024*1024) #5Mb

    action = 'http://%s/upload/'%host

    #headers = {}
    user_agent = "Clip2Net v.0.8.2b"
    http_auth = ('guest','guest')



    form = {
            'language' :'Russian',
            'mode' :'upload',
            'hwid' : 'UIMG-E666',
            'Submit': '',
            }

    def as_file(self, _file):
        return {
                'orig_file': self.filename,
                'file': _file,
                }

    def postload(self ):
        _src = self.response.body
        _regx = r'img\ src=\&quot\;(http:\/\/clip2net.com\/clip/.{2}/.+?)\&quot\;'
        _url = self.findall(_regx ,_src)[0]
        self.img_url = '%s?nocache=1'%_url
        self.img_thumb_url = '%s'%_url

if __name__ == '__main__':
    h= Host()
    h.test_file()
    h.test_url()
