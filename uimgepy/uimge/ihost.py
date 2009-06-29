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
from re import findall
import urllib2
import urllib2_file
from os.path import split as path_split
import httplib
#import os
#import sys
#from uploader import Uploader

#TODO: 
#  Будем делать
#    *http://imgby.com/ - японский хостинг
#
#    * http://directupload.net/
#    * http://pixshock.net/
#    * http://www.picfront.org/
#    * http://zikuka.ru/
#    * http://www.pict.com/
#
#  Look
# http://xpichost.net/
# http://depositimages.com/
# http://image-bits.ro/
# http://hfimg.com/
# http://imageban.ru/
# http://twinpix.nu/
# http://sendpic.ru/
# http://hostpix.ru/
# http://getpic.ru/
# http://www.10pix.ru/

# in http://zenden.ws/imageuploader

#
# * add http://sharepix.ru/
# * add http://avoreg.ru/
# * add http://www.ii4.ru/
# * add http://picbite.com/
#    * http://www.glowfoto.com/
#
# List image hostings
# http://forum.ru-board.com/topic.cgi?forum=11&topic=4219#1
#
# Epic FAIL
#
#    * http://up.li.ru/
#    * http://www.imagevenue.com/
#    * http://xs.to/
#    * http://www.images-hosting.com/ - error php in page
#    * http://paintedover.com/
#    * http://imghost.extra.by/
#    * http://www.imgspot.com/
#    * http://www.pixhost.org/
# http://imgdb.ru/



def host_test( host, _file = '/home/apkawa/1237325744193.jpg', _url = 'http://s41.radikal.ru/i092/0902/93/40b756930f38.png',):
    h = host()
    h.upload(_file)
    print h.get_urls()
    h.upload(_url)
    print h.get_urls()
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



from sys import platform

if platform == "win32":
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
        self.Imagehosts = {}
        import inspect
        __myglobals = dict()
        __myglobals.update( globals()  )
        for key, value in __myglobals.items():
            if key.startswith('Host_'):
                self.Imagehosts.update({key[len('Host_'):]:value})

    def get_hosts_list(self):
        return self.Imagehosts
    def get_host(self, key):
        return self.Imagehosts.get(key)

class Host_r_radikal( Uploader ):
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
        if self.url:
            __url = findall('\[IMG\](http://.*.radikal.ru.*)\[/IMG\]', self.get_src() )
            self.img_url = __url[0]
            self.img_thumb_url =  __url[1]
        else:
            from xml.dom import minidom
            _xml = minidom.parseString( self.get_src() )
            self.img_url = _xml.getElementsByTagName('rurl')[0].firstChild.data
            self.img_thumb_url =  _xml.getElementsByTagName('rurlt')[0].firstChild.data

class Host_o_opicture( Uploader ):
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

class Host_s_smages( Uploader ):
    host='smages.com'
    action = 'http://smages.com/upload'
    form = {'Submit': ''}

    def as_file(self, _file):
        return {'img': _file }
    def postload(self ):
        __url = findall('src=\'http://smages.com/i/(.*?).([\w]{2,4})\'', self.get_src() )[0]
        self.img_url = 'http://smages.com/i/%s.%s'%(__url[0], __url[1])
        self.img_thumb_url = 'http://smages.com/t/%s.jpg'%__url[0]

