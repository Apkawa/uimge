# -*- coding: utf-8 -*-
import httplib, mimetypes
from sys import exit

class Luimge:
    def __init__(self):
        self.USER_AGENT='Mozilla/5.0 (X11; U; Linux i686;\
                en-US; rv:1.9.0.2pre) Gecko/2008072703 Firefox/3.0.2pre (Swiftfox)'
    def _debug(self,function):
        if self.debug:
            print function
        else: return None
    def send(self, filename, ihost, form_vaule,
            url_mode=False, fake_url=False, fake_filename = False, debug=False):
        if not fake_filename:
            self.filename = filename
        else:
            self.filename = 'fakefilename.%s'%filename.split('.')[-1].lower()
        self.ihost = ihost
        self.form_vaule = form_vaule
        self.url_mode = url_mode
        self.fake_url = fake_url
        self.debug = debug

        if not url_mode or fake_url:
            content_type, body = self.encode_multipart_formdata(ihost['name'], self.get_file_contents(filename))
        elif url_mode and not fake_url:
            content_type, body = self.encode_multipart_formdata(ihost['name'])

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
        response = header.getresponse()
        status = response.status
        if status in (200,302,):
            return response
        else:
            exit('Server error %s'%status)

    def encode_multipart_formdata(self, ihost, filedata=None):
        '''
        Подготовка HTTP передачи
        '''
        BOUNDARY = '----------'
        # add additional form fields
        L = ['--%s\nContent-Disposition: form-data; name="%s"\n\n%s'%
                ( BOUNDARY,key, vaule) for key,vaule in self.form_vaule]
        # add file
        if not self.url_mode or self.fake_url:
            L.append('--' + BOUNDARY)
            L.append('Content-Disposition: form-data; name="%s"; filename="%s"' \
                    % (ihost, self.filename))
            L.append('Content-Type: %s' % self.get_content_type(self.filename))
            L.append('')
            L.append(filedata)

        L.append('--' + BOUNDARY + '--')
        L.append('')
        body = '\n'.join(L)
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

