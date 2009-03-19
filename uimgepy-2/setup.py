from distutils.core import setup
from uimge import UimgeApp

setup(name='Uimge',
      #version='0.06.1.4',
      version=UimgeApp.VERSION,
      description='uimge',
      author='Apkawa',
      author_email='apkawa@gmail.com',
      url='http://code.google.com/p/uimge/',
      packages=['uimge',],
      license='GPLv3',
      data_files=[
          ('/usr/share/locale/en/LC_MESSAGES',['locale/en/LC_MESSAGES/uimge.mo']),
          ('/usr/share/locale/ru/LC_MESSAGES',['locale/ru/LC_MESSAGES/uimge.mo']),
          ],

     )
