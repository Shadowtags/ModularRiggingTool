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



def FindAllModuleNames(_relativeDirectory):
    
    validModules = FindAllModules(_relativeDirectory)
    validModuleNames = []
    
    packageFolder = _relativeDirectory.partition('/Modules/')[2]
    
    for m in validModules:
        mod = __import__("%s.%s" %(packageFolder, m), {}, {}, [m])
        reload(mod)
        
        validModuleNames.append(mod.CLASS_NAME)
    
    return (validModules, validModuleNames)
    

def FindAllFiles(_relativeDirectory, _fileExtension):
    
    # Search the relative directory for all files with the given extension
    # Return a list of all file names, excluding the file extension
    allFiles = []
    returnFiles = []
    
    import os
    #fileDirectory = '%s/nwModularRiggingTool/%s/' %(pm.internalVar(userScriptDir = True), _relativeDirectory)
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



def StripAllNamespaces(_nodeName):
    
    if str(_nodeName).find(':') == -1:
        return None
    
    splitString = str(_nodeName).rpartition(':')
    
    return [splitString[0], splitString[2]]




def BasicStretchyIK(_rootJoint, _endJoint, _container = None, _lockMinimumLength = True, _poleVectorObject = None, _scaleCorrectionAttribute = None):
    
    from math import fabs
    
    containedNodes = []
    
    totalOriginalLength = 0
    done = False
    parent = _rootJoint
    
    childJoints = []
    
    # Measure and store length of each joint segment in joint chain
    while not done:
        children = pm.listRelatives(parent, children = True)
        children = pm.ls(children, type = 'joint')
        
        # Empty list, break loop
        if len(children) == 0:
            done = True
        
        # Loop until end of joint chain
        else:
            child = children[0]
            childJoints.append(child)
            
            totalOriginalLength += fabs(pm.getAttr("%s.translateX" %child))
            
            parent = child
            
            if repr(child) == repr(_endJoint):
                done = True
    
    
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
    
    
    
    # Create distance between node between locators
    rootLocatorWithoutNamespace = StripAllNamespaces(rootLocator)[1]
    endLocatorWithoutNamespace = StripAllNamespaces(endLocator)[1]
    
    moduleNamespace = StripAllNamespaces(_rootJoint)[0]
    
    distNode = pm.shadingNode('distanceBetween', asUtility = True, name = "%s:distBetween_%s_%s" %(moduleNamespace, rootLocatorWithoutNamespace, endLocatorWithoutNamespace))
    containedNodes.append(distNode)
    
    pm.connectAttr("%sShape.worldPosition[0]" %rootLocator, "%s.point1" %distNode)
    pm.connectAttr("%sShape.worldPosition[0]" %endLocator, "%s.point2" %distNode)
    
    scaleAttr = "%s.distance" %distNode
    
    
    # Divide distance by total original length
    scaleFactor = pm.shadingNode('multiplyDivide', asUtility = True, name = "%s_scaleFactor" %ikHandle)
    containedNodes.append(scaleFactor)
    
    pm.setAttr("%s.operation" %scaleFactor, 2) # divide
    pm.connectAttr(scaleAttr, "%s.input1X" %scaleFactor)
    pm.setAttr("%s.input2X" %scaleFactor, totalOriginalLength)
    
    translationDriver = "%s.outputX" %scaleFactor
    
    
    # Connect joint to stretchy calculations
    for joint in childJoints:
        multNode = pm.shadingNode('multiplyDivide', asUtility = True, name = "%s_scaleMultiply" %joint)
        containedNodes.append(multNode)
        
        pm.setAttr("%s.input1X" %multNode, pm.getAttr("%s.translateX" %joint))
        pm.connectAttr(translationDriver, "%s.input2X" %multNode)
        pm.connectAttr("%s.outputX" %multNode, "%s.translateX" %joint)
    
    
    
    if _container != None:
        AddNodeToContainer(_container, containedNodes, _includeHierarchyBelow = True)
    
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
    
    # Select objects in scene with move tool to force an update
    pm.setToolTo("moveSuperContext")
    nodes = pm.ls()
    
    for node in nodes:
        pm.select(node, replace = True)
    
    
    pm.select(clear = True)
    pm.setToolTo("selectSuperContext")



