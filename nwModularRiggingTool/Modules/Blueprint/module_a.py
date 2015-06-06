import pymel.core as pm
import System.utils as utils
import os

reload(utils)

CLASS_NAME = "ModuleA"

TITLE = "module A"
DESCRIPTION = "Test description for module A"
ICON = "%s/Icons/_hand.xpm" %os.environ["RIGGING_TOOL_ROOT"]

class ModuleA():
    
    def __init__(self, _userSpecifiedName):
        
        self.moduleName = CLASS_NAME
        self.userSpecName = _userSpecifiedName
        
        self.moduleNamespace = "%s__%s" %(self.moduleName, self.userSpecName)
        
        self.containerName = "%s:module_container" %self.moduleNamespace
        
        self.jointInfo = [ ["root_joint", [0.0, 0.0, 0.0]], ["end_joint", [4.0, 0.0, 0.0]] ]
    
    
    
    def Install(self):
        
        pm.namespace(setNamespace = ':')
        pm.namespace(add = self.moduleNamespace)
        
        self.jointsGrp = pm.group(empty = True, name = "%s:joints_grp" %self.moduleNamespace)
        self.hierarchyRepresentationGrp = pm.group(empty = True, name = "%s:hierarchyRepresentation_grp" %self.moduleNamespace)
        self.orientationGrp = pm.group(empty = True, name = "%s:orientationControls_grp" %self.moduleNamespace)
        self.moduleGrp = pm.group([self.jointsGrp, self.hierarchyRepresentationGrp, self.orientationGrp], name = "%s:module_grp" %self.moduleNamespace)
        
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
        
        
        # Setup strechy joint segment
        for index in range(len(joints) - 1):
            self.SetupStrechyJointSegment(joints[index], joints[index + 1])
        
        
        # NON DEFAULT FUNCTUNALITY
        self.CreateOrientationControl(joints[0], joints[1])
        
        
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
    
    
    
    
    def SetupStrechyJointSegment(self, _parentJoint, _childJoint):
        
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