import pymel.core as pm
import System.utils as utils
reload(utils)

from functools import partial


class ModuleMaintenance:
	
	def __init__(self, _shelfTool_inst):
		
		self.shelfTool_instance = _shelfTool_inst
		self.UIElements = {}
	
	
	
	def SetModuleMaintenanceVisibility(self, _visibility = True):
		characters = utils.FindInstalledCharacters()
		
		for c in characters:
			characterContainer = "%s:character_container" %c
			pm.lockNode(characterContainer, lock = False, lockUnpublished = False)
			
			characterGroup = "%s:character_grp" %c
			pm.setAttr("%s.moduleMaintenanceVisibility" %characterGroup, _visibility)
			
			pm.lockNode(characterContainer, lock = True, lockUnpublished = True)