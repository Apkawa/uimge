# -*- coding: utf-8 -*-
import pycurl
from StringIO import StringIO
import os
from re import findall
from random import choice as rchoice
from mimetypes import guess_type

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

    def findall( self, regex, string):
        rst = findall( regex, string)
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

    def upload(self, obj):
        obj = str(obj)
        self.__form = self.form.copy()
        url = False

        if obj.startswith('http://'):
            self.filename = obj.split('/')[-1]
            if self.__dict__.get('as_url'):
                self.__form.update( self.as_url( obj ) )
                url = True
            else:
                path = self._ufopen( obj, self.filename)
        else:
            path = obj
            self.filename = os.path.split( obj )[1]

        if not url:
            self.check_size( path )
            self.__form.update( self.as_file(
                    ( pycurl.FORM_FILE, path , pycurl.FORM_CONTENTTYPE, self.mime( path ) )
                ))

        if self.__dict__.get('thumb_size'):
            self.__form.update( self.thumb_size( str(self.__thumb_size) ) )

    def send_post(self):
        self._body = StringIO()
        self._headers = StringIO()

        self.curl = pycurl.Curl()
        self.curl.setopt( pycurl.FOLLOWLOCATION, 1)
        #self.curl.setopt(pycurl.TIMEOUT, 20)
        self.curl.setopt( pycurl.MAXREDIRS, 2)
        self.curl.setopt( pycurl.WRITEFUNCTION, self._body.write)
        self.curl.setopt( pycurl.HEADERFUNCTION, self._headers.write)
        self.curl.setopt( pycurl.URL, self.action )
        if self.__dict__.get('cookie'):
            self.curl.setopt( pycurl.COOKIE, self.cookie )
        self.curl.setopt( pycurl.REFERER, 'http://%s/'%self.host)
        if self.headers:
            self.curl.setopt( pycurl.HTTPHEADER, self.headers.items())

        if self.user_agent:
            self.USERAGENT = self.user_agent

        self.curl.setopt( pycurl.USERAGENT, self.USERAGENT )
        #print self.__form.items()
        curl_post = self.curl
        curl_post.setopt( pycurl.HTTPPOST, self.__form.items())
        curl_post.perform()
        self.http_code = curl_post.getinfo(pycurl.HTTP_CODE)
        #TODO: сделать как результат объект `responce`
        #типа `self.responce.url` и `self.responce.body`
        if self.__t:
            os.remove( self.__t.name)
        #print curl.getinfo(pycurl.TOTAL_TIME)
        #print curl.getinfo(pycurl.EFFECTIVE_URL)
        #print self.curl.getinfo(pycurl.INFO_COOKIELIST)

    def _ufopen(self, _url, _filename ):
        import tempfile, urllib
        self.__t = tempfile.NamedTemporaryFile(prefix='',suffix= _filename, delete=False )
        self.__t.write( urllib.urlopen(_url).read())
        self.__t.seek(0)
        return self.__t.name

    def get_src(self, debug = False):
        __src = self._body.getvalue()
        if debug:
            print __src
        return __src

    def get_headers(self):
        return self._headers.getvalue()

    def get_geturl(self):
            red_url = self.curl.getinfo(pycurl.REDIRECT_URL)
            if red_url:
                return red_url
            else:
                return self.curl.getinfo(pycurl.EFFECTIVE_URL)

    def get_filename( self, splitext=False ):
        if not splitext:
            return self.filename
        else:
            return os.path.splitext( self.filename)

    def get_html(self, url):
        self.curl.setopt( pycurl.URL, url)
        self.curl.unsetopt( pycurl.HTTPPOST)
        self.curl.perform()

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
    def __test( self, obj):
        import traceback
        def ex( func, *args):
            try:
                func(*args)
            except KeyboardInterrupt:
                os.sys.exit(1)
            except Exception, err:
                traceback.print_exc()

        print self.host
        ex(self.upload,obj)
        ex(self.preload)
        ex(self.send_post)
        ex(self.postload)
        ex( lambda x: os.sys.stdout.write("%s %s \n"%(x.img_url,x.img_thumb_url) ), self )

    def test_url( self, obj="http://s41.radikal.ru/i092/0902/93/40b756930f38.png" ):
        self.__test( obj)
        pass
    def test_file( self, obj="/home/apkawa/qr.png"):
        self.__test( obj)
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
        _src = self.get_src()
        _regx = r'example'
        _url = findall(_regx ,_src)[0]
        self.img_url = '%s'%_url
        self.img_thumb_url = '%s'%_url
        return True
    '''

