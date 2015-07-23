import pymel.core as pm
import os

import System.blueprint as blueprint
import System.utils as utils
#reload(blueprint)
reload(utils)

CLASS_NAME = "SingleOrientableJoint"
TITLE = "Single Orientable Joint"
DESCRIPTION = "Creates a single joint, with control for position and orientation. Once created (locked) the joint can only rotate. Ideal use: wrist"
ICON = "%s/Icons/_singleOrientable.xpm" %os.environ["RIGGING_TOOL_ROOT"]
#ICON = "%s/nwModularRiggingTool/Icons/_singleOrientable.xpm" %pm.internalVar(userScriptDir = True)

class SingleOrientableJoint(blueprint.Blueprint):

	def __init__(self, _userSpecifiedName, _hookObj):
		jointInfo = [ ["joint", [0.0, 0.0, 0.0]] ]

		blueprint.Blueprint.__init__(self, CLASS_NAME, _userSpecifiedName, jointInfo, _hookObj)


	def Install_custom(self, _joints):
		self.CreateSingleJointOrientationControlAtJoint(_joints[0])
	
	
	def Mirror_custom(self, _originalModule):
		
		jointName = self.jointInfo[0][0]
		originalJoint = "%s:%s" %(_originalModule, jointName)
		newJoint = "%s:%s" %(self.moduleNamespace, jointName)
		
		originalOrientationControl = self.GetSingleJointOrientationControl(originalJoint)
		newOrientationControl = self.GetSingleJointOrientationControl(newJoint)
		
		oldRotation = pm.getAttr("%s.rotate" %originalOrientationControl)
		pm.setAttr("%s.rotate" %newOrientationControl, oldRotation[0], oldRotation[1], oldRotation[2], type = "double3")
	
	
	def UI_custom(self):
		
		joints = self.GetJoints()
		self.CreateRotationOrderUIControl(joints[0])


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
	
		joint = self.GetJoints()[0]
	
	
		# Set locked joint information
		jointPositions.append(pm.xform(joint, query = True, worldSpace = True, translation = True))
	
		jointOrientationValues.append(pm.xform(self.GetSingleJointOrientationControl(joint), query = True, worldSpace = True, rotation = True))
		jointOrientations = (jointOrientationValues, None)
	
		jointRotationOrders.append(pm.getAttr("%s.rotateOrder" %joint))
	
		jointPreferredAngles = None
		hookObject = self.FindHookObjectForLock()
		rootTransform = False
		
	
		# Store locked joint information in a module information tuple and return tuple
		moduleInfo = (jointPositions, jointOrientations, jointRotationOrders, jointPreferredAngles, hookObject, rootTransform)
	
	
		return moduleInfo