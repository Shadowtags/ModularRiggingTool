import pymel.core as pm
import os

import System.blueprint as blueprint
#reload(blueprint)


CLASS_NAME = "SingleJointSegment"
TITLE = "Single Joint Segment"
DESCRIPTION = "Creates 2 joints, with control for 1st joint's orientation and rotation order. Ideal use: clavicle bones/shoulder"
ICON = "%s/Icons/_singleJointSeg.xpm" %os.environ["RIGGING_TOOL_ROOT"]
#ICON = "%s/nwModularRiggingTool/Icons/_singleJointSeg.xpm" %pm.internalVar(userScriptDir = True)

class SingleJointSegment(blueprint.Blueprint):

    def __init__(self, _userSpecifiedName, _hookObj):
        
        jointInfo = [ ["root_joint", [0.0, 0.0, 0.0]], ["end_joint", [4.0, 0.0, 0.0]] ]
        
        blueprint.Blueprint.__init__(self, CLASS_NAME, _userSpecifiedName, jointInfo, _hookObj)
    
    
    # Installs module specific controls
    def Install_custom(self, _joints):
        self.CreateOrientationControl(_joints[0], _joints[1])

    
    def Mirror_custom(self, _originalModule):
        jointName = self.jointInfo[0][0]
        originalJoint = "%s:%s" %(_originalModule, jointName)
        newJoint = "%s:%s" %(self.moduleNamespace, jointName)
        
        originalOrientationControl = self.GetOrientationControl(originalJoint)
        newOrientationControl = self.GetOrientationControl(newJoint)
        
        pm.setAttr("%s.rotateX" %newOrientationControl, pm.getAttr("%s.rotateX" %originalOrientationControl))
    
    
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
        
        jointPositions = []
        jointOrientationValues = []
        jointRotationOrders = []
        cleanParent = "%s:joints_grp" %self.moduleNamespace
        
        joints = self.GetJoints()
        
        
        # Set locked joint information
        for joint in joints:
            jointPositions.append(pm.xform(joint, query = True, worldSpace = True, translation = True))
        
        OrientationInfo = self.OrientationControlledJoint_getOrientation(joints[0], cleanParent)
        
        jointOrientationValues.append(OrientationInfo[0])
        jointOrientations = (jointOrientationValues, None)
        
        jointRotationOrders.append(pm.getAttr("%s.rotateOrder" %joints[0]))
        
        jointPreferredAngles = None
        hookObject = self.FindHookObjectForLock()
        rootTransform = False
        
        
        # delete new clean parent
        pm.delete(OrientationInfo[1])
        
        # Store locked joint information in a module information tuple and return tuple
        moduleInfo = (jointPositions, jointOrientations, jointRotationOrders, jointPreferredAngles, hookObject, rootTransform)
        
        
        return moduleInfo
    
    
    # Creates module specific UI controls
    def UI_custom(self):
        joints = self.GetJoints()
        self.CreateRotationOrderUIControl(joints[0])