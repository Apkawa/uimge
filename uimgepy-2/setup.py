from distutils.core import setup
import uimge

import sys

_platform = sys.platform
if _platform != 'win32':
  _lang_path = '/usr/share/locale/%(lang)s/LC_MESSAGES'
else:
  _prefix = sys.prefix
  _lang_path = _prefix+'\\share\\locale\\%(lang)s\\LC_MESSAGES'

setup(name='Uimge',
      version = uimge.VERSION,
      description='uimge',
      author='Apkawa',
      author_email='apkawa@gmail.com',
      url='http://code.google.com/p/uimge/',
      packages=['uimge',],
      license='GPLv3',
      data_files=[
          ( _lang_path%{'lang':'en'} ,['locale/en/LC_MESSAGES/uimge.mo']),
          ( _lang_path%{'lang':'ru'},['locale/ru/LC_MESSAGES/uimge.mo']),
          ],

     )
