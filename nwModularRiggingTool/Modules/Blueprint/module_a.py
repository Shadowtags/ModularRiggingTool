import pymel.core as pm
import os

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
        
        pm.lockNode(self.containerName, lock = True, lockUnpublished = True)