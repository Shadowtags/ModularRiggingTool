import pymel.core as pm
import os

from functools import partial

import System.blueprint as blueprint
import System.utils as utils
#reload(blueprint)
reload(utils)

CLASS_NAME = "Spline"
TITLE = "Spline"
DESCRIPTION = "Creates an optionally interpolating, joint-count adjustable, spline. Ideal use: spine, neck/head, tails, tentacles etc."
ICON = "%s/Icons/_spline.xpm" %os.environ["RIGGING_TOOL_ROOT"]

class Spline(blueprint.Blueprint):

	def __init__(self, _userSpecifiedName, _hookObj, _numberOfJoints = None, _startJointPos = None, _endJointPos = None):
		
		if _numberOfJoints == None:
			jointsGrp = "%s__%s:joints_grp" %(CLASS_NAME, _userSpecifiedName)
			
			# Default number of joints
			if not pm.objExists(jointsGrp):
				_numberOfJoints = 5
			
			else:
				joints = utils.FindJointChain(jointsGrp)
				joints.pop()
				
				_numberOfJoints = len(joints)
		
		jointInfo = []
		
		if _startJointPos == None:
			_startJointPos = [0.0, 0.0, 0.0]
		if _endJointPos == None:
			_endJointPos = [0.0, 15.0, 0.0]
		
		jointIncrement = list(_endJointPos)
		
		jointIncrement[0] -= _startJointPos[0]
		jointIncrement[1] -= _startJointPos[1]
		jointIncrement[2] -= _startJointPos[2]
		
		jointIncrement[0] /= (_numberOfJoints - 1)
		jointIncrement[1] /= (_numberOfJoints - 1)
		jointIncrement[2] /= (_numberOfJoints - 1)
		
		
		jointPos = _startJointPos
		
		for i in range(_numberOfJoints):
			jointName = "spline_%d_joint" %(i + 1)
			
			jointInfo.append([jointName, list(jointPos)])
			
			jointPos[0] += jointIncrement[0]
			jointPos[1] += jointIncrement[1]
			jointPos[2] += jointIncrement[2]
		

		blueprint.Blueprint.__init__(self, CLASS_NAME, _userSpecifiedName, jointInfo, _hookObj)
		
		self.canBeMirrored = False
	
	
	def Install_custom(self, _joints):
		
		self.SetupInterpolation()
		
		moduleGrp = "%s:module_grp" %self.moduleNamespace
		pm.select(moduleGrp, replace = True)
		
		pm.addAttr(attributeType = "enum", enumName = "y:z", longName = "sao_local")
		pm.addAttr(attributeType = "enum", enumName = "+x:-x:+y:-y:+z:-z", longName = "sao_world")
		
		for attr in ["sao_local", "sao_world"]:
			pm.container(self.containerName, edit = True, publishAndBind = ["%s.%s" %(moduleGrp, attr), attr] )
	
	
	
	def SetupInterpolation(self, _unlockContainer = False, *args):
		previousSelection = pm.ls(selection = True)
		
		if _unlockContainer:
			pm.lockNode(self.containerName, lock = False, lockUnpublished = False)
		
		joints = self.GetJoints()
		numberOfJoints = len(joints)
		
		startControl = self.GetTranslationControl(joints[0])
		endControl = self.GetTranslationControl(joints[numberOfJoints - 1])
		
		pointConstraints = []
		
		for i in range(1, numberOfJoints - 1):
			material = "%s_m_translation_control" %joints[i]
			pm.setAttr("%s.colorR" %material, 0.815)
			pm.setAttr("%s.colorG" %material, 0.629)
			pm.setAttr("%s.colorB" %material, 0.498)
			
			translationControl = self.GetTranslationControl(joints[i])
			
			# Calculate constraint influence depending of distance from start/end
			endWeight = 0.0 + (float(i) / (numberOfJoints - 1))
			startWeight = 1.0 - endWeight
			
			# point constraint between start/end
			pointConstraints.append(pm.pointConstraint(startControl, translationControl, maintainOffset = False, weight = startWeight))
			pointConstraints.append(pm.pointConstraint(endControl, translationControl, maintainOffset = False, weight = endWeight))
			
			# Lock translation attribute of control
			for attr in [".translateX", ".translateY", ".translateZ"]:
				pm.setAttr("%s%s" %(translationControl, attr), lock = True)
		
		interpolationContainer = pm.container(name = "%s:interpolation_container" %self.moduleNamespace)
		utils.AddNodeToContainer(interpolationContainer, pointConstraints)
		utils.AddNodeToContainer(self.containerName, interpolationContainer)
		
		if _unlockContainer:
			pm.lockNode(self.containerName, lock = True, lockUnpublished = True)
		
		
		# Reselect initial selection
		if len(previousSelection) > 0:
			pm.select(previousSelection, replace = True)
		else:
			pm.select(clear = True)
	
	
	def UI_custom(self):
		
		numJoints = len(self.jointInfo)
		
		pm.rowLayout(numberOfColumns = 2, columnWidth = [1, 100], adjustableColumn = 2)
		pm.text(label = "Number of Joints: ")
		self.numberOfJointsField = pm.intField(value = numJoints, minValue = 2, changeCommand = self.ChangeNumberOfJoints)
		
		pm.setParent('..')
		
		joints = self.GetJoints()
		self.CreateRotationOrderUIControl(joints[0])
		
		pm.separator(style = 'in')
		
		pm.text(label = "Orientation: ", align = "left")
		pm.rowLayout(numberOfColumns = 3)
		pm.attrEnumOptionMenu(attribute = "%s:module_grp.sao_local" %self.moduleNamespace, label = "Local: ")
		pm.text(label = " will be oriented to ")
		pm.attrEnumOptionMenu(attribute = "%s:module_grp.sao_world" %self.moduleNamespace, label = "World: ")
		
		pm.setParent('..')
		
		pm.separator(style = 'in')
		
		interpolating = False
		if pm.objExists("%s:interpolation_container" %self.moduleNamespace):
			interpolating = True
		
		
		pm.rowLayout(numberOfColumns = 2, columnWidth = [1, 80], adjustableColumn = 2)
		pm.text(label = "Interpolate: ")
		pm.checkBox(label = "", value = interpolating, onCommand = partial(self.SetupInterpolation, True), offCommand = self.DeleteInterpolation)
	
	
	
	def DeleteInterpolation(self, *args):
		pm.lockNode(self.containerName, lock = False, lockUnpublished = False)
		
		joints = self.GetJoints()
		
		for i in range(1, len(joints) - 1):
			translationControl = self.GetTranslationControl(joints[i])
			
			for attr in [".translateX", ".translateY", ".translateZ"]:
				pm.setAttr("%s%s" %(translationControl, attr), lock = False)
			
			material = "%s_m_translation_control" %joints[i]
			
			pm.setAttr("%s.colorR" %material, 0.758)
			pm.setAttr("%s.colorG" %material, 0.051)
			pm.setAttr("%s.colorB" %material, 0.102)
		
		pm.delete("%s:interpolation_container" %self.moduleNamespace)
		
		pm.lockNode(self.containerName, lock = True, lockUnpublished = True)
	
	
	
	def ChangeNumberOfJoints(self, *args):
		self.blueprint_UI_instance.DeleteScriptJob()
		
		# Collect information from current spline module
		joints = self.GetJoints()
		numJoints = len(joints)
		
		newNumJoints = pm.intField(self.numberOfJointsField, query = True, value = True)
		
		startPos = pm.xform(self.GetTranslationControl(joints[0]), query = True, worldSpace = True, translation = True)
		endPos = pm.xform(self.GetTranslationControl(joints[numJoints - 1]), query = True, worldSpace = True, translation = True)
		
		hookObj = self.FindHookObjectForLock()
		
		rotateOrder = pm.getAttr("%s.rotateOrder" %joints[0])
		sao_local = pm.getAttr("%s:module_grp.sao_local" %self.moduleNamespace)
		sao_world = pm.getAttr("%s:module_grp.sao_world" %self.moduleNamespace)
		
		# Delete current spline module
		self.Delete()
		
		# Create new spline module with new joint count
		newInstance = Spline(self.userSpecifiedName, hookObj, newNumJoints, startPos, endPos)
		newInstance.Install()
		
		# Apply previous attribute values
		newJoints = newInstance.GetJoints()
		pm.setAttr("%s.rotateOrder" %newJoints[0], rotateOrder)
		pm.setAttr("%s:module_grp.sao_local" %newInstance.moduleNamespace, sao_local)
		pm.setAttr("%s:module_grp.sao_world" %newInstance.moduleNamespace, sao_world)
		
		self.blueprint_UI_instance.CreateScriptJob()
		
		pm.select("%s:module_transform" %newInstance.moduleNamespace, replace = True)