#from distutils.core import setup
from setuptools import setup
import uimge

import os

_platform = os.sys.platform
if _platform != 'win32':
  _lang_path = '/usr/share/locale/%(lang)s/LC_MESSAGES'
else:
  _prefix = sys.prefix
  _lang_path = os.path.join(_prefix,'share\\locale\\%(lang)s\\LC_MESSAGES' )

setup(name='uimge',
      version = uimge.VERSION,
      description='uimge - uploader on 14 imagehosting',
      author='Apkawa',
      author_email='apkawa@gmail.com',
      url='http://code.google.com/p/uimge/',
      download_url = 'http://github.com/Apkawa/uimge/',
      packages=['uimge','uimge.hosts'],
      license='GPLv3',
      data_files=[
          ( _lang_path%{'lang':'en'} ,['uimge/locale/en/LC_MESSAGES/uimge.mo']),
          ( _lang_path%{'lang':'ru'},['uimge/locale/ru/LC_MESSAGES/uimge.mo']),
          ],
      entry_points = {
        'console_scripts':[
            'uimge = uimge:main'
        ]
        }


     )
