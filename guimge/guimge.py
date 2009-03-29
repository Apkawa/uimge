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


class gUimge:
    def __init__(self):
        self.uimge = Uimge()
        
        __hosts = self.uimge.hosts()
        self.hosts =dict( [(host.host,key) for key, host in __hosts.items()] )

        self.outprint = Outprint()
        self.result = ''
        
        _xml = 'guimge.glade'
        _windowname = "gUimge"
        self.WidgetsTree = gtk.glade.XML( _xml)
        # Словарик, задающий связи событий с функциями-обработчиками
        con_event = {
                'FileOpen_clicked_cb': self.FileOpen,
                'UploadButton_clicked_cb': self.UploadButton_clicked_cb,
                'SelectHost_changed_cb': self.SelectHost_changed_cb,
                'SelectModeOutView_changed_cb': self.SelectModeOutView_changed_cb,
                'SelectModeOutView_editing_done_cb': self.SelectModeOutView_changed_cb,
                'Clipboard_clicked_cb': self.Clipboard_clicked_cb,
                'About_clicked_cb':self.About_clicked_cb,
                'Exit_clicked_cb': gtk.main_quit,
                }
        # Магическая команда, соединяющая сигналы с обработчиками
        self.WidgetsTree.signal_autoconnect( con_event)
        # Соединяем событие закрытия окна с функцией завершения приложения
        self.window = self.WidgetsTree.get_widget( _windowname)
        if (self.window):
            self.window.connect("destroy", gtk.main_quit)


        self.File_or_URL = self.WidgetsTree.get_widget("File_or_URL")

        #Устанавливаем выпадающий список выбора хостингов
        self.SelectHost = self.WidgetsTree.get_widget("SelectHost")
        for ls in self.hosts.keys():
            self.SelectHost.append_text( ls )
        _active = self.hosts.values().index('r_radikal')
        self.SelectHost.set_active( _active  )
        
        self.upload_progress = self.WidgetsTree.get_widget( "UploadProgress")


        #Устанавливаем список outprint'a
        result_out = self.WidgetsTree.get_widget('SelectModeOutView')
        result_out.append_text( 'Direct url' )
        for k in self.outprint.outprint_rules.keys():
            result_out.append_text( k )
        result_out.set_active( 0 )
        
        #Это извращенный способ установить свою надбись к стоковой кнопке =_=
        upload_button = self.WidgetsTree.get_widget("UploadButton")
        print upload_button.get_children()[0].get_children()[0].get_children()[1].set_label("Upload")
        #upload_button.set_label("Upload")


    def FileOpen(self, widget):
        print widget.name
        chooser = gtk.FileChooserDialog(title="Select image",action=gtk.FILE_CHOOSER_ACTION_OPEN,
                                  buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN,gtk.RESPONSE_OK))
#http://www.pygtk.org/pygtk2tutorial/sec-FileChoosers.html
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

        resp = chooser.run()
        if resp == gtk.RESPONSE_OK:
            __file =  chooser.get_filename()
            print __file
            self.File_or_URL.set_text(__file)

        elif resp == gtk.RESPONSE_CANCEL:
            print 'Closed, no files selected'
        chooser.destroy()

    def SelectHost_changed_cb(self, widget):
        #print "sel host"
        print widget.get_active(),widget.get_active_text(), widget.name
        self.uimge.set_host( self.hosts.get(widget.get_active_text()) )
    def SelectModeOutView_changed_cb( self, widget):
        #print widget.get_active(),widget.get_active_text(), widget.name
        if widget.get_active() != -1:
            self.outprint.set_rules(widget.get_active_text())
        else:
            self.outprint.set_rules(usr=widget.get_active_text())
        if self.result:
            self.result = self.outprint.get_out( self.uimge.img_url, self.uimge.img_thumb_url, self.uimge.filename )
            res = self.ViewResultUrl.get_buffer()
            res.set_text( self.result )
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
            if self.uimge.upload( obj ):
                self.result = self.outprint.get_out( self.uimge.img_url, self.uimge.img_thumb_url, self.uimge.filename )
                textbuffer = gtk.TextBuffer()
                textbuffer.set_text( self.result )
                self.ViewResultUrl = self.WidgetsTree.get_widget("ViewResultUrl")
                self.upload_progress.hide()
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


if __name__ == "__main__":
    gobject.threads_init()
    app = gUimge()
    #gtk.gdk.threads_enter()
    gtk.main()

    #gtk.gdk.threads_leave()

