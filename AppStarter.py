#! /usr/bin/python
# -*- coding:utf-8 -*-
# Author: Joker
# Copyright (c) 2018 OpenString. All rights reserved.
import logging
import traceback

from com.minsx.pycontainer import GUIManager, AppManager

VERSION = '1.0.0'
if __name__ == '__main__':
    logger = logging.getLogger()
    try:
        print('AppName=PyContainer,Version=%s' % VERSION)
        AppManager.checkBeforeStartingContainer()
        AppManager.startContainerSevers()
        AppManager.startAutoStartedApp()
        app = GUIManager.Container()
        app.MainLoop()
    except Exception as e:
        traceback.print_exc()
        logger.error(e)
