import pymel.core as pm


scriptJobNum = None


class ModuleMaintenance_shelfTool:
	
	def __init__(self):
		global scriptJobNum
		
		import System.moduleMaintenance as moduleMaintenance
		reload(moduleMaintenance)
		
		modMaintenance = moduleMaintenance.ModuleMaintenance(self)
		
		if scriptJobNum == None:
			modMaintenance.SetModuleMaintenanceVisibility(True)
			
			modMaintenance.ObjectSelected()
		
		
		else:
			modMaintenance.SetModuleMaintenanceVisibility(False)
			
			if pm.window("modMaintenance_UI_window", exists = True):
				pm.deleteUI("modMaintenance_UI_window")
			
			if pm.scriptJob(exists = scriptJobNum):
				pm.scriptJob(kill = scriptJobNum)
			
			scriptJobNum = None
	
	
	
	
	def SetScriptJobNum(self, _num):
		global scriptJobNum
		scriptJobNum = _num
	
	
	def GetScriptJobNum(self):
		global scriptJobNum
		return scriptJobNum