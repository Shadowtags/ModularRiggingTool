import pymel.core as pm
import os

import System.blueprint as blueprint
import Blueprint.finger as finger
import System.utils as utils
#reload(blueprint)
reload(utils)

CLASS_NAME = "Thumb"
TITLE = "Thumb"
DESCRIPTION = "Creates 4 joints, defining a thumb. Ideal use: thumb"
ICON = "%s/Icons/_thumb.xpm" %os.environ["RIGGING_TOOL_ROOT"]

class Thumb(finger.Finger):

	def __init__(self, _userSpecifiedName, _hookObj):
		jointInfo = [ ["root_joint", [0.0, 0.0, 0.0]], ["knuckle_1_joint", [4.0, 0.0, 0.0]], ["knuckle_2_joint", [8.0, 0.0, 0.0]], ["end_joint", [12.0, 0.0, 0.0]] ]

		blueprint.Blueprint.__init__(self, CLASS_NAME, _userSpecifiedName, jointInfo, _hookObj)