def AddNodeToContainer(_containerName, _nodesIn, _includeHierarchyBelow = False, _includeShapes = False, _force = False):
    
    import types
    
    nodes = []
    
    # create a new list of current list object
    if type(_nodesIn) is types.ListType:
        nodes = list(_nodesIn)
    
    # store current object as a list
    else:
        nodes = [_nodesIn]
    
    # Put maya unit conversion nodes in a list
    conversionNodes = []
    
    for node in nodes:
        node_conversionNodes = pm.listConnections(node, source = True, destination = True)
        node_conversionNodes = pm.ls(node_conversionNodes, typ = 'unitConversion')
        
        conversionNodes.extend(node_conversionNodes)

    
    # Store everything in a single list
    nodes.extend(conversionNodes)
    pm.container(_containerName, edit = True, addNode = nodes, includeHierarchyBelow = _includeHierarchyBelow, includeShapes = _includeShapes, force = _force)



def DoesBlueprintUserSpecifiedNameExist(_name):
    
    pm.namespace(setNamespace = ':')
    namespaces = pm.namespaceInfo(listOnlyNamespaces = True)
    
    names = []
    for namespace in namespaces:
        if namespace.find('__') != -1:
            names.append(namespace.partition('__')[2])
    
    return _name in names


def RP_2segment_stretchy_IK(_rootJoint, _hingeJoint, _endJoint, _container = None, _scaleCorrectionAttribute = None):
    
    moduleNamespaceInfo = StripAllNamespaces(_rootJoint)
    
    moduleNamespace = ""
    if moduleNamespaceInfo != None:
        moduleNamespace = moduleNamespaceInfo[0]
    
    rootLocation = pm.xform(_rootJoint, query = True, worldSpace = True, translation = True)
    elbowLocation = pm.xform(_hingeJoint, query = True, worldSpace = True, translation = True)
    endLocation = pm.xform(_endJoint, query = True, worldSpace = True, translation = True)
    
    # Create Rotate-Plane IK
    ikNodes = pm.ikHandle(startJoint = _rootJoint, endEffector = _endJoint, name = "%s_ikHandle" %_rootJoint, solver = "ikRPsolver")
    ikNodes[1] = pm.rename(ikNodes[1], "%s_ikEffector" %_rootJoint)
    ikHandle = ikNodes[0]
    ikEffector = ikNodes[1]
    
    pm.setAttr("%s.visibility" %ikHandle, 0)
    
    # Create control locators
    rootLocator = pm.spaceLocator(name = "%s_positionLocator" %_rootJoint)
    pm.xform(rootLocator, worldSpace = True, absolute = True, translation = rootLocation)
    pm.parent(_rootJoint, rootLocator, absolute = True)
    
    endLocator = pm.spaceLocator(name = "%s_positionLocator" %ikHandle)
    pm.xform(endLocator, worldSpace = True, absolute = True, translation = endLocation)
    pm.parent(ikHandle, endLocator, absolute = True)
    
    elbowLocator = pm.spaceLocator(name = "%s_positionLocator" %_hingeJoint)
    pm.xform(elbowLocator, worldSpace = True, absolute = True, translation = elbowLocation)
    elbowLocatorConstraint = pm.poleVectorConstraint(elbowLocator, ikHandle)
    
    # Create stretchy setup
    utilityNodes = []
    for locators in ( (rootLocator, elbowLocator, _hingeJoint), (elbowLocator, endLocator, _endJoint) ):
        from math import fabs
        
        
        startLocatorNamespaceInfo = StripAllNamespaces(locators[0])
        startLocatorWithoutNamespace = ""
        
        if startLocatorNamespaceInfo != None:
            startLocatorWithoutNamespace = startLocatorNamespaceInfo[1]
        
        
        endLocatorNamespaceInfo = StripAllNamespaces(locators[1])
        endLocatorWithoutNamespace = ""
        
        if endLocatorNamespaceInfo != None:
            endLocatorWithoutNamespace = startLocatorNamespaceInfo[1]
        
        
        startLocatorShape = "%sShape" %locators[0]
        endLocatorShape = "%sShape" %locators[1]
        
        # Setup utility nodes
        distNode = pm.shadingNode("distanceBetween", asUtility = True, name = "%s:distBetween_%s_%s" %(moduleNamespace, startLocatorWithoutNamespace, endLocatorWithoutNamespace))
        pm.connectAttr("%s.worldPosition[0]" %startLocatorShape, "%s.point1" %distNode)
        pm.connectAttr("%s.worldPosition[0]" %endLocatorShape, "%s.point2" %distNode)
        
        utilityNodes.append(distNode)
        
        scaleFactor = pm.shadingNode("multiplyDivide", asUtility = True, name = "%s_scaleFactor" %distNode)
        utilityNodes.append(scaleFactor)
        
        pm.setAttr("%s.operation" %scaleFactor, 2)  # divide
        originalLength = pm.getAttr("%s.translateX" %locators[2])
        
        pm.connectAttr("%s.distance" %distNode, "%s.input1X" %scaleFactor)
        pm.setAttr("%s.input2X" %scaleFactor, originalLength)
        
        translationDriver = "%s.outputX" %scaleFactor
        
        
        translateX = pm.shadingNode("multiplyDivide", asUtility = True, name = "%s_translationValue" %distNode)
        utilityNodes.append(translateX)
        pm.setAttr("%s.input1X" %translateX, fabs(originalLength))
        pm.connectAttr(translationDriver, "%s.input2X" %translateX)
        
        pm.connectAttr("%s.outputX" %translateX, "%s.translateX" %locators[2])
    
    
    # Add created nodes to container
    if _container != None:
        containedNodes = list(utilityNodes)
        containedNodes.extend(ikNodes)
        containedNodes.extend([rootLocator, elbowLocator, endLocator])
        containedNodes.append(elbowLocatorConstraint)
        
        AddNodeToContainer(_container, containedNodes, _includeHierarchyBelow=True)
    
    
    return (rootLocator, elbowLocator, endLocator, utilityNodes)


