#!/usr/bin/env python
# coding: utf-8
import sys
import os
import threading
import time


import pygtk
pygtk.require('2.0')

import gtk
import gtk.glade
import gobject
        
from uimge import Uimge, Outprint

GLADE_FILE = 'guimge.glade'

UIMGE = Uimge()

__hosts = UIMGE.hosts()
HOSTS =dict( [(host.host,key) for key, host in __hosts.items()] )

OUTPRINT = Outprint()
class gUimge:
    def __init__(self):
        self.current_host = None

        self.result = ''

        self.lastdir = None

        
        _windowname = "gUimge"
        self.WidgetsTree = gtk.glade.XML( GLADE_FILE )
        # Словарик, задающий связи событий с функциями-обработчиками
        con_event = {
                'FileOpen_clicked_cb': self.FileOpen,
                'UploadButton_clicked_cb': self.UploadButton_clicked_cb,
                'SelectHost_changed_cb': self.SelectHost_changed_cb,
                'SelectModeOutView_changed_cb': self.SelectModeOutView_changed_cb,
                'SelectModeOutView_editing_done_cb': self.SelectModeOutView_changed_cb,
                'Clipboard_clicked_cb': self.Clipboard_clicked_cb,
                'About_clicked_cb': self.About_clicked_cb,
                'Exit_clicked_cb': gtk.main_quit,
                }
        # Магическая команда, соединяющая сигналы с обработчиками
        self.WidgetsTree.signal_autoconnect( con_event)
        # Соединяем событие закрытия окна с функцией завершения приложения
        self.window = self.WidgetsTree.get_widget( _windowname)
        if (self.window):
            self.window.connect("destroy", gtk.main_quit)


        self.File_or_URL = self.WidgetsTree.get_widget("File_or_URL")
        #statusbar
        self.statusbar =  self.WidgetsTree.get_widget("StatusBar")
        self.statusbar.push( 1, 'Please select file or url and push button "Upload".')


        #Устанавливаем выпадающий список выбора хостингов
        self.SelectHost = self.WidgetsTree.get_widget("SelectHost")
        for ls in HOSTS.keys():
            self.SelectHost.append_text( ls )
        _active = HOSTS.values().index('r_radikal')
        self.SelectHost.set_active( _active  )
        
        self.upload_progress = self.WidgetsTree.get_widget( "UploadProgress")


        #Устанавливаем список outprint'a
        result_out = self.WidgetsTree.get_widget('SelectModeOutView')
        result_out.append_text( 'Direct url' )
        for k in OUTPRINT.outprint_rules.keys():
            result_out.append_text( k )
        result_out.set_active( 0 )
        
        #Это извращенный способ установить свою надбись к стоковой кнопке =_=
        upload_button = self.WidgetsTree.get_widget("UploadButton")
        print upload_button.get_children()[0].get_children()[0].get_children()[1].set_label("Upload")
        #upload_button.set_label("Upload")

        self.window.show()


    def FileOpen(self, widget):
        chooser = FileChooser(lastdir=self.lastdir)
        resp = chooser.run()
        if resp == gtk.RESPONSE_OK:
            __file =  chooser.get_filename()
            self.lastdir = chooser.get_current_folder_uri()
            print __file
            self.File_or_URL.set_text(__file)
            self.statusbar.push(1, 'Push button \"Upload\"')

        elif resp == gtk.RESPONSE_CANCEL:
            print 'Closed, no files selected'
        chooser.destroy()

    def SelectHost_changed_cb(self, widget):
        #print "sel host"
        print widget.get_active(),widget.get_active_text(), widget.name
        self.current_host = widget.get_active_text()
        UIMGE.set_host( HOSTS.get(widget.get_active_text()) )

    def SelectModeOutView_changed_cb( self, widget):
        #print widget.get_active(),widget.get_active_text(), widget.name
        if widget.get_active() != -1:
            OUTPRINT.set_rules(widget.get_active_text())
        else:
            OUTPRINT.set_rules(usr=widget.get_active_text())
        if self.result:
            self.result = OUTPRINT.get_out( UIMGE.img_url, UIMGE.img_thumb_url, UIMGE.filename )
            res = self.ViewResultUrl.get_buffer()
            res.set_text( self.result)

    def progress(self):
        def rel():
            self.upload_progress.pulse()
            return True
        self.upload_progress.show()
        nya = gobject.timeout_add(50, rel)
        return True


    def UploadButton_clicked_cb(self, widget):
        #gobject.timeout_remove( nya )
        #self.upload_progress.hide()
        obj = self.File_or_URL.get_text()
        if obj:
            print "Upload!"
            if UIMGE.upload( obj ):
                self.result = OUTPRINT.get_out( UIMGE.img_url, UIMGE.img_thumb_url, UIMGE.filename )
                self.statusbar.push( 1, 'file %s uploading to %s'%( os.path.split(obj)[1], self.current_host ))
                textbuffer = gtk.TextBuffer()
                textbuffer.set_text( self.result )
                self.ViewResultUrl = self.WidgetsTree.get_widget("ViewResultUrl")
                self.ViewResultUrl.set_buffer( textbuffer )
    def Clipboard_clicked_cb(self, widget):
        #print widget
        _clip = gtk.Clipboard()
        _clip.clear()
        _clip.set_text( self.result )

    def About_clicked_cb(self, widget):
        about = self.WidgetsTree.get_widget('About')
        about.run()
        about.hide()




