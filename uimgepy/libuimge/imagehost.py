# -*- coding: utf-8 -*-
#import libiu
from libiu import Luimge
from re import findall
from urllib import urlopen

'''
list image hosting http://gluek.info/free-images-hosting/
TODO: add
imageupper.com
xmages.net
'''


class Host_m_smages:
    def __init__(self):
        self.ihost={\
           'host':'smages.com', \
           'post':'/upload', \
           'name':'img',\
           'cookie':''\
           }

        self.form_vaule = [('Submit', '')]

    def send(self, filename, url_mode):
        from re import sub
        src=Luimge().send(filename, self.ihost, self.form_vaule,
                    url_mode, fake_url=True )
        reurl = sub('(\/code\/)|(\.htm)','',src.getheaders()[4][1] )
        url,tmb = 'http://smages.com/i/%s'%reurl,'http://smages.com/t/%s'%reurl
        return [url,tmb]

    def en(self):
        u'Upload to smages.com'
        pass

    def ru(self):
        u'Залить на smages.com'
        pass

class Host_i_ipicture:
    def __init__(self):
        self.ihost={\
           'host':'ipicture.ru', \
           'post':'/Upload/', \
           'name':'userfile',\
           'cookie':''\
           }
        #if label_name != None:
        #    self.form_vaule.insert(-1,('string_small_on','on'))
        #    self.form_vaule.insert(-1,('string_small', label(filename,label_name) ))
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
        url=[url[0],url[2]]
        return url

    def en(self):
        u'Upload to ipicture.ru'
        pass

    def ru(self):
        u'Залить на ipicture.ru'
        pass

class Host_r_radikal:
    def __init__(self):
        self.ihost={\
           'host':'www.radikal.ru', \
           'post':'/action.aspx', \
           'name':'F',\
           'cookie':''\
           }

        self.form_vaule = [\
                  ('upload', 'yes'),\
                  ('VM','200'),\
                  ('CP','yes'),\
                  ('Submit', '')\
                  ]
        Luimge().send = Luimge()

    def send(self, filename,url_mode):
        #if label_name != None:
        #    self.form_vaule.insert(-1,('VE','yes'))
        #    self.form_vaule.insert(-1,('V', label(filename,label_name) ))

        if url_mode:
            self.form_vaule.insert(1,('URLF',filename))

        url=Luimge().send(filename, self.ihost, self.form_vaule, url_mode=url_mode)
        url=findall('\[IMG\](http://.*.radikal.ru.*)\[/IMG\]',url.read())
        return url

    def en(self):
        u'Upload to radikal.ru'
        pass
    def ru(self):
        u'Залить на radikal.ru'
        pass

class Host_s_imageshack:
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
    def send(self,send):
        src=Luimge().send(filename, self.ihost, self.form_vaule,
                url_mode=url_mode, fake_url=True).read()

        url=findall('value=\"(http://img.[\d]+?.imageshack.us/img[\d]+?/.*?/.*?)\"', src)
        tumburl=url[0].split('.')
        tumburl.insert(-1,'th')
        urls=[url[0],'.'.join(tumburl)]
        return urls
    def en(self):
        u'Upload to imageshack.us'
        pass
    def ru(self):
        u'Залить на imageshack.us'
        pass

class Host_t_tinypic:
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
        urls=[url[0],tumburl]
        return urls
    def en(self):
        u'Upload to tinypic.com'
        pass
    def ru(self):
        u'Залить на tinypic.com'
        pass

class Host_u_funkyimg:
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
    def en(self):
        u'Upload to funkyimg.com'
        pass
    def ru(self):
        u'Залить на funkyimg.com'
        pass

class Host_p_picthost:
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
        url=findall('\<a href=\"viewer.php\?file=(.*?)\"',\
                Luimge().send(filename, self.ihost, self.form_vaule,\
                    url_mode=url_mode, fake_url=True).read())

        t = 'http://picthost.ru/images/'
        tumburl=url[0].split('.')
        tumburl[-2] += '_thumb'
        tumburl = '.'.join(tumburl)
        return [t+url[0], t+tumburl]
    def en(self):
        u'Upload to picthost.ru'
        pass
    def ru(self):
        u'Залить на picthost.ru'
        pass

class Host_v_savepic:
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

    def en(self):
        u'Upload to savepic.ru'
        pass

    def ru(self):
        u'Залить на savepic.ru'
        pass


'''
(Request-Line)	POST /search.php HTTP/1.1
Host	savepic.ru
User-Agent	Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.2pre) Gecko/2008072703 Firefox/3.0.2pre (Swiftfox)
Accept	text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language	en-us,en;q=0.5
Accept-Encoding	gzip,deflate
Accept-Charset	ISO-8859-1,utf-8;q=0.7,*;q=0.7
Keep-Alive	300
Proxy-Connection	keep-alive
Referer	http://savepic.ru/
Content-Type	multipart/form-data; boundary=---------------------------120199042317593872921145478277
Content-Length	84531

(MAX_FILE_SIZE','2097152'),
file	filename="motivator387483.jpg" Content-Type: image/jpeg
('note',''),
('font1','comic_bold'),
('font2','20')
('orient','h'),
('size2','800x600')
('size1','1'),
('rotate','00'),
('flip','0'),
('mini','300x225')
('email',''),
('subm2','Îòïðàâèòü')


'''