def FindJointChain(_rootJoint):
    
    joints = [_rootJoint]
    parent = _rootJoint
    done = False
    
    while not done:
        children = pm.listRelatives(parent, children = True)
        children = pm.ls(children, type = "joint")
        
        if len(children) == 0:
            done = True
        else:
            child = children[0]
            joints.append(child)
            parent = child
    
    return joints



def FindAllMayaFiles(_relativeDirectory):
    return FindAllFiles(_relativeDirectory, ".ma")


def FindInstalledCharacters():
    pm.namespace(setNamespace = ":")
    namespaces = pm.namespaceInfo(listOnlyNamespaces = True)
    
    characterNamespaces = []
    
    for n in namespaces:
        if n.find("Character__") == 0:
            characterNamespaces.append(n)
    
    return characterNamespaces


def FindInstalledBlueprintInstances(_characterNamespace):
    
    pm.namespace(setNamespace = _characterNamespace)
    moduleInstances = pm.namespaceInfo(listOnlyNamespaces = True)
    
    returnModuleInstances = []
    for module in moduleInstances:
        returnModuleInstances.append(StripLeadingNamespace(module)[1])
    
    pm.namespace(setNamespace = ":")
    
    return returnModuleInstances


def FindFirstFreeConnection(_attribute):
    
    found = False
    index = 0
    
    while not found:
        if pm.connectionInfo("%s[%d]" %(_attribute, index), isDestination = True):
            index += 1
        
        else:
            found = True
    
    return index