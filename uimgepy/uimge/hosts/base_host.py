import os
os.sys.path.insert(0, os.path.split(os.path.split(os.path.split( __file__ )[0] )[0])[0] )

from uimge.ihost import test_host as __test_host
def test_host( _name ):
    def __host(host):
        print _name, host
        if _name == '__main__':
            print 'test ', host
            __test_host(host)
        else:
            return host
    return __host


import re
findall = re.findall
