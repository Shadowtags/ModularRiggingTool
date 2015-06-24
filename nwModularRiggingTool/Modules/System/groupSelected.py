import pymel.core as pm
import os
from functools import partial

import System.utils as utils
reload(utils)

class GroupSelected:

    def __init__(self):
        self.objectsToGroup = []



    def ShowUI(self):
        self.FindSelectionToGroup()
        
        if len(self.objectsToGroup) == 0:
            return
        
        self.UIElements = {}
        
        if pm.window("groupSelected_UI_window", exists = True):
            pm.deleteUI("groupSelected_UI_window")
        
        
        windowWidth = 300
        windowHeight = 150
        self.UIElements["window"] = pm.window("groupSelected_UI_window", width = windowWidth, height = windowHeight, title = "Group Selected", sizeable = False)
        
        self.UIElements["topLevelColumn"] = pm.columnLayout(adjustableColumn = True, columnAlign = 'center', rowSpacing = 3)
        self.UIElements["groupName_rowColumn"] = pm.rowColumnLayout(numberOfColumns = 2, columnAttach = (1, 'right', 0), columnWidth = [(1, 80), (2, windowWidth - 90)], parent = self.UIElements["topLevelColumn"])
        
        pm.text(label = "Group Name: ", parent = self.UIElements["groupName_rowColumn"])
        self.UIElements["groupName"] = pm.textField(text = "group", parent = self.UIElements["groupName_rowColumn"])
        
        self.UIElements["createAt_rowColumn"] = pm.rowColumnLayout(numberOfColumns = 3, rowOffset = [(1, 'top', 2), (2, 'both', 2), (3, 'both', 2)], columnWidth = [(1, 80), (2, windowWidth - 170), (3, 80)], parent = self.UIElements["topLevelColumn"])
        pm.text(label = "Position at: ", parent = self.UIElements["createAt_rowColumn"])
        pm.text(label = '', parent = self.UIElements["createAt_rowColumn"])
        pm.text(label = '', parent = self.UIElements["createAt_rowColumn"])
        
        pm.text(label = '', parent = self.UIElements["createAt_rowColumn"])
        self.UIElements["createAt_lastSelected"] = pm.button(label = "Last Selected", command = self.CreateAtLastSelected, parent = self.UIElements["createAt_rowColumn"])
        pm.text(label = '', parent = self.UIElements["createAt_rowColumn"])
        
        pm.text(label = '', parent = self.UIElements["createAt_rowColumn"])
        self.UIElements["createAt_averagePosition"] = pm.button(label = "Average Position", command = self.CreateAtAveragePosition, parent = self.UIElements["createAt_rowColumn"])
        pm.text(label = '', parent = self.UIElements["createAt_rowColumn"])
        
        pm.separator(style = 'in', parent = self.UIElements["topLevelColumn"])
        
        
        columnWidth = (windowWidth / 2) - 5
        self.UIElements["button_row"] = pm.rowLayout(numberOfColumns = 2, columnWidth = [(1, columnWidth), (2, columnWidth)], columnAttach = [(1, 'both', 10), (2, 'both', 10)], columnAlign = [(1, 'center'), (2, 'center')], parent = self.UIElements["topLevelColumn"])
        pm.button(label = "Accept", command = self.AcceptWindow, parent = self.UIElements["button_row"])
        pm.button(label = "Cancel", command = self.CancelWindow, parent = self.UIElements["button_row"])
        
        
        pm.showWindow(self.UIElements["window"])
        
        
        self.CreateTemporaryGroupRepresentation()
        
        self.CreateAtAveragePosition()
        
        pm.select(self.tempGroupTransform, replace = True)
        pm.setToolTo("moveSuperContext")
    
    
    
    
    def FindSelectionToGroup(self):
        selectedObjects = pm.ls(selection = True, transforms = True)
        
        self.objectsToGroup = []
        for obj in selectedObjects:
            valid = False
            
            if obj.find("module_transform") != -1:
                splitString = obj.rsplit("module_transform")
                
                if splitString[1] == "":
                    valid = True
            
            
            if valid == False and obj.find("Group__") == 0:
                valid = True
            
            
            if valid == True:
                self.objectsToGroup.append(obj)
    
    
    def CreateTemporaryGroupRepresentation(self):
        controlGrpFile = "%s/ControlObjects/Blueprint/controlGroup_control.ma" %os.environ["RIGGING_TOOL_ROOT"]
        
        pm.importFile(controlGrpFile)
        
        self.tempGroupTransform = pm.rename("controlGroup_control", "Group__tempGroupTransform__")
        
        pm.connectAttr("%s.scaleY" %self.tempGroupTransform, "%s.scaleX" %self.tempGroupTransform)
        pm.connectAttr("%s.scaleY" %self.tempGroupTransform, "%s.scaleZ" %self.tempGroupTransform)
        
        for attr in ['scaleX', 'scaleZ', 'visibility']:
            pm.setAttr("%s.%s" %(self.tempGroupTransform, attr), lock = True, keyable = False)
        
        
        pm.aliasAttr('globalScale', "%s.scaleY" %self.tempGroupTransform)
    
    
    def CreateAtLastSelected(self, *args):
        controlPosition = pm.xform(self.objectsToGroup[len(self.objectsToGroup)-1], query = True, worldSpace = True, translation = True)
        pm.xform(self.tempGroupTransform, worldSpace = True, absolute = True, translation = controlPosition)
    
    
    def CreateAtAveragePosition(self, *args):
        controlPos = [0.0, 0.0, 0.0]
        
        for obj in self.objectsToGroup:
            objPos = pm.xform(obj, query = True, worldSpace = True, translation = True)
            controlPos[0] += objPos[0]  # add X-pos
            controlPos[1] += objPos[1]  # add Y-pos
            controlPos[2] += objPos[2]  # add Z-pos
        
        objectCount = len(self.objectsToGroup)
        controlPos[0] /= objectCount    # average X-pos
        controlPos[1] /= objectCount    # average Y-pos
        controlPos[2] /= objectCount    # average Z-pos
        
        pm.xform(self.tempGroupTransform, worldSpace = True, absolute = True, translation = controlPos)
    
    
    def CancelWindow(self, *args):
        pm.deleteUI(self.UIElements["window"])
        pm.delete(self.tempGroupTransform)
    
    
    def AcceptWindow(self, *args):
        groupName = pm.textField(self.UIElements["groupName"], query = True, text = True)
        
        if self.CreateGroup(groupName) != None:
            pm.deleteUI(self.UIElements["window"])
    
    
    
    def CreateGroup(self, _groupName):
        fullGroupName = "Group__%s" %_groupName
        
        # Check for valid names
        if pm.objExists(fullGroupName):
            pm.confirmDialog(title = "Name Conflict", message = 'Group "%s" already exits.' %_groupName, button= "Accept", defaultButton = "Accept")
            
            return None
        
        groupTransform = pm.rename(self.tempGroupTransform, fullGroupName)

        
        # Create container for grouped objects
        groupContainer = "Group_container"
        if not pm.objExists(groupContainer):
            pm.container(name = groupContainer)
        
        
        # Store containers to be grouped in a list
        containers = [groupContainer]
        for obj in self.objectsToGroup:
            if obj.find("Group__") == 0:
                continue
            
            objNamespace = utils.StripLeadingNamespace(obj)[0]
            containers.append("%s:module_container" %objNamespace)
        
        
        # Unlock all group containers
        for c in containers:
            pm.lockNode(c, lock = False, lockUnpublished = False)
        
        
        if len(self.objectsToGroup) != 0:
            
            # Group objects temprorarily to simulate final heirarchy
            tempGroup = pm.group(self.objectsToGroup, absolute = True)
            groupParent = pm.listRelatives(tempGroup, parent = True)
            
            
            if groupParent != []:
                pm.parent(groupTransform, groupParent[0], absolute = True)
            
            
            pm.parent(self.objectsToGroup, groupTransform, absolute = True)
            
            pm.delete(tempGroup)
        
        
        self.AddGroupToContainer(groupTransform)
        
        # Lock all group containers
        for c in containers:
            pm.lockNode(c, lock = True, lockUnpublished = True)
        
        
        # Make sure the created group is selected
        pm.setToolTo("moveSuperContext")
        pm.select(groupTransform, replace = True)
        
        return groupTransform
    
    
    
    def AddGroupToContainer(self, _group):
        groupContainer = "Group_container"
        utils.AddNodeToContainer(groupContainer, _group, _includeShapes = True)
        
        groupName = _group.partition("Group__")[2]
        
        pm.container(groupContainer, edit = True, publishAndBind = ["%s.translate" %_group, "%s_t" %groupName])
        pm.container(groupContainer, edit = True, publishAndBind = ["%s.rotate" %_group, "%s_r" %groupName])
        pm.container(groupContainer, edit = True, publishAndBind = ["%s.globalScale" %_group, "%s_globalScale" %groupName])