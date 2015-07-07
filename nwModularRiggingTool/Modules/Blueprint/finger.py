import pymel.core as pm
import os

import System.blueprint as blueprint
import System.utils as utils
#reload(blueprint)
reload(utils)

CLASS_NAME = "Finger"
TITLE = "Finger"
DESCRIPTION = "Creates 5 joints, defining a finger. Ideal use: finger"
ICON = "%s/Icons/_finger.xpm" %os.environ["RIGGING_TOOL_ROOT"]

class Finger(blueprint.Blueprint):
	
	def __init__(self, _userSpecifiedName, _hookObj):
		jointInfo = [ ["root_joint", [0.0, 0.0, 0.0]], ["knuckle_1_joint", [4.0, 0.0, 0.0]], ["knuckle_2_joint", [8.0, 0.0, 0.0]], ["knuckle_3_joint", [12.0, 0.0, 0.0]], ["end_joint", [16.0, 0.0, 0.0]]]
		
		blueprint.Blueprint.__init__(self, CLASS_NAME, _userSpecifiedName, jointInfo, _hookObj)
	
	
	def Install_custom(self, _joints):
		
		for i in range(len(_joints) - 1):
			pm.setAttr("%s.rotateOrder" %_joints[i], 3)	 # xzy
			
			self.CreateOrientationControl(_joints[i], _joints[i+1])
			
			preferredAngleControl = self.CreatePreferredAngleRepresentation(_joints[i], self.GetTranslationControl(_joints[i]), _childOfOrientationControl = True)
			pm.setAttr("%s.axis" %preferredAngleControl, 3)
		
		
		if not self.mirrored:
			pm.setAttr("%s:module_transform.globalScale" %self.moduleNamespace, 0.25)
	
	
	def Mirror_custom(self, _originalModule):
		
		for i in range(len(self.jointInfo) - 1):
			jointName = self.jointInfo[i][0]
			
			originalJoint = "%s:%s" %(_originalModule, jointName)
			newJoint = "%s:%s" %(self.moduleNamespace, jointName)
			
			originalOrientationControl = self.GetOrientationControl(originalJoint)
			newOrientationControl = self.GetOrientationControl(newJoint)
			
			pm.setAttr("%s.rotateX" %newOrientationControl, pm.getAttr("%s.rotateX" %originalOrientationControl))
			
			originalPreferredAngleControl = self.GetPreferredAngleControl(originalJoint)
			newPreferredAngleControl = self.GetPreferredAngleControl(newJoint)
			
			pm.setAttr("%s.axis" %newPreferredAngleControl, pm.getAttr("%s.axis" %originalPreferredAngleControl))
	
	
	def UI_custom(self):
		joints = self.GetJoints()
		joints.pop()
		
		for joint in joints:
			self.CreateRotationOrderUIControl(joint)
		
		for joint in joints:
			self.CreatePreferredAngleUIControl(self.GetPreferredAngleControl(joint))
	
	
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
		jointPreferredAngles = []
	
		joints = self.GetJoints()
		
		deleteJoints = []
		
		index = 0
		cleanParent = "%s:joints_grp" %self.moduleNamespace
		
		for joint in joints:
			jointPositions.append(pm.xform(joint, query = True, worldSpace = True, translation = True))
			jointRotationOrders.append(pm.getAttr("%s.rotateOrder" %joint))
			
			if index < len(joints) - 1:
				orientationInfo = self.OrientationControlledJoint_getOrientation(joint, cleanParent)
				
				
				jointOrientationValues.append(orientationInfo[0])
				cleanParent = orientationInfo[1]
				deleteJoints.append(cleanParent)
				
				jointPrefAngles = [0.0, 0.0, 0.0]
				axis = pm.getAttr("%s.axis" %self.GetPreferredAngleControl(joint))
				
				# Preferred angle positive Y
				if axis == 0:
					jointPrefAngles[1] = 50.0
				
				# Preferred angle negative Y
				elif axis == 1:
					jointPrefAngles[1] = -50.0
				
				# Preferred angle positive Z
				elif axis == 2:
					jointPrefAngles[2] = 50.0
				
				# Preferred angle negative Z
				elif axis == 3:
					jointPrefAngles[2] = -50.0
				
				jointPreferredAngles.append(jointPrefAngles)
			
			index += 1
		
		
		jointOrientations = (jointOrientationValues, None)
		
		pm.delete(deleteJoints)
		
		hookObject = self.FindHookObjectForLock()
		
		rootTransform = False
		
		moduleInfo = (jointPositions, jointOrientations, jointRotationOrders, jointPreferredAngles, hookObject, rootTransform)
		
		return moduleInfo