# -*- coding: utf-8 -*-
'''
    This file is part of uimge.

    Uploader picture to different imagehosting Copyright (C) 2008 apkawa@gmail.com

    uimge is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

    site project http://wiki.github.com/Apkawa/uimge
'''
import urllib2
import urllib2_file
from os.path import split as path_split
import httplib


def host_test_all(_file = 'c:\\1.jpg', _url = 'http://s41.radikal.ru/i092/0902/93/40b756930f38.png'):
    u=Uploaders()
    for h in u.get_hosts_list():
        _h = u.get_host(h)()
        print _h.host
        try:
            _h.upload( _file )
            print _h.get_urls()
        except:
            print _h.host,' file fail'
        try:
            _h.upload(_url)
            print _h.get_urls()
        except:
            print _h.host,' url fail'


def test_host( host,  _url = 'http://s41.radikal.ru/i092/0902/93/40b756930f38.png',):
    import sys
    if sys.platform != 'win32':
        _file = '/home/apkawa/1237325744193.jpg'
    else:
        _file = 'C:\\1.jpg'
    h = compile_host(host)()
    h.upload(_file)
    print h.get_urls()
    h.upload(_url)
    print h.get_urls()

import os
if os.sys.platform == "win32":
    r_m = 'rb'
    w_m = 'wb'
else:
    r_m = 'r'
    w_m = 'w'


class Uploader:
    obj = None
    img_url = None
    img_thumb_url = None
    filename = None
    progress = 0


    def construct( self):
        def ufopen( _url, _filename ):
            import tempfile
            __t = tempfile.NamedTemporaryFile(suffix= _filename )
            __t.write( urllib2.urlopen(_url).read())
            __t.seek(0)
            return __t

        self.__form = self.form.copy()
        if self.__obj.startswith('http://'):
            self.filename = path_split(urllib2.urlparse.urlsplit(self.__obj).path)[1]
            try:
                self.__form.update( self.as_url( self.__obj ) )
            except AttributeError:
                self.__form.update( self.as_file( ufopen( self.__obj, self.filename ) ) )

        else:
            self.filename = path_split( self.__obj )[1]

        try:
            self.__form.update( self.as_file( open( self.__obj, r_m ) ) )
        except IOError:
            return False

        try:
            self.__form.update( self.thumb_size( str(self.__thumb_size) ) )
        except AttributeError:
            pass

        return True
    def send_post(self):
        httplib.HTTPConnection.debug = 1
        self.action,self.__form
        __req = urllib2.Request( self.action, self.__form )
        try:
            __req.add_header('Cookie', self.cookie )
        except AttributeError:
            pass

        try:
            for key, val in self.headers.items():
                __req.add_header(key, val)

        except AttributeError:
            pass

        __req.add_header('Referer','http://%s/'%self.host )
        self._open = urllib2.urlopen( __req )


    def get_src(self, debug = False):
        __src = self._open.read()
        if debug:
            print __src
        return __src
    def get_headers(self):
        return self._open.headers.headers
    def get_geturl(self):
        return self._open.geturl()
    def get_filename(self):
        return self.__obj
    def upload( self, obj, thumb_size = 200):
        self.__obj = obj
        self.__thumb_size = thumb_size
        try:
            self.preload()
        except AttributeError:
            pass

        try:
            self.construct()
            #progress = UploaderProgress()
            #progress.start()
            self.send_post()
            self.postload()
            return True
        except IndexError, NameError:
            print "File %(obj)s not uploading"%{'obj': self.__obj}
            return False

    def get_filename( self ):
        return self.filename
    def get_thumb_url( self ):
        return self.img_thumb_url
    def get_img_url( self):
        return self.img_url
    def get_urls( self):
        return self.img_url, self.img_thumb_url

class Uploaders:
    def __init__(self):
        import inspect
        hosts = 'hosts'
        this_dir = os.path.split(__file__)[0]
        os.sys.path.append( this_dir )
        modules= []
        self.Imagehosts = {}
        for fname in os.listdir( this_dir+os.path.sep+hosts):
            if fname.endswith('.py') and not fname.startswith('__init__'):
                #print fname
                module_name = fname[:-3]
                str_module = hosts+'.'+module_name 
                #print str_module
                package = __import__(str_module)
                modules.append( module_name )
        for module_name in modules:
            module_obj = getattr( package, module_name)
            for elem in dir(module_obj):
                obj = getattr( module_obj, elem)
                if inspect.isclass(obj):
                    obj_name = obj.__name__
                    if obj_name.startswith('Host_'):
                        self.Imagehosts.update({ obj_name[len('Host_'):] : compile_host( obj ) })
                    
    def get_hosts_list(self):
        return self.Imagehosts
    def get_host(self, key):
        return self.Imagehosts.get(key)

from new import classobj
def compile_host( host):
    return classobj( host.host, (Uploader, host,),{})
    

#################################################################################################
#################################################################################################
#################################################################################################

















############################################################
#old

class __Host_pi_pict:
    '''example add new host'''
    host='pict.com'
    #action = 'http://www.pict.com/upload/'
    #action = 'http://www.pict.com/api/upload/?auth=m5q9u1vbk0d5v137s8k2sl1nr2'
    action = 'http://www.pict.com/upload/url/cellid/1/albumid/0'
    headers = {
            #'Accept':'application/json',
            #'User-Agent':'Pict.com Uploader v.1.0.4',
            #'Cookie':'PHPSESSID=s55ebesdc4i328mmq12i8grmh3; auth=s55ebesdc4i328mmq12i8grmh3; index_visit=%7B%22time%22%3A1238481373%2C%22pid%22%3A0%7D; localset=%7B%22first_tooltip%22%3A%22false%22%7D',
            #'X-Requested-With':'XMLHttpRequest',
            #'X-Request':'JSON',
            }
    

    form = {
            'cell_id':'30',
            'cellId':'30',
            'album_id':'30',
            'pid':'30',
            #'Submit': '',
            }

    def as_file(self, _file):
        #self.action = 'http://pict.com/api/upload/?auth=m5q9u1vbk0d5v137s8k2sl1nr2'
        self.url = False
        return {'Datafile': _file }
    def as_url(self, _url):
        self.action = 'http://www.pict.com/upload/url/cellid/1/albumid/0'
        self.url = True
        return {'url': _url}
    def postload(self ):
        _src = self.get_src(True).replace('\/','/')
        if self.url:
            _regx = r'\":\"(http://.*?/)[\d]{3}/([\w]{10,100}\.[\w]{3,4})\"}'

        else:
            _regx = r'\'(http://.*?/)[\d]{3}/([\w]{10,100}\.[\w]{3,4})\'\)\;\<\/script\>'

        _url = findall(_regx ,_src)[0]
        self.img_url = ''.join(_url)
        self.img_thumb_url = '150/'.join(_url)


#Example

if __name__ == '__main__':
    host_test_all()
    pass
