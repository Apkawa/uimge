# -*- coding: utf-8 -*-
import pycurl
from StringIO import StringIO

import os
import re

from random import choice as rchoice
from mimetypes import guess_type

import threading

try:
    import psyco
    psyco.full()
except ImportError:
    pass


USER_AGENTS_LIST=(
         'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)',
         'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322)',
         'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727)',
         'Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.1)',
         'Mozilla/4.0 (compatible; MSIE 7.0b; Win32)',
         'Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 6.0)',
         'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; SV1; Arcor 5.005; .NET CLR 1.0.3705; .NET CLR 1.1.4322)',
         'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; YPC 3.0.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
         'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)',
         'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; WOW64; SLCC1; .NET CLR 2.0.50727; .NET CLR 3.0.04506; .NET CLR 3.5.21022)',
         'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; WOW64; SLCC1; .NET CLR 2.0.50727; .NET CLR 3.0.04506; .NET CLR 3.5.21022)',
         'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; WOW64; Trident/4.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 3.5.21022; .NET CLR 3.5.30729; .NET CLR 3.0.30618)',
         'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.8.1) Gecko/20060601 Firefox/2.0 (Ubuntu-edgy)',
         'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.1) Gecko/20061204 Firefox/2.0.0.1',
         'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1.2) Gecko/20070220 Firefox/2.0.0.2',
         'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1.2) Gecko/20070221 SUSE/2.0.0.2-6.1 Firefox/2.0.0.2',
         'Mozilla/5.0 (Windows; U; Windows NT 5.1; en; rv:1.8.1.9) Gecko/20071025 Firefox/2.0.0.9',
         '# 2.0.0.9 i686 \xd0\xbf\xd0\xbe\xd0\xb4 GNU/Linux AMD64 Mozilla/5.0 (X11; U; Linux i686 (x86_64); en-US; rv:1.8.1.9) Gecko/20071025 Firefox/2.0.0.9',
         'Mozilla/5.0 (Windows; U; Windows NT 5.1; en; rv:1.8.1.17) Gecko/20080829 Firefox/2.0.0.17',
         'Mozilla/5.0 (Windows; U; Windows NT 5.1; en; rv:1.8.1.19) Gecko/20081201 Firefox/2.0.0.19',
         'Mozilla/5.0 (X11; U; Linux i686 (x86_64); en-US; rv:1.9a1) Gecko/20061204 GranParadiso/3.0a1',
         'Mozilla/5.0 (Windows; U; Windows NT 5.1; en; rv:1.9) Gecko/2008052906 Firefox/3.0',
         'Mozilla/5.0 (Windows; U; Windows NT 5.1; en; rv:1.9.0.1) Gecko/2008070208 Firefox/3.0.1',
         'Mozilla/5.0 (Windows; U; Windows NT 5.1; en; rv:1.9.0.2) Gecko/2008091620 Firefox/3.0.2',
         'Mozilla/5.0 (X11; U; Linux x86_64; en; rv:1.9.0.2) Gecko/2008092702 Gentoo Firefox/3.0.2',
         'Mozilla/5.0 (Windows; U; Windows NT 5.1; en; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3',
         'Mozilla/5.0 (Windows; U; Windows NT 5.1; en; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3 (.NET CLR 3.5.30729)',
         'Mozilla/5.0 (Windows; U; Windows NT 6.0; en; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3',
         'Mozilla/5.0 (Windows; U; Windows NT 5.2; en; rv:1.9.0.5) Gecko/2008120122 Firefox/3.0.5',
         'Opera/9.0 (Windows NT 5.1; U; en)',
         'Opera/9.01 (X11; Linux i686; U; en)',
         'Opera/9.02 (Windows NT 5.1; U; en)',
         'Opera/9.10 (Windows NT 5.1; U; en)',
         'Opera/9.23 (Windows NT 5.1; U; en)',
         'Opera/9.50 (Windows NT 5.1; U; en)',
         'Opera/9.50 (Windows NT 6.0; U; en)',
         'Opera/9.60 (Windows NT 5.1; U; en) Presto/2.1.1',
         )

