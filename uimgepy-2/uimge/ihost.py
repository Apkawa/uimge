# -*- coding: utf-8 -*-
from re import findall
import urllib2
import urllib2_file


class Uploader:
    def set_rule(self, action, form ):
        self.action = action
        self.form = form
    def send( self):
        self.open = urllib2.urlopen( self.action, self.form )
    def get_src( self ):
        return self.open.read()
    def default(self, action, form):
        '''
        shourtcat
        '''
        self.set_rule( action, form)
        self.send()
        return self.get_src()


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
        self.form.update( {'F': open( _file ) } )
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

class Host_o_opicture:
    host='opicture.ru'
    action = 'http://opicture.ru:8080/upload/'
    form = {
                'preview':	'on',
                'previewwidth':'200',
                'action':'upload',
                }
    def as_file(self, _file):
        self.filename = _file
        self.form.update( {'type': '1' ,'file[]': open( _file ) } )
    def as_url(self, _url):
        self.urlname = _url
        self.form.update( {'type': '2' ,'link[]': _url } )
    def preload(self):
        pass
    def postload(self, __src ):
        __url = findall('showTags\(.*?\'([\d]{4}/[\d]{2}/[\d]{2}/[\d]{2}/[\d]{10,}\.[\w]{2,4})\'', __src )
        self.url = 'http://opicture.ru/upload/%s'% __url[0]
        self.thumb = 'http://opicture.ru/picture/thumbs/%s.jpg'% ''.join( __url[0].split('.')[:-1])
    def upload( self ):
        __u = Uploader()
        __src = __u.default( self.action, self.form)
        self.postload( __src )
        

class Host_s_smages:
    host='smages.com'
    action = 'http://smages.com/upload'
    form = {'Submit': ''}

    def as_file(self, _file):
        self.form.update( {'img': open( _file ) } )
    def as_url(self, _url):
        self.form.update( {'img': ufopen(_url) } )
    def preload(self):
        pass
    def postload(self, __src ):
        __url = findall('src=\'http://smages.com/i/(.*?).([\w]{2,4})\'', __src )[0]
        print __url
        self.url ='http://smages.com/i/%s.%s'%(__url[0], __url[1])
        self.thumb = 'http://smages.com/t/%s.jpg'%__url[0]
        print self.url, self.thumb

    def upload( self ):
        __u = Uploader()
        __src = __u.default( self.action, self.form)
        self.postload( __src )



class Host_i_ipicture:
    host='ipicture.ru'
    action = 'http://ipicture.ru/Upload/'
    form = {
            'thumb_resize_on':'on',
            'thumb_resize':'200',
            'submit':'"Загрузить"',
            }
    def as_file(self, _file):
        self.form.update( {
            'uploadtype':'1',
            'method':'file',
            'file':'upload',
            'userfile': open( _file )
            } )
    def as_url(self, _url):
        self.form.update( {
            'uploadtype':'2',
            'method':'url',
            'userurl[]': _url
            } )
    def preload(self):
        pass
    def postload(self, __src ):
        __reurl=findall('(http://.*.html)',__src[-1])
        __url=findall('\[IMG\](http://.*)\[\/IMG\]',urllib2.urlopen(__reurl[0]).read())
        self.url = __url[0]
        self.thumb = __url[2]
        print self.url, self.thumb

    def upload( self ):
        __u = Uploader()
        __u.set_rule( self.action, self.form)
        __u.send()
        __src = __u.open.headers.headers
        self.postload( __src )

    def __init__(self):
        self.ihost={\
           'host':'ipicture.ru', \
           'post':'/Upload/', \
           'name':'userfile',\
           'cookie':''\
           }
    def send(self, filename, url_mode):
        if not url_mode:
            self.form_vaule = [\
                  ('uploadtype','1'),\
                  ('method','file'),\
                  ('file','upload'),\
                  ('thumb_resize_on','on'),('thumb_resize','200'),\
                  ('submit','"Загрузить"')\
                  ]
        elif url_mode:
            self.form_vaule = [\
                  ('uploadtype','2'),\
                  ('method','url'),\
                  ('userurl[]',filename),\
                  ('thumb_resize_on','on'),('thumb_resize','200'),\
                  ('submit','"Загрузить"')\
                  ]
        reurl=Luimge().send(filename, self.ihost, self.form_vaule, url_mode)
        reurl=reurl.getheaders()[-5]
        reurl=findall('(http://.*.html)',reurl[1])
        url=findall('\[IMG\](http://.*)\[\/IMG\]',urlopen(reurl[0]).read())
        url=(url[0],url[2])
        return url



