CLASS_NAME = "FK"
TITLE = "Forward Kinematic"
DESCRIPTION = "This module provides FK rotational controls for every joint in the blueprint it is installed on."



class FK():
	
	def __init__(self, _moduleNamespace):
		print _moduleNamespace
	
	def CompatibleBlueprintModules(self):
		return ("Finger", "HingeJoint", "LegFoot", "SingleJointSegment", "SingleOrientableJoint", "Spline", "Thumb")
	
	
	def Install(self):
		print "%s INSTALLED" %CLASS_NAME