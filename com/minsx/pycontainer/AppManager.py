#! /usr/bin/python
# -*- coding:utf-8 -*-
# Author: Joker
# Copyright (c) 2019 minsx.com All rights reserved.
import os
import time
from threading import Thread

import wx
import sys
import psutil
import logging
import webbrowser
import subprocess
from com.minsx.pycontainer.Logger import Logger
from com.minsx.util import Email
from com.minsx.pycontainer import ConfigManager, DataManager

APP_SERVER_PID_LIST = {}
config = ConfigManager.getSoftConfig()


def getAppServerPidList():
    global APP_SERVER_PID_LIST
    return APP_SERVER_PID_LIST


def setAppServerPidList(appServerPidList):
    global APP_SERVER_PID_LIST
    APP_SERVER_PID_LIST = appServerPidList


def initialAppMenus(self, MainMenu):
    appList = config.get('AppServerList')
    if (appList != None):
        for appName, appInfo in appList.items():
            logo = appInfo.get('logo')
            appMenu = wx.Menu()
            startAppId, showApp, showStatusId, stopAppId = wx.NewId(), wx.NewId(), wx.NewId(), wx.NewId()
            # 启动程序菜单
            appMenu.Append(startAppId, '启动程序')
            # 打开应用页面菜单
            if (satisfyShowApp(appInfo)):
                appMenu.Append(showApp, '显示程序')
                self.Bind(wx.EVT_MENU, lambda event, args=(appName, appInfo): onShowApp(args), id=showApp)
            # 查看状态及退出菜单
            appMenu.Append(showStatusId, '查看状态')
            appMenu.Append(stopAppId, '退出程序')
            self.Bind(wx.EVT_MENU, lambda event, args=(appName, appInfo): onStartApp(args), id=startAppId)
            self.Bind(wx.EVT_MENU, lambda event, args=(appName, appInfo): onShowStatus(args), id=showStatusId)
            self.Bind(wx.EVT_MENU, lambda event, args=(appName, appInfo): onStopApp(args), id=stopAppId)

            MainMenu.Append(wx.NewId(), appName, appMenu)


def satisfyShowApp(appInfo):
    enableShowAppMenu = appInfo.get('EnableShowAppMenu')
    showAppServer = appInfo.get('ShowAppServer')
    return enableShowAppMenu != None and enableShowAppMenu == True and showAppServer != None


def onShowApp(args):
    appInfo = args[1]
    showAppServer = appInfo.get('ShowAppServer')
    if (len(showAppServer) > 8 and showAppServer[:8] == 'OpenWeb:'):
        webbrowser.open(showAppServer[8:])
    else:
        showAppProcess = subprocess.Popen(showAppServer, shell=True)
        showAppProcess.wait()
        showAppProcess.kill()


def onShowStatus(args):
    appName = args[0]
    appServerPids = getAppServerPidList().get(appName)
    statusReport = []
    statusReport.append('应用名：%s\n' % appName)
    existPid = False
    if (appServerPids != None):
        for serverName, serverPids in appServerPids.items():
            if (len(serverPids) > 0):
                statusReport.append('%s服务相关进程信息：\n' % serverName)
            for serverPid in serverPids:
                exist = psutil.pid_exists(serverPid)
                processStatus = '运行中' if exist else '已退出'
                statusReport.append('   进程ID：%s   进程状态：%s\n' % (serverPid, processStatus))
                existPid = True
    if (not existPid):
        statusReport.append('\n该应用没有服务在运行')
    wx.MessageBox(''.join(statusReport), "状态报告：")


def onStopApp(args):
    appName = args[0]
    appServerPids = getAppServerPidList().get(appName)
    stoppedReport = []
    stoppedReport.append('应用名：%s' % appName)
    existStoppedServer = False
    if (appServerPids != None):
        for serverName, serverPids in appServerPids.items():
            for serverPid in serverPids:
                existStoppedServer = True
                isSuccess = killProcess(serverPid)
                result = '退出成功' if isSuccess else '该服务此前已退出'
                stoppedReport.append('\n服务名：%s  进程号：%s  状态：%s' % (serverName, serverPid, result))
                print('the [%s] of [%s] has stopped whose pid is [%s]' % (serverName, appName, serverPid))
            appServerPids[serverName] = []
    if (not existStoppedServer):
        stoppedReport.append('\n无服务需要退出')
    wx.MessageBox(''.join(stoppedReport), "退出报告：")


def onStartApp(args):
    appName = args[0]
    appInfo = args[1]
    singleMode = appInfo.get('SingleMode')
    if (singleMode and existStartedServer(appName)):
        wx.MessageBox('检测到 %s 已被启动过\n且仍有服务正在运行,请先退出程序后再尝试启动！' % appName, "启动报告：")
        return
    serverCommands = appInfo.get('Servers')
    if (getAppServerPidList().get(appName) == None):
        getAppServerPidList()[appName] = {}
    startedReport = []
    startedReport.append('应用名：%s' % appName)
    for serverName, serverCommand in serverCommands.items():
        process = runProcess(serverCommand)
        if (getAppServerPidList()[appName].get(serverName) == None):
            getAppServerPidList()[appName][serverName] = []
        getAppServerPidList()[appName][serverName].append(process.pid)
        startedReport.append('\n服务名：%s  进程ID：%s' % (serverName, process.pid))
        print('the [%s] of [%s] has started whose pid is [%s]' % (serverName, appName, process.pid))
    wx.MessageBox(''.join(startedReport), "启动报告：")


