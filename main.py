# -*- coding: utf-8 -*-
import sys,os
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtWidgets
import qdarkstyle
import ycphelper
import winreg

class Main(QMainWindow):
    ylandsPath = ''
    rail_user_data = ''
    railidDict = {}
    ycpDict = {}
    ycpGameDict = {}
    ycpCompDict = {}
    ylandDict = {}
    ylandGamelog = ''
    currentRailId = ''
    ui = ycphelper.Ui_MainWindow()
    def __init__(self,parent=None):
        super(Main, self).__init__(parent)
        self.initUI()


    def initUI(self):
        self.InitRaild()

        self.ui.setupUi(self)
        self.ui.comboBox.addItems(list(self.ycpGameDict.keys()))
        self.ui.comboBox.activated[str].connect(self.SetCurrentRailId)
        self.show()
        self.ui.pushButton_3.clicked.connect(self.OpenGameLogTxt)

    def InitRaild(self):
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Rail\YlandsRail")
        value, type = winreg.QueryValueEx(key, "InstallPath")
        if value:
            ylandsPath = value
            rail_user_data = os.path.dirname(ylandsPath) + '\\' + 'rail_user_data\\2000108'

        userRailIdList = os.listdir(rail_user_data)
        for railid in userRailIdList:
            self.railidDict[railid] = rail_user_data + '\\' + railid
            self.ycpGameDict[railid] = rail_user_data + '\\' + railid + '\\' + 'cloud_storage\\files\\Share\\Games'
            self.ylandDict[railid] = rail_user_data + '\\' + railid + '\\' + 'cloud_storage\\files\\Scenarios'
            self.ycpCompDict[railid] = rail_user_data + '\\' + railid + '\\' + 'cloud_storage\\files\\Share\\Compositions'
            self.ylandGamelog = os.path.dirname(ylandsPath) + '\\' + "艾兰岛(2000108)"

    def OpenGameYCPDir(self):
        path = self.ycpGameDict[self.currentRailId]
        if path:
            if not os.path.exists(path):
                os.makedirs(path, mode=0o777)
            os.system("explorer.exe %s" % path)

    def OpenYLANDDir(self):
        path = self.ylandDict[self.currentRailId]
        if path:
            if not os.path.exists(path):
                os.makedirs(path, mode=0o777)
            os.system("explorer.exe %s" % path)

    def OpenCompYCPDir(self):
        path = self.ycpCompDict[self.currentRailId]
        if path:
            if not os.path.exists(path):
                os.makedirs(path, mode=0o777)
            os.system("explorer.exe %s" % path)

    def OpenGameLogTxt(self):
        path = self.ylandGamelog
        if path:
            os.system("explorer.exe %s" % path)





    def SetCurrentRailId(self, text):
        self.currentRailId = text
        if self.ui.comboBox.currentIndex() != 0:
            self.ui.pushButton.clicked.connect(self.OpenGameYCPDir)
            self.ui.pushButton_2.clicked.connect(self.OpenYLANDDir)
            self.ui.pushButton_4.clicked.connect(self.OpenCompYCPDir)
        else:
            self.ui.pushButton.clicked.disconnect(self.OpenGameYCPDir)
            self.ui.pushButton_2.clicked.disconnect(self.OpenGameLogTxt)
            self.ui.pushButton_4.clicked.disconnect(self.OpenCompYCPDir)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    ex = Main()
    sys.exit(app.exec_())