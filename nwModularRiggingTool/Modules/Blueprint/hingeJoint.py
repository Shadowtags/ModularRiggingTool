import pymel.core as pm
import os

import System.blueprint as blueprint
import System.utils as utils
#reload(blueprint)
reload(utils)

CLASS_NAME = "HingeJoint"
TITLE = "Hinge Joint"
DESCRIPTION = "Creates 3 joints (the middle joint acting as a hinge joint). Ideal use: arm/leg"
ICON = "%s/Icons/_hinge.xpm" %os.environ["RIGGING_TOOL_ROOT"]

class HingeJoint(blueprint.Blueprint):

	def __init__(self, _userSpecifiedName, _hookObj):
		jointInfo = [ ["root_joint", [0.0, 0.0, 0.0]], ["hinge_joint", [4.0, 0.0, -1.0]], ["end_joint", [8.0, 0.0, 0.0]] ]

		blueprint.Blueprint.__init__(self, CLASS_NAME, _userSpecifiedName, jointInfo, _hookObj)
	
	
	def Install_custom(self, _joints):
		
		pm.select(clear = True)
		
		ikJoints = []
		
		if not self.mirrored:
			index = 0
			
			# Create IK joints
			for joint in self.jointInfo:
				
				ikJoints.append(pm.joint(name = "%s:IK_%s" %(self.moduleNamespace, joint[0]), position = joint[1], absolute = True, rotationOrder = "xyz"))
				pm.setAttr("%s.visibility" %ikJoints[index], 0)
				
				# Orient parent joint after children
				if index != 0:
					pm.joint(ikJoints[index - 1], edit = True, orientJoint = "xyz", secondaryAxisOrient = "yup")
				
				index += 1
		
		# Mirror module
		else:
			rootJointName = self.jointInfo[0][0]
			tempDuplicateNodes = pm.duplicate("%s:IK_%s" %(self.originalModule, rootJointName), renameChildren = True)
			
			# Make sure entire hierarchy is being stored in tempDuplicateNodes list
			pm.select(tempDuplicateNodes[0], hierarchy = True)
			tempDuplicateNodes = pm.ls(selection = True)
			
			
			pm.delete(tempDuplicateNodes.pop())
			
			mirrorXY = False
			mirrorYZ = False
			mirrorXZ = False
			
			if self.mirrorPlane == "XY":
				mirrorXY = True
			elif self.mirrorPlane == "YZ":
				mirrorYZ = True
			elif self.mirrorPlane == "XZ":
				mirrorXZ = True
			
			mirrorBehavior = False
			if self.rotationFunction == "behaviour":
				mirrorBehavior = True
			
			
			mirrorJoints = pm.mirrorJoint(tempDuplicateNodes[0], mirrorXY = mirrorXY, mirrorYZ = mirrorYZ, mirrorXZ = mirrorXZ, mirrorBehavior = mirrorBehavior)
			
			pm.delete(tempDuplicateNodes)
			pm.xform(mirrorJoints[0], worldSpace = True, absolute = True, translation = pm.xform("%s:%s" %(self.moduleNamespace, rootJointName), query = True, worldSpace = True, translation = True))
			
			
			for i in range(3):
				jointName = self.jointInfo[i][0]
				newName = pm.rename(mirrorJoints[i], "%s:IK_%s" %(self.moduleNamespace, jointName))
				ikJoints.append(newName)
		
		
		utils.AddNodeToContainer(self.containerName, ikJoints)
		
		
		# Publish attributes in container
		for joint in ikJoints:
			jointName = utils.StripAllNamespaces(joint)[1]
			pm.container(self.containerName, edit = True, publishAndBind = ["%s.rotate" %joint, "%s_R" %jointName])
		
		pm.setAttr("%s.preferredAngleY" %ikJoints[0], -50.0)
		pm.setAttr("%s.preferredAngleY" %ikJoints[1], 50.0)
		
		
		# Setup stretchy segments
		ikNodes = utils.RP_2segment_stretchy_IK(ikJoints[0], ikJoints[1], ikJoints[2], self.containerName)
		locators = (ikNodes[0], ikNodes[1], ikNodes[2])
		distanceNodes = ikNodes[3]
		
		# Point constrain to translation controls
		constraints = []
		for i in range(3):
			constraints.append(pm.pointConstraint(self.GetTranslationControl(_joints[i]), locators[i], maintainOffset = False))
			pm.parent(locators[i], "%s:module_grp" %self.moduleNamespace, absolute = True)
			pm.setAttr("%s.visibility" %locators[i], 0)
		
		utils.AddNodeToContainer(self.containerName, constraints)
		
		# Create preferred angle representation
		scaleTarget = self.GetTranslationControl(_joints[1])
		preferredAngleRep = self.CreatePreferredAngleRepresentation(ikJoints[1], scaleTarget)
		
		
		pm.setAttr("%s.axis" %preferredAngleRep, lock = True)
	
	
	def UI_custom(self):
		joints = self.GetJoints()
		
		self.CreateRotationOrderUIControl(joints[0])
		self.CreateRotationOrderUIControl(joints[1])
	
	
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
		
		pm.lockNode(self.containerName, lock = False, lockUnpublished = False)
		
		ikHandle = "%s:IK_%s_ikHandle" %(self.moduleNamespace, self.jointInfo[0][0])
		pm.delete(ikHandle)
		
		for i in range(3):
			jointName = self.jointInfo[i][0]
			ikJointName = "%s:IK_%s" %(self.moduleNamespace, jointName)
			
			pm.makeIdentity(ikJointName, rotate = True, translate = False, scale = False, apply = True)
			
			jointPositions.append(pm.xform(ikJointName, query = True, worldSpace = True, translation = True))
			
			jointRotationOrders.append(pm.getAttr("%s:%s.rotateOrder" %(self.moduleNamespace, jointName)))
			
			if i < 2:
				jointOrientX = pm.getAttr("%s.jointOrientX" %ikJointName)
				jointOrientY = pm.getAttr("%s.jointOrientY" %ikJointName)
				jointOrientZ = pm.getAttr("%s.jointOrientZ" %ikJointName)
				
				jointOrientationValues.append( (jointOrientX, jointOrientY, jointOrientZ) )
				
				joint_preferredAngle_X = pm.getAttr("%s.preferredAngleX" %ikJointName)
				joint_preferredAngle_Y = pm.getAttr("%s.preferredAngleY" %ikJointName)
				joint_preferredAngle_Z = pm.getAttr("%s.preferredAngleZ" %ikJointName)
				
				jointPreferredAngles.append( (joint_preferredAngle_X, joint_preferredAngle_Y, joint_preferredAngle_Z) )
		
		
		jointOrientations = (jointOrientationValues, None)
		
		hookObject = self.FindHookObjectForLock()
		rootTransform = False
		
		moduleInfo = (jointPositions, jointOrientations, jointRotationOrders, jointPreferredAngles, hookObject, rootTransform)
		return moduleInfo