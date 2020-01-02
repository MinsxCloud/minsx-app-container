#! /usr/bin/python
# -*- coding: utf-8 -*-
# Author: Joker
# Copyright (c) 2018 OpenString. All rights reserved.
import codecs
import os
import shutil


def removeAllWithSelf(dir):
    shutil.rmtree(dir)


def removeAllWithoutSelf(dir):
    removeAllWithSelf(dir)
    if not os.path.exists(dir):
        os.makedirs(dir)


def writeFile(filePath, contents):
    f = codecs.open(filePath, 'w', encoding='UTF-8')
    f.write(contents)
    f.close()


def loadFile(filePath):
    f = codecs.open(filePath, 'r', encoding='UTF-8')
    content = f.read()
    f.close()
    return content

def listAllFilePath(dir):
    allFilePath = []
    for file in os.listdir(dir):
        filePath = os.path.join(dir, file)
        if not os.path.isdir(filePath):
            allFilePath.append(filePath)
        else:
            allFilePath.extend(listAllFilePath(filePath))
    return allFilePath
