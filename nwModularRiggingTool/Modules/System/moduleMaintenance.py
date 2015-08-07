import pymel.core as pm
import System.utils as utils
reload(utils)

from functools import partial


class ModuleMaintenance:
	
	def __init__(self, _shelfTool_inst):
		
		self.shelfTool_instance = _shelfTool_inst
		self.UIElements = {}
		self.controlModuleCompatability = self.InitializeControlModuleCompatability()
	
	
	def InitializeControlModuleCompatability(self):
		animationControlModules = utils.FindAllModules("/Modules/Animation")
		
		moduleList = []
		for module in animationControlModules:
			mod = __import__("Animation.%s" %module, {}, {}, [module])
			reload(mod)
			
			moduleClass = getattr(mod, mod.CLASS_NAME)
			moduleInstance = moduleClass(None)
			
			compatabileBlueprintModules = moduleInstance.CompatibleBlueprintModules()
			
			moduleList.append( (mod, mod.CLASS_NAME, compatabileBlueprintModules))
		
		return moduleList
	
	
	def SetModuleMaintenanceVisibility(self, _visibility = True):
		characters = utils.FindInstalledCharacters()
		
		for c in characters:
			characterContainer = "%s:character_container" %c
			pm.lockNode(characterContainer, lock = False, lockUnpublished = False)
			
			characterGroup = "%s:character_grp" %c
			pm.setAttr("%s.moduleMaintenanceVisibility" %characterGroup, _visibility)
			
			pm.lockNode(characterContainer, lock = True, lockUnpublished = True)
	
	
	def ObjectSelected(self):
		objects = pm.ls(selection = True)
		
		pm.select(clear = True)
		
		
		if pm.window("modMaintenance_UI_window", exists = True):
			pm.deleteUI("modMaintenance_UI_window")
		
		
		characters = utils.FindInstalledCharacters()
		
		for character in characters:
			characterContainer = "%s:character_container" %character
			pm.lockNode(characterContainer, lock = False, lockUnpublished = False)
			
			blueprintInstances = utils.FindInstalledBlueprintInstances(character)
			
			for blueprintInstance in blueprintInstances:
				moduleContainer = "%s:%s:module_container" %(character, blueprintInstance)
				pm.lockNode(moduleContainer, lock = False, lockUnpublished = False)
				
				blueprintJointsGrp = "%s:%s:blueprint_joints_grp" %(character, blueprintInstance)
				
				# Change color of module joints depending on wether animation controls heve been installed or not
				if pm.getAttr("%s.controlModulesInstalled" %blueprintJointsGrp):
					# Blue
					pm.setAttr("%s.overrideColor" %blueprintJointsGrp, 6)
				else:
					# Grey
					pm.setAttr("%s.overrideColor" %blueprintJointsGrp, 2)
				
				pm.lockNode(moduleContainer, lock = True, lockUnpublished = True)
			
			pm.lockNode(characterContainer, lock = True, lockUnpublished = True)
		
		
		
		if len(objects) > 0:
			lastSelected = objects[len(objects)-1]
			
			lastSelected_stripNamespaces = utils.StripAllNamespaces(lastSelected)
			
			if lastSelected_stripNamespaces != None:
				lastSelected_withoutNamespaces = lastSelected_stripNamespaces[1]
				
				if lastSelected_withoutNamespaces.find("blueprint_") == 0:
					blueprintModule_fullNamespace = lastSelected_stripNamespaces[0]
					moduleContainer = "%s:module_container" %blueprintModule_fullNamespace
					
					pm.select(moduleContainer, replace = True)
					
					characterNamespace = utils.StripLeadingNamespace(lastSelected)[0]
					
					characterContainer = "%s:character_container" %characterNamespace
					
					containers = [characterContainer, moduleContainer]
					for container in containers:
						pm.lockNode(container, lock = False, lockUnpublished = False)
					
					
					# Change color of blueprint joints to red
					blueprintJointsGrp = "%s:blueprint_joints_grp" %blueprintModule_fullNamespace
					pm.setAttr("%s.overrideColor" %blueprintJointsGrp, 13)
					
					self.CreateUserInterface(blueprintModule_fullNamespace)
					
					for container in containers:
						pm.lockNode(container, lock = True, lockUnpublished = True)
		
		
		self.SetupSelectionScriptJob()
	
	
	def SetupSelectionScriptJob(self):
		scriptJobNum = pm.scriptJob(event = ["SelectionChanged", self.ObjectSelected], runOnce = True, killWithScene = True)
		self.shelfTool_instance.SetScriptJobNum(scriptJobNum)
	
	
	def DisableSelectionScriptJob(self):
		scriptJobNum = self.shelfTool_instance.GetScriptJobNum()
		
		self.shelfTool_instance.SetScriptJobNum(None)
		if pm.scriptJob(exists = scriptJobNum):
			pm.scriptJob(kill = scriptJobNum)


	def CreateUserInterface(self, _blueprintModule):
		self.currentBlueprintModule = _blueprintModule
		
		# Collect character namespace info
		characterNamespaceInfo = utils.StripLeadingNamespace(_blueprintModule)
		characterNamespace = characterNamespaceInfo[0]
		blueprintModuleNamespace = characterNamespaceInfo[1]
		
		characterName = characterNamespace.partition("__")[2]
		
		# Collect blueprint namespace info
		blueprintModuleInfo = blueprintModuleNamespace.partition("__")
		blueprintModuleName = blueprintModuleInfo[0]
		blueprintModuleUserSpecifiedName = blueprintModuleInfo[2]
		
		
		# Create UI
		windowWidth = 600
		windowHeight = 200
		self.UIElements["window"] = pm.window("modMaintenance_UI_window", width = windowWidth, height = windowHeight, title = 'Module Maintenance for %s:%s' %(characterName, blueprintModuleUserSpecifiedName), sizeable = False)
		
		self.UIElements["topRowLayout"] = pm.rowLayout(numberOfColumns = 2, columnWidth2 = (296, 296), columnAttach2 = ("both", "both"), columnOffset2 = (10, 10), rowAttach = ([1, "both", 5], [2, "both", 5]), parent = self.UIElements["window"])
		
		self.UIElements["controlModule_textScrollList"] = pm.textScrollList(selectCommand = self.UI_controlModuleSelected, parent = self.UIElements["topRowLayout"])
		
		# Add compatable control modules to text scroll list
		for controlModule in self.controlModuleCompatability:
			if blueprintModuleName in controlModule[2]:
				
				# Add control module if it hasn't already been installed
				if not self.IsModuleInstalled(controlModule[1]):
					pm.textScrollList(self.UIElements["controlModule_textScrollList"], edit = True, append = controlModule[1])
		
		
		self.UIElements["right_columnLayout"] = pm.columnLayout(adjustableColumn = True, rowSpacing = 3, parent = self.UIElements["topRowLayout"])
		self.UIElements["nameText"] = pm.text(label = 'No Animation Modules to Install', parent = self.UIElements["right_columnLayout"])
		self.UIElements["descriptionScrollField"] = pm.scrollField(wordWrap = True, height = 110, editable = False, text = '', parent = self.UIElements["right_columnLayout"])
		
		pm.separator(style = 'in', parent = self.UIElements["right_columnLayout"])
		self.UIElements["installButton"] = pm.button(enable = False, label = "Install", parent = self.UIElements["right_columnLayout"])
		
		
		if pm.textScrollList(self.UIElements["controlModule_textScrollList"], query = True, numberOfItems = True) != 0:
			pm.textScrollList(self.UIElements["controlModule_textScrollList"], edit = True, selectIndexedItem = 1)
			self.UI_controlModuleSelected()
		
		
		pm.showWindow(self.UIElements["window"])
	
	
	def IsModuleInstalled(self, _moduleName):
		pm.namespace(setNamespace = self.currentBlueprintModule)
		installedModules = pm.namespaceInfo(listOnlyNamespaces = True)
		pm.namespace(setNamespace = ":")
		
		if installedModules != None:
			for module in installedModules:
				installedModuleNameWithoutSuffix = utils.StripAllNamespaces(module)[1]
				installedModuleName = installedModuleNameWithoutSuffix.rpartition("_")[0]
				
				if installedModuleName == _moduleName:
					return True
		
		return False
	
	
	def UI_controlModuleSelected(self, *args):
		moduleNameInfo = pm.textScrollList(self.UIElements["controlModule_textScrollList"], query = True, selectItem = True)
		
		if len(moduleNameInfo) == 0:
			pm.text(self.UIElements["nameText"], edit = True, label = 'No Animation Modules to Install')
			pm.scrollField(self.UIElements["descriptionScrollField"], edit = True, text = '')
			pm.button(self.UIElements["installButton"], edit = True, enable = False)
			return
		
		else:
			moduleName = moduleNameInfo[0]
			
			mod = None
			for controlModule in self.controlModuleCompatability:
				if controlModule[1] == moduleName:
					mod = controlModule[0]
			
			if mod != None:
				moduleTitle = mod.TITLE
				moduleDescription = mod.DESCRIPTION
				
				pm.text(self.UIElements["nameText"], edit = True, label = moduleTitle)
				pm.scrollField(self.UIElements["descriptionScrollField"], edit = True, text = moduleDescription)
				
				pm.button(self.UIElements["installButton"], edit = True, enable = True, command = partial(self.InstallModule, mod, moduleName))
	
	
	def InstallModule(self, _mod, _moduleName, *args):
		self.DisableSelectionScriptJob()
		
		moduleNamespace = "%s:%s_1" %(self.currentBlueprintModule, _mod.CLASS_NAME)
		
		moduleClass = getattr(_mod, _mod.CLASS_NAME)
		moduleInstance = moduleClass(moduleNamespace)
		moduleInstance.Install()
		
		# Delete installed control module in scroll list and reselect the top one
		pm.textScrollList(self.UIElements["controlModule_textScrollList"], edit = True, removeItem = _moduleName)
		
		if pm.textScrollList(self.UIElements["controlModule_textScrollList"], query = True, numberOfItems = True) != 0:
			pm.textScrollList(self.UIElements["controlModule_textScrollList"], edit = True, selectIndexedItem = 1)
		
		self.UI_controlModuleSelected()
		
		utils.ForceSceneUpdate()
		
		pm.select("%s:module_container" %self.currentBlueprintModule, replace = True)
		
		
		self.SetupSelectionScriptJob()