def startContainerSevers():
    appName = 'Container'
    if (getAppServerPidList().get(appName) == None):
        getAppServerPidList()[appName] = {}
    containerSeverList = config.get('ContainerSeverList')
    if (containerSeverList != None):
        for serverName, serverCommand in containerSeverList.items():
            process = runProcess(serverCommand)
            if (getAppServerPidList()[appName].get(serverName) == None):
                getAppServerPidList()[appName][serverName] = []
            getAppServerPidList()[appName][serverName].append(process.pid)
            print('the [%s] of [%s] has started whose pid is [%s]' % (serverName, appName, process.pid))


def startAutoStartedApp():
    appList = config.get('AppServerList')
    if (appList != None):
        for appName, appInfo in appList.items():
            startWithContainer = appInfo.get('StartWithContainer')
            if (startWithContainer != None and startWithContainer):
                serverCommands = appInfo.get('Servers')
                if (getAppServerPidList().get(appName) == None):
                    getAppServerPidList()[appName] = {}
                startedReport = []
                startedReport.append('应用名：%s' % appName)
                for serverName, serverCommand in serverCommands.items():
                    process = runProcess(serverCommand)
                    if (getAppServerPidList()[appName].get(serverName) == None):
                        getAppServerPidList()[appName][serverName] = []
                    getAppServerPidList()[appName][serverName].append(process.pid)
                    startedReport.append('\n服务名：%s  进程ID：%s' % (serverName, process.pid))
                    print('the [%s] of [%s] has started whose pid is [%s]' % (serverName, appName, process.pid))
        # 启动监控
        openAppStatusMonitor()


def existStartedServer(appName):
    appServerInfo = getAppServerPidList().get(appName)
    if (appServerInfo != None):
        for serverName, pids in appServerInfo.items():
            for pid in pids:
                if (psutil.pid_exists(pid)):
                    return True
    return False


def checkBeforeStartingContainer():
    mainPid = DataManager.getAppData().get('MainPid')
    createTime = DataManager.getAppData().get('CreateTime')
    if (mainPid != None and psutil.pid_exists(mainPid) and createTime != None):
        currentProcessCreateTime = psutil.Process(mainPid).create_time()
        if (createTime == currentProcessCreateTime):
            print('the container has been started already and this instance will exit')
            sys.exit(0)
    DataManager.refreshAppData()


def stopAllApp():
    for appName, appServerPids in getAppServerPidList().items():
        if (appServerPids != None):
            for serverName, serverPids in appServerPids.items():
                for serverPid in serverPids:
                    killProcess(serverPid)
                    print('the [%s] of [%s] has stopped whose pid is [%s]' % (serverName, appName, serverPid))
                appServerPids[serverName] = []


def runProcess(serverCommand):
    if (os.path.exists(serverCommand)):
        return subprocess.Popen(serverCommand, cwd=os.path.dirname(serverCommand), shell=True)
    else:
        return subprocess.Popen(serverCommand, shell=True)


def killProcess(pid):
    process = subprocess.Popen(("taskkill /pid %s -t -f" % pid), shell=True)
    process.wait()
    return process.returncode == 0


def getAppStatus():
    needAdviced, appStatus = False, {}
    appList = config.get('AppServerList')
    if (appList != None):
        for appName, appInfo in appList.items():
            enableMonitorAdvice = appInfo.get('EnableMonitorAdvice')
            if (enableMonitorAdvice != None and enableMonitorAdvice):
                appServerPids = getAppServerPidList().get(appName)
                if (appServerPids == None or len(appServerPids) == 0):
                    appStatus[appName] = {}
                    needAdviced = True
                else:
                    serverStatus = {}
                    for serverName, serverPids in appServerPids.items():
                        exist = False
                        for serverPid in serverPids:
                            if (psutil.pid_exists(serverPid)):
                                exist = True
                        if (not exist): needAdviced = True
                        serverStatus[serverName] = 'running' if exist else 'stopped'
                    appStatus[appName] = serverStatus
    return needAdviced, appStatus


def monitorAppStatus():
    monitorAdviceConfig = ConfigManager.getSoftConfig().get('MonitorAdvice')
    if (monitorAdviceConfig != None):
        enable = monitorAdviceConfig.get('Enable')
        if (enable != None and enable):
            lastAdvicedTime, lastAppStatus = 0, {}
            time.sleep(30)
            while (True):
                needAdviced, appStatus = getAppStatus()
                same = lastAppStatus.__eq__(appStatus)
                intervalSeconds = monitorAdviceConfig.get('SendEmailIntervalSeconds')
                intervalSeconds = intervalSeconds if intervalSeconds != None else 6 * 3600
                reachTime = time.time() - lastAdvicedTime > intervalSeconds
                if (needAdviced and ((same and reachTime) or not same)):
                    adviceMsg = '监测到指定应用未在运行\n应用状态: %s' % (appStatus)
                    Email.sendAdviceEmail(adviceMsg)
                    lastAdvicedTime = time.time()
                    lastAppStatus = appStatus

                monitorFrequencySeconds = monitorAdviceConfig.get('MonitorFrequencySeconds')
                monitorFrequencySeconds = monitorFrequencySeconds if monitorFrequencySeconds != None else 60
                time.sleep(monitorFrequencySeconds)


def openAppStatusMonitor():
    Thread(target=monitorAppStatus, args=(), daemon=True).start()