class Host_k_imageshack:
    host='imageshack.us'
    def __init__(self):
        self.ihost={\
           'host':'imageshack.us', \
           'post':'/', \
           'name':'fileupload',\
           'cookie':''\
           }

        self.form_vaule = [\
                  ('uploadtype', 'on'),\
                  ('Submit', '"host it!"')\
                  ]
    def send(self, filename, url_mode):
        src=Luimge().send(filename, self.ihost, self.form_vaule,
                url_mode=url_mode, fake_url=True).read()

        url=findall('value=\"(http://img.[\d]+?.imageshack.us/img[\d]+?/.*?/.*?)\"', src)
        tumburl=url[0].split('.')
        tumburl.insert(-1,'th')
        urls=(url[0],'.'.join(tumburl))
        return urls

class Host_t_tinypic:
    host='tinypic.com'
    def __init__(self):
        self.ihost={\
           'host':'s3.tinypic.com', \
           'post':'/upload.php', \
           'name':'the_file',\
           'cookie':''\
           }

        self.form_vaule = [\
                  ('action', 'upload'),\
                  ('MAX_FILE_SIZE', '200000000'),\
                  ('action', 'upload'),\
                  ('Submit', '')\
                  ]
    def send(self, filename, url_mode):
        src=Luimge().send(filename, self.ihost, self.form_vaule,
                url_mode=url_mode, fake_url=True).read()

        reurl=findall('http://tinypic.com/view.php\?pic=.*?\&s=[\d]',src)
        src=urlopen(reurl[0]).read()
        url=findall('\[IMG\](http://i[\d]+?.tinypic.com/.*?)\[/IMG\]',src)
        tumburl=url[0].split('.')
        tumburl[-2] += '_th'
        tumburl = '.'.join(tumburl)
        urls= (url[0],tumburl)
        return urls

class Host_u_funkyimg:
    host='funkyimg.com'
    def __init__(self):
        self.ihost={\
               'host':'funkyimg.com', \
               'post':'/up.php', \
               'name':'file_0',\
               'cookie':''\
               }
        self.form_vaule = [\
                      ('addInfo','on'),\
                      ('upload','"Upload Images"'),('uptype','file'),\
                      ('file_1',''),('maxNumber','1'),('maxId','')
                      ]
    def send(self, filename, url_mode):
        url=findall('\[IMG\](http://funkyimg.com/.*)\[/IMG\]\[/URL\]',\
                         Luimge().send(filename, self.ihost, self.form_vaule,
                             url_mode=url_mode,fake_url=True).read())
        url.reverse()
        return url

class Host_p_picthost:
    host='picthost.ru'
    def __init__(self):
        self.ihost={\
               'host':'picthost.ru', \
               'post':'/upload.php', \
               'name':'userfile[]',\
               'cookie':''\
               }
        self.form_vaule = [\
                      ('private_upload','1'),\
                      ('upload','"Upload Images"'),('uptype','file'),\
                      ]
    def send(self, filename, url_mode):
        src = Luimge().send(filename, self.ihost, self.form_vaule,\
                    url_mode=url_mode, fake_url=True)
        url=findall('\<a href=\"viewer.php\?file=(.*?)\"',src.read() )

        t = 'http://picthost.ru/images/'
        print url
        tumburl=url[0].split('.')
        tumburl[-2] += '_thumb'
        tumburl = '.'.join(tumburl)
        return (t+url[0], t+tumburl)

class Host_v_savepic:
    host='savepic.ru'

    def __init__(self):
        self.ihost={\
           'host':'savepic.ru', \
           'post':'/search.php', \
           'name':'file',\
           'cookie':''\
           }

        self.form_vaule = [
                ('MAX_FILE_SIZE','2097152'),
                ('note',''),
                ('font1','comic_bold'),
                ('font2','20'),
                ('orient','h'),
                ('size2','800x600'),
                ('size1','1'),
                ('rotate','00'),
                ('flip','0'),
                ('mini','300x225'),
                ('email',''),
                ('subm2','Îòïðàâèòü'),
                ]

    def send(self, filename, url_mode):
        src = Luimge().send(filename, self.ihost, self.form_vaule, url_mode, fake_url=True ).read()
        reurl = findall('\"/([\d]+?).htm\"',src)[0]
        ext = filename.split('.')[-1].lower()
        url,tmb = 'http://savepic.ru/%s.%s'%(reurl,ext),'http://savepic.ru/%sm.%s'%(reurl,ext)
        return (url,tmb)


def ufopen( _url ):
    import tempfile
    __t = tempfile.TemporaryFile()
    __t.write( urllib2.urlopen(_url).read() )
    __t.seek(0)
    return __t


if __name__ == '__main__':
    h = Host_i_ipicture()
    h.as_file('/home/apkawa/pictres/1201337718895.jpeg')
    h.upload()
    h.as_url('http://s41.radikal.ru/i092/0902/93/40b756930f38.png')
    h.upload()
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
        self.form.update( {'F': open( _file ) } )
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
