#!/usr/bin/python
from os import popen
from libuimge import imagehost
from sys import argv
import re


class Zenity:
    def __init__(self):
        self.zenity = popen('whereis zenity').read()
        if re.search('not found', self.zenity):
            exit()
        hosts = imagehost.Hosts().get_hosts_list()
        hosts = [ '\n'.join(
            ('None\n-'+i.split('_')[0], hosts.get(i).host)
            ) for i in hosts]
        self.hosts = '\n'.join(hosts)

    def main(self):
        self.sel_file()
        self.sel_host()
        self.put_to_host()
        self.out()

    def sel_host(self):
        select_host = '''echo "%s" | zenity --list --text="Test" --column="check" --column="lala" --column='None' --radiolist --hide-column='2' '''%( self.hosts)
        self.key =  popen(select_host).read()[:-1]
    def sel_file(self):
        sel_file = '''zenity --file-selection --multiple '''
        self.files = popen(sel_file).read()[:-1].split('|')


    def progress(self,count, max_count):
        cmd = '''zenity --progress --auto-close --percentage=%i'''
        percent = count*100/3
        popen(cmd%percent)

    def put_to_host(self, args=None):
        import uimge
        max_count = len(self.files)
        self.files.append(self.key)
        uimge = uimge.Main()
        urls = uimge.api(self.files)
        print max_count
        count = 0
        self.text_out = []
        for url in urls:
            #self.progress(count,max_count)
            self.text_out.append(url)
            count += 1
            print count
        print self.text_out
        self.text_out = ''.join(self.text_out)
        return 1

    def out(self):

        text_out = '''echo "%s" |zenity --text-info'''%self.text_out
        popen(text_out)


if __name__ == '__main__':
    main = Zenity()
    main.main()
    pass
