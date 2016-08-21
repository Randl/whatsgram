#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# A Bot to integrate WhatsApp with Telegram

import logging
import sys

import wgcore.main


def setupLogging():
    consoleHandler = logging.StreamHandler(stream=sys.stdout)
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO,
                        handlers=[consoleHandler])


def main():
    setupLogging()
    wgcore.main.runWhatsgram()

if __name__ == '__main__':
    main()
