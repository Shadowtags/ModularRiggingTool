import pymel.core as pm
import System.controlModule as controlModule
reload(controlModule)
import System.utils as utils
reload(utils)

import System.controlObject as controlObject
reload(controlObject)


CLASS_NAME = "FK"
TITLE = "Forward Kinematic"
DESCRIPTION = "This module provides FK rotational controls for every joint in the blueprint it is installed on."



class FK(controlModule.ControlModule):
	
	def __init__(self, _moduleNamespace):
		controlModule.ControlModule.__init__(self, _moduleNamespace)

	
	def CompatibleBlueprintModules(self):
		return ("Finger", "HingeJoint", "LegFoot", "SingleJointSegment", "SingleOrientableJoint", "Spline", "Thumb")
	
	
	def Install_custom(self, _joints, _moduleGrp, _moduleContainer):
		controlsGrp = pm.group(empty = True, name = "%s:%s:controls_grp" %(self.blueprintNamespace, self.moduleNamespace))
		pm.parent(controlsGrp, _moduleGrp, absolute = True)
		
		utils.AddNodeToContainer(_moduleContainer, controlsGrp)
		
		numJoints = len(_joints) -1
		
		for i in range(1, len(_joints)):
			if i < numJoints or numJoints == 1:
				self.CreateFKControl(_joints[i], controlsGrp, _moduleContainer)
	
	
	def CreateFKControl(self, _joint, _parent, _moduleContainer):
		jointName = utils.StripAllNamespaces(_joint)[1]
		containedNodes = []
		name = "%s_fkControl" %jointName
		
		controlObjectInstance = controlObject.ControlObject()
		
		fkControlInfo = controlObjectInstance.Create(name, "sphere.ma", self, _lod = 1, _translation = False, _rotation = True, _globalScale = False, _spaceSwitching = False)
		fkControl = fkControlInfo[0]
		
		pm.connectAttr("%s.rotateOrder" %_joint, "%s.rotateOrder" %fkControl)
		
		orientGrp = pm.group(name = "%s_orientGrp", empty = True, parent = _parent)
		containedNodes.append(orientGrp)
		
		pm.delete(pm.parentConstraint(_joint, orientGrp, maintainOffset = False))
		
		jointParent = pm.listRelatives(_joint, parent = True)[0]
		
		orientGrp_parentConstraint = pm.parentConstraint(jointParent, orientGrp, maintainOffset = True, name = "%s_parentConstraint" %orientGrp)
		orientGrp_scaleConstraint = pm.scaleConstraint(jointParent, orientGrp, maintainOffset = True, name = "%s_scaleConstraint" %orientGrp)
		
		pm.parent(fkControl, orientGrp, relative = True)
		
		orientConstraint = pm.orientConstraint(fkControl, _joint, maintainOffset = False, name = "%s_orientConstraint" %_joint)
		
		containedNodes.extend([orientGrp_parentConstraint, orientGrp_scaleConstraint, orientConstraint])
		
		utils.AddNodeToContainer(_moduleContainer, containedNodes)
		
		return fkControl
	
	
	def UI(self, _parentLayout):
		jointsGrp = "%s:%s:joints_grp" %(self.blueprintNamespace, self.moduleNamespace)
		joints = utils.FindJointChain(jointsGrp)
		
		joints.pop(0)
		numJoints = len(joints)
		
		if numJoints > 1:
			numJoints -= 1
		
		for i in range(numJoints):
			fkControl = "%s_fkControl" %joints[i]
			controlObjectInstance = controlObject.ControlObject(fkControl)
			
			controlObjectInstance.UI(_parentLayout)