#!/usr/bin/python
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
import os
import gettext
import inspect
from hosts.base import UploaderError
from tempfile import NamedTemporaryFile

VERSION = '0.07.12.0'


try:
    import psyco
    psyco.full()
except ImportError:
    pass

try:
    import Image
except:
    Image = None

try:
    gettext.install('uimge',unicode=True)
except IOError:
    gettext.install('uimge', localedir = 'locale',unicode=True)


class Outprint:
    def __init__(self):
        self.outprint_rules = {
                'bo_bb-orig': {
                    'rule': '[img]%(img_url)s[/img]',
                    'desc' : _('Output in bb code in the original amount')
                    },
                'bt_bb-thumb' : {
                    'rule': '[url=%(img_url)s][img]%(img_thumb_url)s[/img][/url]',
                    'desc' : _('Output in bb code with a preview')
                    },
                'ho_html-orig' : {
                    'rule': '<img src="%(img_url)s" alt="" />',
                    'desc' : _('Output in html code in the original amount')
                    },
                'ht_html-thumb' : {
                    'rule': '<a href="%(img_url)s"><img src="%(img_thumb_url)s" alt="" /></a>',
                    'desc' : _('Output in html code with a preview')
                    },
                'wi_wiki':{
                    'rule': '[[%(img_url)s|{{%(img_thumb_url)s}}]]',
                    'desc' : _('Output in doku wiki format code with a preview')
                    },
                
                }
        self.rule = None
        pass
    def set_rules(self, key=None, usr=None):
        if key:
            self.rule = self.outprint_rules.get(key)
            if not self.rule:
                return False
            else:
                self.rule = self.rule.get('rule')
                return True
        elif usr:
            replace = (
            ('#url#','%(img_url)s'),
            ('#tmb#','%(img_thumb_url)s'),
            ('#file#','%(filename)s'),
            #TODO: Надо бы придумать потом что нить с этим...
            #('#size#','%(size)s'),
            #('#h#', '%(height)s'),
            #('#w#', '%(width)s'),
            )
            self.rule = usr.replace('#url#','%(img_url)s').replace('#tmb#','%(img_thumb_url)s').replace('#file#','%(filename)s')
            return True
        else:
            return None

    def get_out(self, img_url='', img_thumb_url='', filename=''):
        if not self.rule:
            return '%s'%img_url
        else:
            return self.rule%({'img_url': img_url, 'img_thumb_url': img_thumb_url ,'filename': filename })

