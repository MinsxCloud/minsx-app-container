#! /usr/bin/python
# -*- coding:utf-8 -*-
# Author: Joker
# Copyright (c) 2019 minsx.com All rights reserved.
import json
import os
import sys
from collections import OrderedDict

from com.minsx.util import FileUtil

SOFT_CONFIG = None
HELP_CONTENT = None
dirName, fileName = os.path.split(os.path.abspath(sys.argv[0]))


def getSoftConfig():
    global SOFT_CONFIG
    if (SOFT_CONFIG == None):
        configStr = FileUtil.loadFile("%s/config/Config.json" % dirName)
        SOFT_CONFIG = json.loads(configStr, object_pairs_hook=OrderedDict)
    return SOFT_CONFIG


def getSoftDir():
    return dirName


def getResourcePath(resourcePath):
    return '%s/resource/%s' % (dirName, resourcePath)


def getHelpContent():
    global HELP_CONTENT
    if (HELP_CONTENT == None):
        HELP_CONTENT = FileUtil.loadFile("%s/config/HelpConfig.txt" % dirName)
    return HELP_CONTENT
