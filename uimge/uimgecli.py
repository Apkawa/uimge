#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gettext
import os
from uimge import Uimge, UimgeError, Outprint, Hosts, VERSION, host_test_all

try:
    gettext.install('uimge',unicode=True)
except IOError:
    gettext.install('uimge', localedir = 'locale',unicode=True)

import optparse


class UimgeApp:
    "Класс cli приложения"
    def __init__(self):
        self.out = Outprint()
        self.outprint_rules = self.out.outprint_rules
        self._uimge = Uimge()
        self.Imagehosts = Hosts.hosts_dict
        self.key_hosts = '|'.join(['-'+i.split('_')[0] for i in self.Imagehosts.keys()])
        self.version = 'uimge-'+VERSION
        self.usage = _('python %%prog [%s] picture')%self.key_hosts
        self.objects = []
    def main(self, _argv):
        self.parseopt(_argv)
        self._uimge.set_host( self.Imagehosts.get(self.opt.check) )# , self.opt.thumb_size)
        if self.opt.thumb_size:
            self._uimge.setup( thumb=True, thumb_size=self.opt.thumb_size)
        self.read_filelist( self.opt.filelist )
        self.objects.extend( self.arguments )
        self.out.set_rules( key=self.opt.out, usr=self.opt.out_usr )
        #print self.objects
        for f in self.objects:
            #_p = self.Progress()
            #_p.start()
            try:
                self._uimge.upload( f )
                self.outprint( delim = self.opt.out_delim )
            except UimgeError as e:
                self.error( _('File %s uploading error')%f )
            except KeyboardInterrupt:
                self.error( _("Upload process aborted") )
                os.sys.exit(1)

    def read_filelist(self, _list):
        if _list:
            #print _list
            f = open( _list,'r')
            self.objects.extend( [ i[:-1] for i in f.xreadlines()] )
            f.close()
            return True
        return False

    def outprint(self, delim='\n',):
        img_url = self._uimge.img_url
        img_thumb_url = self._uimge.img_thumb_url
        filename = self._uimge.filename
        delim = delim.replace( '\\n','\n')
        _out = self.out.get_out( img_url, img_thumb_url, filename )
        os.sys.stdout.write( _out )
        os.sys.stdout.write( delim)
    def error( self, msg):
        os.sys.stderr.write( msg+'\n' )
    def parseopt(self, argv):
        parser = optparse.OptionParser(usage=self.usage, version=self.version)
        # Major options
        group_1 = optparse.OptionGroup(parser, _('Major options'))
        for key, host in self.Imagehosts.iteritems():
            short_key, long_key = host.short_key, host.long_key
            if len( short_key) == 1:
                short_key='-'+short_key
            else:# len( short_key ) >= 2:
                short_key = '--'+short_key
            group_1.add_option(short_key,'--'+ long_key,
                    action='store_const', const=key, dest='check',
                    help='%s http://%s'%(_('Upload to'),host.host))

        parser.add_option_group(group_1)

        # Additional options
        group_2 = optparse.OptionGroup(parser, _('Additional options'))
        group_2.add_option('-t','--thumb_size',
                                type="int", action='store', default=None, dest='thumb_size',
                                help=_('Set thumbinal size. (Used PIL)'))

        group_2.add_option('-f','--file',
                            action='store', default=None, dest='filelist', \
                            help=_('Upload image from list'))

        parser.add_option_group(group_2)

        group_3 = optparse.OptionGroup(parser, _('Output options'))
        for key in sorted(self.outprint_rules):
            _short_key, _long_key = key.split('_')
            #if key != 'usr_user-out':
            group_3.add_option('--'+ _short_key,'--'+ _long_key,
                        const=key, action='store_const',
                        default=None, dest='out',
                        help= self.outprint_rules[key].get('desc') or key )
        group_3.add_option('--usr','--user-out', action='store',
                    default=None, dest='out_usr',
                    help=_( 'Set user output #url# - original image, #tmb# - preview image, #file# - filename   Sample: [URL=#url#][IMG]#tmb#[/IMG][/URL]' ))
        group_3.add_option('-d','--delimiter', action='store',
                    default='\n', dest='out_delim',
                    help=_( 'Set delimiter. Default - "\\n"' ) )
        group_3.add_option('--test', action='callback',callback= host_test_all,  help=optparse.SUPPRESS_HELP )

        parser.add_option_group(group_3)

        self.opt, self.arguments = parser.parse_args(args=argv)
        #print self.opt, self.arguments
        if self.opt.check == None:
            print _('No major option! Enter option [%s]...')%self.key_hosts
            parser.print_help()
            exit()


def main():
    u = UimgeApp()
    u.main(os.sys.argv[1:])

if __name__ == '__main__':
    main()
    #host_test_all()