class UimgeError( Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr( "%s\n"%self.value )


def make_thumb(obj, size):
    if Image:
        #FIXME: make crossplatform
        tmb = Image.open( obj)
        tmb.thumbnail( (size, size), Image.ANTIALIAS)
        thumb = NamedTemporaryFile(
                prefix='thumb_',
                suffix= '.png')
        tmb.save( thumb.file,'PNG')
        thumb.seek(0)
        del tmb
        return thumb.name, thumb
    else:
        print "Not installed pil"

class Uimge:
    '''
    Usage:
    >>> import uimge
    >>> u = uimge.Uimge()
    >>> u.set_host( uimge.Hosts.s_smages )
    <class uimge.smages.com at 0x8541a4c>
    >>> u.upload( 'http://github.com/images/modules/header/logov3.png')
    True
    >>> u.get_urls()
    ('http://smages.com/i/ba/76/ba7669f248a8661836d6747b3fe89771.png', 'http://s
    mages.com/t/ba/76/ba7669f248a8661836d6747b3fe89771.jpg')

    '''

    current_host=None
    proxy_type = ['socks','http']
    options = dict(
                    proxy      = False,
                    proxy_port = None,
                    proxy_type = None,
                    #
                    thumb      = False,
                    thumb_size = 200,
                    thumb_func = make_thumb,


                    )

    def __init__(self, host=None, obj=None, proxy=None, proxy_port=None, proxy_type=None):
        if host:
            self.set_host( host )
        if proxy:
            self.set_proxy( proxy, proxy_port, proxy_type)
        if obj:
            self.upload(obj)
    def setup(self, **kwargs):
        self.options.update( kwargs)

    def set_host(self, host):
        if Hosts.hosts_dict.get(host.key):
            self.current_host=host
            return self.current_host
        else:
            raise Exception( 'Host not is class')


    def _ufopen(self, _url, _filename ):
        '''Open url and save in tempfile'''
        import urllib
        __t = NamedTemporaryFile(prefix='',suffix= _filename )
        __t.write( urllib.urlopen(_url).read())
        __t.seek(0)
        return __t.name, __t

    def _uploaded(self, obj, host):
        host.upload(obj)
        host.send_post()
        host.postload()
        res =  host.img_url, host.img_thumb_url, host.filename
        del host
        return res

    def upload(self,obj):
        '''
        upload( fb ) -> dict response
        '''

        if not self.current_host:
            raise UimgeError('Not select host')

        try:
            self.filepath = obj
            img_url= None
            img_thumb_url=None
            temp_obj = None
            thumb_obj = None

            host = self.current_host()
            self.filename = os.path.split( obj )[1]
            # thumb option
            if not self.options.get('thumb'):
                if not host.as_url and self.isurl( obj):
                     obj, temp_obj = self._ufopen( obj,  self.filename)
                self.img_url , self.img_thumb_url, self.filename = self._uploaded( obj, host)
            else:
                if self.isurl(obj):
                     obj, temp_obj = self._ufopen( obj, self.filename)

                thumb_path, thumb_obj = self.options['thumb_func']( obj, self.options.get( 'thumb_size') )

                self.img_url , self.img_thumb_url, self.filename = self._uploaded( obj, host)
                self.img_thumb_url = self._uploaded( thumb_path, host)[0]

            response = {'img_direct_url': self.img_url,
                        'img_thumb_url': self.img_thumb_url,
                        'img_file_name': self.filename,
                        'img_file_path': self.filepath,
                    }
            if temp_obj:
                temp_obj.close()
            if thumb_obj:
                thumb_obj.close()

#            del host, temp_obj, thumb_obj
            return type( self.current_host.host,(dict,),{})( response )

        except ( IndexError,KeyError,IndexError, UploaderError  ) as e:
            raise UimgeError('Uimge: upload error %s'%obj )

    def clear(self):
        '''Featres:
        delete temp file and temp obj'''
        pass

    def isurl(self, string):
        ''' Return True if then url else False '''
        return not not [True for s in 'http://','ftp://','https://' if string.startswith(s) ]


    def cancel(self):
        self._host.cancel()

    def get_thumb_url( self ):
        return self.img_thumb_url

    def get_img_url( self):
        return self.img_url

    def get_urls( self):
        return self.img_url, self.img_thumb_url




class Hosts:
    '''
    `hosts_dict` - dict hosts '`short_key`_`long_key`': hostclassobj
    '''
    pass

def get_hosts():
    hosts = 'hosts'
    this_dir = os.path.split(__file__)[0]
    if this_dir:
        list_hosts = os.listdir(this_dir+os.path.sep+hosts)
    else:
        list_hosts = os.listdir( hosts)
    os.sys.path.append( this_dir )
    modules= []
    hosts_obj = {}
    dev_hosts = {}
    for fname in list_hosts:
        if fname.endswith('.py') and not fname.startswith('__init__'):
            module_name = fname[:-3]
            str_module = hosts+'.'+module_name
            package = __import__(str_module)
            modules.append( module_name )
    for module_name in modules:
        module_obj = getattr( package, module_name)
        for elem in dir(module_obj):
            obj = getattr( module_obj, elem)
            if inspect.isclass(obj):
                obj_name = obj.__name__
                if obj_name.startswith('Host'):
                    host_key = '_'.join( (obj.short_key,obj.long_key) )
                    setattr( obj, "key", host_key )
                    if not obj.dev_mode:
                        setattr( Hosts, host_key , obj )
                        hosts_obj.update({ host_key : obj })
                    else:
                        dev_hosts.update({ host_key : obj })
    setattr( Hosts, 'hosts_dict', hosts_obj )
    setattr( Hosts, 'dev_hosts_dict', dev_hosts )

get_hosts()

def host_test_all(option=None, opt_str=None, value=None, parser=None, *args, **kwargs):
    u = Uimge()
    for H in Hosts.hosts_dict.values():
        h = H()
        h.test_file()
        h.test_url()
        print '--'
    for H in Hosts.dev_hosts_dict.values():
        print H.key, 'http://', H.host
        print '--'
    os.sys.exit(1)


def main():
    pass


if __name__ == '__main__':
    host_test_all()
    main()