'''
Example add Host

#--------------------------------------------------------------------
class Host_e_example:
    def __init__(self):
        self.ihost={\
           'host':'example.com', \
           'post':'/upload', \
           'name':'img',\
           'cookie':''\
           }

        self.form_vaule = [('Submit', '')]

    def send(self, filename, url_mode):
        filename,label,url_mode=send[0],send[1],send[2]
        reurl = Luimge().send(filename, self.ihost, self.form_vaule, (None, url_mode) ).getheaders()
        url,tmb = 'http://example.com/i/%s'%reurl,'http://example.com/t/%s'%reurl
        return [url,tmb]

    def en(self):
        u'Upload to exapmle.com'
        pass

    def ru(self):
        u'Залить на example.com'
        pass


#--------------------------------------------------------------------
Old code.
#--------------------------------------------------------------------
def _host_avangard_foto_cod(send):
    import urllib2
    email='nanodesu@in-mail.ru'
    passwd='splenchb'
    username='nanodesu4'
    album_id='7469727749'
    host='avangard.photo.cod.ru'

    def auth_id_cod(user,passwd):
        cookes=str(urllib2.urlopen('https://id.cod.ru/auth?email=%s&password=%s' %(user,passwd)).info())
        cookes=findall('(codsid=.+?;)[\s\S\w\W]*(auth=YES;)[\s\S\w\W]*(modified=\d+?;)', cookes)[0]
        cookes='%s %s %s' %(cookes[0],cookes[1],cookes[2])
        return cookes
    def get_pages_urls(cookie,o):
        def get_pages(i,cookie):
            urlpage='http://avangard.photo.cod.ru/users/%s/%s/?page=%d' %(username,album_id,i)
            req = urllib2.Request(urlpage)
            req.add_header('Cookie', cookie)
            return urllib2.urlopen(req).read()
        i=1
        url_data= get_pages(i,cookie)
        i=findall('<td width="80%" align="center" class="f12">.*<b>(\d{1,})</b></td>',url_data)
        if i and not o:
            i=int(i[0])
            url_data= get_pages(i,cookie)
            urls = findall('(http://avangard.photo.cod.ru/photos.*/w100_.*)" alt=',url_data)
        elif i and o:
            i=int(i[0])
            urls=[]
            for i in range(o,i+1):
                url_data = get_pages(i,cookie)
                for url in findall('(http://avangard.photo.cod.ru/photos.*/w100_.*)" alt=',url_data):
                    urls.append(url)
        elif not i:
            url_data= get_pages(1,cookie)
            urls = findall('(http://avangard.photo.cod.ru/photos.*/w100_.*)" alt=',url_data)
        #print type(urls), len(urls)
        return urls,i
    def output_urls(urls):
        out_url=[]
        for url in urls:
            tmb_100=url
            urlre=url.split('/w100_')
            tmb_400='%s/w400_%s'%(urlre[0],urlre[1])
            direct_url = '%s/%s'%(urlre[0],urlre[1])
            out_url.append((direct_url,tmb_400))
        return out_url
    def main(files):
        url_mode  = None
        cookie=auth_id_cod(email,passwd)
        self.ihost={\
       'host':host, \
       'post':'/upload/', \
       'name':'photos[]',\
       'cookie':cookie\
       }

        self.form_vaule = [\
              ('action', 'photo_upload'),\
              ('album_id',album_id),\
              ('Submit', '')\
              ]
        old_urls, o= get_pages_urls(cookie, None)
        for file in files:
            if Luimge().send(file, self.ihost, self.form_vaule , (None, url_mode)).status == 302: pass
            else: print 'error'
        new_urls, o=get_pages_urls(cookie, o)
        upload_urls = list( set(old_urls) ^ set(new_urls) )
        return output_urls(upload_urls)
    return main(send)

def label(file, name):
    from PIL import Image
    from os import stat
    img=Image.open(file)
    size=stat(file).st_size/1024
    title='%s %sx%s %s Kb' %(name,str(img.size[0]),str(img.size[1]),str(size) )
    return title

class _Host_v_imagevenue:
    'Не заливает png, только jpg'
    def __init__(self):
        self.ihost={\
           'host':'www.imagevenue.com', \
           'post':'/upload.php', \
           'name':'userfile[]',\
           'cookie':''\
           }

        self.form_vaule = [('Submit', ''),
                ('action','1'),
                ('imgcontent','contentnone'),
                ]

    def send(self, filename, url_mode):
        filename,label,url_mode=send[0],send[1],send[2]
        reurl = Luimge().send(filename, self.ihost, self.form_vaule,url_mode )
        print reurl.read()
        url,tmb = 'http://example.com/i/%s'%reurl,'http://example.com/t/%s'%reurl
        return [url,tmb]

    def en(self):
        u'Upload to exapmle.com'
        pass

    def ru(self):
        u'Залить на example.com'
        pass


class _Host_a_imageshost:
    'Пока не работает'
    def __init__(self):
        self.ihost={\
           'host':'imageshost.ru', \
           'post':'/upload.php', \
           'name':'userimg1',\
           'cookie':'quality=95; pvs1=250; to_angle=0;'\
           }

        self.form_vaule = [
                ('type','1'),('dnt','1'),
                ('imgcontent','contentnone'),
                ('to_size_w',''),
                ('to_size_h',''),
                ('to_angle','0'),
                ('noedit','on'),
                ('pvs1','250'), ('quality','95'),
                ('is_pr_text',''),('pr_text',''),
                ('text',''),
                ('description',''),
                ('rules','on'),
                ('submit_button','Çàãðóçèòü'),
                ]

    def send(self, filename, url_mode):
        filename,label,url_mode=send[0],send[1],send[2]
        reurl = Luimge().send(filename, self.ihost, self.form_vaule,url_mode )
        print reurl.getheaders(),reurl.read()
        url,tmb = 'http://example.com/i/%s'%reurl,'http://example.com/t/%s'%reurl
        return [url,tmb]

    def en(self):
        u'Upload to exapmle.com'
        pass

    def ru(self):
        u'Залить на example.com'
        pass
#--------------------------------------------------------------------
'''

if __name__ == '__main__':
    pass