class Host_i_ipicture(Uploader):
    host='ipicture.ru'
    action = 'http://ipicture.ru/Upload/'
    form = {
            'thumb_resize_on':'on',
            'ramka_off':'on',
            'ignorAllCheck':'on',
            'submit':'"Загрузить"',
            }
    '''
    POST /api HTTP/1.1
User-Agent: iPicture ImageUploader
Accept: text/html
Content-Type: multipart/form-data; boundary=995997794
Host: ipicture.ru
Content-Length: 830394
Expect: 100-continue
Connection: Keep-Alive


    '''
    def as_file(self, _file):
        #self.action = 'http://ipicture.ru/api/'
        return {
            'uploadtype':'1',
            'method':'file',
            'file':'upload',
            'userfile': _file
            }
    def as_url(self, _url):
            return {
            'uploadtype':'2',
            'method':'url',
            'userurl[]': _url
            }
    def thumb_size(self, _thumb_size):
        return {'thumb_resize':_thumb_size,}
    def postload(self):
        __reurl=findall('(http://.*.html)', self.get_headers()[-1])
        __url=findall('\[IMG\](http://.*)\[\/IMG\]',urllib2.urlopen(__reurl[0]).read())
        self.img_url= __url[0]
        self.img_thumb_url = __url[2]
        '''
        else:
            _src = self.get_src()
            print _src
            self.img_url, self.img_thumb_url = findall('<(?:image|thumb)path>(.*?)</(?:image|thumb)path>', _src )
        '''

class Host_u_funkyimg( Uploader):
    host='funkyimg.com'
    action = 'http://funkyimg.com/up.php'
    form = {
            'addInfo': 'on',
            'maxId': '2',
            'maxNumber': '2',
            'upload': '"Upload Images"',
            }
    def as_file(self, _file):
        return {
                'uptype': 'file',
                'file_1':_file,}
    def as_url(self, _url):
        return {
                'uptype': 'url',
                'url':'',
                'url_1':_url,
                }
    def postload(self):
        __url=findall('\[IMG\](http://funkyimg.com/.*)\[/IMG\]\[/URL\]', self.get_src() )
        __url.reverse()
        self.img_url= __url[0]
        self.img_thumb_url = __url[1]

class Host_sp_savepic( Uploader):
    host='savepic.ru'
    action = 'http://savepic.ru/search.php'
    form = {'MAX_FILE_SIZE': '2097152',
             'email': '',
             'flip': '0',
             'font1': 'comic_bold',
             'font2': '20',
             'mini': '300x225',
             'note': '',
             'orient': 'h',
             'rotate': '00',
             'size1': '1',
             'size2': '800x600',
             'subm2': '\xc3\x8e\xc3\xb2\xc3\xaf\xc3\xb0\xc3\xa0\xc3\xa2\xc3\xa8\xc3\xb2\xc3\xbc'}
    def as_file(self, _file):
        return {'file':_file}

    def postload(self):
        reurl = findall('\"/([\d]+?).htm\"', self.get_src() )[0]
        ext ='png'#self.get_filename().split('.')[-1].lower()
        url,tmb = 'http://savepic.ru/%s.%s'%(reurl,ext),'http://savepic.ru/%sm.%s'%(reurl,ext)
        self.img_url = url
        self.img_thumb_url = tmb

class Host_up_upimg( Uploader ):
    host='upimg.ru'
    action = 'http://upimg.ru/u/'
    form = {'Submit': 'Загрузить'}


    def as_file(self, _file):
        return {'img': _file }
    def postload(self ):
        __url = findall('value=\"http://upimg.ru/i/(.*?)\"', self.get_src() )
        self.img_url = 'http://upimg.ru/i/%s'%(__url[0])
        self.img_thumb_url = 'http://upimg.ru/p/%s'%__url[0]

class Host_pc_piccy( Uploader ):
    host='piccy.info'
    action = 'http://piccy.info/ru/upload/'
    form = {'Submit': ''}
    cookie = 'sid=460e033265472bd2a69b1e4cc1c50bf0'

    def as_file(self, _file):
        return {'file': _file }
    def postload(self ):
        _src =  self.get_src()
        self.img_url = findall( 'value=\"(http://.*?)\"></td>', _src)[1]
        self.img_thumb_url = findall('src=\"(http://.*?)\" alt=\"Piccy.info', _src)[0]

