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
			
			scriptJobNum = 10
		
		
		else:
			modMaintenance.SetModuleMaintenanceVisibility(False)
			
			if pm.scriptJob(exists = scriptJobNum):
				pm.scriptJob(kill = scriptJobNum)
			
			scriptJobNum = None
	
	
	
	
	def SetScriptJobNum(self, _num):
		global scriptJobNum
		scriptJobNum = _num
	
	
	def GetScriptJobNum(self):
		global scriptJobNum
		return scriptJobNum