class UploaderError( Exception ):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr( self.value )

class Uploader:
    USER_AGENT = rchoice( USER_AGENTS_LIST )
    __t = None
    proxy = []
    proxy_type = {}
    stop = False

    def findall( self, regex, string):
        rst = re.findall( regex, string)
        if rst:
            return rst
        else:
            raise UploaderError( 'Error parse regex %s'%regex)

    def mime( self, obj):
        mime = guess_type( obj)
        if mime[0]:
            return mime[0]
        else:
            return "application/octet-stream"

    def check_size(self, path ):
        size = os.stat( path ).st_size
        if self.max_file_size and  size > self.max_file_size:
            raise UploaderError( "Big file size: %ib > %ib"%( size, self.max_file_size ) )

    def get_proxytype(self):
        for key, val in  pycurl.__dict__.items():
            if key.startswith("PROXYTYPE_"):
                self.proxy_type.update( { key[ len("PROXYTYPE_"): ].lower() : val } )
        return self.proxy_type

    def set_proxy(self, proxy, port, proxy_type="http", user="", passwd=""):
        proxy_type_dict = self.get_proxytype()
        _proxy_type = proxy_type_dict.get( proxy_type.lower() )
        self.proxy.append( (pycurl.HTTPPROXYTUNNEL,1))

        # self.proxy.append( ( pycurl.PROXY, proxy) )
        if type(port) == int:
            self.proxy.append( ( pycurl.PROXY, "%s:%i"%( proxy, port ) ) )
        else:
            raise UploaderError("proxy value is not int")

        if proxy_type:
            self.proxy.append( ( pycurl.PROXYTYPE, _proxy_type ) )
        else:
            raise UploaderError("\"%s\" is not correct PROXYTYPE"% proxy_type )

        if user:
            self.proxy.append( ( pycurl.PROXYUSERPWD, "%s:%s"%(user, passwd) ))

    def isurl(self, string):
        return not not [True for s in 'http://','ftp://','https://' if string.startswith(s) ]

    def upload(self, obj):
        obj = str(obj)
        self.__form = self.form.copy()
        url = False

        self.filename = os.path.split( obj )[1]

        if self.isurl(obj):
            if self.as_url:
                self.__form.update( self.as_url( obj ) )
                url = True
            else:
                path = self._ufopen( obj, self.filename)
        else:
            path = obj

        if not url:
            self.check_size( path )
            self.__form.update( self.as_file(
                    ( pycurl.FORM_FILE, path , pycurl.FORM_CONTENTTYPE, self.mime( path ) )
                ))


    def send_post(self):
        self._body = StringIO()
        self._headers = StringIO()

        self.curl = pycurl.Curl()

        self.curl.setopt( pycurl.FOLLOWLOCATION, 1)
        self.curl.setopt( pycurl.TIMEOUT, 60)
        self.curl.setopt( pycurl.MAXREDIRS, 2)
        self.curl.setopt( pycurl.WRITEFUNCTION, self._body.write)
        self.curl.setopt( pycurl.HEADERFUNCTION, self._headers.write)
        self.curl.setopt( pycurl.NOSIGNAL, 1)
        self.curl.setopt( pycurl.URL, self.action )

        if self.__dict__.get('cookie'):
            self.curl.setopt( pycurl.COOKIE, self.cookie )
        self.curl.setopt( pycurl.REFERER, 'http://%s/'%self.host)
        if self.headers:
            self.curl.setopt( pycurl.HTTPHEADER, self.headers.items())

        if self.user_agent:
            self.USER_AGENT = self.user_agent

        self.curl.setopt( pycurl.USERAGENT, self.USER_AGENT )

        #print self.__form.items()
        curl_post = self.curl
        curl_post.setopt( pycurl.HTTPPOST, self.__form.items())
        if self.proxy:
            for arg in self.proxy:
                print arg
                self.curl.setopt( *arg )
        # curl_post.perform()
        multi = pycurl.CurlMulti()
        multi.add_handle( curl_post )
        num_handles = 1
        self.stop = False
        while num_handles:
            while 1:
                ret, num_handles = multi.perform()
                if ret != pycurl.E_CALL_MULTI_PERFORM:
                    break
                if self.stop:
                    raise UploaderError("Upload cancel")
            multi.select(1.0)


        self.http_code = curl_post.getinfo(pycurl.HTTP_CODE)
        if self.http_code in (404, 500):
            raise UploaderError("%s %s error"%( self.host, self.http_code) )
        #TODO: сделать как результат объект `responce`
        #типа `self.responce.url` и `self.responce.body`
        if self.__t:
            os.remove( self.__t.name)
        #print curl.getinfo(pycurl.TOTAL_TIME)
        #print curl.getinfo(pycurl.EFFECTIVE_URL)
        #print self.curl.getinfo(pycurl.INFO_COOKIELIST)
        # __url = self.curl.getinfo(pycurl.REDIRECT_URL)
        dict_response = {
                "body": self._body.getvalue(),
                "headers": self._headers.getvalue(),
                "url": self.curl.getinfo(pycurl.EFFECTIVE_URL),
                }
        self.response = type("responce",(), dict_response )

    def cancel(self):
        self.stop = True

    def _ufopen(self, _url, _filename ):
        import urllib
        from tempfile import NamedTemporaryFile
        self.__t = NamedTemporaryFile(prefix='',suffix= _filename, delete=False )
        self.__t.write( urllib.urlopen(_url).read())
        self.__t.seek(0)
        return self.__t.name

    def get_filename( self, splitext=False ):
        if not splitext:
            return self.filename
        else:
            return os.path.splitext( self.filename)

    def get_html(self, url):
        self.curl.setopt( pycurl.URL, url)
        self.curl.unsetopt( pycurl.HTTPPOST)
        self.curl.perform()

    def error(self, msg="Error"):
        raise UploaderError( msg )

    def __test( self, obj):
        import traceback
        import timeit
        def ex( func, *args):
            try:
                func(*args)
            except KeyboardInterrupt:
                os.sys.exit(1)
            except Exception, err:
                traceback.print_exc()

        print 'http://%s'%self.host
        t = timeit.Timer()
        _t0 = t.timer()
        # self.set_proxy( proxy="127.0.0.1", port=9050, proxy_type= "socks5" )
        ex(self.upload,obj)
        ex(self.preload)
        ex(self.send_post)
        ex(self.postload)
        _t1 = t.timer()
        print "Upload time: %.3f second"%(_t1 - _t0)
        ex( lambda x: os.sys.stdout.write("%s %s \n"%(x.img_url,x.img_thumb_url) ), self )

    def test_url( self, obj="http://s41.radikal.ru/i092/0902/93/40b756930f38.png" ):
        self.__test( obj)
        pass
    def test_file( self, obj="/home/apkawa/qr.png"):
        self.__test( obj)

class BaseHost( Uploader ):
    dev_mode = False
    max_file_size = None
    short_key = ""
    long_key  = ""
    host= ""
    action = ""
    user_agent = ""
    form = {}
    headers = {}

    as_file = None
    as_url  = None

    def preload(self):
        pass

    def postload(self):
        pass


    '''
    def self_test(self):
        _url = 'http://s41.radikal.ru/i092/0902/93/40b756930f38.png'
        if os.sys.platform != 'win32':
            _file = '/home/apkawa/1237325744193.jpg'
        else:
            _file = 'C:\\1.jpg'

        ex(self.upload,_url)
        print self.get_urls()
        print '--'

    def as_file(self, _file):
        return {'image': _file }
    def as_url(self, _url):
        return {'url': _url}
    def thumb_size(self, _thumb_size):
        return { 'thumb_size': _thumb_size, }
    def postload(self ):
        _src = self.response.body
        _regx = r'example'
        _url = findall(_regx ,_src)[0]
        self.img_url = '%s'%_url
        self.img_thumb_url = '%s'%_url
        return True
    '''

