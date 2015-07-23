import pymel.core as pm
import os
import System.utils as utils
reload(utils)

class InstallCharacter_UI:
	
	def __init__(self):
		
		self.UIElements = {}
		#self.directory = '%s/nwModularRiggingTool' %pm.internalVar(userScriptDir = True)
		characters = utils.FindAllMayaFiles("/Characters")
		
		
		if len(characters) == 0:
			pm.confirmDialog(title = "Character Install", message = "No published characters found. \nAborting character install.", button = ["Accept"], defaultButton = "Accept")
			return
		
		
		if pm.window("installCharacter_UI_window", exists = True):
			pm.deleteUI("installCharacter_UI_window")
		
		
		windowWidth = 320
		windowHeight = 190
		self.UIElements["window"] = pm.window("installCharacter_UI_window", width = windowWidth, height = windowHeight, title = "Install Character", sizeable = False)
		
		self.UIElements["topColumn"] = pm.columnLayout(adjustableColumn = True, columnOffset = ["both", 5], rowSpacing = 3, parent = self.UIElements["window"])
		
		self.UIElements["characterList"] = pm.textScrollList(numberOfRows = 9, allowMultiSelection = False, append = characters, selectIndexedItem = 1, parent = self.UIElements["topColumn"])
		
		pm.separator(style = 'in', parent = self.UIElements["topColumn"])
		
		self.UIElements["newCharacterButton"] = pm.button(label = "Create New Character", command = self.InstallCharacter, parent = self.UIElements["topColumn"])
		
		pm.separator(style = 'in', parent = self.UIElements["topColumn"])
		
		
		pm.showWindow(self.UIElements["window"])
	
	
	
	def InstallCharacter(self, *args):
		characterName = pm.textScrollList(self.UIElements["characterList"], query = True, selectItem = True)[0]
		
		#characterFileName = "%s/Characters/%s.ma" %(self.directory, characterName)
		characterFileName = "%s/Characters/%s.ma" %(os.environ["RIGGING_TOOL_ROOT"], characterName)
		
		baseNamespace = "Character__%s_" %characterName
		
		pm.namespace(setNamespace = ":")
		namespaces = pm.namespaceInfo(listOnlyNamespaces = True)
		
		highestSuffix = utils.FindHighestTrailingNumber(namespaces, baseNamespace)
		highestSuffix += 1
		
		characterNamespace = "%s%d" %(baseNamespace, highestSuffix)
		
		pm.importFile(characterFileName, namespace = characterNamespace)
		
		pm.deleteUI(self.UIElements["window"])