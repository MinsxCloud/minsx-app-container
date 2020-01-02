#! /usr/bin/python
# -*- coding:utf-8 -*-
# Author: Joker
# Copyright (c) 2019 minsx.com All rights reserved.
import os
import json
import psutil

from com.minsx.util import FileUtil
from com.minsx.pycontainer import ConfigManager

dataFilePath = '%s/config/Data.json' % ConfigManager.getSoftDir()


def getAppData():
    try:
        dataStr = FileUtil.loadFile(dataFilePath)
        data = json.loads(dataStr)
    except Exception:
        data = {}
    return data


def refreshAppData():
    data = {'MainPid': os.getpid(), 'CreateTime': psutil.Process(os.getpid()).create_time()}
    dataStr = json.dumps(data)
    FileUtil.writeFile(dataFilePath, dataStr)
