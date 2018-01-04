# todo: add the start and end frame layout
# todo : run the export function through button


import maya.cmds as cmd
import maya.OpenMaya as api

import fbxExporterUI

import maya.OpenMaya as OpenMaya
import fbxExporterUtil
import os



winSelectCallback = None
sceneUpdateSelectCallback = None

#initialize Scene
#todo  1. select event 2.scene type 3.export Info
def initializeFile():

    global isAnimation
    global endFrame
    global fileInfo
    global fbxPreset
    # path

    fileInfo = fbxExporterUtil.getFileInfo()

    savedPath = win.loadPath()

    if savedPath == '':
        targetPath = fileInfo[2]
    else:
        targetPath = savedPath + fileInfo[2].split('/')[-1]
        print targetPath

    endFrame = 0
    win.setTargetPath(targetPath)
    fbxPreset = geometryFBXPreset
    isAnimation = False

def initializeWin():

    cleanSlectCallback()
    initializeFile()
    cmd.button(win.fbxExExportBtn, edit = True, c = export)


def cleanSlectCallback():
    global winSelectCallback
    global sceneUpdateSelectCallback
    global fileOpenCallback

    if winSelectCallback != None:
        OpenMaya.MMessage.removeCallback(winSelectCallback)
        winSelectCallback = None
    if sceneUpdateSelectCallback != None:
        OpenMaya.MMessage.removeCallback(sceneUpdateSelectCallback)
        sceneUpdateSelectCallback = None
    if fileOpenCallback != None:
        api.MSceneMessage.removeCallback(fileOpenCallback)
        fileOpenCallback = None



def updateExportSelection():
    global root
    global fbxPreset
    global isAnimation
    global endFrame

    root = fbxExporterUtil.getSceneRootFromSel()
    if root !=None:
        isAnimation = fbxExporterUtil.getSceneType(root)[0]
        if isAnimation:
            fbxPreset = animationFBXPreset
            endFrame = fbxExporterUtil.getSceneType(root)[1]
            print endFrame

    win.setSceneType(isAnimation)

def export(*args):
    global fileInfo
    global isAnimation
    global fbxPreset
    global endFrame
    global fileInfo
    global root
    # get export path
    userPath = win.getTargetPath()
    checkPath = os.path.dirname(userPath)
    if root == None:
        win.setFbxExInfoContent('please select one object to enable exporting')
    elif not os.path.exists(checkPath):
        win.setFbxExInfoContent('path does not exist')
    else:
        win.setFbxExInfoContent('exporting...')
        # save temp File
        fbxExporterUtil.fileSaveAsCopy(fileInfo[1])
        # export
        fbxExporterUtil.exportSceneFromRoot(root, isAnimation, fbxPreset, 0, endFrame, userPath)
        # restore original file
        fbxExporterUtil.fileRestoreOrigi(fileInfo[0], fileInfo[1])
        # win.setFbxExInfoContent('exported')



def updateSceneSelectCallback(*args, **kwargs):
    updateExportSelection()

def openFileCallback(*args):
    initializeFile()

# window instance for the
def main():
    global win
    global winSelectCallback
    global sceneUpdateSelectCallback
    global fileOpenCallback
    global root
    global animationFBXPreset
    global geometryFBXPreset

    root = None
    winSelectCallback = None
    sceneUpdateSelectCallback = None
    fileOpenCallback = None

    localToolPath = fbxExporterUtil.getLocalToolPath()
    animationFBXPreset = localToolPath +'/presets/IOFBXExportAnimation.fbxexportpreset'
    geometryFBXPreset = localToolPath +'/presets/IOFBXExportGeometry.fbxexportpreset'

    win = fbxExporterUI.fbxExporterWinUI()
    initializeWin()

    cmd.showWindow(win.window)

    cleanSlectCallback()
    cmd.scriptJob( uid = ['fbxExWindow',cleanSlectCallback])
    winSelectCallback = OpenMaya.MEventMessage.addEventCallback("SelectionChanged", win.selectCallback)
    sceneUpdateSelectCallback = OpenMaya.MEventMessage.addEventCallback("SelectionChanged", updateSceneSelectCallback)
    fileOpenCallback = api.MSceneMessage.addCallback(api.MSceneMessage.kAfterOpen, openFileCallback)

reload(fbxExporterUtil)
reload(fbxExporterUI)
reload(fbxExporterUI)
# only for debug
main()