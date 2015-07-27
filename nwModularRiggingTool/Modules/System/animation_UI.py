import pymel.core as pm
import os
import System.utils as utils
import System.controlObject as controlObject
from functools import partial

reload(utils)
reload(controlObject)



class Animation_UI:
	
	def __init__(self):
		self.directory = "%s/nwModularRiggingTool" %pm.internalVar(userScriptDir = True)
		
		self.previousBlueprintListEntry = None
		self.previousBlueprintModule = None
		self.previousAnimationModule = None
		
		#baseIconsDir = "%s/Icons/" %self.directory
		baseIconsDir = "%s/Icons/" %os.environ["RIGGING_TOOL_ROOT"]
		
		self.selectedCharacter = self.FindSelectedCharacter()
		
		if self.selectedCharacter == None:
			return
		
		self.characterName = self.selectedCharacter.partition("__")[2]
		
		self.windowName = "%s_window" %self.characterName
		
		# Create UI
		self.UIElements = {}
		
		if pm.window(self.windowName, exists = True):
			pm.deleteUI(self.windowName)
		
		self.windowWidth = 420
		self.windowHeight = 730
		
		self.frameColumnHeight = 125
		
		self.UIElements["window"] = pm.window(self.windowName, width = self.windowWidth, height = self.windowHeight, title = "Animation UI: %s" %self.characterName, sizeable = False)
		
		self.UIElements["topColumnLayout"] = pm.columnLayout(adjustableColumn = True, rowSpacing = 3, parent = self.UIElements["window"])
		
		buttonWidth = 32
		columnOffset = 5
		buttonColumnWidth = buttonWidth + (2 * columnOffset)
		textScrollWidth = (self.windowWidth - buttonColumnWidth - 8) / 2
		
		self.UIElements["listboxRowLayout"] = pm.rowLayout(numberOfColumns = 3, columnWidth3 = [textScrollWidth, textScrollWidth, buttonColumnWidth], columnAttach = ([1, "both", columnOffset], [2, "both", columnOffset], [3, "both", columnOffset]), parent = self.UIElements["topColumnLayout"])
		
		self.UIElements["blueprintModule_textScroll"] = pm.textScrollList(numberOfRows = 12, allowMultiSelection = False, selectCommand = self.RefreshAnimationModuleList, parent = self.UIElements["listboxRowLayout"])
		self.InitializeBlueprintModuleList()
		
		self.UIElements["animationModule_textScroll"] = pm.textScrollList(numberOfRows = 12, allowMultiSelection = False, selectCommand = self.SetupModuleSpecificControls, parent = self.UIElements["listboxRowLayout"])
		
		self.UIElements["buttonColumnLayout"] = pm.columnLayout(parent = self.UIElements["listboxRowLayout"])
		self.UIElements["pinButton"] = pm.symbolCheckBox(onImage = "%s_pinned.xpm" %baseIconsDir, offImage = "%s_unpinned.xpm" %baseIconsDir, width = buttonWidth, height = buttonWidth, onCommand = self.DeleteScriptJob, offCommand = self.SetupScriptjob, parent = self.UIElements["buttonColumnLayout"])
		
		if pm.objExists("%s:non_blueprint_grp" %self.selectedCharacter):
			value = pm.getAttr("%s:non_blueprint_grp.display" %self.selectedCharacter)
			self.UIElements["non_blueprintVisibility"] = pm.symbolCheckBox(image = "%s_shelf_character.xpm" %baseIconsDir, value = value, width = buttonWidth, height = buttonWidth, onCommand = self.ToggleNonBlueprintVisibility, offCommand = self.ToggleNonBlueprintVisibility, parent = self.UIElements["buttonColumnLayout"])
		
		value = pm.getAttr("%s:character_grp.animationControlVisibility" %self.selectedCharacter)
		self.UIElements["animControlVisibility"] = pm.symbolCheckBox(image = "%s_visibility.xpm" %baseIconsDir, value = value, width = buttonWidth, height = buttonWidth, onCommand = self.ToggleAnimControlVisibility, offCommand = self.ToggleAnimControlVisibility, parent = self.UIElements["buttonColumnLayout"])
		
		self.UIElements["deleteModuleButton"] = pm.symbolButton(image = "%s_shelf_delete.xpm" %baseIconsDir, width = buttonWidth, height = buttonWidth, enable = False, command = self.DeleteSelectedModule, parent = self.UIElements["buttonColumnLayout"])
		self.UIElements["duplicateModuleButton"] = pm.symbolButton(image = "%s_duplicate.xpm" %baseIconsDir, width = buttonWidth, height = buttonWidth, enable = False, parent = self.UIElements["buttonColumnLayout"])
		
		
		pm.separator(style = "in", parent = self.UIElements["topColumnLayout"])
		
		self.UIElements["activeModuleColumn"] = pm.columnLayout(adjustableColumn = True, parent = self.UIElements["topColumnLayout"])
		self.SetupActiveModuleControls()
		
		pm.separator(style = "in", parent = self.UIElements["topColumnLayout"])
		
		self.UIElements["matchingButton"] = pm.button(label = "Match Controls to Result", enable = False, parent = self.UIElements["topColumnLayout"])
		
		pm.separator(style = "in", parent = self.UIElements["topColumnLayout"])
		
		
		pm.rowColumnLayout("module_rowColumn", numberOfRows = 1, rowAttach = [1, "both", 0], rowHeight = [1, self.windowHeight - 395], parent = self.UIElements["topColumnLayout"])
		
		self.UIElements["moduleSpecificControlsScroll"] = pm.scrollLayout(width = self.windowWidth + 10, horizontalScrollBarThickness = 0, parent = "module_rowColumn")
		
		self.UIElements["moduleSpecificControlsColumn"] = pm.columnLayout(columnWidth = self.windowWidth, columnAttach = ["both", 5], parent = self.UIElements["moduleSpecificControlsScroll"])
		
		
		self.RefreshAnimationModuleList()
		
		self.SetupScriptjob()
		
		
		pm.showWindow(self.UIElements["window"])
		
		self.SelectionChanged()
	
	
	def InitializeBlueprintModuleList(self):
		pm.namespace(setNamespace = self.selectedCharacter)
		blueprintNamespaces = pm.namespaceInfo(listOnlyNamespaces = True)
		pm.namespace(setNamespace = ":")
		
		self.blueprintModules = {}
		
		if len(blueprintNamespaces) > 0:
			for namespace in blueprintNamespaces:
				blueprintModule = utils.StripLeadingNamespace(namespace)[1]
				userSpecifiedName = blueprintModule.partition("__")[2]
				
				pm.textScrollList(self.UIElements["blueprintModule_textScroll"], edit = True, append = userSpecifiedName)
				self.blueprintModules[userSpecifiedName] = namespace
		
		pm.textScrollList(self.UIElements["blueprintModule_textScroll"], edit = True, selectIndexedItem = 1)
		
		selectedBlueprintModule = pm.textScrollList(self.UIElements["blueprintModule_textScroll"], query = True, selectItem = True)
		self.selectedBlueprintModule = self.blueprintModules[selectedBlueprintModule[0]]
	
	
	def RefreshAnimationModuleList(self, _index = 1):
		pm.textScrollList(self.UIElements["animationModule_textScroll"], edit = True, removeAll = True)
		
		pm.symbolButton(self.UIElements["deleteModuleButton"], edit = True, enable = False)
		pm.symbolButton(self.UIElements["duplicateModuleButton"], edit = True, enable = False)
		
		selectedBlueprintModule = pm.textScrollList(self.UIElements["blueprintModule_textScroll"], query = True, selectItem = True)
		self.selectedBlueprintModule = self.blueprintModules[selectedBlueprintModule[0]]
		
		self.SetupActiveModuleControls()
		
		pm.namespace(setNamespace = self.selectedBlueprintModule)
		controlModuleNamespaces = pm.namespaceInfo(listOnlyNamespaces = True)
		pm.namespace(setNamespace = ":")
		
		if len(controlModuleNamespaces) != 0:
			for module in controlModuleNamespaces:
				moduleName = utils.StripAllNamespaces(module)[1]
				pm.textScrollList(self.UIElements["animationModule_textScroll"], edit = True, append = moduleName)
		
			pm.textScrollList(self.UIElements["animationModule_textScroll"], edit = True, selectIndexedItem = _index)
			
			pm.symbolButton(self.UIElements["deleteModuleButton"], edit = True, enable = True)
			pm.symbolButton(self.UIElements["duplicateModuleButton"], edit = True, enable = True)
		
		
		self.SetupModuleSpecificControls()
		
		self.previousBlueprintListEntry = selectedBlueprintModule
	
	
	
	def FindSelectedCharacter(self):
		
		selection = pm.ls(selection = True, transforms = True)
		character = None
		
		if len(selection) > 0:
			selected = selection[0]
			selectedNamespaceInfo = utils.StripLeadingNamespace(selected)
			
			if selectedNamespaceInfo != None:
				selectedNamespace = selectedNamespaceInfo[0]
				
				if selectedNamespace.find("Character__") == 0:
					character = selectedNamespace
		
		return character
	
	
	def ToggleNonBlueprintVisibility(self, *args):
		visibility = not pm.getAttr("%s:non_blueprint_grp.display" %self.selectedCharacter)
		pm.setAttr("%s:non_blueprint_grp.display" %self.selectedCharacter, visibility)
	
	
	def ToggleAnimControlVisibility(self, *args):
		visibility = not pm.getAttr("%s:character_grp.animationControlVisibility" %self.selectedCharacter)
		pm.setAttr("%s:character_grp.animationControlVisibility" %self.selectedCharacter, visibility)
	
	
	def SetupScriptjob(self, *args):
		self.scriptJobNum = pm.scriptJob(parent = self.UIElements["window"], event = ["SelectionChanged", self.SelectionChanged])
	
	
	def DeleteScriptJob(self, *args):
		pm.scriptJob(kill = self.scriptJobNum)
	
	
	def SelectionChanged(self):
		selection = pm.ls(selection = True, transforms = True)
		if len(selection) > 0:
			selectedNode = selection[0]
			
			characterNamespaceInfo = utils.StripLeadingNamespace(selectedNode)
			if characterNamespaceInfo != None and characterNamespaceInfo[0] == self.selectedCharacter:
				blueprintNamespaceInfo = utils.StripLeadingNamespace(characterNamespaceInfo[1])
				
				if blueprintNamespaceInfo != None:
					listEntry = blueprintNamespaceInfo[0].partition("__")[2]
					allEntries = pm.textScrollList(self.UIElements["blueprintModule_textScroll"], query = True, allItems = True)
					
					if listEntry in allEntries:
						pm.textScrollList(self.UIElements["blueprintModule_textScroll"], edit = True, selectItem = listEntry)
						
						if listEntry != self.previousBlueprintListEntry:
							self.RefreshAnimationModuleList()
						
						moduleNamespaceInfo = utils.StripLeadingNamespace(blueprintNamespaceInfo[1])
						
						if moduleNamespaceInfo != None:
							allEntries = pm.textScrollList(self.UIElements["animationModule_textScroll"], query = True, allItems = True)
							
							if moduleNamespaceInfo[0] in allEntries:
								pm.textScrollList(self.UIElements["animationModule_textScroll"], edit = True, selectItem = moduleNamespaceInfo[0])
		
		
		self.SetupModuleSpecificControls()
	
	
	def SetupActiveModuleControls(self):
		existingControls = pm.columnLayout(self.UIElements["activeModuleColumn"], query = True, childArray = True)
		if existingControls != None:
			pm.deleteUI(existingControls)
		
		largeButtonSize = 100
		enumOptionWidth = self.windowWidth - (2 * largeButtonSize)
		
		self.settingsLocator = "%s:SETTINGS" %self.selectedBlueprintModule
		activeModuleAttribute = "%s.activeModule" %self.settingsLocator
		
		currentEntries = pm.attributeQuery("activeModule", node = self.settingsLocator, listEnum = True)
		enable = True
		
		if currentEntries[0] == "None":
			enable = False
		
		self.UIElements["activeModue_rowLayout"] = pm.rowLayout(numberOfColumns = 3, adjustableColumn = 1, columnAttach3 = ("both", "both", "both"), columnWidth3 = (enumOptionWidth, largeButtonSize, largeButtonSize), parent = self.UIElements["activeModuleColumn"])
		
		attributes = pm.listAttr(self.settingsLocator, keyable = False)
		weightAttributes = []
		for attr in attributes:
			if attr.find("_weight") != -1:
				weightAttributes.append(attr)
		
		self.UIElements["activeModule"] = pm.attrEnumOptionMenu(label = "Active Module", width = enumOptionWidth, attribute = activeModuleAttribute, changeCommand = partial(self.ActiveModule_enumCallback, weightAttributes), enable = enable, parent = self.UIElements["activeModue_rowLayout"])
		self.UIElements["keyModuleWeights"] = pm.button(label = "Key All", command = partial(self.KeyModuleWeights, weightAttributes), enable = enable, parent = self.UIElements["activeModue_rowLayout"])
		self.UIElements["graphModuleWeights"] = pm.button(label = "Graph Weights", command = self.GraphModuleWeights, enable = enable, parent = self.UIElements["activeModue_rowLayout"])
		
		
		self.UIElements["moduleWeights_frameLayout"] = pm.frameLayout(collapsable = True, collapse = False, label = "Module Weights", height = 100, collapseCommand = self.ModuleWeights_UICollapse, expandCommand = self.ModuleWeights_UIExpand, parent = self.UIElements["activeModuleColumn"])
		pm.scrollLayout("frame_scroll", horizontalScrollBarThickness = 0, parent = self.UIElements["moduleWeights_frameLayout"])
		pm.columnLayout("frameScroll_column", adjustableColumn = True, parent = "frame_scroll")
		
		pm.attrFieldSliderGrp(attribute = "%s.creationPoseWeight" %self.settingsLocator, enable = False, parent = "frameScroll_column")
		pm.separator(style = "in", parent = "frameScroll_column")
		
		for attr in weightAttributes:
			self.UIElements[attr] = pm.floatSliderGrp(label = attr, field = True, precision = 4, minValue = 0.0, maxValue = 1.0, value = pm.getAttr("%s.%s" %(self.settingsLocator, attr)), changeCommand = partial(self.ModuleWeights_sliderCallback, attr, weightAttributes), parent = "frameScroll_column")
		
		parentUIElement = self.UIElements["moduleWeights_frameLayout"]
		self.Create_moduleWeightScriptJob(parentUIElement, weightAttributes)
		
		self.ModuleWeights_updateMatchingButton()
	
	
	def ModuleWeights_UICollapse(self, *args):
		pm.columnLayout(self.UIElements["activeModuleColumn"], edit = True, height = 47)
	
	
	def ModuleWeights_UIExpand(self, *args):
		pm.columnLayout(self.UIElements["activeModuleColumn"], edit = True, height = self.frameColumnHeight)
	
	
	def ActiveModule_enumCallback(self, _weightAttributes, *args):
		enumValue = args[0]
		
		for attr in _weightAttributes:
			value = 0
			
			if "%s_weight" %enumValue == attr:
				value = 1
			
			pm.setAttr("%s.%s" %(self.settingsLocator, attr), value)
		
		pm.setAttr("%s.creationPoseWeight" %self.settingsLocator, 0)
		self.ModuleWeights_timeUpdateScriptJobCallback(_weightAttributes)
		self.ModuleWeights_updateMatchingButton()
	
	
	def ModuleWeights_sliderCallback(self, _controlledAttribute, _weightAttributes, *args):
		value = float(args[0])
		currentTotalWeight = 0.0
		
		for attr in _weightAttributes:
			if attr != _controlledAttribute:
				currentTotalWeight += pm.getAttr("%s.%s" %(self.settingsLocator, attr))
		
		if currentTotalWeight + value > 1.0:
			value = 1.0 - currentTotalWeight
		
		pm.setAttr("%s.%s" %(self.settingsLocator, _controlledAttribute), value)
		pm.floatSliderGrp(self.UIElements[_controlledAttribute], edit = True, value = value)
		
		newTotalWeight = currentTotalWeight + value
		
		creationPoseWeight = 1.0 - newTotalWeight
		pm.setAttr("%s.creationPoseWeight" %self.settingsLocator, creationPoseWeight)
		
		self.ModuleWeights_updateMatchingButton()
	
	
	def Create_moduleWeightScriptJob(self, _parentUIElement, _weightAttributes):
		pm.scriptJob(event = ["timeChanged", partial(self.ModuleWeights_timeUpdateScriptJobCallback, _weightAttributes)], parent = _parentUIElement)
	
	
	def ModuleWeights_timeUpdateScriptJobCallback(self, _weightAttributes):
		for attr in _weightAttributes:
			value = pm.getAttr("%s.%s" %(self.settingsLocator, attr))
			pm.floatSliderGrp(self.UIElements[attr], edit = True, value = value)
		
		self.ModuleWeights_updateMatchingButton()
	
	
	def ModuleWeights_updateMatchingButton(self):
		currentlySelectedModuleInfo = pm.textScrollList(self.UIElements["animationModule_textScroll"], query = True, selectItem = True)
		
		if len(currentlySelectedModuleInfo) != 0:
			currentlySelectedModuleNamespace = currentlySelectedModuleInfo[0]
			
			moduleWeightValue = pm.getAttr("%s.%s_weight" %(self.settingsLocator, currentlySelectedModuleNamespace))
			
			matchButtonEnable = moduleWeightValue > 0.0001
			pm.button(self.UIElements["matchingButton"], edit = True, enable = matchButtonEnable)
	
	
	def KeyModuleWeights(self, _weightAttributes, *args):
		for attr in _weightAttributes:
			pm.setKeyframe(self.settingsLocator, attribute = attr, inTangentType = "linear", outTangentType = "linear")
		
		pm.setKeyframe(self.settingsLocator, attribute = "creationPoseWeight", inTangentType = "linear", outTangentType = "linear")
	
	
	def GraphModuleWeights(self, *args):
		import maya.mel as mel
		
		pm.select(self.settingsLocator, replace = True)
		
		mel.eval('tearOffPanel "Graph Editor" graphEditor true')
	
	
	def SetupModuleSpecificControls(self):
		currentlySelectedModuleInfo = pm.textScrollList(self.UIElements["animationModule_textScroll"], query = True, selectItem = True)
		currentlySelectedModuleNamespace = None
		
		if len(currentlySelectedModuleInfo) != 0:
			currentlySelectedModuleNamespace = currentlySelectedModuleInfo[0]
			
			if currentlySelectedModuleNamespace == self.previousAnimationModule and self.selectedBlueprintModule == self.previousBlueprintModule:
				return
		
		existingControls = pm.columnLayout(self.UIElements["moduleSpecificControlsColumn"], query = True, childArray = True)
		if existingControls != None:
			pm.deleteUI(existingControls)
		
		pm.button(self.UIElements["matchingButton"], edit = True, enable = False)
		
		pm.setParent(self.UIElements["moduleSpecificControlsColumn"])
		
		moduleNameInfo = utils.FindAllModuleNames("/Modules/Animation")
		modules = moduleNameInfo[0]
		moduleNames = moduleNameInfo[1]
		
		
		if len(currentlySelectedModuleInfo) != 0:
			currentlySelectedModule = currentlySelectedModuleNamespace.rpartition("_")[0]
			
			if currentlySelectedModule in moduleNames:
				moduleWeightValue = pm.getAttr("%s:SETTINGS.%s_weight" %(self.selectedBlueprintModule, currentlySelectedModuleNamespace))
				matchButtonEnable = moduleWeightValue > 0.0001
				
				moduleIndex = moduleNames.index(currentlySelectedModule)
				module = modules[moduleIndex]
				
				pm.attrControlGrp(attribute = "%s:%s:module_grp.levelOfDetail" %(self.selectedBlueprintModule, currentlySelectedModuleNamespace), label = "Module LOD")
				
				mod = __import__("Animation.%s" %module, (), (), [module])
				reload(mod)
				
				moduleClass = getattr(mod, mod.CLASS_NAME)
				
				moduleInst = moduleClass("%s:%s" %(self.selectedBlueprintModule, currentlySelectedModuleNamespace))
				
				moduleInst.UI(self.UIElements["moduleSpecificControlsColumn"])
				
				self.UIElements["moduleSpecificControls_preferenceFrame"] = pm.frameLayout(borderVisible = False, label = "preferences", collapsable = True, parent = self.UIElements["moduleSpecificControlsColumn"])
				self.UIElements["moduleSpecificControls_preferenceColumn"] = pm.columnLayout(columnAttach = ["both", 5], adjustableColumn = True, parent = self.UIElements["moduleSpecificControls_preferenceFrame"])
				
				pm.attrControlGrp(attribute = "%s:%s:module_grp.iconScale" %(self.selectedBlueprintModule, currentlySelectedModuleNamespace), label = "Icon Scale")
				
				value = pm.getAttr("%s:%s:module_grp.overrideColor" %(self.selectedBlueprintModule, currentlySelectedModuleNamespace)) + 1
				self.UIElements["iconColor"] = pm.colorIndexSliderGrp(label = "Icon Color", maxValue = 32, value = value, changeCommand = partial(self.IconColor_callback, currentlySelectedModuleNamespace), parent = self.UIElements["moduleSpecificControls_preferenceColumn"])
				
				moduleInst.UI_preferences(self.UIElements["moduleSpecificControls_preferenceColumn"])
				
				pm.button(self.UIElements["matchingButton"], edit = True, enable = matchButtonEnable)
			
			self.previousBlueprintModule = self.selectedBlueprintModule
			self.previousAnimationModule = currentlySelectedModuleNamespace
	
	
	def IconColor_callback(self, _moduleNamespace, *args):
		value = pm.colorIndexSliderGrp(self.UIElements["iconColor"], query = True, value = True) - 1
		pm.setAttr("%s:%s:module_grp.overrideColor" %(self.selectedBlueprintModule, _moduleNamespace), value)
	
	
	def DeleteSelectedModule(self, *args):
		selectedModule = pm.textScrollList(self.UIElements["animationModule_textScroll"], query = True, selectItem = True)[0]
		
		selectedModuleNamespace = "%s:%s" %(self.selectedBlueprintModule, selectedModule)
		
		moduleNameInfo = utils.FindAllModuleNames("/Modules/Animation")
		modules = moduleNameInfo[0]
		moduleNames = moduleNameInfo[1]
		
		selectedModuleName = selectedModule.rpartition("_")[0]
		
		if selectedModuleName in moduleNames:
			moduleIndex = moduleNames.index(selectedModuleName)
			module = modules[moduleIndex]
			
			mod = __import__("Animation.%s" %module, (), (), [module])
			reload(mod)
			
			moduleClass = getattr(mod, mod.CLASS_NAME)
			
			moduleInst = moduleClass(selectedModuleNamespace)
			
			moduleInst.Uninstall()
			
			self.RefreshAnimationModuleList()