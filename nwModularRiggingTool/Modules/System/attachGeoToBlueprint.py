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
		print self.skinning
		print self.parenting