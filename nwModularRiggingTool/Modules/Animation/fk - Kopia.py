CLASS_NAME = "temp"
TITLE = "temp"
DESCRIPTION = "temp"



class temp():
	
	def __init__(self, _moduleNamespace):
		print _moduleNamespace
	
	def CompatibleBlueprintModules(self):
		return ("Finger", "HingeJoint", "LegFoot", "SingleJointSegment", "SingleOrientableJoint", "Spline", "Thumb")
	
	
	def Install(self):
		print "%s INSTALLED" %CLASS_NAME