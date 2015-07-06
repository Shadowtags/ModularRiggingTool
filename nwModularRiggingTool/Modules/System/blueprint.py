import pymel.core as pm
import System.utils as utils
import os

from functools import partial

reload(utils)


class Blueprint():
    
    def __init__(self, _moduleName, _userSpecifiedName, _jointInfo, _hookObjIn):
        
        self.moduleName = _moduleName
        self.userSpecifiedName = _userSpecifiedName
        
        self.moduleNamespace = "%s__%s" %(self.moduleName, self.userSpecifiedName)
        
        self.containerName = "%s:module_container" %self.moduleNamespace
        
        self.jointInfo = _jointInfo
        
        self.hookObject = None
        if _hookObjIn != None:
            partitionInfo = _hookObjIn.rpartition("_translation_control")
            
            if partitionInfo[1] != '' and partitionInfo[2] == '':
                self.hookObject = _hookObjIn
        
        
        self.canBeMirrored = True
        
        self.mirrored = False
    
    
    
    # METHODS INTENDED FOR OVERRIDING BY DERIVED CLASSES
    def Install_custom(self, _joints):
        print "Install custom method is not implemented by the derived class"
    
    
    def Mirror_custom(self, _originalModule):
        print "Mirror_Custom() method is not implemented by derived class"
    
    
    def Lock_phase1(self):
        
        # Gather and return all require information from this module's control objects
        
        # jointPositions = List of joint position, from root down the hierarchy
        # jointOrientations = list of orientations, or list of axis information (orientJoint and secondaryAxisOrient for joint command)
        #               # These are passed in the following tuple: (orientation, None) or (None, axisInfo)
        
        # jointRotationOrder = list of joint rotation orders (integer values gathered with getAttr)
        # jointPreferredAngles = list of joint preferred angles, optional (can pass None)
        # hookObject = self.FindHookObjectForLock()
        # rootTransform = bool, either true or false. True = rotate, translate and scale on root joint. False = rotate only
        
        # moduleInfo = (jointPositions, jointOrientations, jointRotationOrders, jointPreferredAngles, hookObject, rootTransform)
        # return moduleInfo
        return None
    
    
    def UI_custom(self):
        temp = 1
    
    
    
    
    # BASE CLASS METHODS
    def Install(self):
        
        pm.namespace(setNamespace = ':')
        pm.namespace(add = self.moduleNamespace)
        
        self.jointsGrp = pm.group(empty = True, name = "%s:joints_grp" %self.moduleNamespace)
        self.hierarchyRepresentationGrp = pm.group(empty = True, name = "%s:hierarchyRepresentation_grp" %self.moduleNamespace)
        self.orientationGrp = pm.group(empty = True, name = "%s:orientationControls_grp" %self.moduleNamespace)
        self.preferredAngleRepresentationGroup = pm.group(empty = True, name = "%s:preferredAngleRepresentation_grp")
        
        self.moduleGrp = pm.group([self.jointsGrp, self.hierarchyRepresentationGrp, self.orientationGrp, self.preferredAngleRepresentationGroup], name = "%s:module_grp" %self.moduleNamespace)
        
        pm.container(name = self.containerName, addNode = self.moduleGrp, includeHierarchyBelow = True)
        
        pm.select(clear = True)
        
        index = 0
        joints = []
        
        for joint in self.jointInfo:
            
            jointName = joint[0]
            jointPos = joint[1]
            parentJoint = ''
            
            # Select parent joint
            if index > 0:
                parentJoint = "%s:%s" %(self.moduleNamespace, self.jointInfo[index - 1][0])
                pm.select(parentJoint, replace = True)
            
            
            # Create joint and hide
            jointName_full = pm.joint(name = "%s:%s" %(self.moduleNamespace, jointName), position = jointPos)
            joints.append(jointName_full)
            pm.setAttr("%s.visibility" %jointName_full, 0)
            
            # Add to container and publish attributes
            utils.AddNodeToContainer(self.containerName, jointName_full)
            
            pm.container(self.containerName, edit = True, publishAndBind = ["%s.rotate" %jointName_full, "%s_R" %jointName])
            pm.container(self.containerName, edit = True, publishAndBind = ["%s.rotateOrder" %jointName_full, "%s_RotateOrder" %jointName])
            
            # Reorient child joints
            if index > 0:
                pm.joint(parentJoint, edit = True, orientJoint = 'xyz', secondaryAxisOrient = 'yup')
            
            index += 1
        
        
        if self.mirrored:
            mirrorXY = False
            mirrorYZ = False
            mirrorXZ = False
            
            if self.mirrorPlane == "XY":
                mirrorXY = True
            elif self.mirrorPlane == "YZ":
                mirrorYZ = True
            elif self.mirrorPlane == "XZ":
                mirrorXZ = True
            
            
            mirrorBehaviour = False
            if self.rotationFunction == "behaviour":
                mirrorBehaviour = True
            
            mirroredNodes = pm.mirrorJoint(joints[0], mirrorXY = mirrorXY, mirrorYZ = mirrorYZ, mirrorXZ = mirrorXZ, mirrorBehavior = mirrorBehaviour)
            
            pm.delete(joints)
            
            mirroredJoints = []
            for node in mirroredNodes:
                if pm.objectType(node, isType = 'joint'):
                    mirroredJoints.append(node)
                else:
                    pm.delete(node)
            
            
            index = 0
            for joint in mirroredJoints:
                jointName = self.jointInfo[index][0]
                newJointName = pm.rename(joint, "%s:%s" %(self.moduleNamespace, jointName))
                
                self.jointInfo[index][1] = pm.xform(newJointName, query = True, worldSpace = True, translation = True)
                
                index += 1
        
        
        # Parent joint chain into joint group
        pm.parent(joints[0], self.jointsGrp, absolute = True)
        
        
        # Create transform control for entire module
        self.InitializeModuleTransform(self.jointInfo[0][1])
        
        
        
        # Create translation controls for each joint in module
        translationControls = []
        for joint in joints:
            translationControls.append(self.CreateTransationControlAtJoint(joint))
        
        rootJoint_pointConstraint = pm.pointConstraint(translationControls[0], joints[0], maintainOffset = False, name = "%s_pointConstraint" %joints[0])
        utils.AddNodeToContainer(self.containerName, rootJoint_pointConstraint)
        
        
        # Initialize hook object
        self.InitializeHook(translationControls[0])
        
        
        
        # Setup strechy joint segment
        for index in range(len(joints) - 1):
            self.SetupStretchyJointSegment(joints[index], joints[index + 1])
        
        
        # NON DEFAULT FUNCTUNALITY
        self.Install_custom(joints)
        
        
        # Lock down unpublished module attributes
        pm.lockNode(self.containerName, lock = True, lockUnpublished = True)
    
    
    
    def CreateTransationControlAtJoint(self, _joint):
        
        # Import control object
        posControlFile = "%s/ControlObjects/Blueprint/translation_control.ma" %os.environ["RIGGING_TOOL_ROOT"]
        pm.importFile(posControlFile)
        
        # Rename object and add to container
        container = pm.rename("translation_control_container", "%s_translation_control_container" %_joint)
        utils.AddNodeToContainer(self.containerName, container)
        
        # Rename objects in imported container
        for node in pm.container(container, query = True, nodeList = True):
            pm.rename(node, "%s_%s" %(_joint, node), ignoreShape = True)
        
        
        # Get a reference to control object and parent into tranform group
        control = "%s_translation_control" %_joint
        pm.parent(control, self.moduleTransform, absolute = True)
        
        
        # Position control objects
        jointPos = pm.xform(_joint, query = True, worldSpace = True, translation = True)
        pm.xform(control, worldSpace = True, absolute = True, translation = jointPos)
        
        niceName = utils.StripLeadingNamespace(_joint)[1]
        attrName = "%s_T" %niceName
        
        # Publish control object attributes
        pm.container(container, edit = True, publishAndBind = ["%s.translate" %control, attrName])
        pm.container(self.containerName, edit = True, publishAndBind = ["%s.%s" %(container, attrName), attrName])
        
        return control
    
    
    
    def GetTranslationControl(self, _jointName):
        return "%s_translation_control" %_jointName
    
    def GetOrientationControl(self, _jointName):
        return "%s_orientation_control" %_jointName
    
    
    
    
    def SetupStretchyJointSegment(self, _parentJoint, _childJoint):
        
        parentTranslationControl = self.GetTranslationControl(_parentJoint)
        childTranslationControl = self.GetTranslationControl(_childJoint)
        
        # Create and group a polevector locator for the joint segment
        poleVectorLocator = pm.spaceLocator(name = "%s_poleVectorLocator" %parentTranslationControl)
        poleVectorLocatorGrp = pm.group(poleVectorLocator, name = "%s_parentConstraintGrp" %poleVectorLocator)
        
        # Group the polevector group and parentConstraint to the parent control
        pm.parent(poleVectorLocatorGrp, self.moduleGrp, absolute = True)
        parentConstraint = pm.parentConstraint(parentTranslationControl, poleVectorLocatorGrp, maintainOffset = False)
        
        pm.setAttr("%s.visibility" %poleVectorLocator, 0)
        pm.setAttr("%s.ty" %poleVectorLocator, -0.5)
        
        
        # Create the stretchy setup and collect the nodes returned
        ikNodes = utils.BasicStretchyIK(_parentJoint, _childJoint, _container = self.containerName, _lockMinimumLength = False, _poleVectorObject = poleVectorLocator, _scaleCorrectionAttribute = None)
        ikHandle = ikNodes["ikHandle"]
        rootLocator = ikNodes["rootLocator"]
        endLocator = ikNodes["endLocator"]
        
        
        if self.mirrored:
            if self.mirrorPlane == "XZ":
                pm.setAttr("%s.twist" %ikHandle, 90)
        
        
        
        # PointConstraint end locator to child control
        childPointConstraint = pm.pointConstraint(childTranslationControl, endLocator, maintainOffset = False, name = "%s_pointConstraint" %endLocator)
        
        # Add nodes to container, group ik nodes and hide them
        utils.AddNodeToContainer(self.containerName, [poleVectorLocatorGrp, parentConstraint, childPointConstraint], _includeHierarchyBelow = True)
        
        for node in [ikHandle, rootLocator, endLocator]:
            pm.parent(node, self.jointsGrp, absolute = True)
            pm.setAttr("%s.visibility" %node, 0)
        
        
        # Setup joint segment hierarchy representation
        self.CreateHierarchyRepresentation(_parentJoint, _childJoint)
    
    
    
    def CreateHierarchyRepresentation(self, _parentJoint, _childJoint):
        
        nodes = self.CreateStretchyObject("/ControlObjects/Blueprint/hierarchy_representation.ma", "hierarchy_representation_container", "hierarchy_representation", _parentJoint, _childJoint)
        constrainedGrp = nodes [2]
        
        pm.parent(constrainedGrp, self.hierarchyRepresentationGrp, relative = True)
    
    
    
    def CreateStretchyObject(self, _objectRelativeFilePath, _objectContainerName, _objectName, _parentJoint, _childJoint):
        
        # Import object
        objectFile = "%s%s" %(os.environ["RIGGING_TOOL_ROOT"], _objectRelativeFilePath)
        pm.importFile(objectFile)
        
        # Rename imported scene container and container objects
        objectContainer = pm.rename(_objectContainerName, "%s_%s" %(_parentJoint, _objectContainerName))
        
        for node in pm.container(objectContainer, query = True, nodeList = True):
            pm.rename(node, "%s_%s" %(_parentJoint, node), ignoreShape = True)
        
        obj = "%s_%s" %(_parentJoint, _objectName)
        constrainedGrp = pm.group(empty = True, name = "%s_parentConstraint_grp" %obj)
        
        pm.parent(obj, constrainedGrp, absolute = True)
        parentConstraint = pm.parentConstraint(_parentJoint, constrainedGrp, maintainOffset = False)
        
        # Connect stretch fuctionality
        pm.connectAttr("%s.translateX" %_childJoint, "%s.scaleX" %constrainedGrp)
        
        # Connect module transform global scale to object scale Y and Z
        scaleConstraint = pm.scaleConstraint(self.moduleTransform, constrainedGrp, skip = ['x'], maintainOffset = False)
        
        
        utils.AddNodeToContainer(objectContainer, [constrainedGrp, parentConstraint], True)
        utils.AddNodeToContainer(self.containerName, objectContainer)
        
        return (objectContainer, obj, constrainedGrp)
    
    
    def InitializeModuleTransform(self, _rootPos):
        
        controlGrpFile = "%s/ControlObjects/Blueprint/controlGroup_control.ma" %os.environ["RIGGING_TOOL_ROOT"]
        pm.importFile(controlGrpFile)
        
        # Rename and position transform object
        self.moduleTransform = pm.rename("controlGroup_control", "%s:module_transform" %self.moduleNamespace)
        pm.xform(self.moduleTransform, worldSpace = True, absolute = True, translation = _rootPos)
        
        
        # position mirrored nodes correctly
        if self.mirrored:
            duplicateTransform = pm.duplicate("%s:module_transform" %self.originalModule, parentOnly = True, name = "TEMP_TRANSFORM")
            emptyGroup = pm.group(empty = True)
            
            pm.parent(duplicateTransform, emptyGroup, absolute = True)
            
            scaleAttr = ".scaleX"
            if self.mirrorPlane == "XZ":
                scaleAttr = ".scaleY"
            elif self.mirrorPlane == "XY":
                scaleAttr = ".scaleZ"
            
            
            pm.setAttr("%s%s" %(emptyGroup, scaleAttr), -1)
            
            parentConstraint = pm.parentConstraint(duplicateTransform, self.moduleTransform, maintainOffset = False)
            pm.delete(parentConstraint)
            pm.delete(emptyGroup)
            
            tempLocator = pm.spaceLocator()
            scaleConstraint = pm.scaleConstraint("%s:module_transform" %self.originalModule, tempLocator, maintainOffset = False)
            scale = pm.getAttr("%s.scaleX" %tempLocator)
            pm.delete([tempLocator, scaleConstraint])
            
            pm.xform(self.moduleTransform, objectSpace = True, scale = [scale, scale, scale])
        
        utils.AddNodeToContainer(self.containerName, self.moduleTransform, True)
        
        # Setup global scaling
        pm.connectAttr("%s.scaleY" %self.moduleTransform, "%s.scaleX" %self.moduleTransform)
        pm.connectAttr("%s.scaleY" %self.moduleTransform, "%s.scaleZ" %self.moduleTransform)
        
        pm.aliasAttr("globalScale", "%s.scaleY" %self.moduleTransform)
        
        pm.container(self.containerName, edit = True, publishAndBind = ["%s.translate" %self.moduleTransform, "moduleTransform_T"])
        pm.container(self.containerName, edit = True, publishAndBind = ["%s.rotate" %self.moduleTransform, "moduleTransform_R"])
        pm.container(self.containerName, edit = True, publishAndBind = ["%s.globalScale" %self.moduleTransform, "moduleTransform_globalScale"])
    
    
    
    
    def DeleteHierarchyRepresentation(self, _parentJoint):
        
        hierarchyContainer = "%s_hierarchy_representation_container" %_parentJoint
        pm.delete(hierarchyContainer)
    
    
    
    def CreateOrientationControl(self, _parentJoint, _childJoint):
        
        # Delete default hierarchy representation nodes
        self.DeleteHierarchyRepresentation(_parentJoint)
        
        # Create orientation object and store nodes in list
        nodes = self.CreateStretchyObject("/ControlObjects/Blueprint/orientation_control.ma", "orientation_control_container", "orientation_control", _parentJoint, _childJoint)
        orientationContainer = nodes[0]
        orientationControl = nodes[1]
        constrainedGrp = nodes[2]
        
        pm.parent(constrainedGrp, self.orientationGrp, relative = True)
        
        parentJointWithoutNamespace = utils.StripAllNamespaces(_parentJoint)[1]
        attrName = "%s_orientation" %parentJointWithoutNamespace
        
        pm.container(orientationContainer, edit = True, publishAndBind = ["%s.rotateX" %orientationControl, attrName])
        pm.container(self.containerName, edit = True, publishAndBind = ["%s.%s" %(orientationContainer, attrName), attrName])
        
        return orientationControl
    
    
    
    def GetJoints(self):
        
        jointBaseName = "%s:" %self.moduleNamespace
        joints = []
        
        for jointInf in self.jointInfo:
            joints.append("%s%s" %(jointBaseName, jointInf[0]))
        
        
        return joints
    
    
    
    def OrientationControlJoint_getOrientation(self, _joint, _cleanParent):
        
        # Create clean copy of joint, as to be able to get the orientation values without destroying any connections
        newCleanParent = pm.duplicate(_joint, parentOnly = True)[0]
        
        # Make sure the duplicate is parented correctly
        if not _cleanParent in pm.listRelatives(newCleanParent, parent = True):
            pm.parent(newCleanParent, _cleanParent, absolute = True)
        
        # Freeze rotations
        pm.makeIdentity(newCleanParent, apply = True, rotate = True, scale = False, translate = False)
        
        # Match orientation of orientation control
        orientationControl = self.GetOrientationControl(_joint)
        pm.setAttr("%s.rotateX" %newCleanParent, pm.getAttr("%s.rotateX" %orientationControl))
        
        pm.makeIdentity(newCleanParent, apply = True, rotate = True, scale = False, translate = False)
        
        # Get new orientation values
        orientX = pm.getAttr("%s.jointOrientX" %newCleanParent)
        orientY = pm.getAttr("%s.jointOrientY" %newCleanParent)
        orientZ = pm.getAttr("%s.jointOrientZ" %newCleanParent)
        
        # Store as a tuple for return
        orientationValues = (orientX, orientY, orientZ)
        
        return (orientationValues, newCleanParent)
    
    
    
    def Lock_phase2(self, _moduleInfo):
        
        # Aquire information about the modules
        jointPosition = _moduleInfo[0]
        numJoints = len(jointPosition)
        
        jointOrientations = _moduleInfo[1]
        orientWithAxis = False
        pureOrientations = False
        
        if jointOrientations[0] == None:
            orientWithAxis = True
            jointOrientations = jointOrientations[1]
        else:
            pureOrientations = True
            jointOrientations = jointOrientations[0]
        
        numOrientations = len(jointOrientations)
        
        jointRotationOrders = _moduleInfo[2]
        numRotationOrders = len(jointRotationOrders)
        
        jointPreferredAngles = _moduleInfo[3]
        numPreferredAngles = 0
        
        if jointPreferredAngles != None:
            numPreferredAngles = len(jointPreferredAngles)
        
        hookObject = _moduleInfo[4]
        
        rootTransform = _moduleInfo[5]
        
        
        mirrorInfo = None
        oldModuleGrp = "%s:module_grp" %self.moduleNamespace
        if pm.attributeQuery("mirrorInfo", node = oldModuleGrp, exists = True):
            mirrorInfo = pm.getAttr("%s.mirrorInfo" %oldModuleGrp)
        
        
        # Delete our blueprint controls
        pm.lockNode(self.containerName, lock = False, lockUnpublished = False)
        pm.delete(self.containerName)
        
        # Set namespace to root
        pm.namespace(setNamespace = ':')
        
        # Default radius of joint is 1.
        jointRadius = 1
        if numJoints == 1:
            jointRadius = 1.5
        
        
        newJoints = []
        for i in range(numJoints):
            
            # Create new joint
            newJoint = ''
            pm.select(clear = True)
            
            if orientWithAxis:
                newJoint = pm.joint(name = "%s:blueprint_%s" %(self.moduleNamespace, self.jointInfo[i][0]), position = jointPosition[i], rotationOrder = 'xyz', radius = jointRadius)
                
                # Orient parent joint in joint chain
                if i != 0:
                    offsetIndex = i-1
                    pm.parent(newJoint, newJoints[offsetIndex], absolute = True)
                    
                    if offsetIndex < numOrientations:
                        pm.joint(newJoints[offsetIndex], edit = True, orientJoint = jointOrientations[offsetIndex][0], secondaryAxisOrient = jointOrientations[offsetIndex][1])
                        pm.makeIdentity(newJoint, rotate = True, apply = True)
            
            else:
                if i != 0:
                    pm.select(newJoints[i-1])
                
                # Orient parent joint in joint chain
                jointOrientation = [0.0, 0.0, 0.0]
                if i < numOrientations:
                    jointOrientation = [jointOrientations[i][0], jointOrientations[i][1], jointOrientations[i][2]]
                
                newJoint = pm.joint(name = "%s:blueprint_%s" %(self.moduleNamespace, self.jointInfo[i][0]), position = jointPosition[i], orientation = jointOrientation, rotationOrder = 'xyz', radius = jointRadius)
            
            newJoints.append(newJoint)
            
            if i < numRotationOrders:
                pm.setAttr("%s.rotateOrder" %newJoint, int(jointRotationOrders[i]))
            
            if i < numPreferredAngles:
                pm.setAttr("%s.preferredAngleX" %newJoint, jointPreferredAngles[i][0])
                pm.setAttr("%s.preferredAngleY" %newJoint, jointPreferredAngles[i][1])
                pm.setAttr("%s.preferredAngleZ" %newJoint, jointPreferredAngles[i][2])
            
            pm.setAttr("%s.segmentScaleCompensate" %newJoint, 0)
        
        
        # Group new joint chain
        blueprintGrp = pm.group(empty = True, name = "%s:blueprint_points_grp" %self.moduleNamespace)
        pm.parent(newJoints[0], blueprintGrp, absolute = True)
        
        
        creationPoseGrpNodes = pm.duplicate(blueprintGrp, name = "%s:creationPose_joint_grp" %self.moduleNamespace, renameChildren = True)
        creationPoseGrp = creationPoseGrpNodes[0]
        
        
        # Store duplicated nodes in list
        pm.select(creationPoseGrp, hierarchy = True)
        creationPoseGrpNodes = pm.ls(selection = True)
        pm.select(clear = True)
        
        
        # Remove group from list
        creationPoseGrpNodes.pop(0)
        
        # Rename joints
        i = 0
        for node in creationPoseGrpNodes:
            renameNode = pm.rename(node, "%s:creationPose_%s" %(self.moduleNamespace, self.jointInfo[i][0]))
            pm.setAttr("%s.visibility" %renameNode)
            
            i += 1
        
        pm.select(blueprintGrp, replace = True)
        pm.addAttr(attributeType = 'bool', defaultValue = 0, longName = "controlModuleInstalled", keyable = False)
        
        
        hookGroup = pm.group(empty = True, name = "%s:HOOK_IN" %self.moduleNamespace)
        for obj in [blueprintGrp, creationPoseGrp]:
            pm.parent(obj, hookGroup, absolute = True)
        
        
        settingsLocator = pm.spaceLocator(name = "%s:SETTINGS" %self.moduleNamespace)
        pm.setAttr("%s.visibility" %settingsLocator, 0)
        
        pm.select(settingsLocator, replace = True)
        pm.addAttr(attributeType = 'enum', longName = "activeModule", enumName = "None:", keyable = False)
        pm.addAttr(attributeType = 'float', longName = "creationPoseWeight", defaultValue = 1, keyable = False)
        
        i = 0
        utilityNodes = []
        for joint in newJoints:
            
            # Create utility rotate nodes for root joint
            if i < (numJoints-1) or numJoints == 1:
                addNode = pm.shadingNode("plusMinusAverage", name = "%s_addRotations" %joint, asUtility = True)
                pm.connectAttr("%s.output3D" %addNode, "%s.rotate" %joint, force = True)
                utilityNodes.append(addNode)
                
                dummyRotationsMultiply = pm.shadingNode("multiplyDivide", name = "%s_dummyRotationsMultiply" %joint, asUtility = True)
                pm.connectAttr("%s.output" %dummyRotationsMultiply, "%s.input3D[0]" %addNode, force = True)
                utilityNodes.append(dummyRotationsMultiply)
            
            
            # Create utility translate nodes for every joint except the root
            if i > 0:
                originalTx = pm.getAttr("%s.tx" %joint)
                addTxNode = pm.shadingNode("plusMinusAverage", name = "%s_addTx" %joint, asUtility = True)
                pm.connectAttr("%s.output1D" %addTxNode, "%s.translateX" %joint, force = True)
                utilityNodes.append(addTxNode)
                
                originalTxMultiply = pm.shadingNode("multiplyDivide", name = "%s_original_Tx" %joint, asUtility = True)
                pm.setAttr("%s.input1X" %originalTxMultiply, originalTx, lock = True)
                pm.connectAttr("%s.creationPoseWeight" %settingsLocator, "%s.input2X" %originalTxMultiply, force = True)
                pm.connectAttr("%s.outputX" %originalTxMultiply, "%s.input1D[0]" %addTxNode, force = True)
                utilityNodes.append(originalTxMultiply)
            
            # Create utility translate nodes root joint
            else:
                if rootTransform:
                    originalTranslates = pm.getAttr("%s.translate" %joint)
                    addTranslateNode = pm.shadingNode("plusMinusAverage", name = "%s_addTranslate" %joint, asUtility = True)
                    pm.connectAttr("%s.output3D" %addTranslateNode, "%s.translate" %joint, force = True)
                    utilityNodes.append(addTranslateNode)
                    
                    originalTranslateMultiply = pm.shadingNode("multiplyDivide", name = "%s_original_Translate" %joint, asUtility = True)
                    pm.setAttr("%s.input1" %originalTranslateMultiply, originalTranslates[0], originalTranslates[1], originalTranslates[2], type = 'double3')
                    
                    for attr in ['X', 'Y', 'Z']:
                        pm.connectAttr("%s.creationPoseWeight" %settingsLocator, "%s.input2%s" %(originalTranslateMultiply, attr), force = True)
                    
                    pm.connectAttr("%s.output" %originalTranslateMultiply, "%s.input3D[0]" %addTranslateNode, force = True)
                    utilityNodes.append(originalTranslateMultiply)
                    
                    # Scale
                    originalScales = pm.getAttr("%s.scale" %joint)
                    addScaleNode = pm.shadingNode("plusMinusAverage", name = "%s_addScale" %joint, asUtility = True)
                    pm.connectAttr("%s.output3D" %addScaleNode, "%s.scale" %joint, force = True)
                    utilityNodes.append(addScaleNode)
                
                    originalScaleMultiply = pm.shadingNode("multiplyDivide", name = "%s_original_Scale" %joint, asUtility = True)
                    pm.setAttr("%s.input1" %originalScaleMultiply, originalScales[0], originalScales[1], originalScales[2], type = 'double3')
                
                    for attr in ['X', 'Y', 'Z']:
                        pm.connectAttr("%s.creationPoseWeight" %settingsLocator, "%s.input2%s" %(originalScaleMultiply, attr), force = True)
                
                    pm.connectAttr("%s.output" %originalScaleMultiply, "%s.input3D[0]" %addScaleNode, force = True)
                    utilityNodes.append(originalScaleMultiply)
            
            i += 1
        
        
        blueprintNodes = utilityNodes
        blueprintNodes.append(blueprintGrp)
        blueprintNodes.append(creationPoseGrp)
        
        blueprintContainer = pm.container(name = "%s:blueprint_container" %self.moduleNamespace)
        utils.AddNodeToContainer(blueprintContainer, blueprintNodes, True)
        
        moduleGrp = pm.group(empty = True, name = "%s:module_grp" %self.moduleNamespace)
        for obj in [hookGroup, settingsLocator]:
            pm.parent(obj, moduleGrp, absolute = True)
        
        
        
        moduleContainer = pm.container(name = "%s:module_container" %self.moduleNamespace)
        utils.AddNodeToContainer(moduleContainer, [moduleGrp, hookGroup, settingsLocator, blueprintContainer], _includeShapes = True)
        
        pm.container(moduleContainer, edit = True, publishAndBind = ["%s.activeModule" %settingsLocator, "activeModule"])
        pm.container(moduleContainer, edit = True, publishAndBind = ["%s.creationPoseWeight" %settingsLocator, "creationPoseWeight"])
        
        
        if mirrorInfo != None:
            enumNames = "none:x:y:z"
            pm.select(moduleGrp, replace = True)
            pm.addAttr(attributeType = "enum", enumName = enumNames, longName = "mirrorInfo", keyable = False)
            pm.setAttr("%s.mirrorInfo" %moduleGrp, mirrorInfo)
        
        
        pm.select(moduleGrp, replace = True)
        pm.addAttr(attributeType = "float", longName = "hierarchicalScale")
        pm.connectAttr("%s.scaleY" %hookGroup, "%s.hierarchicalScale" %moduleGrp)
        
    
    
    
    def UI(self, _blueprint_UI_instance, _parentColumnLayout):
        
        self.blueprint_UI_instance = _blueprint_UI_instance
        self.parentColumnLayout = _parentColumnLayout
        
        self.UI_custom()
    
    
    
    def CreateRotationOrderUIControl(self, _joint):
        
        jointName = utils.StripAllNamespaces(_joint)[1]
        attrControlGroup = pm.attrControlGrp(attribute = "%s.rotateOrder" %_joint, label = jointName)
        
        pm.scriptJob(attributeChange = ["%s.rotateOrder" %_joint, partial(self.AttributeChange_callbackMethod, _joint, ".rotateOrder")], parent = attrControlGroup)
    
    
    def AttributeChange_callbackMethod(self, _object, _attribute, *args):
        
        if pm.checkBox(self.blueprint_UI_instance.UIElements["symmetryMoveCheckBox"], query = True, value = True):
            moduleInfo = utils.StripLeadingNamespace(_object)
            module = moduleInfo[0]
            objectName = moduleInfo[1]
            
            moduleGroup = "%s:module_grp" %module
            if pm.attributeQuery("mirrorLinks", node = moduleGroup, exists = True):
                mirrorLinks = pm.getAttr("%s.mirrorLinks" %moduleGroup)
                mirrorModule = mirrorLinks.rpartition("__")[0]
                
                newValue = pm.getAttr("%s%s" %(_object, _attribute))
                mirrorObj = "%s:%s" %(mirrorModule, objectName)
                pm.setAttr("%s%s" %(mirrorObj, _attribute), newValue)
    
    
    def Delete(self):
        
        # Unlock container before deleting module
        pm.lockNode(self.containerName, lock = False, lockUnpublished = False)
        
        
        validModuleInfo = utils.FindAllModuleNames("/Modules/Blueprint")
        validModules = validModuleInfo[0]
        validModuleNames = validModuleInfo[1]
        
        # Store hooked modules in set
        hookedModules = set()
        for jntInfo in self.jointInfo:
            
            joint = jntInfo[0]
            translationControl = self.GetTranslationControl("%s:%s" %(self.moduleNamespace, joint))
            
            connections = pm.listConnections(translationControl)
            
            # Check if module is hooked to another module and if so, store hooked modules in a list
            for connection in connections:
                moduleInstance = utils.StripLeadingNamespace(connection)
                
                if moduleInstance != None:
                    splitString = moduleInstance[0].partition("__")
                    
                    if moduleInstance[0] != self.moduleNamespace and splitString[0] in validModuleNames:
                        index = validModuleNames.index(splitString[0])
                        
                        hookedModules.add( (validModules[index], splitString[2]) )
        
        
        # Unhook module before deleting
        for module in hookedModules:
            mod = __import__("Blueprint.%s" %module[0], {}, {}, [module[0]])
            moduleClass = getattr(mod, mod.CLASS_NAME)
            moduleInst = moduleClass(module[1], None)
            moduleInst.Rehook(None)
        
        
        # Remove mirror links attribute
        if pm.attributeQuery("mirrorLinks", node = "%s:module_grp" %self.moduleNamespace, exists = True):
            mirrorLinks = pm.getAttr("%s:module_grp.mirrorLinks" %self.moduleNamespace)
            
            linkedBlueprint = mirrorLinks.rpartition("__")[0]
            pm.lockNode("%s:module_container" %linkedBlueprint, lock = False, lockUnpublished = False)
            
            pm.deleteAttr("%s:module_grp.mirrorLinks" %linkedBlueprint)
            
            pm.lockNode("%s:module_container" %linkedBlueprint, lock = True, lockUnpublished = True)
        
        
        pm.delete(self.containerName)
        
        pm.namespace(setNamespace = ':')
        pm.namespace(removeNamespace = self.moduleNamespace)
    
    
    def RenameModuleInstance(self, _newName):
        
        if _newName == self.userSpecifiedName:
            return True
        
        if utils.DoesBlueprintUserSpecifiedNameExist(_newName):
            pm.confirmDialog(title = 'Name Conflict', message = 'Name "%s" already exists.\nAborting rename.' %_newName, button = ['Accept'], defaultButton = 'Accept')
            return False
        
        else:
            newNamespace = "%s__%s" %(self.moduleName, _newName)
            
            pm.lockNode(self.containerName, lock = False, lockUnpublished = False)
            
            # Add new namespace
            pm.namespace(setNamespace = ':')
            pm.namespace(add = newNamespace)
            pm.namespace(setNamespace = ':')
            
            # Move old one
            pm.namespace(moveNamespace = [self.moduleNamespace, newNamespace])
            
            # Remove old namespace
            pm.namespace(removeNamespace = self.moduleNamespace)
            
            
            if pm.attributeQuery("mirrorLinks", node = "%s:module_grp" %newNamespace, exists = True):
                mirrorLinks = pm.getAttr("%s:module_grp.mirrorLinks" %newNamespace)
                
                nodeAndAxis = mirrorLinks.rpartition("__")
                node = nodeAndAxis[0]
                axis = nodeAndAxis[2]
                
                pm.lockNode("%s:module_container" %node, lock = False, lockUnpublished = False)
                
                pm.setAttr("%s:module_grp.mirrorLinks" %node, "%s__%s" %(newNamespace, axis), type = "string")
                
                pm.lockNode("%s:module_container" %node, lock = True, lockUnpublished = True)
            
            # Update variables
            self.moduleNamespace = newNamespace
            self.containerName = "%s:module_container" %self.moduleNamespace
            
            # Lock container
            pm.lockNode(self.containerName, lock = True, lockUnpublished = True)
            
            return True
    
    
    
    def InitializeHook(self, _rootTranslationControl):
        
        unhookedLocator = pm.spaceLocator(name = "%s:unhookedTarget" %self.moduleNamespace)
        pm.pointConstraint(_rootTranslationControl, unhookedLocator, offset = [0, 0.001, 0])
        pm.setAttr("%s.visibility" %unhookedLocator, 0)
        
        if self.hookObject == None:
            self.hookObject = unhookedLocator
        
        
        rootPos = pm.xform(_rootTranslationControl, query = True, worldSpace = True, translation = True)
        targetPos = pm.xform(self.hookObject, query = True, worldSpace = True, translation = True)
        
        # Make sure nothing is selected when creating the hook joints
        pm.select(clear = True)
        
        rootJointWithoutNamespace = "hook_root_joint"
        rootJoint = pm.joint(name = "%s:%s" %(self.moduleNamespace, rootJointWithoutNamespace), position = rootPos)
        pm.setAttr("%s.visibility" %rootJoint, 0)
        
        targetJointWithoutNamespace = "hook_target_joint"
        targetJoint = pm.joint(name = "%s:%s" %(self.moduleNamespace, targetJointWithoutNamespace), position = targetPos)
        pm.setAttr("%s.visibility" %targetJoint, 0)
        
        pm.joint(rootJoint, edit = True, orientJoint = 'xyz', secondaryAxisOrient = 'yup')
        
        hookGroup = pm.group([rootJoint, unhookedLocator], name = "%s:hook_grp" %self.moduleNamespace, parent = self.moduleGrp)
        
        hookContainer = pm.container(name = "%s:hook_container" %self.moduleNamespace)
        utils.AddNodeToContainer(hookContainer, hookGroup, True)
        utils.AddNodeToContainer(self.containerName, hookContainer)
        
        for joint in [rootJoint, targetJoint]:
            jointName = utils.StripAllNamespaces(joint)[1]
            pm.container(hookContainer, edit = True, publishAndBind = ["%s.rotate" %joint, "%s_R" %jointName])
        
        
        ikNodes = utils.BasicStretchyIK(rootJoint, targetJoint, hookContainer, False)
        ikHandle = ikNodes["ikHandle"]
        rootLocator = ikNodes["rootLocator"]
        endLocator = ikNodes["endLocator"]
        poleVectorLocator = ikNodes["poleVectorObject"]
        
        rootPointConstraint = pm.pointConstraint(_rootTranslationControl, rootJoint, maintainOffset = False, name = "%s_pointConstraint" %rootJoint)
        targetPointConstraint = pm.pointConstraint(self.hookObject, endLocator, maintainOffset = False, name = "%s:hook_pointConstraint" %self.moduleNamespace)
        
        utils.AddNodeToContainer(hookContainer, [rootPointConstraint, targetPointConstraint])
        
        for node in [ikHandle, rootLocator, endLocator, poleVectorLocator]:
            pm.parent(node, hookGroup, absolute = True)
            pm.setAttr("%s.visibility" %node, 0)
        
        
        objectNodes = self.CreateStretchyObject("/ControlObjects/Blueprint/hook_representation.ma", "hook_representation_container", "hook_representation", rootJoint, targetJoint)
        constrainedGrp = objectNodes[2]
        pm.parent(constrainedGrp, hookGroup, absolute = True)
        
        hookRepresentationContainer = objectNodes[0]
        pm.container(self.containerName, edit = True, removeNode = hookRepresentationContainer)
        utils.AddNodeToContainer(hookContainer, hookRepresentationContainer)
    
    
    
    def Rehook(self, _newHookObject):
        oldHookObject = self.FindHookObject()
        
        self.hookObject = "%s:unhookedTarget" %self.moduleNamespace
        
        # Make sure module has a module to hook to
        if _newHookObject != None:
            
            # Make sure the name of the object can be split correctly
            if _newHookObject.find("_translation_control") != -1:
                splitString = _newHookObject.split("_translation_control")
                
                # Make sure it's the correct control
                if splitString[1] == '':
                    # Make sure hooking is not happening with itself
                    if utils.StripLeadingNamespace(_newHookObject)[0] != self.moduleNamespace:
                        self.hookObject = _newHookObject
        
        
        # Cancel hooking if hooking to same object
        if self.hookObject == oldHookObject:
            return
        
        
        # Make sure the module is not constrained to any other modules
        self.UnconstrainRootFromHook()
        
        
        pm.lockNode(self.containerName, lock = False, lockUnpublished = False)
        
        # Rewire point constraint connections to new hook object
        hookConstraint = "%s:hook_pointConstraint" %self.moduleNamespace
        
        pm.connectAttr("%s.parentMatrix[0]" %self.hookObject, "%s.target[0].targetParentMatrix" %hookConstraint, force = True)
        pm.connectAttr("%s.translate" %self.hookObject, "%s.target[0].targetTranslate" %hookConstraint, force = True)
        pm.connectAttr("%s.rotatePivot" %self.hookObject, "%s.target[0].targetRotatePivot" %hookConstraint, force = True)
        pm.connectAttr("%s.rotatePivotTranslate" %self.hookObject, "%s.target[0].targetRotateTranslate" %hookConstraint, force = True)
        
        pm.lockNode(self.containerName, lock = True, lockUnpublished = True)
    
    
    def FindHookObject(self):
        hookConstraint = "%s:hook_pointConstraint" %self.moduleNamespace
        sourceAttr = pm.connectionInfo("%s.target[0].targetParentMatrix" %hookConstraint, sourceFromDestination = True)
        sourceNode = str(sourceAttr).rpartition(".")[0]
        
        return sourceNode
    
    
    
    def FindHookObjectForLock(self):
        hookObject = self.FindHookObject()
        
        if hookObject == "%s:unhookedTarget" %self.moduleNamespace:
            hookObject = None
        else:
            self.Rehook(None)
        
        return hookObject
    
    
    
    def Lock_phase3(self, _hookObject):
        
        moduleContainer = "%s:module_container" %self.moduleNamespace
        
        if _hookObject != None:
            hookObjectModuleNode = utils.StripLeadingNamespace(_hookObject)
            hookObjectModule = hookObjectModuleNode[0]
            hookObjectJoint = hookObjectModuleNode[1].split("_translation_control")[0]
            
            hookObj = "%s:blueprint_%s" %(hookObjectModule, hookObjectJoint)
            
            parentConstraint = pm.parentConstraint(hookObj, "%s:HOOK_IN" %self.moduleNamespace, maintainOffset = True, name = "%s:hook_parent_constraint" %self.moduleNamespace)
            scaleConstraint = pm.scaleConstraint(hookObj, "%s:HOOK_IN" %self.moduleNamespace, maintainOffset = True, name = "%s:hook_scale_constraint" %self.moduleNamespace)
            
            utils.AddNodeToContainer(moduleContainer, [parentConstraint, scaleConstraint])
        
        pm.lockNode(moduleContainer, lock = True, lockUnpublished = True)
    
    
    
    def SnapRootToHook(self):
        
        rootControl = self.GetTranslationControl("%s:%s" %(self.moduleNamespace, self.jointInfo[0][0]))
        hookObject = self.FindHookObject()
        
        if hookObject == "%s:unhookedTarget" %self.moduleNamespace:
            return
        
        hookObjectPos = pm.xform(hookObject, query = True, worldSpace = True, translation = True)
        pm.xform(rootControl, worldSpace = True, absolute = True, translation = hookObjectPos)
    
    
    def ConstrainRootToHook(self):
        rootControl = self.GetTranslationControl("%s:%s" %(self.moduleNamespace, self.jointInfo[0][0]))
        hookObject = self.FindHookObject()
    
        if hookObject == "%s:unhookedTarget" %self.moduleNamespace:
            return
        
        pm.lockNode(self.containerName, lock = False, lockUnpublished = False)
        
        pm.pointConstraint(hookObject, rootControl, maintainOffset = False, name = "%s_hookConstraint" %rootControl)
        pm.setAttr("%s.translate" %rootControl, lock = True)
        pm.setAttr("%s.visibility" %rootControl, lock = False)
        pm.setAttr("%s.visibility" %rootControl, 0)
        pm.setAttr("%s.visibility" %rootControl, lock = True)
        
        pm.select(clear = True)
        
        pm.lockNode(self.containerName, lock = True, lockUnpublished = True)
    
    
    def UnconstrainRootFromHook(self):
        
        pm.lockNode(self.containerName, lock = False, lockUnpublished = False)
        
        rootControl = self.GetTranslationControl("%s:%s" %(self.moduleNamespace, self.jointInfo[0][0]))
        rootControl_hookConstraint = "%s_hookConstraint" %rootControl
        
        if pm.objExists(rootControl_hookConstraint):
            pm.delete(rootControl_hookConstraint)
            
            pm.setAttr("%s.translate" %rootControl, lock = False)
            pm.setAttr("%s.visibility" %rootControl, lock = False)
            pm.setAttr("%s.visibility" %rootControl, 1)
            pm.setAttr("%s.visibility" %rootControl, lock = True)
            
            pm.select(rootControl, replace = True)
            pm.setToolTo("moveSuperContext")
        
        
        pm.lockNode(self.containerName, lock = True, lockUnpublished = True)
    
    
    def IsRootConstrained(self):
        
        rootControl = self.GetTranslationControl("%s:%s" %(self.moduleNamespace, self.jointInfo[0][0]))
        rootControl_hookConstraint = "%s_hookConstraint" %rootControl
        
        return pm.objExists(rootControl_hookConstraint)
    
    
    def CanModuleBeMirrored(self):
        return self.canBeMirrored
    
    
    def Mirror(self, _originalModule, _mirrorPlane, _rotationFunction, _translationFunction):
        
        self.mirrored = True
        self.originalModule = _originalModule
        self.mirrorPlane = _mirrorPlane
        self.rotationFunction = _rotationFunction
        
        self.Install()
        
        pm.lockNode(self.containerName, lock = False, lockUnpublished = False)
        
        for jointInfo in self.jointInfo:
            jointName = jointInfo[0]
            
            originalJoint = "%s:%s" %(self.originalModule, jointName)
            newJoint = "%s:%s" %(self.moduleNamespace, jointName)
            
            originalRotationOrder = pm.getAttr("%s.rotateOrder" %originalJoint)
            pm.setAttr("%s.rotateOrder" %newJoint, originalRotationOrder)
        
        index = 0
        for jointInfo in self.jointInfo:
            mirrorPoleVectorLocator = False
            
            if index < len(self.jointInfo) - 1:
                mirrorPoleVectorLocator = True
            
            jointName = jointInfo[0]
            
            originalJoint = "%s:%s" %(self.originalModule, jointName)
            newJoint = "%s:%s" %(self.moduleNamespace, jointName)
        
            originalTranslationControl = self.GetTranslationControl(originalJoint)
            newTranslationControl = self.GetTranslationControl(newJoint)
            
            originalTranslationControlPosition = pm.xform(originalTranslationControl, query = True, worldSpace = True, translation = True)
            
            if self.mirrorPlane == "YZ":
                originalTranslationControlPosition[0] *= -1
            elif self.mirrorPlane == "XZ":
                originalTranslationControlPosition[1] *= -1
            elif self.mirrorPlane == "XY":
                originalTranslationControlPosition[2] *= -1
            
            pm.xform(newTranslationControl, worldSpace = True, absolute = True, translation = originalTranslationControlPosition)
            
            
            if mirrorPoleVectorLocator:
                originalPoleVectorLocator = "%s_poleVectorLocator" %originalTranslationControl
                newPoleVectorLocator = "%s_poleVectorLocator" %newTranslationControl
                originalPoleVectorLocatorPosition = pm.xform(originalPoleVectorLocator, query = True, worldSpace = True, translation = True)
                
                if self.mirrorPlane == "YZ":
                    originalPoleVectorLocatorPosition[0] *= -1
                elif self.mirrorPlane == "XZ":
                    originalPoleVectorLocatorPosition[1] *= -1
                elif self.mirrorPlane == "XY":
                    originalPoleVectorLocatorPosition[2] *= -1
                
                pm.xform(newPoleVectorLocator, worldSpace = True, absolute = True, translation = originalPoleVectorLocatorPosition)
            
            index += 1
        
        
        self.Mirror_custom(_originalModule)
        
        
        moduleGroup = "%s:module_grp" %self.moduleNamespace
        pm.select(moduleGroup, replace = True)
        
        enumNames = "none:x:y:z"
        pm.addAttr(attributeType = "enum", enumName = enumNames, longName = "mirrorInfo", k = False)
        
        enumValue = 0
        if _translationFunction == "mirrored":
            if _mirrorPlane == "YZ":
                enumValue = 1
            elif _mirrorPlane == "XZ":
                enumValue = 2
            elif _mirrorPlane == "XY":
                enumValue = 3
        
        pm.setAttr("%s.mirrorInfo" %moduleGroup, enumValue)
        
        linkedAttribute = "mirrorLinks"
        
        pm.lockNode("%s:module_container" %_originalModule, lock = False, lockUnpublished = False)
        
        for moduleLink in ((_originalModule, self.moduleNamespace), (self.moduleNamespace, _originalModule)):
            
            moduleGroup = "%s:module_grp" %moduleLink[0]
            attributeValue = "%s__" %moduleLink[1]
            
            if _mirrorPlane == "YZ":
                attributeValue += "X"
            elif _mirrorPlane == "XZ":
                attributeValue += "Y"
            elif _mirrorPlane == "XY":
                attributeValue += "Z"
            
            pm.select(moduleGroup, replace = True)
            
            pm.addAttr(dataType = "string", longName = linkedAttribute, keyable = False)
            pm.setAttr("%s.%s" %(moduleGroup, linkedAttribute), attributeValue, type = "string")
        
        for c in ["%s:module_container" %_originalModule, self.containerName]:
            pm.lockNode(c, lock = True, lockUnpublished = True)
        
        pm.select(clear = True)
    
    
    
    def CreatePreferredAngleRepresentation(self, _joint, _scaleTarget, _childOfOrientationControl = False):
        
        preferredAngleRepFile = "%s/ControlObjects/Blueprint/preferredAngle_representation.ma" %os.environ["RIGGING_TOOL_ROOT"]
        pm.importFile(preferredAngleRepFile)
        
        container = pm.rename("preferredAngle_representation_container", "%s_preferredAngle_representation_container" %_joint)
        utils.AddNodeToContainer(self.containerName, container)
        
        for node in pm.container(container, query = True, nodeList = True):
            pm.rename(node, "%s_%s" %(_joint, node), ignoreShape = True)
        
        control = "%s_preferredAngle_representation" %_joint
        controlName = utils.StripAllNamespaces(control)[1]
        pm.container(self.containerName, edit = True, publishAndBind = ["%s.axis" %container, "%s_axis" %controlName])
        
        controlGroup = pm.group(control, name = "%s_preferredAngle_parentConstrainGrp" %_joint, absolute = True)
        containedNodes = [controlGroup]
        
        pm.parent(controlGroup, self.preferredAngleRepresentationGroup, absolute = True)
        
        containedNodes.append(pm.parentConstraint(_joint, controlGroup, maintainOffset = False))
        
        if _childOfOrientationControl:
            rotateXGrp = pm.group(control, name = "%s_rotateX_grp" %control, absolute = True)
            orientationControl = self.GetOrientationControl(_joint)
            
            pm.connectAttr("%s.rotateX" %orientationControl, "%s.rotateX" %rotateXGrp)
            
            containedNodes.append(rotateXGrp)
        
        containedNodes.append(pm.scaleConstraint(_scaleTarget, controlGroup, maintainOffset = False))
        
        utils.AddNodeToContainer(container, containedNodes)
        
        return control
    
    
    def GetPreferredAngleControl(self, _jointName):
        return "%s_preferredAngle_representation" %_jointName
    
    
    def CreatePreferredAngleUIControl(self, _preferredAngle_representation):
        
        label = utils.StripLeadingNamespace(_preferredAngle_representation)[1].partition("_representation")[0]
        enumOptionMenu = pm.attrEnumOptionMenu(label = label, attribute = "%s.axis" %_preferredAngle_representation)
        
        pm.scriptJob(attributeChange = ["%s.axis" %_preferredAngle_representation, partial(self.AttributeChange_callbackMethod, _preferredAngle_representation, ".axis")], parent = enumOptionMenu)
    
    
    def CreateSingleJointOrientationControlAtJoint(self, _joint):
        
        controlFile = "%s/ControlObjects/Blueprint/singleJointOrientation_control.ma" %os.environ["RIGGING_TOOL_ROOT"]
        pm.importFile(controlFile)
        
        container = pm.rename("singleJointOrientation_control_container", "%s_singleJointOrientation_control_container" %_joint)
        utils.AddNodeToContainer(self.containerName, container)
        
        for node in pm.container(container, query = True, nodeList = True):
            pm.rename(node, "%s_%s" %(_joint, node), ignoreShape = True)
        
        control = "%s_singleJointOrientation_control"  %_joint
        pm.parent(control, self.moduleTransform, absolute = True)
        
        translationControl = self.GetTranslationControl(_joint)
        
        pointConstraint = pm.pointConstraint(translationControl, control, maintainOffset = False, name = "%s_pointConstraint" %control)
        utils.AddNodeToContainer(self.containerName, pointConstraint)
        
        jointOrient = pm.xform(_joint, query = True, worldSpace = True, rotation = True)
        pm.xform(control, worldSpace = True, absolute = True, rotation = jointOrient)
        
        jointNameWithoutNamespace = utils.StripLeadingNamespace(_joint)[1]
        attrName = "%s_R" %jointNameWithoutNamespace
        
        pm.container(container, edit = True, publishAndBind = ["%s.rotate" %control, attrName])
        pm.container(self.containerName, edit = True, publishAndBind = ["%s.%s" %(container, attrName), attrName])
        
        return control
    
    
    def GetSingleJointOrientationControl(self, _jointName):
        return "%s_singleJointOrientation_control" %_jointName