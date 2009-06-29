from distutils.core import setup
import py2exe
import glob

setup(
    name = 'guimge',
    description = 'Multiuploading image',
    version = '0.1.1',

    windows = [
                  {
                      'script': 'guimge.py',
                      #'script':'uimge/uimge.py',
                      'icon_resources': [(1, "icons/guimge.ico")],
                  }
              ],

    options = {
                  'py2exe': {
                      'packages':'encodings',
                    #"excludes": "pango,atk,gobject",
                    #"dll_excludes": [
                    #"iconv.dll","intl.dll","libatk-1.0-0.dll",
                    #"libgdk_pixbuf-2.0-0.dll","libgdk-win32-2.0-0.dll",
                    #"libglib-2.0-0.dll","libgmodule-2.0-0.dll",
                    #"libgobject-2.0-0.dll","libgthread-2.0-0.dll",
                    #"libgtk-win32-2.0-0.dll","libpango-1.0-0.dll",
                    #"libpangowin32-1.0-0.dll"],
                      'includes': 'cairo, pango, pangocairo, atk, gobject',
                  }
              },

    data_files=[   ('icons',glob.glob('icons/*.*'), ),
                    ('icons/hosts',glob.glob('icons/hosts/*.ico'),),
                   ('guimge.glade'),    ]
)
