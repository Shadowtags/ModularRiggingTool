import pymel.core as pm

def FindAllModules(_relativeDirectory):
    
    # Search the relative directory for all available modules
    # Return a list of all module names (excluding the ".py" extension)
    returnModules = []
    
    
    allPyFiles = FindAllFiles(_relativeDirectory, ".py")
    
    for f in allPyFiles:
        if f != "__init__":
            returnModules.append(f)
    
    
    return returnModules
    
    

def FindAllFiles(_relativeDirectory, _fileExtension):
    
    # Search the relative directory for all files with the given extension
    # Return a list of all file names, excluding the file extension
    allFiles = []
    returnFiles = []
    
    import os
    
    fileDirectory = "%s/%s/" %(os.environ["RIGGING_TOOL_ROOT"], _relativeDirectory)
    
    allFiles = os.listdir(fileDirectory)
    
    
    # refine all files, listing only those of the specific file extension
    for f in allFiles:
        splitString = str(f).rpartition(_fileExtension)
        
        if not splitString[1] == '' and splitString[2] == '':
            returnFiles.append(splitString[0])
    
    
    return returnFiles


def FindHighestTrailingNumber(_names, _basename):
    
    import re
    
    
    highestValue = 0
    
    for n in _names:
        if n.find(_basename) == 0:
            suffix = n.partition(_basename)[2]
            
            if re.match("^[0-9]*$", suffix):
                numericalElement = int(suffix)
                
                if numericalElement > highestValue:
                    highestValue = numericalElement
    
    return highestValue



def StripLeadingNamespace(_nodeName):
    
    if str(_nodeName).find(':') == -1:
        return None
    
    splitString = str(_nodeName).partition(':')
    
    return [splitString[0], splitString[2]]


def BasicStrechyIK(_rootJoint, _endJoint, _container = None, _lockMinimumLength = True, _poleVectorObject = None, _scaleCorrectionAttribute = None):
    
    containedNodes = []
    
    # Create RP IK on joint chain
    ikNodes = pm.ikHandle(startJoint = _rootJoint, endEffector = _endJoint, solver = 'ikRPsolver', name = "%s_ikHandle" %_rootJoint)
    ikNodes[1] = pm.rename(ikNodes[1], "%s_ikEffector" %_rootJoint)
    ikHandle = ikNodes[0]
    ikEffector = ikNodes[1]
    
    pm.setAttr("%s.visibility" %ikHandle, 0)
    
    containedNodes.extend(ikNodes)
    
    # Create polevector locator
    if _poleVectorObject == None:
        
        _poleVectorObject = pm.spaceLocator(name = "%s_poleVector" %ikHandle)
        containedNodes.append(_poleVectorObject)
        
        pm.xform(_poleVectorObject, worldSpace = True, absolute = True, translation = pm.xform(_rootJoint, query = True, worldSpace = True, translation = True))
        pm.xform(_poleVectorObject, worldSpace = True, relative = True, translation = [0.0, 1.0, 0.0])
        
        pm.setAttr("%s.visibility" %_poleVectorObject, 0)
    
    
    poleVectorConstraint = pm.poleVectorConstraint(_poleVectorObject, ikHandle)
    containedNodes.append(poleVectorConstraint)
    
    # Create root and end locators
    rootLocator = pm.spaceLocator(name = "%s_rootPosLocator" %_rootJoint)
    rootLocator_pointConstraint = pm.pointConstraint(_rootJoint, rootLocator, maintainOffset = False, name = "%s_pointConstraint" %rootLocator)
    
    endLocator = pm.spaceLocator(name = "%s_endPosLocator" %_rootJoint)
    pm.xform(endLocator, worldSpace = True, absolute = True, translation = pm.xform(ikHandle, query = True, worldSpace = True, translation = True))
    ikHandle_pointConstraint = pm.pointConstraint(endLocator, ikHandle, maintainOffset = False, name = "%s_pointConstraint" %endLocator)
    
    containedNodes.extend([rootLocator, endLocator, rootLocator_pointConstraint, ikHandle_pointConstraint])
    
    pm.setAttr("%s.visibility" %rootLocator, 0)
    pm.setAttr("%s.visibility" %endLocator, 0)
    
    if _container != None:
        pm.container(_container, edit = True, addNode = containedNodes, includeHierarchyBelow = True)
    
    returnDict = {}
    returnDict["ikHandle"] = ikHandle
    returnDict["ikEffector"] = ikEffector
    returnDict["rootLocator"] = rootLocator
    returnDict["endLocator"] = endLocator
    returnDict["poleVectorObject"] = _poleVectorObject
    returnDict["ikHandle_pointConstraint"] = ikHandle_pointConstraint
    returnDict["rootLocator_pointConstraint"] = rootLocator_pointConstraint
    
    return returnDict


def ForceSceneUpdate():
    
    pm.setTool("moveSuperContext")
    nodes = pm.ls()
    
    for node in nodes:
        pm.select(node, replace = True)
    
    
    pm.select(clear = True)
    pm.setTool("selectSuperContext")
    