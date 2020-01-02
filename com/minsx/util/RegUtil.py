#! /usr/bin/python
# -*- coding:utf-8 -*-
# Author: Joker
# Copyright (c) 2018 OpenString. All rights reserved.
# import winreg
import subprocess


def existKey(key):
    # reg = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Run")
    # try:
    #     winreg.QueryValueEx(reg, key)
    #     return True
    # except WindowsError as e:
    #     pass
    # finally:
    #     winreg.CloseKey(reg)
    return False


def setBootStarted(key, exePath):
    cmd = 'reg add HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Run /v %s /t REG_SZ /d """"%s""" /regrun /%s" /f'
    process = subprocess.Popen(cmd % (key, exePath, key), shell=True)
    process.wait()
    return process.returncode == 0


def setUnBootStarted(key):
    cmd = 'reg delete HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Run /v %s /f'
    process = subprocess.Popen(cmd % (key), shell=True)
    process.wait()
    return process.returncode == 0
