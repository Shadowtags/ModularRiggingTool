import pymel.core as pm
import System.utils as utils
reload(utils)

import os
from functools import partial

class ControlObject:
	
	def __init__(self, _controlObject = None):
		
		#self.directory = '%s/nwModularRiggingTool' %pm.internalVar(userScriptDir = True)
		
		if _controlObject != None:
			self.controlObject = _controlObject
			
			self.translation = []
			self.translation.append(not pm.getAttr("%s.translateX" %self.controlObject, lock = True))
			self.translation.append(not pm.getAttr("%s.translateY" %self.controlObject, lock = True))
			self.translation.append(not pm.getAttr("%s.translateZ" %self.controlObject, lock = True))
			
			self.rotation = []
			self.rotation.append(not pm.getAttr("%s.rotateX" %self.controlObject, lock = True))
			self.rotation.append(not pm.getAttr("%s.rotateY" %self.controlObject, lock = True))
			self.rotation.append(not pm.getAttr("%s.rotateZ" %self.controlObject, lock = True))
			
			self.globalScale = not pm.getAttr("%s.scaleY" %self.controlObject, lock = True)
	
	
	def Create(self, _name, _controlFile, _animationModuleInstance, _lod = 1, _translation = True, _rotation = True, _globalScale = True, _spaceSwitching = False):
		
		if _translation == True or _translation == False:
			translation = [_translation, _translation, _translation]
		
		if _rotation == True or _rotation == False:
			rotation = [_rotation, _rotation, _rotation]
		
		self.translation = translation
		self.rotation = rotation
		self.globalScale = _globalScale
		
		animationModuleName = _animationModuleInstance.moduleNamespace
		blueprintModuleNameSpace = _animationModuleInstance.blueprintNamespace
		blueprintModuleUserSpecifiedName = utils.StripAllNamespaces(blueprintModuleNameSpace)[1].partition("__")[2]
		
		animationModuleNamespace = "%s:%s" %(blueprintModuleNameSpace, animationModuleName)
		
		# import control object
		#controlObjectFile = "%s/ControlObjects/Animation/%s" %(self.directory, _controlFile)
		controlObjectFile = "%s/ControlObjects/Animation/%s" %(os.environ["RIGGING_TOOL_ROOT"], _controlFile)
		pm.importFile(controlObjectFile)
		
		self.controlObject = pm.rename("control", "%s:%s" %(animationModuleNamespace, _name))
		self.rootParent = self.controlObject
		
		
		self.SetupIconScale(animationModuleNamespace)
		
		
		pm.setAttr("%s.overrideEnabled" %self.controlObject, 1)
		pm.setAttr("%s.overrideShading" %self.controlObject, 0)
		pm.connectAttr("%s:module_grp.overrideColor" %animationModuleNamespace, "%s.overrideColor" %self.controlObject)
		
		
		pm.container("%s:module_container" %animationModuleNamespace, edit = True, addNode = self.controlObject, includeHierarchyBelow = True, includeNetwork = True)
		
		if _globalScale:
			pm.connectAttr("%s.scaleY" %self.controlObject, "%s.scaleX" %self.controlObject)
			pm.connectAttr("%s.scaleY" %self.controlObject, "%s.scaleZ" %self.controlObject)
			pm.aliasAttr("globalScale", "%s.scaleY" %self.controlObject)
		
		
		attributes = []
		if self.translation == [True, True, True]:
			attributes.append([True, ".translate", "T"])
		else:
			attributes.extend([[translation[0], ".translateX", "TX"], [translation[1], ".translateY", "TY"], [translation[2], ".translateZ", "TZ"]])
		
		
		if self.rotation == [True, True, True]:
			attributes.append([True, ".rotate", "R"])
		else:
			attributes.extend([[rotation[0], ".rotateX", "RX"], [rotation[1], ".rotateY", "RY"], [rotation[2], ".rotateZ", "RZ"]])
		
		attributes.append([_globalScale, ".globalScale", "scale"])
		
		for attrInfo in attributes:
			if attrInfo[0]:
				attributeNiceName = "%s_%s" %(_name, attrInfo[2])
				_animationModuleInstance.PublishNameToModuleContainer("%s%s" %(self.controlObject, attrInfo[1]), attributeNiceName, True)
		
		
		pm.select(self.controlObject, replace = True)
		pm.addAttr(attributeType = "bool", defaultValue = 1, keyable = True, longName = "display")
		_animationModuleInstance.PublishNameToModuleContainer("%s.display" %self.controlObject, "display", False)
		
		moduleGrp = "%s:module_grp" %animationModuleNamespace
		
		visibilityExpression = '%s.visibility = %s.display * (%s.levelOfDetail >= %d);' %(self.controlObject, self.controlObject, moduleGrp, _lod)
		expression = pm.expression(name = "%s_visibility_expression" %self.controlObject, string = visibilityExpression)
		utils.AddNodeToContainer("%s:module_container" %animationModuleNamespace, expression)
		
		
		return (self.controlObject, self.rootParent)
	
	
	def SetupIconScale(self, _animationModuleNamespace):
		
		clusterNodes = pm.cluster(self.controlObject, name = "%s_icon_scale_cluster" %self.controlObject, relative = True)
		pm.container("%s:module_container" %_animationModuleNamespace, edit = True, addNode = clusterNodes, includeHierarchyBelow = True, includeShapes = True)
		
		clusterHandle = clusterNodes[1]
		
		pm.setAttr("%s.scalePivotX" %clusterHandle, 0)
		pm.setAttr("%s.scalePivotY" %clusterHandle, 0)
		pm.setAttr("%s.scalePivotZ" %clusterHandle, 0)
		
		pm.connectAttr("%s:module_grp.iconScale" %_animationModuleNamespace, "%s.scaleX" %clusterHandle)
		pm.connectAttr("%s:module_grp.iconScale" %_animationModuleNamespace, "%s.scaleY" %clusterHandle)
		pm.connectAttr("%s:module_grp.iconScale" %_animationModuleNamespace, "%s.scaleZ" %clusterHandle)
		
		pm.parent(clusterHandle, self.controlObject, absolute = True)
		pm.setAttr("%s.visibility" %clusterHandle, 0)
	
	
	def UI(self, _parentLayout):
		
		pm.setParent(_parentLayout)
		
		pm.separator(style = "in", parent = _parentLayout)
		
		niceName = utils.StripAllNamespaces(self.controlObject)[1]
		pm.text(label = niceName)
		
		pm.attrControlGrp(attribute = "%s.display" %self.controlObject, label = "Visibility")
		
		if self.translation == [True, True, True]:
			pm.attrControlGrp(attribute = "%s.translate" %self.controlObject, label = "Translate")
		else:
			if self.translation[0] == True:
				pm.attrControlGrp(attribute = "%s.translateX" %self.controlObject, label = "Translate X")
			
			if self.translation[1] == True:
				pm.attrControlGrp(attribute = "%s.translateY" %self.controlObject, label = "Translate Y")
			
			if self.translation[2] == True:
				pm.attrControlGrp(attribute = "%s.translateZ" %self.controlObject, label = "Translate Z")
		
		
		if self.rotation == [True, True, True]:
			pm.attrControlGrp(attribute = "%s.rotate" %self.controlObject, label = "Rotate")
		else:
			if self.rotation[0] == True:
				pm.attrControlGrp(attribute = "%s.rotateX" %self.controlObject, label = "Rotate X")
	
			if self.rotation[1] == True:
				pm.attrControlGrp(attribute = "%s.rotateY" %self.controlObject, label = "Rotate Y")
	
			if self.rotation[2] == True:
				pm.attrControlGrp(attribute = "%s.rotateZ" %self.controlObject, label = "Rotate Z")
		
		
		if self.globalScale == True:
			pm.attrControlGrp(attribute = "%s.globalScale" %self.controlObject, label = "Scale")