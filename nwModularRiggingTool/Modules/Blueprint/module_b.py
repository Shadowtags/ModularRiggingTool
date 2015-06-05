import os

CLASS_NAME = "ModuleB"

TITLE = "module B"
DESCRIPTION = "Test description for module B"
ICON = "%s/Icons/_hinge.xpm" %os.environ["RIGGING_TOOL_ROOT"]

class ModuleB():
    
    def __init__(self):
        
        print "we're in the constructor"
    
    
    def Install(self):
        
        print "Install %s" %CLASS_NAME