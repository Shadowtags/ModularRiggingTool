import pymel.core as pm
import os

import System.blueprint as blueprint
import Blueprint.hingeJoint as hingeJoint

import System.utils as utils
#reload(blueprint)
reload(utils)

CLASS_NAME = "LegFoot"
TITLE = "Leg and Foot"
DESCRIPTION = "Creates 5 joints. The first 3 acting as hip, knee and ankle(a hinge joint setup), the last 2 acting as ball and toe. Ideal use: leg and foot"
ICON = "%s/Icons/_legFoot.png" %os.environ["RIGGING_TOOL_ROOT"]
#ICON = "%s/nwModularRiggingTool/Icons/_legFoot.png" %pm.internalVar(userScriptDir = True)

class LegFoot(hingeJoint.HingeJoint):

	def __init__(self, _userSpecifiedName, _hookObj):
		jointInfo = [ ["hip_joint", [0.0, 0.0, 0.0]], ["knee_joint", [4.0, 0.0, -1.0]], ["ankle_joint", [8.0, 0.0, 0.0]], ["ball_joint", [0.0, -9.0, 3.0]], ["toe_joint", [0.0, -9.0, 6.0]] ]

		blueprint.Blueprint.__init__(self, CLASS_NAME, _userSpecifiedName, jointInfo, _hookObj)
	
	
	def Install_custom(self, _joints):
		
		hingeJoint.HingeJoint.Install_custom(self, _joints)
		
		ankleOrientationControl = self.CreateOrientationControl(_joints[2], _joints[3])
		ballOrientationControl = self.CreateOrientationControl(_joints[3], _joints[4])
		
		pm.setAttr("%s.rotateX" %ankleOrientationControl, -90)
		pm.setAttr("%s.rotateX" %ballOrientationControl, -90)
		
		pm.xform(self.GetTranslationControl(_joints[1]), worldSpace = True, absolute = True, translation = [0.0, -4.0, 1.0])
		pm.xform(self.GetTranslationControl(_joints[2]), worldSpace = True, absolute = True, translation = [0.0, -8.0, 0.0])
		
		
		for i in range(len(_joints) - 1):
			joint = _joints[i]
			
			rotateOrder = 3		# xzy
			
			if i >= 2:
				rotateOrder = 0		# xyz
			
			pm.setAttr("%s.rotateOrder" %joint, rotateOrder)
	
	
	def Mirror_custom(self, _originalModule):
		
		offset = 0
		
		for i in range(2, 4):
			
			if i == 3:
				offset = -90
			
			jointName = self.jointInfo[i][0]
			
			originalJoint = "%s:%s" %(_originalModule, jointName)
			newJoint = "%s:%s" %(self.moduleNamespace, jointName)
		
			originalOrientationControl = self.GetOrientationControl(originalJoint)
			newOrientationControl = self.GetOrientationControl(newJoint)
			
			pm.setAttr("%s.rotateX" %newOrientationControl, pm.getAttr("%s.rotateX" %originalOrientationControl) + offset)
	
	
	def UI_custom(self):
		
		hingeJoint.HingeJoint.UI_custom(self)
		
		joints = self.GetJoints()
		self.CreateRotationOrderUIControl(joints[2])
		self.CreateRotationOrderUIControl(joints[3])
	
	
	
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
		
		moduleInfo = hingeJoint.HingeJoint.Lock_phase1(self)
		
		jointPositions = moduleInfo[0]
		jointOrientationValues = moduleInfo[1][0]
		jointRotationOrders = moduleInfo[2]
		
		joints = self.GetJoints()
		for i in range(3, 5):
			joint = joints[i]
			
			jointPositions.append(pm.xform(joint, query = True, worldSpace = True, translation = True))
			jointRotationOrders.append(pm.getAttr("%s.rotateOrder" %joint))
		
		pm.lockNode(self.containerName, lock = False, lockUnpublished = False)
		
		jointNameInfo = utils.StripAllNamespaces(joints[1])
		cleanParent = "%s:IK_%s" %(jointNameInfo[0], jointNameInfo[1])  # ikKnee
		
		# Get orientation values for ankle and ball joints
		deleteJoints = []
		for i in range(2, 4):
			orientationInfo = self.OrientationControlledJoint_getOrientation(joints[i], cleanParent)
			jointOrientationValues.append(orientationInfo[0])
			cleanParent = orientationInfo[1]
			deleteJoints.append(cleanParent)
		
		pm.delete(deleteJoints)
		
		pm.lockNode(self.containerName, lock = True, lockUnpublished = True)
		
		return moduleInfo