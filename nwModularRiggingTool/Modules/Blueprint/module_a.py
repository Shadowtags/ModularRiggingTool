import os

CLASS_NAME = "ModuleA"

TITLE = "module A"
DESCRIPTION = "Test description for module A"
ICON = "%s/Icons/_hand.xpm" %os.environ["RIGGING_TOOL_ROOT"]

class ModuleA():
    
    def __init__(self):
        
        print "we're in the constructor"
    
    
    def Install(self):
        
        print "Install %s" %CLASS_NAME