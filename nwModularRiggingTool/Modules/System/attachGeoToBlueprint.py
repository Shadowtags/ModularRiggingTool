import pymel.core as pm
from functools import partial
import System.utils as utils
reload(utils)

class AttachGeoToBlueprint_ShelfTool:
	
	def AttachWithParenting(self):
		self.parenting = True
		self.skinning = False
		
		self.ProcessInitialSelection()
	
	
	def AttachWithSkinning(self):
		self.skinning = True
		self.parenting = False
		self.ProcessInitialSelection()
	
	
	def ProcessInitialSelection(self):
		
		selection = pm.ls(selection = True)
		
		self.blueprintJoints = []
		self.geometry = []
		
		self.blueprintJoints = self.FindBlueprintJoints(selection)
		self.geometry = self.FindGeometry(selection)
		
		
		if self.blueprintJoints == None:
			pm.headsUpMessage("Please select the blueprint joint(s) you wish to attach geometry to.")
			pm.scriptJob(event = ["SelectionChanged", self.SelectBlueprintJoint_callBack], runOnce = True)
		
		elif self.geometry == None:
			pm.headsUpMessage("Please select the geometry you wish to attach to the specified blueprint joint.")
			pm.scriptJob(event = ["SelectionChanged", self.SelectGeometry_callBack], runOnce = True)
		
		else:
			self.AttachGeometryToBlueprint_attachment()
		
	
	
	def SelectBlueprintJoint_callBack(self):
		
		selection = pm.ls(selection = True)
		self.blueprintJoints = self.FindBlueprintJoints(selection)
		
		
		if self.blueprintJoints == None:
			pm.confirmDialog(title = "Attach Geometry to Blueprint", message = "Blueprint joint selection invalid. \nTerminating tool.", button = ["Accept"], defaultButton = "Accept")
		
		elif self.geometry == None:
			pm.headsUpMessage("Please select the geometry you wish to attach to the specified blueprint joint(s).")
			pm.scriptJob(event = ["SelectionChanged", self.SelectGeometry_callBack], runOnce = True)
		
		else:
			self.AttachGeometryToBlueprint_attachment()
	
	
	def SelectGeometry_callBack(self):
		
		selection = pm.ls(selection = True)
		self.geometry = self.FindGeometry(selection)
		
		if self.geometry == None:
			pm.confirmDialog(title = "Attach Geometry to Blueprint", message = "Geometry selection invalid. \nTerminating tool.", button = ["Accept"], defaultButton = "Accept")
		else:
			self.AttachGeometryToBlueprint_attachment()
	
	
	
	def AttachGeometryToBlueprint_attachment(self):

		if self.parenting:
			self.AttachGeometryToBlueprint_parenting(self.blueprintJoints[0], self.geometry)
	
		else:
			self.AttachGeometryToBlueprint_skinning(self.blueprintJoints, self.geometry)

	
	
	def FindBlueprintJoints(self, _selection):
		
		selectedBlueprintJoints = []
		
		for obj in _selection:
			
			if pm.objectType(obj, isType = "joint"):
				jointNameInfo = utils.StripAllNamespaces(obj)
				
				if jointNameInfo != None:
					jointName = jointNameInfo[1]
					
					if jointName.find("blueprint_") == 0:
						selectedBlueprintJoints.append(obj)
		
		if len(selectedBlueprintJoints) > 0:
			return selectedBlueprintJoints
		
		else:
			return None
	
	
	def FindGeometry(self, _selection):
		_selection = pm.ls(_selection, transforms = True)
		
		nonJointSelection = []
		
		for node in _selection:
			if not pm.objectType(node, isType = "joint"):
				nonJointSelection.append(node)
		
		
		if len(nonJointSelection) > 0:
			return nonJointSelection
		
		else:
			return None
	
	
	
	def AttachGeometryToBlueprint_parenting(self, _blueprintJoint, _geometry):
		
		jointName = utils.StripAllNamespaces(_blueprintJoint)[1]
		parentGroup = pm.group(empty = True, name = "%s_geoAttach_parentGrp#" %jointName)
		
		if len(_geometry) == 1:
			geoParent = pm.listRelatives(_geometry, parent = True)
			
			if len(geoParent) != 0:
				pm.parent(parentGroup, geoParent)
		
		pm.parentConstraint(_blueprintJoint, parentGroup, maintainOffset = False, name = "%s_parentConstraint" %jointName)
		pm.scaleConstraint(_blueprintJoint, parentGroup, maintainOffset = False, name = "%s_scaleConstraint" %jointName)
		
		geoParent = parentGroup
		
		children = pm.listRelatives(_blueprintJoint, children = True)
		children = pm.ls(children, type = "joint")
		
		if len(children) != 0:
			
			childJoint = children[0]
			
			scaleGroup = pm.group(empty = True, name = "%s_geoAttach_scaleGrp" %childJoint)
			pm.parent(scaleGroup, parentGroup, relative = True)
			
			geoParent = scaleGroup
			
			originalTxValue = pm.getAttr("%s.translateX" %childJoint)
			scaleFactor = pm.shadingNode("multiplyDivide", asUtility = True, name = "%s_scaleFactor" %scaleGroup)
			
			pm.setAttr("%s.operation" %scaleFactor)
			pm.connectAttr("%s.translateX" %childJoint, "%s.input1X" %scaleFactor)
			pm.setAttr("%s.input2X" %scaleFactor, originalTxValue)
			
			pm.connectAttr("%s.outputX" %scaleFactor, "%s.scaleX" %scaleGroup)
		
		for geo in _geometry:
			pm.parent(geo, geoParent, absolute = True)
	
	
	def AttachGeometryToBlueprint_skinning(self, _blueprintJoints, _geometry):
		
		blueprintModules = set([])
		
		# Get namespaces of joint chains
		for joint in _blueprintJoints:
			blueprintNamespace = utils.StripLeadingNamespace(joint)[0]
			blueprintModules.add(blueprintNamespace)
		
		
		# Unlock containers
		for module in blueprintModules:
			pm.lockNode("%s:module_container" %module, lock = False, lockUnpublished = False)
		
		# Attach all geometry to joint chain
		for geo in _geometry:
			pm.skinCluster(_blueprintJoints, geo, toSelectedBones = True, name = "%s_skinCluster" %geo)
		
		# Lock containers
		for module in blueprintModules:
			pm.lockNode("%s:module_container" %module, lock = True, lockUnpublished = True)