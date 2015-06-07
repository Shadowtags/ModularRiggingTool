import pymel.core as pm
import os

import System.blueprint as blueprint
reload(blueprint)


CLASS_NAME = "SingleJointSegment"
TITLE = "Single Joint Segment"
DESCRIPTION = "Creates 2 joints, with control for 1st joint's orientation and rotation order. Ideal use: clavicle bones/shoulder"
ICON = "%s/Icons/_singleJointSeg.xpm" %os.environ["RIGGING_TOOL_ROOT"]

class SingleJointSegment(blueprint.Blueprint):

    def __init__(self, _userSpecifiedName):
        
        jointInfo = [ ["root_joint", [0.0, 0.0, 0.0]], ["end_joint", [4.0, 0.0, 0.0]] ]
        
        blueprint.Blueprint.__init__(self, CLASS_NAME, _userSpecifiedName, jointInfo)
    
    
    
    #def Install_custom(self, _joints):
        #self.CreateOrientationControl(_joints[0], _joints[1])
    
    
    def Lock_phase1(self):
        print "LOCK PHASE 1"