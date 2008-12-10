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
import gettext



i18l = gettext.translation('uimge')
_ = i18l.ugettext

class Input():
    '''Usage:
    > i = input(opt,filename)
    > i.upload()
    '''
    def __init__(self,opt,filenames, host):
        '''__init__(self,opt, filenames)
        Начальная иницилизация'''
        if opt.filelist:
            self.read_list(opt.filelist)
        else:
            self.filenames = filenames
        self.count= 0
        self.url_mode = False
        self.name = None
        self.host = host
        self.out = opt.out
        self.out_eval = None
    def upload(self):
        '''функция заливки изображений или урлов с изображениями'''
        host = self.host()
        for filename in self.filenames:
            self.check(filename)
            yield host.send(filename,self.url_mode)

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


class Main:
    VERSION = '0.06.1.4'
    def __init__(self):
        self.Imagehosts = imagehost.Hosts().get_hosts_list()
        self.Outprint = {
                'default':{
                    'out':'%(url_o)s\n',
                    'help':None},
                'bt_bb-thumb':{
                    'out':'[url=%(url_o)s][img]%(tmb_o)s[/img][/url] ',
                    'help':_('Output in bb code with a preview')},
                'bo_bb-orig':{
                    'out':'[img]%(url_o)s[/img]\n',
                    'help':'Output in bb code in the original amount'},
                'wi_wiki':{
                    'out':'[[%(url_o)s|{{%(tmb_o)s}}]] ',
                    'help': _('Output in bb code in the original amount')},
                'usr_user-out':{
                    'out':'',
                    'help':_('Set user output #url# - original image, #tmb# - preview image   Sample: [URL=%url%][IMG]%tmb%[/IMG][/URL]')},
                }


        self.key_hosts = '|'.join(['-'+i.split('_')[0] for i in self.Imagehosts.keys()])
        self.version = 'uimge-'+self.VERSION
        self.usage = _('python %%prog [%s] picture')%self.key_hosts

        self.count = 0
        self.max_count = 0
        self.url = None

        pass
    def main(self, argv):
        self.parseopt(argv)
        host = self.Imagehosts.get( self.opt.check )
        urls = Input(self.opt, self.arguments, host).upload()
        for url in urls:
            stdout.write(self.outprint(url, self.opt.out))

    def api(self, argv):
        self.parseopt(argv)
        host = self.Imagehosts.get( self.opt.check )
        urls = Input(self.opt, self.arguments, host).upload()
        for url in urls:
            yield self.outprint(url, self.opt.out)

    def outprint(self, url, key):
        url_o = url[0]
        tmb_o = url[1]
        get_out = self.Outprint.get(key)
        if get_out:
            return get_out['out']% locals()
        else:
            regx=sub('\\\\n','\n',sub('#tmb#','%(tmb_o)s',sub('#url#','%(url_o)s', key )))
            return regx%locals()

    def parseopt(self, argv):
        parser = optparse.OptionParser(usage=self.usage, version=self.version)
        # Major options
        group_1 = optparse.OptionGroup(parser, _('Major options'))
        for host in self.Imagehosts.keys():
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
        self.opt, self.arguments = parser.parse_args(args=argv)
        if self.opt.check == None:
            print _('No major option! Enter option [%s]...')%self.key_hosts
            parser.print_help()
            exit()

if __name__ == '__main__':
    try:
        Main().main(argv[1:])
    except KeyboardInterrupt:
        pass
        #stderr.write(_('KeyboardInterrupt\n'))

