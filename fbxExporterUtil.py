
import sys
import os
import inspect
import pymel.core as pm
import maya.cmds as cmd


def getLocalToolPath():
    localToolPath = os.path.dirname(inspect.getfile(inspect.currentframe())).replace('\\', '/')
    p4Path = os.getenv('P4ROOT')
    if p4Path is not None:
        localToolPath = p4Path
    return localToolPath

def fileSaveAsCopy(path):
    cmd.file(rename=path)
    cmd.file(save=True, type='mayaAscii')

def fileRestoreOrigi(origiPath, copyPath):
    # open the iriginal file and remove the temporary created for exorting
    cmd.file(save=True, de=False, type='mayaAscii')
    cmd.file(origiPath, o=True)
    os.remove(copyPath)

def getFileInfo ():

    print '************************************'
    print 'fbxExporterUtil:::getFileInfo'
    fbxFilePath = ''
    tempFilePath = ''

    currentFilePath = cmd.file(query=True, sceneName=True)

    if currentFilePath !='':
        fbxFilePath = currentFilePath.split('.')[0] + '.fbx'
        # todo : get the tempFile name
        dirPath = os.path.dirname(currentFilePath)
        tempFilePath = dirPath + '/_' + currentFilePath.split('/')[-1]
    return [currentFilePath,tempFilePath,fbxFilePath]


def getSceneRootFromSel():
    print '************************************'
    print 'fbxExporterUtil:::getSceneRootFromSel'
    rootRig = None
    select = len(cmd.ls(sl=True))
    if select!=1:
        return None

    # todo : there are sth wrong with
    _root = []
    baseJoint = cmd.ls(sl=True)[0]

    isNotRoot = True
    while isNotRoot:
        target = cmd.listRelatives(baseJoint, ap=True)
        if target != None:
            _root = target
            baseJoint = target
        else:
            isNotRoot = False

    if len(_root) != 1:
        print ('error : Can not find root')
        sys.exit()

    rootRig = pm.PyNode(_root[0])

    return rootRig

def getSceneType(root):
    print '************************************'
    print 'fbxExporterUtil:::getSceneType'
    isAnimation = False
    animEnd = 0
    for child in [x for x in root.getChildren() if x.nodeType() == 'transform']:
        print child
        # depend on the control grp naming convention,may vary on rig
        # if 'RestPoseGrp' in child.name():
        if '_MAINCtrl' in child.name():
            controlRoot = child
            controlGroup = controlRoot.getChildren(ad=True)
            for ele in controlGroup:
                if ele.type() == 'transform':
                    if cmd.keyframe(ele.name(), query=True, keyframeCount=True) > 0:
                        animEnd = max(animEnd, cmd.findKeyframe(ele.name()))
                        isAnimation = True
    return [isAnimation,animEnd]

# get the skin of given joints (skinJoints)
def getSkinGeometry(skinJoints):
    print '************************************'
    print 'fbxExporterUtil:::getSkinGeometry'
    if len(skinJoints) <1:
        print ('error : no skinned joints, can not bake animation')
        sys.exit()

    localSkinGroup = []
    for jointEle in skinJoints:
        myConnection = jointEle.connections()
        for eleConnect in myConnection:
            if eleConnect.nodeType() == 'skinCluster':
                eleConnect.getGeometry()
                mySkin = eleConnect.getGeometry()
                if mySkin != None and mySkin not in localSkinGroup:
                    localSkinGroup.append(mySkin)
    if len(localSkinGroup) <1:
        print ('error : can not find skinned joints')
        sys.exit()
    else:
        print (localSkinGroup)
    return localSkinGroup

def importFromReference():
    # todo if there are 2 or more reference file...
    print '************************************'
    print 'fbxExporterUtil:::importFromReference'
    if len(cmd.ls(type='reference')) > 0:
        refFile = cmd.referenceQuery(cmd.ls(type='reference')[0], f=True)
        print ('find reference file :'+refFile)
        cmd.file(refFile, importReference=True)
    else:
        print ('no reference found')


def exportSceneFromRoot(root,isAnimation,fbxPreset,startFrame,endFrame,outputFile):
    print '************************************'
    print 'fbxExporterUtil:::exportSceneFromRoot'
    exportGroup = []
    importFromReference()
    for child in [x for x in root.getChildren() if x.nodeType() == 'transform']:
        if 'MAINCtrl' in child.name():
            controlRoot = child
            controlGroup = controlRoot.getChildren(ad=True)

            if isAnimation:
                print ('This scene contain animation')
                print('animation end at :' + str(endFrame))
            else:
                print ('This is a static mesh scene')

        elif 'SHJntGrp' in child.name():

            rrSklJ = child

            if len(child.getChildren(ad=True, type='joint')) > 0:
                skinJoints = child.getChildren(ad=True, type='joint')

                exportGroup.extend(skinJoints)
                pm.mel.FBXLoadExportPresetFile(f=fbxPreset)

                if isAnimation:

                    skinJointsName = [joint.name() for joint in skinJoints]
                    # FBX setting
                    pm.mel.FBXExportInAscii(v=True)
                    pm.mel.FBXExportBakeComplexStart(value=startFrame)
                    pm.mel.FBXExportBakeComplexEnd(value=endFrame)
                    cmd.bakeSimulation(skinJointsName, t=(startFrame, endFrame))

                else:
                    skinGroup = getSkinGeometry(skinJoints)
                    exportGroup.extend(skinGroup)

            for constrainNode in rrSklJ.getChildren(ad=True, type='constraint'):
                cmd.delete(constrainNode.name())

            # get base bone to the top of the hiarachy
            for joint in skinJoints:
                if 'ROOTSHJnt' in joint.name():
                    cmd.parent(joint.name(), world=True)

    if exportGroup:

        pm.select(exportGroup)
        pm.mel.FBXExport(f=outputFile, s=True)