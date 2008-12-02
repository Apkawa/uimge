# -*- coding: utf-8 -*-
import httplib, mimetypes
#import sys,os
class Luimge:
    def __init__(self):
        self.USER_AGENT='Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.7.12) \
                        Gecko/20050922 Firefox/1.0.7 (Debian package 1.0.7-1)'
    def debug(self,function):
        if self.debug:
            print function
        else: return None
    def send(self, filename, ihost, form_vaule, url_mode=False, fake_url=False, debug=False):
        self.filename = filename
        self.ihost = ihost
        self.form_vaule = form_vaule
        self.url_mode = url_mode
        self.fake_url = fake_url
        self.debug = debug

        if not url_mode or fake_url:
            file_data = (ihost['name'], filename, self.get_file_contents(filename))
        elif url_mode and not fake_url:
            file_data = (ihost['name'], filename, None)

        content_type, body = self.encode_multipart_formdata(file_data)
        header = httplib.HTTPConnection(ihost['host'])
        header.putrequest('POST', ihost['post'])
        header.putheader('Content-Type', content_type)
        header.putheader('Content-Length', str(len(body)))
        header.putheader('Referer', 'http://'+ihost['host']+'/')
        header.putheader('Cookie',ihost['cookie'])
        header.putheader('User-Agent', self.USER_AGENT)
        header.endheaders()
        if self.debug:
            header.set_debuglevel(1)
        header.send(body)
        if self.debug:
            header.set_debuglevel(1)
        return header.getresponse()

    def encode_multipart_formdata(self, file_data):
        '''
        Подготовка HTTP передачи
        '''
        BOUNDARY = '----------'
        L = []
        # add additional form fields
        for (key, vaule) in self.form_vaule:
            L.append('--' + BOUNDARY)
            L.append('Content-Disposition: form-data; name="%s"' % key)
            L.append('')
            L.append(vaule)
        # add file
        if not self.url_mode or self.fake_url:
            L.append('--' + BOUNDARY)
            L.append('Content-Disposition: form-data; name="%s"; filename="%s"' \
                    % (file_data[0], file_data[1]))
            L.append('Content-Type: %s' % self.get_content_type(file_data[1]))
            L.append('')
            L.append(file_data[2])

        L.append('--' + BOUNDARY + '--')
        L.append('')
        body = '\r\n'.join(L)
        content_type = 'multipart/form-data; boundary=%s' % BOUNDARY
        return content_type, body

    def get_file_contents(self,file_name):
        '''
        Получаем содержание файла.
        '''
        if not self.fake_url:
            f = open(file_name,'r')
            data = f.read()
            f.close()
        elif self.fake_url:
            from urllib import urlopen
            data = urlopen(file_name).read()
        return data

    def get_content_type(self,file_name):
        cont_type=mimetypes.guess_type(file_name)[0] or 'application/octet-stream'
        return cont_type

def _send_file(file_name, ihost, form_vaule, mode, url_mode=False, fake_url=False):
    '''
    send_file(file_name, ihost={'name':'','post':'','cookie':''}, form_vaule={}, mode=[True,True])
    mode,flag = mode[0],mode[1]
    mode = False - заливаем просто файл, если True - то заливаем по урлу.
    flag = True - хостинг не поддерживает задивку по урлам, и поэтому обманываем его.
    '''
#    mode,flag = mode[0],mode[1]
    if not url_mode:
        file_data = (ihost['name'], file_name, get_file_contents(file_name))
    elif url_mode and not fake_url:
        file_data = (ihost['name'], file_name, None)
#    elif not mode and flag:
    elif url_mode and fake_url:
        from urllib import urlopen
        file_data = (ihost['name'], file_name.split('/')[-1], urlopen(file_name).read())

    content_type, body = encode_multipart_formdata(form_vaule, file_data, mode)
    header = httplib.HTTPConnection(ihost['host'])
    header.putrequest('POST', ihost['post'])
    header.putheader('Content-Type', content_type)
    header.putheader('Content-Length', str(len(body)))
    header.putheader('Referer', 'http://'+ihost['host']+'/')
    header.putheader('Cookie',ihost['cookie'])
    header.putheader('User-Agent', USER_AGENT)
    header.endheaders()
    header.send(body)
    #header.set_debuglevel(1)
    return header.getresponse()
