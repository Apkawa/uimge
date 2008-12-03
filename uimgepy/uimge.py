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



import optparse
from sys import argv,exit,stderr,stdout
from os import stat
from re import sub,search
from libuimge import imagehost
import inspect
import gettext

VERSION = '0.06.1.2'

i18l = gettext.GNUTranslations(open('libuimge/default.mo'))
_ = lambda i: unicode(i18l.gettext(i), 'utf-8')

IMAGEHOSTS = {}
for (name,value) in inspect.getmembers(imagehost):
    if name.startswith('Host_'):
        IMAGEHOSTS[name[len('Host_'):]]= value

OUTPRINT={
            'default': lambda url, eva: stdout.write('%s\n'%url[0]),
            'bt_bb-thumb':  lambda url, eva: stdout.write('[url=%s][img]%s[/img][/url] ' %(url[0], url[1])),
            'bo_bb-orig':  lambda url, eva: stdout.write('[img]%s[/img]\n' %(url[0])),
            'wi_wiki':  lambda url, eva: stdout.write('[[%s|{{%s}}]] ' %(url[0],url[1])),
            'usr_user-output': lambda url, eva: stdout.write(sub('\\\\n','\n',sub('%tmb%',url[1],sub('%url%',url[0], eva))))
          }

class Input():
    '''Usage:
    > i = input(opt,filename)
    > i.upload()
    '''
    def __init__(self,opt,filenames):
        '''__init__(self,opt, filenames)
        Начальная иницилизация'''
        if opt.filelist:
            self.read_list(opt.filelist)
        else:
            self.filenames = filenames
        self.count= 0
        self.url_mode = False
        self.name = None
        self.host = opt.check
        self.out = opt.out
        self.out_eval = None
        if not OUTPRINT.has_key(self.out):
            self.out_eval=self.out
            self.out = 'usr_user-output'
    def upload(self):
        '''функция заливки изображений или урлов с изображениями'''
        host = IMAGEHOSTS[self.host]()
        for filename in self.filenames:
            if not self.check(filename):
                continue
            url = host.send(filename,self.url_mode)
            OUTPRINT[self.out](url,self.out_eval)
        stdout.write('\n')

    def read_list(self,filelist):
        f = open(filelist,'r')
        self.filenames = [ i[:-1] for i in f.xreadlines()]
        f.close()

    def check(self,filename):
        if search('^http\:\/\/',filename): self.url_mode = True
        else: self.url_mode = False
        if not self.url_mode:
            try:
                test=stat(filename)
            except OSError:
                stderr.write( mes('Not found file\n','Файл не найден\n'))
                return False
        return True

class Output:
    def __init__(self):
        OUTPRINT={
                    'default': lambda url, eva: stdout.write('%s\n'%url[0]),
                    'bt_bb-thumb':  lambda url, eva: stdout.write('[url=%s][img]%s[/img][/url] ' %(url[0], url[1])),
                    'bo_bb-orig':  lambda url, eva: stdout.write('[img]%s[/img]\n' %(url[0])),
                    'wi_wiki':  lambda url, eva: stdout.write('[[%s|{{%s}}]] ' %(url[0],url[1])),
                    'usr_user-output': lambda url, eva: stdout.write(sub('\\\\n','\n',sub('%tmb%',url[1],sub('%url%',url[0], eva))))
                  }
        pass
    def main(self):
        pass

    def Out_bt_bbthumb(self, url):
        pass
    def Out_bo_bborig(self):
        pass
    def Out_wi_wiki(self):
        pass
    def Out_usr_useroutput(self):
        pass

