#! /usr/bin/python
# -*- coding:utf-8 -*-
# Author: Joker
# Copyright (c) 2019 minsx.com All rights reserved.
import logging
from com.minsx.pycontainer import ConfigManager


class Logger:

    def __init__(self):
        self.logger = logging.getLogger()
        infoLogPath = '%s/log/info.log' % ConfigManager.getSoftDir()
        fileHandler = logging.FileHandler(infoLogPath)
        self.logger.addHandler(fileHandler)
        self.logger.setLevel(logging.INFO)
