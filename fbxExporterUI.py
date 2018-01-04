import maya.cmds as cmd
import os
import sys
import maya.OpenMaya as OpenMaya

import fbxExporterUtil
# todo: add the start and end frame layout
# todo: link export path data to textField
# todo : run the export function through button

localToolPath = fbxExporterUtil.getLocalToolPath()
savedPath = localToolPath+'/savePath.txt'


class fbxExporterWinUI:

    # todo : runtime error related to the UI element
    def __init__(self):
        self.window = None
        # if self.window!=None:
        #     cmd.deleteUI(self.window, wnd=True)
        if cmd.window('fbxExWindow', query=True, exists=True):
            cmd.deleteUI('fbxExWindow')

        self.window = cmd.window('fbxExWindow', title = 'FBX Exporter', w=300,sizeable = False)
        cmd.columnLayout()
        cmd.separator(h=5)
        cmd.text(label = 'export path')
        cmd.separator(h=5)
        self.fbxExPathTextfield = cmd.textField(w=300)
        cmd.separator(h=5)
        self.savePathButton = cmd.button(l='save export path', h=32, w=300, c=self.fbxSavePath_onClick)
        cmd.separator(h=15)
        cmd.text(label = 'scene type')
        cmd.separator(h=5)
        self.sceneTypeRadioBtn = cmd.radioButtonGrp(labelArray2=['Mesh', 'Animation'], numberOfRadioButtons=2, cat = [1,'both',10])
        cmd.separator(h=15)
        self.fbxExExportBtn = cmd.button( l = 'export',h = 32,w = 300,c=self.fbxExExportBtn_onClick)
        cmd.separator(h=15)
        cmd.text(label = 'export info:')
        cmd.separator(h=15)
        self.fbxExInfoContent = cmd.text(label = 'lalala ')
        self.callBackObj = None

    def fbxExExportBtn_onClick(self,*args):
        print 'export btn clicked'

    def fbxSavePath_onClick(self,*args):
        self.savePath()

    def setTargetPath(self,path):
        if path != None:
            cmd.textField(self.fbxExPathTextfield, edit=True, text=path)

    def getTargetPath(self):
        myPath = cmd.textField(self.fbxExPathTextfield, query=True, text=True)
        return myPath

    def setSceneType(self,isAnimation):
        if isAnimation:
            cmd.radioButtonGrp(self.sceneTypeRadioBtn, edit=True, sl=2)
        else:
            cmd.radioButtonGrp(self.sceneTypeRadioBtn, edit=True, sl=1)

    def setFbxExInfoContent(self, info):
        if info!='' :
            cmd.text(self.fbxExInfoContent, edit=True, label=info)

    def selectCallback(self,*args, **kwargs):
    # def selectCallback(self):
        select = len(cmd.ls(sl=True))
        message = 'error'
        if select == 0:
            message = 'need to select at lease one object'
        elif select == 1:
            message = 'object selected'
            # updateSceneType(cmd.ls(sl=True)[0])
        elif select > 1:
            message = 'please select only one object'
        self.setFbxExInfoContent(message)

    def savePath(self):
        userPath = self.getTargetPath().replace('\\', '/')
        if '.' in userPath :
            print 'this is a file'
            userPath = os.path.dirname(userPath)

        if os.path.exists(userPath):
            if not userPath.endswith('/'):
                userPath = userPath + '/'

            with open(savedPath, 'w') as f:
                f.write(userPath)
                self.setFbxExInfoContent('Path saved')
        else:
            self.setFbxExInfoContent('This is not a valid path')

    def loadPath(self):
        path = ''
        if os.stat(savedPath).st_size != 0:
            with open(savedPath, 'r') as f:
                for line in f:
                    path = line
        return path