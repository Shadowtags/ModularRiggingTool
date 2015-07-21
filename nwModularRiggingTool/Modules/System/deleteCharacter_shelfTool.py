import pymel.core as pm
import System.utils as utils
reload(utils)

class DeleteCharacter_ShelfTool:
	
	def __init__(self):
		
		character = self.FindSelectedCharacter()
		
		if character == None:
			return
		
		niceName = character.partition("__")[2]
		
		result = pm.confirmDialog(title = "Delete Character", message = 'Are you sure you want to delete the character "%s"? \nCharacter deletion cannot be undone.' %niceName, button = ["Yes", "Cancel"], defaultButton = "Yes", cancelButton = "Cancel", dismissString = "Cancel")
		if result == "Cancel":
			return
		
		characterContainer = "%s:character_container" %character
		
		# Unlock and delete selected character
		pm.lockNode(characterContainer, lock = False, lockUnpublished = False)
		pm.delete(characterContainer)
		
		# Collect list of blueprints used by this character
		pm.namespace(setNamespace = character)
		blueprintNamespaces = pm.namespaceInfo(listOnlyNamespaces = True)
		
		# Loop through blueprint namespaces
		for blueprintNamespace in blueprintNamespaces:
			pm.namespace(setNamespace = ":")
			pm.namespace(setNamespace = blueprintNamespace)
			
			# Collect module namespaces within each blueprint
			moduleNamespaces = pm.namespaceInfo(listOnlyNamespaces = True)
			pm.namespace(setNamespace = ":")
			
			# Remove the module namespaces
			if moduleNamespaces != None:
				for moduleNamespace in moduleNamespaces:
					pm.namespace(removeNamespace = moduleNamespace)
			
			# Remove the blueprint namespaces
			pm.namespace(removeNamespace = blueprintNamespace)
		
		# Remove the character namespace
		pm.namespace(removeNamespace = character)
	
	
	
	
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