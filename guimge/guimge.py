#!/usr/bin/env python
# coding: utf-8
import sys
import os

import pygtk
pygtk.require('2.0')

import gtk
import gtk.glade
        
from uimge import Uimge, Outprint

class gUimge:
    def __init__(self):
        self.uimge = Uimge()
        
        __hosts = self.uimge.hosts()
        self.hosts =dict( [(host.host,key) for key, host in __hosts.items()] )

        self.outprint = Outprint()
        self.result = ''
        
        _xml = 'guimge.glade'
        self.windowname = "gUimge"
        self.WidgetsTree = gtk.glade.XML( _xml)
        # Словарик, задающий связи событий с функциями-обработчиками
        con_event = {
                #'FileChooser_confirm': self.FileOpen,
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
        self.window = self.WidgetsTree.get_widget( self.windowname)
        if (self.window):
            self.window.connect("destroy", self.close_app)


        self.File_or_URL = self.WidgetsTree.get_widget("File_or_URL")

        #Устанавливаем выпадающий список выбора хостингов
        self.SelectHost = self.WidgetsTree.get_widget("SelectHost")

        for ls in self.hosts.keys():
            self.SelectHost.append_text( ls )
        _active = self.hosts.values().index('r_radikal')
        self.SelectHost.set_active( _active  )

        result_out = self.WidgetsTree.get_widget('SelectModeOutView')
        result_out.append_text( 'Direct url' )
        for k in self.outprint.outprint_rules.keys():
            result_out.append_text( k )
        result_out.set_active( 0 )

        upload_button = self.WidgetsTree.get_widget("UploadButton")
        print upload_button.get_children()[0].get_children()[0].get_children()[1].set_label("Upload")
        #upload_button.set_label("Upload")


    def FileOpen(self, widget):
        print widget.name
        chooser = gtk.FileChooserDialog(title=None,action=gtk.FILE_CHOOSER_ACTION_OPEN,
                                  buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN,gtk.RESPONSE_OK))
#http://www.pygtk.org/pygtk2tutorial/sec-FileChoosers.html
#TODO: adding filter

        _filter = gtk.FileFilter()
        _filter.set_name("Images")
        _filter.add_mime_type("image/png")
        _filter.add_mime_type("image/jpeg")
        _filter.add_mime_type("image/gif")
        _filter.add_pattern("*.png")
        _filter.add_pattern("*.jpg")
        _filter.add_pattern("*.gif")
        _filter.add_pattern("*.tif")
        _filter.add_pattern("*.bmp")
        chooser.add_filter(_filter)
        #chooser.set_select_multiple(True)

        resp = chooser.run()
        if resp == gtk.RESPONSE_OK:
            __file =  chooser.get_filename()
            print __file
            self.File_or_URL.set_text(__file)

        elif resp == gtk.RESPONSE_CANCEL:
            print 'Closed, no files selected'
        chooser.destroy()

    def SelectHost_changed_cb(self, widget):
        print "sel host"
        print widget.get_active(),widget.get_active_text(), widget.name
        self.uimge.set_host( self.hosts.get(widget.get_active_text()) )
    def SelectModeOutView_changed_cb( self, widget):
        print widget.get_active(),widget.get_active_text(), widget.name
        if widget.get_active() != -1:
            self.outprint.set_rules(widget.get_active_text())
        else:
            self.outprint.set_rules(usr=widget.get_active_text())
        if self.result:
            self.result = self.outprint.get_out( self.uimge.img_url, self.uimge.img_thumb_url, self.uimge.filename )
            res = self.ViewResultUrl.get_buffer()
            res.set_text( self.result )


    def UploadButton_clicked_cb(self, widget):
        obj = self.File_or_URL.get_text()
        if obj:
            print "Upload!"
            if self.uimge.upload( obj ):
                self.result = self.outprint.get_out( self.uimge.img_url, self.uimge.img_thumb_url, self.uimge.filename )
                textbuffer = gtk.TextBuffer()
                textbuffer.set_text( self.result )
                self.ViewResultUrl = self.WidgetsTree.get_widget("ViewResultUrl")
                self.ViewResultUrl.set_buffer( textbuffer )
    def Clipboard_clicked_cb(self, widget):
        print widget
        _clip = gtk.Clipboard()
        _clip.clear()
        _clip.set_text( self.result )
    def About_clicked_cb(self, widget):
        about = self.WidgetsTree.get_widget('About')
        about.run()
        about.hide()

    def close_app(self, widget):
        gtk.main_quit()

if __name__ == "__main__":
    app = gUimge()
    gtk.main()

    '''
    def text_operation(self,widget):
        "Функция, которая перебрасывает текст туда-сюда"
        # виджет-источник
    	source = self.widgetsTree.get_widget(self.routes[widget.name][0])
        # виджет-получатель
	    destination = self.widgetsTree.get_widget(self.routes[widget.name][1])
        # текстовый буфер источника
	    source_text_buffer = source.get_buffer()
        # массив итераторов границ текста в текстовом буфере источника (начало и конец)
        source_text_buffer_bounds = source_text_buffer.get_bounds()
        # собственно текст
	    source_text = source_text_buffer.get_text(source_text_buffer_bounds[0],
                                                  source_text_buffer_bounds[1])
        # устанавливаем текст в текстовом буфере виджета-получателя
        destination.get_buffer().set_text(source_text)
        # очищаем текстовый буфер источника
        source_text_buffer.set_text('')

    '''
