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
				
				if index != 0:
					pm.joint(ikJoints[index - 1], edit = True, orientJoint = "xyz", secondaryAxisOrient = "yup")
				
				index += 1
		
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