class Host_pm_picamatic( Uploader ):
    host='picamatic.com'
    action = 'http://www.picamatic.com/'
    form = {
            'MAX_FILE_SIZE'	:'3145728',
            'upload':'',
            'Submit': '',
            }

    def as_file(self, _file):
        return {'Filedata': _file }
    def preload(self):
        self.action = findall('href="(http://www.picamatic.com/.*?)"', urllib2.urlopen('http://www.picamatic.com/?js&schedule').read() )[0]
    def postload(self ):
        _src =  self.get_src()
        self.img_url = findall( '"js-url-direct">(http://www.picamatic.com/show/.*?)</textarea>', _src)[0]
        self.img_thumb_url = findall('&gt;&lt;img src="(http://www.picamatic.com/show/.*?)" border="0"', _src)[0]

class Host_4p_4picture( Uploader ):
    host='4picture.ru'
    action = 'http://4picture.ru/process.php'
    form = {'tags1': 'uimge',
            'picname1':'uimge',
            'picrazdel1':'1',
            'Submit': '',
            }
    def as_file(self, _file):
        return {'image1': _file }
    def postload(self ):
        _src =  self.get_src()
        _url = findall( '\[IMG\]http://www.4picture.ru/pictures/(.*?)\[/IMG\]\[/URL\]', _src)[0]
        self.img_url = 'http://www.4picture.ru/pictures/%s'%_url
        self.img_thumb_url = 'http://www.4picture.ru/thumbnails/%s'%_url 

class Host_k4_keep4u( Uploader ):
    host='keep4u.ru'
    action = 'http://keep4u.ru/'
    form = {
            'disable_effects':'on',
            'preview':'yes',
            'sbmt':'',
            'Submit': '',
            }
    def as_file(self, _file):
        return {'pfile': _file }
    def thumb_size(self, _thumb_size):
        return { 'preview_size': _thumb_size, }
    def postload(self ):
        _src =  self.get_src()
        _url = findall( 'value=\"\[img\]http://keep4u.ru/imgs/b/(.*?)\[/img\]\"', _src)[0]
        self.img_url = 'http://keep4u.ru/imgs/b/%s'%_url
        self.img_thumb_url = 'http://keep4u.ru/imgs/s/%s'%_url 

class Host_tp_tinypic( Uploader):
    'to slooooy'
    host='tinypic.com'
    action = 'http://s5.tinypic.com/upload.php'
    form = {
            'domain_lang':'en',
            'shareopt':'true',
            'description':'uimge',
            'file_type':'image',
            'dimension':'1600',
            'video-settings':'sd',
            'addresses':'',

            'MAX_FILE_SIZE': '500000000',
            'Submit': '',
            'action': 'upload'}
    def as_file(self, _file):
        return {'the_file': _file} 
    def preload(self):
        __src = urllib2.urlopen( 'http://%s'%self.host).read()
        __form = {
            'UPLOAD_IDENTIFIER': findall('name="UPLOAD_IDENTIFIER" id="uid" value="(.*?)"',__src)[0] ,
            'upk': findall( 'name="upk" value="(.*?)"', __src)[0],
            }
        self.form.update( __form)
    def postload(self):
        __src = self.get_src()
        key = dict( findall('name="(pic|ival|type)" value="(.*?)"', __src))
        self.img_url = 'http://i%(ival)s.tinypic.com/%(pic)s%(type)s'%(key)
        self.img_thumb_url = 'http://i%(ival)s.tinypic.com/%(pic)s_th%(type)s'%( key)

class Host_hm_hostmyjpg( Uploader ):
    host='hostmyjpg.com'
    action = 'http://www.hostmyjpg.com/'
    form = {
            'page':'upload',
            'types':'0',
            'upload':'Host Them !',
            'Submit': '',
            }

    def as_file(self, _file):
        return {'userfile0': _file }
    def postload(self ):
        _src = self.get_src()

        __url = findall('\[IMG\]http://img.hostmyjpg.com/(.*?)\[/IMG\]',  _src )[0]
        self.img_url = 'http://img.hostmyjpg.com/%s'%__url
        self.img_thumb_url = 'http://www.hostmyjpg.com/thumbs/%s'%__url

