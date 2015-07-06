import pymel.core as pm
import os

import System.blueprint as blueprint
import System.utils as utils
import Blueprint.singleOrientableJoint as singleOrientableJoint

reload(blueprint)
reload(utils)
reload(singleOrientableJoint)

CLASS_NAME = "RootTransform"
TITLE = "Root Transform"
DESCRIPTION = "Creates a single joint, with control for position and orientation. Once created (locked) the joint can rotate, translate and scale. Ideal use: global/master control"
ICON = "%s/Icons/_rootTxfrm.xpm" %os.environ["RIGGING_TOOL_ROOT"]

class RootTransform(singleOrientableJoint.SingleOrientableJoint):

	def __init__(self, _userSpecifiedName, _hookObj):
		jointInfo = [ ["joint", [0.0, 0.0, 0.0]] ]

		blueprint.Blueprint.__init__(self, CLASS_NAME, _userSpecifiedName, jointInfo, _hookObj)


	def Lock_phase1(self):
		
		moduleInfo = list(singleOrientableJoint.SingleOrientableJoint.Lock_phase1(self))
		moduleInfo[5] = True
		
		return moduleInfo