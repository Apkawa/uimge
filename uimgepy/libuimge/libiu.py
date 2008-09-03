# -*- coding: utf-8 -*-
import httplib, mimetypes
#import sys,os
USER_AGENT='Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.7.12) \
                        Gecko/20050922 Firefox/1.0.7 (Debian package 1.0.7-1)'

def get_file_contents(file_name):
    ''' 
    Получаем содержание файла.
    '''
    f = open(file_name);
    data = f.read()
    f.close()
    return data
def get_content_type(file_name):
    cont_type=mimetypes.guess_type(file_name)[0] or 'application/octet-stream'
    return cont_type
def encode_multipart_formdata(form_vaule, file_data, mode):
    '''
    Подготовка HTTP передачи
    '''
    BOUNDARY = '----------'
    CRLF = '\r\n'
    L = []
    # add additional form fields
    for (key, value) in form_vaule:
        L.append('--' + BOUNDARY)
        L.append('Content-Disposition: form-data; name="%s"' % key)
        L.append('')
        L.append(value)
    # add file
    if not mode:
        L.append('--' + BOUNDARY)
        L.append('Content-Disposition: form-data; name="%s"; filename="%s"' \
                % (file_data[0], file_data[1]))
        L.append('Content-Type: %s' % get_content_type(file_data[1]))
        L.append('')
        L.append(file_data[2])

    L.append('--' + BOUNDARY + '--')
    L.append('')
    body = CRLF.join(L)
    content_type = 'multipart/form-data; boundary=%s' % BOUNDARY
    
    return content_type, body

def send_file(file_name, ihost, form_vaule, mode):
    '''
    send_file(file_name, ihost={'name':'','post':'','cookie':''}, form_vaule={}, mode=[True,True])
    mode,flag = mode[0],mode[1]
    mode = False - заливаем просто файл, если True - то заливаем по урлу.
    
    flag = True - хостинг не поддерживает задивку по урлам, и поэтому обманываем его. 
    '''
    mode,flag = mode[0],mode[1]
    
    if not mode and not flag:
        file_data = (ihost['name'], file_name, get_file_contents(file_name))
        
    elif mode and not flag: 
        file_data = (ihost['name'], file_name, None)
    elif not mode and flag:
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
