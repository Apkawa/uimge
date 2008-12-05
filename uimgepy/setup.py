from distutils.core import setup
from uimge import Main

setup(name='Uimge',
      version=Main.VERSION,
      description='uimge',
      author='Apkawa',
      author_email='apkawa@gmail.com',
      url='http://code.google.com/p/uimge/',
      packages=['','libuimge',],
      license='GPLv3',
      data_files=[('/usr/bin',['uimge.py']),],

     )
