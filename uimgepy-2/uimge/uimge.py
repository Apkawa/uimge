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

    site project http://code.google.com/p/uimge/
'''
import os
import urllib2
import optparse
from sys import argv,exit,stderr,stdout

import ihost
import gettext

_ = gettext.translation('uimge').ugettext

class Uploaders:

    def __init__(self):
        self.ihost = None
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
            return self.ihost
        else:
            return False

#TODO: написать класс для апи
class Uimge:
    pass

class UimgeApp:
    "Класс cli приложения"

    VERSION = '0.06.1.4'
    
    def __init__(self):
        self.__uploaders = Uploaders()
        self.Imagehosts = self.__uploaders.Imagehosts

        self.key_hosts = '|'.join(['-'+i.split('_')[0] for i in self.Imagehosts.keys()])
        self.version = 'uimge-'+self.VERSION
        self.usage = _('python %%prog [%s] picture')%self.key_hosts
        self.objects = []
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
                    'desc' : _('Output in bb code with a preview')
                    },
                'wi_wiki':{
                    'rule': '[[%(img_url)s|{{%(img_thumb_url)s}}]]',
                    'desc' : _('Output in doku wiki format code with a preview')
                    },
                
                }
    def main(self, _argv):

        self.parseopt(_argv)
        self.__ihost = self.__uploaders.set_host( self.opt.check )()
        self.read_filelist( self.opt.filelist )
        self.objects.extend( self.arguments )
        #print self.objects
        for f in self.objects:
            self.__ihost.upload( f )
            self.outprint( rule_key =  self.opt.out, usr = self.opt.out_usr, delim = self.opt.out_delim )
    def read_filelist(self, _list):
        if _list:
            #print _list
            f = open( _list,'r')
            self.objects.extend( [ i[:-1] for i in f.xreadlines()] )
            f.close()
            return True
        return False

    def outprint(self, rule_key = None , usr=None, delim='\n',):
        rule = None
        img_url, img_thumb_url = self.__ihost.get_urls()
        filename = ''
        delim = delim.replace( '\\n','\n')

        if usr:
            rule = usr.replace('#url#','%(img_url)s').replace('#tmb#','%(img_thumb_url)s')

        if rule_key:
            stage1 = self.outprint_rules.get( rule_key )
            rule = stage1.get('rule')

        if not rule:
            stdout.write('%s' % img_url )
            stdout.write( delim)
        else:
            stdout.write( rule % ( {'img_url': img_url, 'img_thumb_url': img_thumb_url } ) )
            stdout.write( delim)

    def parseopt(self, argv):
        parser = optparse.OptionParser(usage=self.usage, version=self.version)
        # Major options
        group_1 = optparse.OptionGroup(parser, _('Major options'))
        _imagehosts_list = self.__uploaders.get_hosts_list()
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

        group_3 = optparse.OptionGroup(parser, _('Output options'))
        for key in self.outprint_rules:
            _short_key, _long_key = key.split('_')
            #if key != 'usr_user-out':
            group_3.add_option('--'+ _short_key,'--'+ _long_key,
                        const=key, action='store_const',
                        default=None, dest='out',
                        help= self.outprint_rules[key].get('desc') or key )
        group_3.add_option('--usr','--user-out', action='store',
                    default=None, dest='out_usr',
                    help=_( 'Set user output #url# - original image, #tmb# - preview image   Sample: [URL=#url#][IMG]#tmb#[/IMG][/URL]' ))
        group_3.add_option('-d','--delimiter', action='store',
                    default='\n', dest='out_delim',
                    help=_( 'Set delimiter. Default - "\\n"' ))

        parser.add_option_group(group_3)

        self.opt, self.arguments = parser.parse_args(args=argv)
        #print self.opt, self.arguments
        if self.opt.check == None:
            print _('No major option! Enter option [%s]...')%self.key_hosts
            parser.print_help()
            exit()


if __name__ == '__main__':
    u = UimgeApp()
    u.main(argv[1:])
    
