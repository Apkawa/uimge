import os
os.sys.path.insert(0, os.path.split(os.path.split(os.path.split( __file__ )[0] )[0])[0] )

from uimge.ihost import test_host
test_host = test_host

import re
findall = re.findall
