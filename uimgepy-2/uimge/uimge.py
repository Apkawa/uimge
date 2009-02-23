# -*- coding: utf-8 -*-

# напишем небольшой набросок структуры.
#
import ihost
import urllib2
import urllib2_file
'''
import urllib2_file
import urllib2

data = {'name': 'value',
        'file':  open('/etc/services')
       }
data2 = [ 'the bus,     'felt near Coroico',
          'userfile', open('/home/foo/bar.png')
        ]
urllib2.urlopen('http://site.com/script_upload.php', data)


form_vaule = [\
                  ('upload', 'yes'),\
                  ('VM','200'),\
                  ('CP','yes'),\
                 ( 'F', open('/home/apkawa/pictres/1201337718895.jpeg' ,'r') ),
                  ('Submit', '')\
                  ]

'''

class Host:
    ihost = None
    def _start(self):
        self.Imagehosts = {}
        import inspect
        __myglobals = dict()
        __myglobals.update( inspect.getmembers(ihost) )
        for key, value in __myglobals.items():
            if key.startswith('Host_'):
                self.Imagehosts.update({key[len('Host_'):]:value})

        '''
        modules = [self.Imagehosts.update({key[len('Host_'):]:value})
               for key, value in myglobals.items()
               if key.startswith('Host_') ]
        '''
    def get_hosts_list(self):
        return self.Imagehosts
    def get_host(self, key):
        return self.Imagehosts.get(key)
    def set_host(self, key):
        self.ihost = self.Imagehosts.get(key)
        return True
    def upload( self, upload_obj ):
        self._u = self.ihost()
        if upload_obj.startswith('http://'):
            self._u.as_url( upload_obj )
        else:
            self._u.as_file( upload_obj )

        self._u.upload()
    def get_thumb_url( self ):
        return self._u.thumb
    def get_url( self):
        return self._u.url
        pass

class Uimge( Host ):
    def __init__(self):
        self._start()
        pass

if __name__ == '__main__':
    u = Uimge()
    print u.get_hosts_list()
    u.set_host('r_radikal')
    u.upload('/home/apkawa/pictres/1201337718895.jpeg')
    print u.get_url()
    u.upload('http://i037.radikal.ru/0902/12/36d18ce760e2.jpg')
    print u.get_url()
    
