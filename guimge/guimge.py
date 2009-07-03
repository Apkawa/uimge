#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    This file is part of uimge.

    Uploader picture to different imagehosting Copyright (C) 2008 apkawa@gmail.com

    uimge is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

    site project http://wiki.github.com/Apkawa/uimge
'''

import sys
import os



import gtk
import gtk.glade
import gobject
#gtk.gdk.threads_init()

#TODO: Сделать относительные пути импорта

sys.path.insert(0, os.path.abspath('..'+os.path.sep+'uimgepy') )
from uimge import Uimge, Outprint


if not sys.platform == 'win32':
    import pygtk
    pygtk.require('2.0')
    HOME = os.environ['HOME']+os.path.sep

else:
    HOME = os.environ['HOMEDRIVE']+os.environ['HOMEPATH']+os.path.sep
    CONF_FILE = 'guimge.conf'


if __file__.startswith('/usr/bin/'):
    DATA_DIR = '/usr/share/guimge/'
    CONF_FILE = os.path.join(HOME,'.guimge','guimge.conf')
else:
    DATA_DIR = ''
    CONF_FILE = 'guimge.conf'

GLADE_FILE = '%sguimge.glade'%DATA_DIR
ICONS_DIR = '%sicons'%DATA_DIR

UIMGE = Uimge()
GUIMGE = {'version':'0.1.2-0',}





__hosts = UIMGE.hosts()
HOSTS =dict( [(host.host,key) for key, host in __hosts.items()] )

OUTPRINT = Outprint()

class gUimge:
    lastdir = 'file://'+HOME
    result = []
    guimge_icon_ico = gtk.gdk.pixbuf_new_from_file( ICONS_DIR+os.path.sep+'guimge.ico')
    guimge_icon_png = gtk.gdk.pixbuf_new_from_file( ICONS_DIR+os.path.sep+'guimge.png')


    def __init__(self):
        from ConfigParser import ConfigParser
        self.conf = ConfigParser( )#
        self.conf_default_section = 'defaults'
        if os.path.exists( CONF_FILE ):
            self.conf.read( CONF_FILE)
        else:
            print 'Not found config'
            _defaults={'host':'radikal.ru', 'modeout': ''}
            self.conf.add_section( self.conf_default_section )
            for key, val in _defaults.items():
                self.conf.set( self.conf_default_section, key, val)
        self.default_host = self.conf.get( self.conf_default_section, 'host')
        self.default_modeout = self.conf.get( self.conf_default_section, 'modeout')
        #print self.conf.items( self.conf_default_section)


        self.WidgetsTree = gtk.glade.XML( GLADE_FILE )
        conn = {
            'FileOpen_clicked_cb': self.FileOpen_clicked_cb ,
            'UploadButton_clicked_cb': self.UploadButton_clicked_cb,
            'SelectHost_changed_cb': self.SelectHost_changed_cb,
            'SelectModeOutView_changed_cb': self.SelectModeOutView_changed_cb,
            #'SelectModeOutView_editing_done_cb': self.SelectModeOutView_changed_cb,
            'DelimiterSelect_changed_cb': self.update_result_text,
            'Clipboard_clicked_cb': self.Clipboard_clicked_cb,
            'SettingsToggle_toggled_cb': self.SettingsToggle_toggled_cb,
            'SaveSettings_clicked_cb':self.SaveSettings_clicked_cb,
            'About_clicked_cb': self.About_clicked_cb,
            'FileList_button_press_event_cb':self.FileList_event_cb,
            'FileList_key_press_event_cb':self.FileList_event_cb,
            'ClearFileList_clicked_cb':self.ClearFileList_clicked_cb,
            'gtk_main_quit': gtk.main_quit,
            'exit_event': self.exit_event,
            }
        window = self.WidgetsTree.get_widget( 'gUimge_multiple')
        self.WidgetsTree.signal_autoconnect( conn)
        if (window):
            window.connect("destroy", gtk.main_quit)
        window.set_icon( self.guimge_icon_ico)
        window.show()

        def FileList():
            #http://www.pygtk.org/pygtk2tutorial/sec-CellRenderers.html#sec-CellRendererTypes
            #заполняем список заливок 
            self.store = gtk.ListStore(str,gtk.gdk.Pixbuf, str, str)
            #Test
            #pixbuf = gtk.gdk.pixbuf_new_from_file_at_size( 'c:\\1.jpg', 150, 150)
            #[ self.store.append(['c:\\1.jpg',pixbuf, "test %i"%i,'%i Kb'%i]) for i in xrange(5)]
            #
            tree = self.WidgetsTree.get_widget('FileList')
            tree.set_model( self.store )
            tree.set_rubber_banding(True)
            tree.get_selection().set_mode(gtk.SELECTION_MULTIPLE)

            col = gtk.TreeViewColumn("Name")
            col.set_expand(True)

            render_pixbuf = gtk.CellRendererPixbuf()
            col.pack_start(render_pixbuf, expand=False)
            col.add_attribute(render_pixbuf, 'pixbuf', 1)

            render_text = gtk.CellRendererText()
            col.pack_start(render_text, expand=False)
            col.add_attribute(render_text, 'text', 2)
            tree.append_column(col)

            col = gtk.TreeViewColumn("Size")
            render_text = gtk.CellRendererText()
            col.pack_start(render_text, expand=False)
            col.add_attribute(render_text, 'text', 3)
            tree.append_column(col)

        def initFileListIcons():
            self.store = gtk.ListStore(str,gtk.gdk.Pixbuf, str, str)
            icon_list = self.WidgetsTree.get_widget('FileListIcons')
            icon_list.set_model( self.store)
            icon_list.set_pixbuf_column(1)
            icon_list.set_text_column(2)

        def initSelectHost():
            #Устанавливаем выпадающий список выбора хостингов c иконостасом
            self.SelectHost = self.WidgetsTree.get_widget("SelectHost")
            list_store = gtk.ListStore( gtk.gdk.Pixbuf, str)
            self.SelectHost.set_model( list_store)

            crp = gtk.CellRendererPixbuf()
            self.SelectHost.pack_start(crp,False,)
            self.SelectHost.add_attribute(crp, 'pixbuf', 0)
            crt = gtk.CellRendererText()
            self.SelectHost.pack_start(crt,False)
            self.SelectHost.add_attribute(crt, 'text', 1)

            for ls in HOSTS.keys():
                ico_name = ls+'.ico'
                ico_dir = ICONS_DIR+os.path.sep+'hosts'
                ico_path = ico_dir+os.path.sep+ico_name
                #print ico_path
                if not os.path.exists(ico_path):
                    import urllib
                    u = urllib.urlopen('http://%s/favicon.ico'%ls)
                    print ico_path
                    t = open( ico_path, 'w+b')
                    t.write(u.read())
                    t.close()
                else:
                    pass

                try:
                    ico = gtk.gdk.pixbuf_new_from_file_at_size( ico_path, 16,16)
                except:
                    ico = self.guimge_icon_ico.scale_simple(16,16, gtk.gdk.INTERP_HYPER)
                self.SelectHost.get_model().append( [ico,ls] )
            _active = HOSTS.keys().index( self.default_host)
            #print self.default_host
            self.SelectHost.set_active( _active  )
        initSelectHost()
        initFileListIcons()



        #Устанавливаем список outprint'a
        result_out = self.WidgetsTree.get_widget('SelectModeOutView')
        result_out.set_model( gtk.ListStore( str, str) )
        result_out.get_model().append(['Direct url','False'])
        for k in OUTPRINT.outprint_rules.keys():
            result_out.get_model().append(
                    [OUTPRINT.outprint_rules[k]['desc'].replace('Output in ',''),k ]
                    )

        if not self.default_modeout:
            result_out.set_active( 0 )
        else:
            _active = OUTPRINT.outprint_rules.keys().index( self.default_modeout )
            result_out.set_active( _active )

        #Устанавливаем разделитель.
        self.delim = self.WidgetsTree.get_widget('DelimiterSelect')
        self.delim.append_text('\\n')
        self.delim.set_active(0)

        self.result_text = self.WidgetsTree.get_widget('ResultText')

    def FileOpen_clicked_cb(self, widget):
        print self.lastdir
        chooser = FileChooser(self.lastdir)
        chooser.set_select_multiple(True)
        resp = chooser.run()
        print resp
        if resp == gtk.RESPONSE_OK:
            __file =  chooser.get_filenames()
            self.lastdir = chooser.get_current_folder_uri()
            print __file
            for f in __file:
                f = unicode(f,'utf-8')
                try:
                    pixbuf = gtk.gdk.pixbuf_new_from_file_at_size( f, 150, 150)
                except:
                    'Stock pixbuf'
                    _t = gtk.TreeView()
                    pixbuf = _t.render_icon(
                            gtk.STOCK_MISSING_IMAGE,
                            gtk.ICON_SIZE_DIALOG,
                            None)
                filename =  os.path.split(f)[1]
                image_info = gtk.gdk.pixbuf_get_file_info(f)
                size = '%.2f Kb'%(os.stat(f).st_size/float(1024))
                if image_info:
                    image_size = ' %sx%s'%( image_info[1], image_info[2],)
                    image_mime=   ' '.join( image_info [0]['mime_types'])
                else:
                    image_size = ''
                    image_mime=   ''
                if len(filename) > 31:
                    filename = '%s...%s'%(
                            filename[0:15],filename[-15:],
                            )
                else:
                    filename = '%s'%(
                            filename,
                            )
                title = '%s %s %s\n%s'%( image_size, image_mime, size, filename)
                self.store.append([f, pixbuf, title, size])
        elif resp == gtk.RESPONSE_CANCEL:
            print 'Closed, no files selected'
        if [s for s in self.store]:
            self.WidgetsTree.get_widget('UploadButton').set_sensitive(True)
            self.WidgetsTree.get_widget('ClearFileList').set_sensitive(True)
        else:
           self.WidgetsTree.get_widget('UploadButton').set_sensitive(False)
        chooser.destroy()

    def SelectHost_changed_cb(self, widget):
        #print "sel host"
        print widget.get_active(),widget.get_model()[widget.get_active()][1], widget.name
        self.current_host = widget.get_model()[widget.get_active()][1]
        print self.current_host
        UIMGE.set_host( HOSTS.get( self.current_host ))

    def SelectModeOutView_changed_cb( self, widget):
        #print widget.get_active(),widget.get_active_text(), widget.name
        if widget.get_active() != -1:
            key_out = widget.get_model()[widget.get_active()][1]
            #print key_out
            self.current_modeout = key_out
            OUTPRINT.set_rules(key_out)
        else:
            #print widget.get_active_text()
            self.current_modeout = ''
            OUTPRINT.set_rules(usr=widget.get_active_text())
        self.update_result_text()

    # Key event
    def FileList_event_cb(self,widget, event):
        #print event.hardware_keycode
        #print event.keyval
        if event.keyval == 65535:
            selection = widget.get_selected_items()
            #print selection
            for s in selection:
                self.store.remove( widget.get_model().get_iter( s[0] ) )
            if not [s for s in self.store]:
                self.WidgetsTree.get_widget('UploadButton').set_sensitive(False)
                self.WidgetsTree.get_widget('ClearFileList').set_sensitive(False)
    def ClearFileList_clicked_cb(self, widget):
        self.store.clear()
        self.WidgetsTree.get_widget('UploadButton').set_sensitive(False)
        self.WidgetsTree.get_widget('ClearFileList').set_sensitive(False)



    def exit_event(self, widget, event):
        print widget
        print event.keyval
        if event.keyval == 65307:
            gtk.main_quit()

    def UploadButton_clicked_cb(self, widget):
        #progress = self.WidgetsTree.get_widget('progressbar1')
        objects = [ s[0] for s in self.store]
        self.result = []
        if objects:
            print "Upload!"
            for obj in objects:
                #gtk.gdk.threads_enter()
                #progress.show()
                #gtk.gdk.threads_leave()
                state = UIMGE.upload( unicode(obj, 'utf-8') )
                if state:
                    self.result.append( (
                        UIMGE.img_url,
                        UIMGE.img_thumb_url,
                        UIMGE.filename
                        ) )
                    print self.result
                    self.update_result_text()
                    self.WidgetsTree.get_widget('ResultExpander').set_sensitive(True)
                    self.WidgetsTree.get_widget('Clipboard').set_sensitive(True)

    def update_result_text(self, widget=None):
        _result = self.make_result()
        if _result:
            self.result_text.get_buffer().set_text( _result)
            return True
        else:
            return False

    def make_result(self):
        try:
            _delim = self.delim.get_active_text().replace('\\n','\n')
        except AttributeError:
            _delim = '\n'
        return _delim.join([OUTPRINT.get_out( r[0], r[1], r[2]) for r in self.result] )

    def Clipboard_clicked_cb(self, widget):
        result = self.make_result()
        _clip = gtk.Clipboard()
        _clip.clear()
        _clip.set_text( result )

    def SettingsToggle_toggled_cb(self, widget):
        settings_vbox = self.WidgetsTree.get_widget('SettingVBox')
        if widget.get_active():
            settings_vbox.show()
        else:
            settings_vbox.hide()
    def SaveSettings_clicked_cb(self, widget):
        self.conf.set( self.conf_default_section ,'host',self.current_host)
        self.conf.set( self.conf_default_section ,'modeout',self.current_modeout)
        conf_dir = os.path.split( CONF_FILE)[0]
        if conf_dir:
            os.makedirs( conf_dir)
        self.conf.write( open(CONF_FILE, 'w+b') )
        pass


    def About_clicked_cb(self, widget):
        about = self.WidgetsTree.get_widget('About')
        about.set_logo( self.guimge_icon_png)
        about.set_icon( self.guimge_icon_ico )
        about.set_version( GUIMGE['version'])
        about.run()
        about.hide()


def FileChooser(lastdir=False):
    chooser = gtk.FileChooserDialog(
            title="Select image",
            action=gtk.FILE_CHOOSER_ACTION_OPEN,
            buttons=(
                gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,
                gtk.STOCK_OPEN,gtk.RESPONSE_OK),
                              )
#http://www.pygtk.org/pygtk2tutorial/sec-FileChoosers.html
#        http://pygtk.org/docs/pygtk/class-gtkfilechooser.html
    #Set filters
    list_filters = (
            ("Images",(
                ("image/png","image/jpeg", "image/gif"),
                ("*.png","*.jpg","*.jpeg","*.gif","*.tif","*.tiff","*.bmp") ) ),
            ("PNG",(
                ("image/png",),
                ("*.png",) ) ),
            ("JPG/JPEG",(
                ("image/jpeg",),
                ("*.jpg","*.jpeg",) ) ),
            ("GIF",(
                ("image/gif",),
                ("*.gif",) ) ),
            )

    for f_name, filtr in list_filters:
        _filter = gtk.FileFilter()
        _filter.set_name( f_name )
        for f_mime in filtr[0]:
            _filter.add_mime_type(f_mime)
        for f_pattern in filtr[1]:
            _filter.add_pattern( f_pattern)
        chooser.add_filter(_filter)
    #Set prewiew
    def update_preview( file_chooser, prewiew):
        filename = file_chooser.get_preview_filename()
        try:
            pixbuf = gtk.gdk.pixbuf_new_from_file_at_size( filename, 200, 200)
            prewiew.set_from_pixbuf( pixbuf)
            have_preview = True
        except:
            have_preview = False
        file_chooser.set_preview_widget_active(have_preview)
        return
    if lastdir:
        chooser.set_current_folder_uri( lastdir )

    preview = gtk.Image()
    chooser.set_preview_widget( preview )
    chooser.connect("update-preview", update_preview ,preview )
    return chooser


if __name__ == "__main__":
    #gobject.threads_init()
    app = gUimge()

    #app = guimge_multiple()
    #gtk.gdk.threads_enter()
    gtk.main()

    #gtk.gdk.threads_leave()

