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
        self.moduleGrp = pm.group(self.jointsGrp, name = "%s:module_grp" %self.moduleNamespace)
        
        pm.container(name = self.containerName, addNode = [self.moduleGrp], includeHierarchyBelow = True)
        
        pm.select(clear = True)
        
        index = 0
        joints = []
        
        for joint in self.jointInfo:
            
            jointName = joint[0]
            jointPos = joint[1]
            parentJoint = ''
            
            if index > 0:
                parentJoint = "%s:%s" %(self.moduleNamespace, self.jointInfo[index - 1][0])
                pm.select(parentJoint, replace = True)
            
            jointName_full = pm.joint(name = "%s:%s" %(self.moduleNamespace, jointName), position = jointPos)
            joints.append(jointName_full)
            
            pm.container(self.containerName, edit = True, addNode = jointName_full)
            
            pm.container(self.containerName, edit = True, publishAndBind = ["%s.rotate" %jointName_full, "%s_R" %jointName])
            pm.container(self.containerName, edit = True, publishAndBind = ["%s.rotateOrder" %jointName_full, "%s_RotateOrder" %jointName])
            
            if index > 0:
                pm.joint(parentJoint, edit = True, orientJoint = 'xyz', secondaryAxisOrient = 'yup')
            
            index += 1
        
        
        pm.parent(joints[0], self.jointsGrp, absolute = True)
        
        
        translationControls = []
        for joint in joints:
            translationControls.append(self.CreateTransationControlAtJoint(joint))
        
        rootJoint_pointConstraint = pm.pointConstraint(translationControls[0], joints[0], maintainOffset = False, name = "%s_pointConstraint" %joints[0])
        pm.container(self.containerName, edit = True, addNode = rootJoint_pointConstraint)
        
        # Setup strechy joint segment
        for index in range(len(joints) - 1):
            self.SetupStrechyJointSegment(joints[index], joints[index + 1])
        
        
        pm.lockNode(self.containerName, lock = True, lockUnpublished = True)
    
    
    
    def CreateTransationControlAtJoint(self, _joint):
        
        posControlFile = "%s/ControlObjects/Blueprint/translation_control.ma" %os.environ["RIGGING_TOOL_ROOT"]
        pm.importFile(posControlFile)
        
        container = pm.rename("translation_control_container", "%s_translation_control_container" %_joint)
        pm.container(self.containerName, edit = True, addNode = container)
        
        
        for node in pm.container(container, query = True, nodeList = True):
            pm.rename(node, "%s_%s" %(_joint, node), ignoreShape = True)
        
        
        control = "%s_translation_control" %_joint
        
        jointPos = pm.xform(_joint, query = True, worldSpace = True, translation = True)
        pm.xform(control, worldSpace = True, absolute = True, translation = jointPos)
        
        niceName = utils.StripLeadingNamespace(_joint)[1]
        attrName = "%s_T" %niceName
        
        pm.container(container, edit = True, publishAndBind = ["%s.translate" %control, attrName])
        pm.container(self.containerName, edit = True, publishAndBind = ["%s.%s" %(container, attrName), attrName])
        
        return control
    
    
    
    def GetTranslationControl(self, _jointName):
        return "%s_translation_control" %_jointName
    
    
    
    
    def SetupStrechyJointSegment(self, _parentJoint, _childJoint):
        
        parentTranslationControl = self.GetTranslationControl(_parentJoint)
        childTranslationControl = self.GetTranslationControl(_childJoint)
        
        poleVectorLocator = pm.spaceLocator(name = "%s_poleVectorLocator" %parentTranslationControl)
        
        poleVectorLocatorGrp = pm.group(poleVectorLocator, name = "%s_parentConstraintGrp" %poleVectorLocator)
        
        pm.parent(poleVectorLocatorGrp, self.moduleGrp, absolute = True)
        parentConstraint = pm.parentConstraint(parentTranslationControl, poleVectorLocatorGrp, maintainOffset = False)
        
        pm.setAttr("%s.visibility" %poleVectorLocator)
        pm.setAttr("%s.ty" %poleVectorLocator, -0.5)
        
        
        ikNodes = utils.BasicStrechyIK(_parentJoint, _childJoint, _container = self.containerName, _lockMinimumLength = False, _poleVectorObject = poleVectorLocator, _scaleCorrectionAttribute = None)
        ikHandle = ikNodes["ikHandle"]
        rootLocator = ikNodes["rootLocator"]
        endLocator = ikNodes["endLocator"]
        
        childPointConstraint = pm.pointConstraint(childTranslationControl, endLocator, maintainOffset = False, name = "%s_pointConstraint" %endLocator)
        
        pm.container(self.containerName, edit = True, addNode = [poleVectorLocatorGrp, parentConstraint, childPointConstraint], includeHierarchyBelow = True)
        
        for node in [ikHandle, rootLocator, endLocator]:
            pm.parent(node, self.jointsGrp, absolute = True)
            pm.setAttr("%s.visibility" %node, 0)