import pymel.core as pm
import System.utils as utils
reload(utils)

from functools import partial


class ControlModule:
	
	def __init__(self, _moduleNamespace):
		
		# Class variables
		self.moduleContainer = None
		self.blueprintNamespace = ''
		self.moduleNamespace = ''
		self.characterNamespace = ''
		self.publishedNames = []
		
		
		if _moduleNamespace == None:
			return
		
		# Break down namespace info for easy access
		moduleNamespaceInfo = utils.StripAllNamespaces(_moduleNamespace)
		
		self.blueprintNamespace = moduleNamespaceInfo[0]
		self.moduleNamespace = moduleNamespaceInfo[1]
		self.characterNamespace = utils.StripLeadingNamespace(self.blueprintNamespace)[0]
		
		self.moduleContainer = "%s:%s:module_container" %(self.blueprintNamespace, self.moduleNamespace)
	
	
	def Install_custom(self, _joints, _moduleGrp, _moduleContainer):
		print "Install_custom() method not implemented bt derived module"

	
	def CompatibleBlueprintModules(self):
		return ("-1")
	
	
	def Install(self):
		nodes = self.Install_init()
		joints = nodes[0]
		moduleGrp = nodes[1]
		moduleContainer = nodes[2]
		
		self.Install_custom(joints, moduleGrp, moduleContainer)
		
		self.Install_finalize()
	
	
	def Install_init(self):
		pm.namespace(setNamespace = self.blueprintNamespace)
		pm.namespace(add = self.moduleNamespace)
		pm.namespace(setNamespace = ":")
		
		characterContainer = "%s:character_container" %self.characterNamespace
		blueprintContainer = "%s:module_container" %self.blueprintNamespace
		container = [characterContainer, blueprintContainer]
		
		for c in container:
			pm.lockNode(c, lock = False, lockUnpublished = False)
		
		self.joints = self.DuplicateAndRenameCreationPose()
		moduleJointsGrp = self.joints[0]
		
		moduleGrp = pm.group(empty = True, name = "%s:%s:module_grp" %(self.blueprintNamespace, self.moduleNamespace))
		hookIn = "%s:HOOK_IN" %self.blueprintNamespace
		pm.parent(moduleGrp, hookIn, relative = True)
		pm.parent(moduleJointsGrp, moduleGrp, absolute = True)
		
		pm.select(moduleGrp, replace = True)
		pm.addAttr(attributeType = "float", longName = "iconScale", minValue = 0.001, softMaxValue = 10.0, defaultValue = 1.0, keyable = True)
		pm.setAttr("%s.overrideEnabled" %moduleGrp, 1)
		pm.setAttr("%s.overrideColor" %moduleGrp, 6)
		
		
		utilityNodes = self.SetupBlueprintWeightBasedBlending()
		
		self.SetupModuleVisibility(moduleGrp)
		
		
		containedNodes = []
		containedNodes.extend(self.joints)
		containedNodes.append(moduleGrp)
		containedNodes.extend(utilityNodes)
		
		
		self.moduleContainer = pm.container(name = self.moduleContainer)
		utils.AddNodeToContainer(self.moduleContainer, containedNodes, True)
		utils.AddNodeToContainer(blueprintContainer, self.moduleContainer)
		
		index = 0
		for joint in self.joints:
			if index > 0:
				niceJointName = utils.StripAllNamespaces(joint)[1]
				self.PublishNameToModuleContainer("%s.rotate" %joint, "%s_R" %niceJointName, False)
			
			index += 1
		
		self.PublishNameToModuleContainer("%s.levelOfDetail" %moduleGrp, "Control_LOD")
		self.PublishNameToModuleContainer("%s.iconScale" %moduleGrp, "Icon_Scale")
		self.PublishNameToModuleContainer("%s.overrideColor" %moduleGrp, "Icon_Color")
		self.PublishNameToModuleContainer("%s.visibility" %moduleGrp, "Visibility", False)
		
		return (self.joints, moduleGrp, self.moduleContainer)
	
	
	def Install_finalize(self):
		self.PublishModuleContainerNamesToOuterContainers()
		
		pm.setAttr("%s:blueprint_joints_grp.controlModulesInstalled" %self.blueprintNamespace, True)
		
		characterContainer = "%s:character_container" %self.characterNamespace
		blueprintContainer = "%s:module_container" %self.blueprintNamespace
		
		containers = [characterContainer, blueprintContainer, self.moduleContainer]
		for c in containers:
			pm.lockNode(c, lock = True, lockUnpublished = True)
	
	
	def DuplicateAndRenameCreationPose(self):
		joints = pm.duplicate("%s:creationPose_joints_grp" %self.blueprintNamespace, renameChildren = True)
		pm.select(joints, hierarchy = True)
		joints = pm.ls(selection = True)
		
		for i in range(len(joints)):
			nameSuffix = joints[i].rpartition("creationPose_")[2]
			joints[i] = pm.rename(joints[i], "%s:%s:%s" %(self.blueprintNamespace, self.moduleNamespace, nameSuffix))
		
		return joints
	
	
	def SetupBlueprintWeightBasedBlending(self):
		settingsLocator = "%s:SETTINGS" %self.blueprintNamespace
		
		attributes = pm.listAttr(settingsLocator, keyable = False)
		weightAttributes = []
		for attr in attributes:
			if attr.find("_weight") != -1:
				weightAttributes.append(attr)
		
		
		value = 0
		if len(weightAttributes) == 0:
			value = 1
			pm.setAttr("%s.creationPoseWeight" %settingsLocator, 0)
		
		
		pm.select(settingsLocator, replace = True)
		weightAttributeName = "%s_weight" %self.moduleNamespace
		
		pm.addAttr(longName = weightAttributeName, attributeType = "double", minValue = 0, maxValue = 1, defaultValue = value, keyable = False)
		
		pm.container("%s:module_container" %self.blueprintNamespace, edit = True, publishAndBind = ["%s.%s" %(settingsLocator, weightAttributeName), weightAttributeName])
		
		currentEntries = pm.attributeQuery("activeModule", node = settingsLocator, listEnum = True)
		
		newEntry = self.moduleNamespace
		
		if currentEntries[0] == "None":
			pm.addAttr("%s.activeModule" %settingsLocator, edit = True, enumName = newEntry)
			pm.setAttr("%s.activeModule" %settingsLocator, 0)
		
		else:
			pm.addAttr("%s.activeModule" %settingsLocator, edit = True, enumName = "%s:%s" %(currentEntries[0], newEntry))
		
		
		utilityNodes = []
		
		for i in range(1, len(self.joints)):
			joint = self.joints[i]
			
			nameSuffix = utils.StripAllNamespaces(joint)[1]
			blueprintJoint = "%s:blueprint_%s" %(self.blueprintNamespace, nameSuffix)
			
			weightNodeAttr = "%s.%s" %(settingsLocator, weightAttributeName)
			
			if i < len(self.joints) - 1 or len(self.joints) == 2:
				multiplyRotations = pm.shadingNode("multiplyDivide", name = "%s_multiplyRotationsWeight" %joint, asUtility = True)
				utilityNodes.append(multiplyRotations)
				
				pm.connectAttr("%s.rotate" %joint, "%s.input1" %multiplyRotations, force = True)
				
				for attr in ["input2X", "input2Y", "input2Z"]:
					pm.connectAttr(weightNodeAttr, "%s.%s" %(multiplyRotations, attr), force = True)
				
				index = utils.FindFirstFreeConnection("%s_addRotations.input3D" %blueprintJoint)
				pm.connectAttr("%s.output" %multiplyRotations, "%s_addRotations.input3D[%d]" %(blueprintJoint, index), force = True)
			
			
			if i == 1:
				addNode = "%s_addTranslate" %blueprintJoint
				
				if pm.objExists(addNode):
					multiplyTranslation = pm.shadingNode("multiplyDivide", name = "%s_multiplyTranslationWeight" %joint, asUtility = True)
					utilityNodes.append(multiplyTranslation)
					
					pm.connectAttr("%s.translate" %joint, "%s.input1" %multiplyTranslation, force = True)
					for attr in ["input2X", "input2Y", "input2Z"]:
						pm.connectAttr(weightNodeAttr, "%s.%s" %(multiplyTranslation, attr), force = True)
					
					index = utils.FindFirstFreeConnection("%s.input3D" %addNode)
					pm.connectAttr("%s.output" %multiplyTranslation, "%s.input3D[%d]" %(addNode, index), force = True)
					
					addNode = "%s_addScale" %blueprintJoint
					if pm.objExists(addNode):
						multiplyScale = pm.shadingNode("multiplyDivide", name = "%s_multiplyScaleWeight" %joint, asUtility = True)
						utilityNodes.append(multiplyScale)
						
						pm.connectAttr("%s.scale" %joint, "%s.input1" %multiplyScale, force = True)
						for attr in ["input2X", "input2Y", "input2Z"]:
							pm.connectAttr(weightNodeAttr, "%s.%s" %(multiplyScale, attr), force = True)
						
						index = utils.FindFirstFreeConnection("%s.input3D" %addNode)
						pm.connectAttr("%s.output" %multiplyScale, "%s.input3D[%d]" %(addNode, index), force = True)

			
			else:
				multiplyTranslation = pm.shadingNode("multiplyDivide", name = "%s_multiplyTranslationWeight" %joint, asUtility = True)
				utilityNodes.append(multiplyTranslation)
				
				pm.connectAttr("%s.translateX" %joint, "%s.input1X" %multiplyTranslation, force = True)
				pm.connectAttr(weightNodeAttr, "%s.input2X" %multiplyTranslation, force = True)
				
				addNode = "%s_addTx" %blueprintJoint
				
				index = utils.FindFirstFreeConnection("%s.input1D" %addNode)
				pm.connectAttr("%s.outputX" %multiplyTranslation, "%s.input1D[%d]" %(addNode, index), force = True)
		
		
		return utilityNodes
	
	
	def SetupModuleVisibility(self, _moduleGrp):
		pm.select(_moduleGrp, replace = True)
		pm.addAttr(attributeType = "byte", defaultValue = 1, minValue = 0, softMaxValue = 3, longName = "levelOfDetail", keyable = True)
		
		moduleVisibilityMultiply = "%s:moduleVisibilityMultiply" %self.characterNamespace
		pm.connectAttr("%s.outputX" %moduleVisibilityMultiply, "%s.visibility" %_moduleGrp, force = True)
	
	
	def PublishNameToModuleContainer(self, _attribute, _attributeNiceName, _publishToOuterContainer = True):
		
		if self.moduleContainer == None:
			return
		
		blueprintName = utils.StripLeadingNamespace(self.blueprintNamespace)[1].partition("__")[2]
		
		attributePrefix = "%s_%s_" %(blueprintName, self.moduleNamespace)
		publishedName = "%s%s" %(attributePrefix, _attributeNiceName)
		
		if _publishToOuterContainer:
			self.publishedNames.append(publishedName)
		
		
		pm.container(self.moduleContainer, edit = True, publishAndBind = [_attribute, publishedName])
	
	
	def PublishModuleContainerNamesToOuterContainers(self):
		
		if self.moduleContainer == None:
			return
		
		
		characterContainer = "%s:character_container" %self.characterNamespace
		blueprintContainer = "%s:module_container" %self.blueprintNamespace
		
		for publishedNames in self.publishedNames:
			outerPublishedNames = pm.container(blueprintContainer, query = True, publishName = True)
			
			if publishedNames in outerPublishedNames:
				continue
			
			pm.container(blueprintContainer, edit = True, publishAndBind = ["%s.%s" %(self.moduleContainer, publishedNames), publishedNames])
			pm.container(characterContainer, edit = True, publishAndBind = ["%s.%s" %(blueprintContainer, publishedNames), publishedNames])
	
	
	def UI(self, _parentLayout):
		print "No custom user interface provided"
	
	
	def UI_preferences(self, _parentLayout):
		print "No custom user interface provided"