class guimge_multiple:
    lastdir = False
    result = []

    def __init__(self):
        self.WidgetsTree = gtk.glade.XML( GLADE_FILE )
        conn = { 
            'FileOpen_clicked_cb': self.FileOpen_clicked_cb ,
            'UploadButton_clicked_cb': self.UploadButton_clicked_cb,
            'SelectHost_changed_cb': self.SelectHost_changed_cb,
            'SelectModeOutView_changed_cb': self.SelectModeOutView_changed_cb,
            'SelectModeOutView_editing_done_cb': self.SelectModeOutView_changed_cb,
            'Clipboard_clicked_cb': self.Clipboard_clicked_cb,
            'About_clicked_cb': self.About_clicked_cb,
            'FileList_button_press_event_cb':self.FileList_event_cb,
            'gUimge_multiple_key_press_event_cb': self.gUimge_multiple_key_press_event_cb,
            'FileList_key_press_event_cb':self.FileList_event_cb,
            'Exit_clicked_cb': gtk.main_quit,
            }
        window = self.WidgetsTree.get_widget( 'gUimge_multiple')
        self.WidgetsTree.signal_autoconnect( conn)
        if (window):
            window.connect("destroy", gtk.main_quit)
        window.show()

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

        col = gtk.TreeViewColumn("Name")
        col.set_expand(True)

        #render_toggle = gtk.CellRendererToggle()
        #col.pack_start( render_toggle, expand=False)
#    col.add_attribute(render_toggle, 'toggle', 0)
        
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

        col = gtk.TreeViewColumn()
        render_text = gtk.CellRendererPixbuf()
