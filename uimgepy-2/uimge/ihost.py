# -*- coding: utf-8 -*-
from re import findall
import urllib2
import urllib2_file

DEBUG =0

def debug( *_mes ):
    if DEBUG:
        for m in _mes:
            print m
D = debug

def ufopen( _url ):
    import tempfile
    __t = tempfile.NamedTemporaryFile(suffix= urllib2.urlparse.urlsplit( _url).path.split('.')[-1])
    __t.write( urllib2.urlopen(_url).read() )
    __t.seek(0)
    return __t

def host_test( host, _file = '/home/apkawa/pictres/1201337718895.jpeg', _url = 'http://s41.radikal.ru/i092/0902/93/40b756930f38.png'):
    h = host()
    h.upload(_file)
    h.upload(_url)

class Uploader:
    obj = None
    img_url = None
    img_thumb_url = None
    def construct( self):

        D( self.__obj )
        self.__form = self.form.copy()
        if self.__obj.startswith('http://'):
            try:
                self.__form.update( self.as_url( self.__obj ) )
            except AttributeError:
                self.__form.update( self.as_file( ufopen( self.__obj ) ) )

        else:
            self.__form.update( self.as_file( open( self.__obj ) ) )
        try:
            self.__form.update( self.thumb_size( str(self.__thumb_size) ) )
        except AttributeError:
            pass
    def send_post(self):
        D( self.action,self.__form )
        self._open = urllib2.urlopen( self.action, self.__form )
    def get_src(self, debug = False):
        __src = self._open.read()
        if debug:
            print __src
        return __src
    def get_headers(self):
        return self._open.headers.headers
    def get_filename(self):
        return self.__obj
    def upload( self, __obj, __thumb_size = 200):
        self.__obj = __obj
        self.__thumb_size = __thumb_size
        #self.preload()
        self.construct()
        self.send_post()
        return self.postload()

    def get_thumb_url( self ):
        return self.img_thumb_url
    def get_img_url( self):
        return self.img_url
    def get_urls( self):
        return self.img_url, self.img_thumb_url

class Host_r_radikal( Uploader ):
    host = 'radikal.ru'
    action = 'http://www.radikal.ru/action.aspx' 
    form = {
                'CP': 'yes',
                'Submit': '',
                'upload': 'yes'
                }
    def as_file(self, _file):
        return {'F': _file }
    def as_url(self, _url):
        return {'URLF': _url }
    def thumb_size(self, _thumb_size):
        return { 'VM': _thumb_size, }
    def postload(self):
        __url = findall('\[IMG\](http://.*.radikal.ru.*)\[/IMG\]', self.get_src() )
        self.img_url = __url[0]
        self.img_thumb_url =  __url[1]
#        D( resp)

class Host_o_opicture( Uploader ):
    host='opicture.ru'
    action = 'http://opicture.ru:8080/upload/'
    form = {
                'preview':	'on',
                'action':'upload',
                }
    def as_file(self, _file):
        return {'type': '1' ,'file[]': _file } 
    def as_url(self, _url):
        return {'type': '2' ,'link[]': _url } 
    def thumb_size(self, _thumb_size):
        return { 'previewwidth': _thumb_size, }
    def postload(self):
        __url = findall('showTags\(.*?\'([\d]{4}/[\d]{2}/[\d]{2}/[\d]{2}/[\d]{10,}\.[\w]{2,4})\'', self.get_src() )
        self.img_url = 'http://opicture.ru/upload/%s'% __url[0]
        self.img_thumb_url = 'http://opicture.ru/picture/thumbs/%s.jpg'% ''.join( __url[0].split('.')[:-1])
        #D( resp)
        
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
            'submit':'"Загрузить"',
            }
    def as_file(self, _file):
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


class Host_v_savepic( Uploader):
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

#FAIL
class __Host_t_tinypic( Uploader):
    '''
    сломана заливка. надо чинить
    '''
    host='tinypic.com'
    action = 'http://s3.tinypic.com/upload.php'
    form = {'MAX_FILE_SIZE': '200000000', 'Submit': '', 'action': 'upload'}
    def as_file(self, _file):
        return {'name': _file} 
    def as_url(self, _url):
        return {'name': ufopen(_url)}
    def postload(self):
        __src = self.get_src()
        D(__src)
        reurl=findall('http://tinypic.com/view.php\?pic=.*?\&s=[\d]', __src)

        src=urlopen(reurl[0]).read()
        url=findall('\[IMG\](http://i[\d]+?.tinypic.com/.*?)\[/IMG\]',src)
        tumburl=url[0].split('.')
        tumburl[-2] += '_th'
        tumburl = '.'.join(tumburl)
        urls= (url[0],tumburl)
        return urls

#не работает заливка с урла.
class __Host_p_picthost( Uploader ):
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
        resp = {'url':t+url[0], 'thumb':t+tumburl}
        D(resp)
        return resp

#@host_test
#Нестабильный хостинг. 
class __Host_k_imageshack(Uploader):
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
        urls=(url[0],'.'.join(tumburl))
        resp = { 'url': urls[0], 'thumb': urls[1]}
        D(resp)
        return resp

if __name__ == '__main__':
    #t = Host_r_radikal()
    #t.as_file('/home/apkawa/pictres/1201337718895.jpeg')
    #t.upload()

    pass
'''
class Host_r_radikal:
    host='radikal.ru'
    action = 'http://www.radikal.ru/action.aspx'
    form = {
                'CP': 'yes',
                'Submit': '',
                'VM': '200',
                'upload': 'yes'
                }
    def as_file(self, _file):
        self.form.update( {'F': _file } )
    def as_url(self, _url):
        self.form.update( {'URLF': _url } )
    def preload(self):
        pass
    def postload(self, __src ):
        __url = findall('\[IMG\](http://.*.radikal.ru.*)\[/IMG\]', __src )
        print __url
        self.url = __url[0]
        self.thumb = __url[1]

    def upload( self ):
        __u = Uploader()
        __src = __u.default( self.action, self.form)
        self.postload( __src )

'''