class Host_pu_pikucha( Uploader ):
    host='pikucha.ru'
    action = 'http://pikucha.ru/upload'
    form = {
            'MAX_FILE_SIZE':'10485760',
            'description':'on',
            'description_value':'uimge',
            'upload':'',
            'Submit': '',
            }

    def as_file(self, _file):
        return {'image': _file }
    def postload(self ):
        _src = self.get_src()
        _url = findall('\[img\]http://pikucha.ru/([\d]{4,10})/thumbnail/(.*?)\[/img\]',_src)[0]
        self.img_url = 'http://pikucha.ru/%s/%s'%_url
        self.img_thumb_url = 'http://pikucha.ru/%s/thumbnail/%s'%_url

class Host_ba_bayimg( Uploader ):
    host='bayimg.com'
    action = 'http://upload.%s/upload'%host
    form = {
            'code':'666',
            'tags':'guimge',
            'Submit': '',
            }

    def as_file(self, _file):
        return {'file': _file }
    #def as_url(self, _url):
    #    return {'url': _url}
    #def thumb_size(self, _thumb_size):
    #    return { 'thumb_size': _thumb_size, }
    def postload(self ):
        _src = self.get_src()
        _regx = r'img src="http://bayimg.com/thumb/(.+?)"'
        _url = findall(_regx ,_src)[0]
        self.img_url = 'http://bayimg.com/image/%s'%_url
        self.img_thumb_url = 'http://bayimg.com/thumb/%s'%_url

class Host_k_imageshack(Uploader):
    host='imageshack.us'
    action = 'http://imageshack.us/'
    form = {'uploadtype': 'on', 'Submit':'"host it!"'}
    def __init__(self):
        self.ihost={\
           'host':'imageshack.us', \
           'post':'/', \
           'cookie':''\
           }
    def as_file(self,_file):
        return {'fileupload': _file }
    def postload(self):
        url=findall('value=\"(http://img.[\d]+?.imageshack.us/img[\d]+?/.*?/.*?)\"', self.get_src() )
        tumburl=url[0].split('.')
        tumburl.insert(-1,'th')
        self.img_url = url[0]
        self.img_thumb_url = '.'.join(tumburl)

class Host_p_picthost( Uploader ):
    host='picthost.ru'
    action = 'http://picthost.ru/upload.php'
    form = {'private_upload': '1', 'upload': '"Upload Images"', }
    def as_file(self, _file):
        return {'userfile[]': _file}
    def as_url(self, _url):
        action = 'http://picthost.ru/upload.php?url=1'
        return {'userfile[]': _url}
    def postload(self):
        url=findall('\<a href=\"viewer.php\?file=(.*?)\"', self.get_src() )

        t = 'http://picthost.ru/images/'
        tumburl=url[0].split('.')
        tumburl[-2] += '_thumb'
        tumburl = '.'.join(tumburl)
        self.img_url = t+url[0]
        self.img_thumb_url = t+tumburl

class Host_xe_xegami( Uploader ):
    host='xegami.com'
    action = 'http://%s/upload.php'%host
    form = {
            'description_a':'checked',
            'description':'uimge',
            'password':'',
            'Submit': '',
            }

    def as_file(self, _file):
        return {'upload_image': _file }
    def postload(self ):
        _src = self.get_src()
        _regx = r'img src=\"http://xegami.com/thumbs/(.+?)\"'
        _url = findall(_regx ,_src)[0]
        self.img_url = 'http://xegami.com/uploads/%s'%_url
        self.img_thumb_url = 'http://xegami.com/thumbs/%s'%_url

############################################################
#old

class __Host_pi_pict( Uploader ):
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
class __Host_ex_example( Uploader ):
    '''example add new host'''
    host='example.org'
    action = 'http://example.org/upload'
    form = {
            'Submit': '',
            }

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

if __name__ == '__main__':
    #host_test_all()
    pass
