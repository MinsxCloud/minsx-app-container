#! /usr/bin/python
# -*- coding:utf-8 -*-
# Author: Joker
# Copyright (c) 2019 minsx.com All rights reserved.
import wx
import sys
import wx.adv
import webbrowser
from com.minsx.pycontainer import ConfigManager, AppManager
from com.minsx.util import RegUtil

config = ConfigManager.getSoftConfig()


class ContainerTaskBarIcon(wx.adv.TaskBarIcon):
    # 菜单名
    APP_TITLE = config.get('ContainerName')
    APP_ICON = ConfigManager.getResourcePath(config.get('ContainerLogo'))
    APP_ICON_PNG = ConfigManager.getResourcePath('ContainerLogo.png')
    # 菜单ID
    APP_ID_BOOT_START_SET = wx.NewId()
    APP_ID_Help = wx.NewId()
    APP_ID_EXIT = wx.NewId()
    APP_ID_SHOW = wx.NewId()

    # 初始化
    def __init__(self):
        wx.adv.TaskBarIcon.__init__(self)
        self.SetIcon(wx.Icon(self.APP_ICON), self.APP_TITLE)
        self.Bind(wx.EVT_MENU, self.onbootStartSet, id=self.APP_ID_BOOT_START_SET)
        self.Bind(wx.EVT_MENU, self.onHelp, id=self.APP_ID_Help)
        self.Bind(wx.EVT_MENU, self.onExit, id=self.APP_ID_EXIT)
        self.Bind(wx.EVT_MENU, self.onShow, id=self.APP_ID_SHOW)

    # 创建菜单选项
    def CreatePopupMenu(self):
        menu = wx.Menu()
        AppManager.initialAppMenus(self, menu)
        appList = config.get('AppServerList')
        openWebMenuName = config.get('OpenWebMenuName')
        exitMenuName = config.get('ExitMenuName')
        getHelpMenuName = config.get('GetHelpMenuName')
        bootStartSetMenuName = config.get('BootStartSetMenuName')
        if (appList != None and len(appList) > 0):
            menu.AppendSeparator()
        if (config.get('EnableBootStartSetMenu')):
            menu.Append(self.APP_ID_BOOT_START_SET, bootStartSetMenuName)
        if (config.get('EnableGetHelpMenu')):
            menu.Append(self.APP_ID_Help, getHelpMenuName)
        if (config.get('EnableOpenWebMenu')):
            menu.Append(self.APP_ID_SHOW, openWebMenuName)

        menu.Append(self.APP_ID_EXIT, exitMenuName)
        return menu

    def onbootStartSet(self, event):
        REG_KEY = self.APP_TITLE
        status = RegUtil.existKey(REG_KEY)
        msgContent = '当前状态：{s}\n注：设置开机启动需要以管理员身份运行'.format(s='已设置开机启动' if status else '未设置开机启动')
        msgDialog = wx.MessageDialog(None, msgContent, '开机启动设置:', wx.YES_NO | wx.CANCEL | wx.ICON_INFORMATION)
        msgDialog.SetYesNoCancelLabels('设置开机启动', '关闭开机启动', '取消')
        choice = msgDialog.ShowModal()
        if choice == wx.ID_YES:
            execResult = RegUtil.setBootStarted(REG_KEY, sys.argv[0])
            exist = RegUtil.existKey(REG_KEY)
            msg = '设置成功' if execResult and exist else '设置失败'
            wx.MessageBox(msg, "提示：")
        elif choice == wx.ID_NO:
            execResult = RegUtil.setUnBootStarted(REG_KEY)
            exist = RegUtil.existKey(REG_KEY)
            msg = '设置成功' if execResult and not exist else '设置失败'
            wx.MessageBox(msg, "提示：")
        msgDialog.Destroy()

    def onHelp(self, event):
        # info = wx.adv.AboutDialogInfo()
        # info.SetIcon(wx.Icon(self.APP_ICON_PNG, wx.BITMAP_TYPE_PNG))
        # info.SetDescription(SoftConfigRepository.getHelpContent())
        # info.SetName(self.APP_TITLE)
        # wx.adv.AboutBox(info)
        msgDialog = wx.MessageDialog(None, ConfigManager.getHelpContent(), '帮助说明', wx.OK | wx.ICON_INFORMATION)
        msgDialog.SetIcon(wx.Icon(self.APP_ICON_PNG, wx.BITMAP_TYPE_PNG))
        msgDialog.ShowModal()

    def onExit(self, event):
        AppManager.stopAllApp()
        self.RemoveIcon()
        wx.Exit()

    def onShow(self, event):
        webbrowser.open(config.get('WebAddress'))


class ContainerFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, parent=None)
        ContainerTaskBarIcon()


class Container(wx.App):
    def OnInit(self):
        ContainerFrame()
        return True
