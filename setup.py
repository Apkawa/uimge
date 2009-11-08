from setuptools import setup, find_packages
from uimge import uimge

import os

_prefix = os.sys.prefix
_lang_path = os.path.join( _prefix,'share','locale','%(lang)s','LC_MESSAGES' )

setup(name='uimge',
      version = uimge.VERSION,
      description='uimge - this various imagehostings picture uploader',
      author='Apkawa',
      author_email='apkawa@gmail.com',
      url='http://code.google.com/p/uimge/',
      download_url = 'http://github.com/Apkawa/uimge/',
      packages=find_packages(),
      license='GPLv3',
      data_files=[
          ( _lang_path%{'lang':'en'} ,['uimge/locale/en/LC_MESSAGES/uimge.mo']),
          ( _lang_path%{'lang':'ru'},['uimge/locale/ru/LC_MESSAGES/uimge.mo']),
          ],
      entry_points = {
        'console_scripts':[
            'uimge = uimgecli:main'
        ]
        }
     )
