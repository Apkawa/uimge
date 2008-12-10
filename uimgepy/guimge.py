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
        self.sel_host()

    def sel_host(self):
        select_host = '''echo "%s" | zenity --list --text="Test" --column="check" --column="lala" --column='None' --radiolist --hide-column='2' '''%( self.hosts)
        self.key =  popen(select_host).read()[:-1]
    def file_select(self):
        sel_file = '''zenity --file-selection --multiple '''
        self.files = popen(sel_file).read()[:-1].split('|')


    def get_to_host(self, args=None):
        import uimge
        self.files.append(self.key)
        self.text_out = uimge.Main().main(self.files)

    def out(self):

        text_out = '''echo "%s" |zenity --text-info'''%''.join(self.text_out)
        popen(text_out)







if __name__ == '__main__':
    main = Zenity()
    main.sel_host()
    main.file_select()
    main.get_to_host()
    main.out()
    pass
