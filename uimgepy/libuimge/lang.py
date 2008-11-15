# -*- coding: utf-8 -*-
from locale import getdefaultlocale

def ru_RU():
    options_help = {'usage':u'Использование: python %prog [-i|-r|-f|-s|-t] картинка',\
                    'Major options':u'Основные опции',\
                    '--ipicture':u'Залить на ipicture.ru',\
                    '--radikal':u'Залить на radikal.ru',\
                    '--imageshack':u'Залить на imageshack.us',\
                    '--tinypic':u'Залить на tinypic.com',\
                    '--smages':u'Залить на smages.com',\
                    '--funkyimg':u'Залить на funkyimg.com',\
                    '--picthost':u'Залить на picthost.ru',\
                    '--photo-cod':u'Залить на avangard.photo.cod.ru',\
                    'Additional options':u'Дополнительные опции',\
                    '--name':u'Добавить свое имя в превью картинки (Требуется PIL)',\
                    '--file':u'Взять список файлов или url из текстового файла.',\
                    '--url-mode':u'Режим перезаливки картинок с других источников в сети.',\
                    'Output options':u'Опции вывода',\
                    '--bb-all':u'Объединяет опции -bo и -bt',\
                    '--bb-thumb':u'Вывести в ввиде BB-кода с превью',\
                    '--bb-orig':u'Вывести в ввиде BB-кода в оригинальном размере',\
                    '--direct-url':u'Прямая ссылка на картинку',\
                    '--user-output':u'Установить свой вид вывода. \n%url% - url к картинке оригинального размера, \n%tmb% - url к превью. \nПример: [URL=%url%][IMG]%tmb%[/IMG][/URL]',\
                }
    error_mesages = {'Enter option':'Нет основных опций! Введите [-i|-r|-f|-s|-t]...',\
                     'ImportError PIL':'Ошибка: Нет модуля Python Imaging Library (PIL)!\nПожалуйста установите его.\n',\
                     'Not support hosting':'Данная операция не позволяется этим хостингом\n',\
                     'file format':'This file not image format\n',\
                 }
    messages={'progress':'Залито %d картинок из %d.\r'}
    return options_help,error_mesages,messages

def en_EN():
    options_help = {'usage':'usage: python %prog [-i|-r|-f|-s|-t] picture',\
                    'Major options':'Major options',\
                    '--ipicture':'Upload to ipicture.ru',\
                    '--radikal':'Upload to radikal.ru',\
                    '--imageshack':'Upload to imageshack.us',\
                    '--tinypic':'Upload to tinypic.com',\
                    '--smages':'Upload to smages.com',\
                    '--funkyimg':u'Upload to funkyimg.com',\
                    '--picthost':u'Upload to picthost.ru',\
                    '--photo-cod':'Upload to avangard.photo.cod.ru',\
                    'Additional options':'Additional options',\
                    '--name':'Adding a name to preview images (Used PIL). Works with [-r|-i]',\
                    '--file':'Upload image from list',\
                    '--url-mode':'Upload by url. Work with [-r|-i]',\
                    'Output options':'Output options',\
                    '--bb-all':'List all the options bb code',\
                    '--bb-thumb':'Output in bb code with a preview',\
                    '--bb-orig':'Output in bb code in the original amount',\
                    '--direct-url':'The withdrawal of direct references to pictures',\
                    '--user-output':'Set user output %url% - original image, %tmb% - preview image   Sample: [URL=%url%][IMG]%tmb%[/IMG][/URL]',\
                }
    error_mesages = {'Enter option':'Enter option [-i|-r|-f|-s|-t]...',\
                     'ImportError PIL':'Error: No module Python Imaging Library (PIL)!\nPlease install it.\n',\
                     'Not support hosting':'This operation does not allow it hosted.\n',\
                     'file format':'This file not image format\n',\
                 }
    messages={'progress':'Upload %d images of %d.\r'}
    return options_help,error_mesages,messages

def check(LANG=getdefaultlocale()[0]):
    if LANG == 'ru_RU':
        return ru_RU()
    else:
        return en_EN()
    
#check(getdefaultlocale()[0])