#        col.pack_start(render_text, expand=False)
        col.set_property('pixbuf', pb)

        #col.add_attribute(render_text, 'text', )
        tree.append_column(col)

        #Устанавливаем выпадающий список выбора хостингов
        self.SelectHost = self.WidgetsTree.get_widget("SelectHost")
        for ls in HOSTS.keys():
            self.SelectHost.append_text( ls )
        _active = HOSTS.values().index('r_radikal')
        self.SelectHost.set_active( _active  )
        
        self.upload_progress = self.WidgetsTree.get_widget( "UploadProgress")


        #Устанавливаем список outprint'a
        result_out = self.WidgetsTree.get_widget('SelectModeOutView')
        result_out.append_text( 'Direct url' )
        for k in OUTPRINT.outprint_rules.keys():
            result_out.append_text( k )
        result_out.set_active( 0 )

        

    def FileOpen_clicked_cb(self, widget):
        chooser = FileChooser(self.lastdir)
        chooser.set_select_multiple(True)
        resp = chooser.run()
        if resp == gtk.RESPONSE_OK:
            __file =  chooser.get_filenames()
            self.lastdir = chooser.get_current_folder_uri()
            print __file
            for f in __file:
                pixbuf = gtk.gdk.pixbuf_new_from_file_at_size( f, 100, 100)
                title =  os.path.split(f)[1]
                size = '%.2f Kb'%(os.stat(f).st_size/float(1024))
                self.store.append([f, pixbuf, title,size])
            self.WidgetsTree.get_widget('UploadButton').set_sensitive(True)
        elif resp == gtk.RESPONSE_CANCEL:
            print 'Closed, no files selected'
        chooser.destroy()

    def SelectHost_changed_cb(self, widget):
        #print "sel host"
        print widget.get_active(),widget.get_active_text(), widget.name
        self.current_host = widget.get_active_text()
        UIMGE.set_host( HOSTS.get(widget.get_active_text()) )

    def SelectModeOutView_changed_cb( self, widget):
        #print widget.get_active(),widget.get_active_text(), widget.name
        if widget.get_active() != -1:
            OUTPRINT.set_rules(widget.get_active_text())
        else:
            OUTPRINT.set_rules(usr=widget.get_active_text())
        if self.result:
            pass
            #self.result = OUTPRINT.get_out( UIMGE.img_url, UIMGE.img_thumb_url, UIMGE.filename )
            #res = self.ViewResultUrl.get_buffer()
            #res.set_text( self.result)

# Key event
    def FileList_event_cb(self,widget, event):
        #print event.hardware_keycode
        #print event.keyval
        if event.hardware_keycode == 46:
            selection = widget.get_selection()
            #print selection
            rows = selection.get_selected_rows()
            [ rows[0].remove( rows[0][r].iter ) for r in rows[1]]
            if not [s for s in self.store]:
                self.WidgetsTree.get_widget('UploadButton').set_sensitive(False)

    def gUimge_multiple_key_press_event_cb(self, widget, event):
        if event.hardware_keycode == 27:
            gtk.main_quit()



    def UploadButton_clicked_cb(self, widget):
        objects = [ s[0] for s in self.store]
        self.result = []
        if objects:
            print "Upload!"
            for obj in objects:
                if UIMGE.upload( obj ):
                    self.result.append( (UIMGE.img_url, UIMGE.img_thumb_url, UIMGE.filename) )
                    print self.result
                    self.WidgetsTree.get_widget('Clipboard').set_sensitive(True)

    def Clipboard_clicked_cb(self, widget):
        #print widget
        print self.result
        result = '\n'.join([OUTPRINT.get_out( r[0], r[1], r[2]) for r in self.result] )
        print result
        _clip = gtk.Clipboard()
        _clip.clear()
        _clip.set_text( result )

    def About_clicked_cb(self, widget):
        about = self.WidgetsTree.get_widget('About')
        about.run()
        about.hide()


def FileChooser(lastdir=False):
    chooser = gtk.FileChooserDialog(title="Select image",action=gtk.FILE_CHOOSER_ACTION_OPEN,
                              buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN,gtk.RESPONSE_OK),
                              )
#http://www.pygtk.org/pygtk2tutorial/sec-FileChoosers.html
#        http://pygtk.org/docs/pygtk/class-gtkfilechooser.html
    #Set filters
    list_filters = (
            ("Images",( ("image/png","image/jpeg", "image/gif"), ("*.png","*.jpg","*.jpeg","*.gif","*.tif","*.tiff","*.bmp") ) ),
            ("PNG",( ("image/png",), ("*.png",) ) ),
            ("JPG/JPEG",( ("image/jpeg",), ("*.jpg","*.jpeg",) ) ),
            ("GIF",( ("image/gif",), ("*.gif",) ) ),
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

#experimental









if __name__ == "__main__":
    #gobject.threads_init()
    #app = gUimge()

    app = guimge_multiple()
    #gtk.gdk.threads_enter()
    gtk.main()

    #gtk.gdk.threads_leave()

