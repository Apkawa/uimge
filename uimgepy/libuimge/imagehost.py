# -*- coding: utf-8 -*-
import libiu
from re import findall
from urllib import urlopen

def label(file, name):
    from PIL import Image
    from os import stat
    img=Image.open(file)
    size=stat(file).st_size/1024
    title='%s %sx%s %s Kb' %(name,str(img.size[0]),str(img.size[1]),str(size) )
    return title

def host_i_ipicture(send):
    file_name,label_name,mode=send[0],send[1],send[2]
    if not mode:
        ihost={\
           'host':'ipicture.ru', \
           'post':'/Upload/', \
           'name':'userfile',\
           'cookie':''\
           }
    
        form_vaule = [\
              ('uploadtype','1'),\
              ('method','file'),\
              ('file','upload'),\
              ('thumb_resize_on','on'),('thumb_resize','200'),\
              ('submit','"Загрузить"')\
              ]
    elif mode:
        ihost={\
           'host':'ipicture.ru', \
           'post':'/Upload/', \
           'name':'userfile',\
           'cookie':''\
           
           }
        form_vaule = [\
              ('uploadtype','2'),\
              ('method','url'),\
              ('userurl[]',file_name),\
              ('thumb_resize_on','on'),('thumb_resize','200'),\
              ('submit','"Загрузить"')\
              ]
    if label_name != None:
        form_vaule.insert(-1,('string_small_on','on'))
        form_vaule.insert(-1,('string_small', label(file_name,label_name) ))
        
    reurl=libiu.send_file(file_name, ihost, form_vaule, (mode,None))
    reurl=reurl.getheaders()[-5]
    reurl=findall('(http://.*.html)',reurl[1])
    url=findall('\[IMG\](http://.*)\[\/IMG\]',urlopen(reurl[0]).read())
    url=[url[0],url[2]]
    #return ihost,form_vaule
    return url

def host_r_radikal(send):
    file_name,label_name, mode=send[0],send[1],send[2]
    ihost={\
       'host':'www.radikal.ru', \
       'post':'/action.aspx', \
       'name':'F',\
       'cookie':''\
       }

    form_vaule = [\
              ('upload', 'yes'),\
              ('VM','200'),\
              ('CP','yes'),\
              ('Submit', '')\
              ]
    if label_name != None:
        form_vaule.insert(-1,('VE','yes'))
        form_vaule.insert(-1,('V', label(file_name,label_name) ))
    
    if mode:
        form_vaule.insert(1,('URLF',file_name))
    url=libiu.send_file(file_name, ihost, form_vaule, (mode,None)).read()
    url=findall('\[IMG\](http://.*.radikal.ru.*)\[/IMG\]',url)
    return url

def host_s_imageshack(send):
    file_name,label,mode=send[0],send[1],send[2]
    ihost={\
       'host':'imageshack.us', \
       'post':'/', \
       'name':'fileupload',\
       'cookie':''\
       }

    form_vaule = [\
              ('uploadtype', 'on'),\
              ('Submit', '"host it!"')\
              ]
    src=libiu.send_file(file_name, ihost, form_vaule, (None, mode)).read()
    url=findall('value=\"(http://img.[\d]+?.imageshack.us/img[\d]+?/.*?/.*?)\"', src)
    
    tumburl=url[0].split('.')
    tumburl.insert(-1,'th')
    urls=[url[0],'.'.join(tumburl)]
    return urls

def host_t_tinypic(send):
    file_name,label,mode=send[0],send[1],send[2]
    ihost={\
       'host':'s3.tinypic.com', \
       'post':'/upload.php', \
       'name':'the_file',\
       'cookie':''\
       }

    form_vaule = [\
              ('action', 'upload'),\
              ('MAX_FILE_SIZE', '200000000'),\
              ('action', 'upload'),\
              ('Submit', '')\
              ]
    
    src=libiu.send_file(file_name, ihost, form_vaule , (None, mode)).read()
    reurl=findall('http://tinypic.com/view.php\?pic=.*?\&s=[\d]',src)
    src=urlopen(reurl[0]).read()
    url=findall('\[IMG\](http://i[\d]+?.tinypic.com/.*?)\[/IMG\]',src)
    tumburl=url[0].split('.')
    tumburl[-2] += '_th'
    tumburl = '.'.join(tumburl)
    urls=[url[0],tumburl]
    return urls

def host_m_smages(send):
    from re import sub
    file_name,label,mode=send[0],send[1],send[2]
    ihost={\
       'host':'smages.com', \
       'post':'/upload', \
       'name':'img',\
       'cookie':''\
       }

    form_vaule = [('Submit', '')]
    reurl = sub('(\/code\/)|(\.htm)','', libiu.send_file(file_name, ihost, form_vaule , (None, mode) ).getheaders()[4][1])
    url,tmb = 'http://smages.com/i/%s'%reurl,'http://smages.com/t/%s'%reurl
    return [url,tmb]

def host_u_funkyimg(send):
    file_name,label,mode=send[0],send[1],send[2]
    ihost={\
           'host':'funkyimg.com', \
           'post':'/up.php', \
           'name':'file_0',\
           'cookie':''\
           }
    form_vaule = [\
                  ('addInfo','on'),\
                  ('upload','"Upload Images"'),('uptype','file'),\
                  ('file_1',''),('maxNumber','1'),('maxId','')
                  ]
    url=findall('\[IMG\](http://funkyimg.com/.*)\[/IMG\]\[/URL\]',\
                     libiu.send_file(file_name, ihost, form_vaule, (None,mode)).read())
    url.reverse()
    return url

def host_p_picthost(send):
    file_name,label,mode=send[0],send[1],send[2]
    ihost={\
           'host':'picthost.ru', \
           'post':'/upload.php', \
           'name':'userfile[]',\
           'cookie':''\
           }
    form_vaule = [\
                  ('private_upload','1'),\
                  ('upload','"Upload Images"'),('uptype','file'),\
                  ('file_1',''),('maxNumber','1'),('maxId','')
                  ]
    #print libiu.send_file(file_name, ihost, form_vaule, (None,mode)).read()
    url=findall('\<a href=\"viewer.php\?file=(.*?)\"',\
                     libiu.send_file(file_name, ihost, form_vaule, (None,mode)).read())
    t = 'http://picthost.ru/images/'
    tumburl=url[0].split('.')
    tumburl[-2] += '_thumb'
    tumburl = '.'.join(tumburl)
    return [t+url[0], t+tumburl]


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
        mode  = None
        cookie=auth_id_cod(email,passwd)
        ihost={\
       'host':host, \
       'post':'/upload/', \
       'name':'photos[]',\
       'cookie':cookie\
       }

        form_vaule = [\
              ('action', 'photo_upload'),\
              ('album_id',album_id),\
              ('Submit', '')\
              ]
        
        old_urls, o= get_pages_urls(cookie, None)
        for file in files:
            if libiu.send_file(file, ihost, form_vaule , (None, mode)).status == 302: pass
            else: print 'error'
        new_urls, o=get_pages_urls(cookie, o)
        upload_urls = list( set(old_urls) ^ set(new_urls) )
        return output_urls(upload_urls)
    
    return main(send)


    