class Main:
    def __init__(self):
        self.Outprint = {}
        for key,vaule in inspect.getmembers(Output):
            if key.startswith('Out_'):
                self.Outprint[key[len('Out_'):]] = vaule

        self.Imagehosts = {}
        for (name,value) in inspect.getmembers(imagehost):
            if name.startswith('Host_'):
                self.Imagehosts[name[len('Host_'):]]= value

        self.key_hosts = '|'.join(['-'+i.split('_')[0] for i in self.Imagehosts.keys()])
        self.version = 'uimgepy-'+VERSION
        self.usage = _('python %%prog [%s] picture')%self.key_hosts
        pass
    def main(self, argv):
        self.parseopt(argv)
        Input(self.opt, self.arguments).upload()
        pass
    def parseopt(self, argv):
        parser = optparse.OptionParser(usage=self.usage, version=self.version)
        # Major options
        group_1 = optparse.OptionGroup(parser, _('Major options'))
        for host in self.Imagehosts.keys():
            sp = host.split('_')
            group_1.add_option('-'+sp[0],'--'+sp[1],
                    action='store_const', const=host, dest='check',
                    help='%s %s'%(_('Upload to'),IMAGEHOSTS[host].host))

        parser.add_option_group(group_1)
        # Additional options
        group_2 = optparse.OptionGroup(parser, _('Additional options'))
        group_2.add_option('-f','--file', action='store', default=None, dest='filelist', \
                           help=_('--file'))
        parser.add_option_group(group_2)
        group_3 = optparse.OptionGroup(parser, _('Output options'))
        for key in self.Outprint.keys():
            if key != 'default':
                sp = key.split('_')
                if key != 'usr_user-output':
                    group_3.add_option('--'+sp[0],'--'+sp[1],
                            const=key, action='store_const',
                            default='default', dest='out',
                            help=_(self.Outprint[key].__doc__ or key))
                else:
                    group_3.add_option(
                            '--'+sp[0],'--'+sp[1], action='store',
                            default='default', dest='out',
                            help=_( self.Outprint[key].__doc__ or key))

        parser.add_option_group(group_3)
        self.opt, self.arguments = parser.parse_args(args=argv,)
        if self.opt.check == None:
            print _('No major option! Enter option [%s]...')%self.key_hosts
            parser.print_help()
            exit()
        #return opt, arguments

def parseopt(arg):
    '''Функциия парсинга опций и вывод справки'''
    key_hosts = '|'.join(['-'+i.split('_')[0] for i in IMAGEHOSTS.keys()])
    version = 'uimgepy-'+VERSION
    usage = _('python %%prog [%s] picture')%key_hosts
    parser = optparse.OptionParser(usage=usage, version=version)
    # Major options
    group_1 = optparse.OptionGroup(parser, _('Major options'))
    for host in IMAGEHOSTS.keys():
        sp = host.split('_')
        group_1.add_option('-'+sp[0],'--'+sp[1],
                action='store_const', const=host, dest='check',
                help='%s %s'%(_('Upload to'),IMAGEHOSTS[host].host))

    parser.add_option_group(group_1)
    # Additional options
    group_2 = optparse.OptionGroup(parser, _('Additional options'))
    group_2.add_option('-f','--file', action='store', default=None, dest='filelist', \
                       help=_('--file'))
    parser.add_option_group(group_2)
    group_3 = optparse.OptionGroup(parser, _('Output options'))
    for key in OUTPRINT.keys():
        if key != 'default':
            sp = key.split('_')
            if key != 'usr_user-output':
                group_3.add_option('--'+sp[0],'--'+sp[1], const=key, action='store_const', \
                        default='default', dest='out', help=_('--'+sp[1]))
            else:
                group_3.add_option('--'+sp[0],'--'+sp[1], action='store', \
                        default='default', dest='out', help=_('--'+sp[1]))
    parser.add_option_group(group_3)
    opt, arguments = parser.parse_args(args=arg,)

    if opt.check == None:
        print _('No major option! Enter option [%s]...')%key_hosts
        parser.print_help()
        exit()
    return opt, arguments

if __name__ == '__main__':
    Main().main(argv[1:])
    #opt, filenames = parseopt(argv[1:])
    #inp=Input(opt, filenames)
    #inp.upload()
