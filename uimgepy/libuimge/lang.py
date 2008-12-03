# -*- coding: utf-8 -*-
from locale import getdefaultlocale

class Lang:

    def __init__(self,LANG=getdefaultlocale()[0]):
        self._LANG = LANG.split('_')[0]
        if 'ru' in LANG:
            self.lang = 0
            self.dict_lang = self.ru_RU()
        else:
            self.lang = 1
            self.dict_lang = self.en_EN()

    def mes(self, en='Unkown string', ru='Неизвестная запись'):
        if self.lang:
            return en
        else:
            return ru
    def errmes(self, en='Unkown string', ru='Неизвестная запись'):
        if self.lang:
            stderr.write(en)
        else:
            return ru
    def get_string(self, key, typ=0):
        try:
            return self.dict_lang[typ][key]
        except KeyError:
            return 'Not found string. %i %s'%(typ,key)

    def get_help_module(self,host):
        string = eval(host.__doc__).get(self._LANG)
        if string:
            return unicode(string, 'utf-8')
        else:
            return unicode('%s %s %s'%(self.mes(),host,host.__doc__), 'utf-8')
    def get_help_outprint(self, func):
        return func.__doc__[self._LANG]



    def ru_RU(self):
        options_help = {'usage':u'Использование: python %prog [-i|-r|-f|-s|-t] картинка',\
                        'Major options':u'Основные опции',\
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


if __name__ == '__main__':
    pass
#check(getdefaultlocale()[0])
