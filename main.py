#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# A Bot to integrate WhatsApp with Telegram
from gettext import translation

from telegram_bot import *

# _=gettext
localizations_list = ['telegram_bot']

def main():
    run_telegram_bot()


def set_lang(languages):
    global trans

    if languages is not list:
        langs = [languages]
    else:
        langs = languages
    for file in localizations_list:
        try:
            translation(file, 'locale', langs).install()
        except:
            pass

if __name__ == '__main__':
    # localization
    set_lang(['ru_RU'])
    # x = translation('telegram_bot', 'locale', ['ru_RU'])
    #x.install()
    main()
