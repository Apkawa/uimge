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

    site project http://code.google.com/p/uimge/
'''

# напишем небольшой набросок структуры.
#
import os
import urllib2
import optparse
from sys import argv,exit,stderr,stdout

import ihost
import urllib2_file

import gettext

i18l = gettext.translation('uimge')
_ = i18l.ugettext

class Host:
    ihost = None
    img_thumb_url = None
    img_url = None

    def _start(self):
        self.Imagehosts = {}
        import inspect
        __myglobals = dict()
        __myglobals.update( inspect.getmembers(ihost) )
        for key, value in __myglobals.items():
            if key.startswith('Host_'):
                self.Imagehosts.update({key[len('Host_'):]:value})

    def get_hosts_list(self):
        return self.Imagehosts
    def get_host(self, key):
        return self.Imagehosts.get(key)
    def set_host(self, key):
        __ih = self.Imagehosts.get(key)
        if __ih:
            self.ihost = __ih
            return True
        else:
            return False
    def upload( self, upload_obj ):
        _u = self.ihost()
        resp = _u.upload(upload_obj)
        self.img_thumb_url = resp['thumb']
        self.img_url = resp['url']
        return True
    def get_thumb_url( self ):
        return self.img_thumb_url
    def get_img_url( self):
        return self.img_url
    def get_urls( self):
        return self.img_url, self.img_thumb_url

class Uimge( Host ):
    VERSION = '0.06.1.4'
    
    def __init__(self):
        self._start()
        self.key_hosts = '|'.join(['-'+i.split('_')[0] for i in self.Imagehosts.keys()])
        self.version = 'uimge-'+self.VERSION
        self.usage = _('python %%prog [%s] picture')%self.key_hosts
        self.objects = []
    def main(self, _argv):
        self.parseopt(_argv)
        self.set_host( self.opt.check )
        self.read_filelist( self.opt.filelist )
        self.objects.extend( self.arguments )
        print self.objects
        for f in self.objects:
            self.upload( f )
            self.outprint()
    def read_filelist(self, _list):
        if _list:
            print _list
            f = open( _list,'r')
            self.objects.extend( [ i[:-1] for i in f.xreadlines()] )
            f.close()
            return True
        return False

    def outprint(self):
        stdout.write('%s\n'%self.img_url )
        pass
    def parseopt(self, argv):
        parser = optparse.OptionParser(usage=self.usage, version=self.version)
        # Major options
        group_1 = optparse.OptionGroup(parser, _('Major options'))
        _imagehosts_list = self.get_hosts_list()
        for host in _imagehosts_list.keys():
            sp = host.split('_')
            group_1.add_option('-'+sp[0],'--'+sp[1],
                    action='store_const', const=host, dest='check',
                    help='%s %s'%(_('Upload to'),self.Imagehosts[host].host))

        parser.add_option_group(group_1)
    
        # Additional options
        group_2 = optparse.OptionGroup(parser, _('Additional options'))
        group_2.add_option('-f','--file', action='store', default=None, dest='filelist', \
                           help=_('Upload image from list'))
        parser.add_option_group(group_2)
        '''
        group_3 = optparse.OptionGroup(parser, _('Output options'))
        for key in self.Outprint.keys():
            if key != 'default':
                sp = key.split('_')
                if key != 'usr_user-out':
                    group_3.add_option('--'+sp[0],'--'+sp[1],
                            const=key, action='store_const',
                            default='default', dest='out',
                            help=_(self.Outprint[key].get('help') or key))
                else:
                    group_3.add_option('--'+sp[0],'--'+sp[1], action='store',
                            default='default', dest='out',
                            help=_(self.Outprint[key].get('help') or key))

        parser.add_option_group(group_3)
        '''
        self.opt, self.arguments = parser.parse_args(args=argv)
        print self.opt, self.arguments
        if self.opt.check == None:
            print _('No major option! Enter option [%s]...')%self.key_hosts
            parser.print_help()
            exit()


if __name__ == '__main__':
    u = Uimge()
    u.main(argv[1:])
    '''
    _file= '/home/apkawa/pictres/1201337718895.jpeg'
    _url = 'http://i037.radikal.ru/0902/12/36d18ce760e2.jpg'
    for key in u.get_hosts_list():
        print key
        print 'FILE: ', _file
        u.set_host(key)
        u.upload(_file)
        print u.get_urls()
        print 'URL: ', _url
        u.upload(_url)
        print u.get_urls()
    '''
    
