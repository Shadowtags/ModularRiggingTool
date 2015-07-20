import pymel.core as pm
import os
from functools import partial

import System.utils as utils

reload(utils)

class Blueprint_UI:
    
    def __init__(self):
        
        self.moduleInstance = None
        
        self.DeleteSymmetryMoveExpressions()
        
        # Store UI elements in a dictionary
        self.UIElements = {}
        
        # Refresh all UI
        if pm.window("blueprint_UI_window", exists = True):
            pm.deleteUI("blueprint_UI_window")

        if pm.window("mirrorModule_UI_window", exists = True):
            pm.deleteUI("mirrorModule_UI_window")
        
        if pm.window("groupSelected_UI_window", exists = True):
            pm.deleteUI("groupSelected_UI_window")
        
        if pm.window("saveTemplate_UI_window", exists = True):
            pm.deleteUI("saveTemplate_UI_window")
        
        
        
        windowWidth = 400
        windowHeight = 748
        
        self.UIElements["window"] = pm.window("blueprint_UI_window", width = windowWidth, height = windowHeight, title = "Blueprint Modue UI", sizeable = False)
        
        self.UIElements["topLevelColumn"] = pm.columnLayout(adjustableColumn = True, columnAlign = "center", parent = self.UIElements["window"])
        
        # Setup tab
        tabHeight = 630
        self.UIElements["tabs"] = pm.tabLayout(width = windowWidth, height = tabHeight, innerMarginWidth = 5, innerMarginHeight = 5, parent = self.UIElements["topLevelColumn"])
        
        tabWidth = pm.tabLayout(self.UIElements["tabs"], query = True, width = True)
        self.scrollWidth = tabWidth - 40
        
        self.InitializeModuleTab(tabWidth, tabHeight)
        
        # Template tab
        self.InitializeTemplatesTab(tabHeight, tabWidth)
        
        
        scenePublished = pm.objExists("Scene_Published")
        sceneUnlocked = not pm.objExists("Scene_Locked") and not scenePublished
        
        
        pm.tabLayout(self.UIElements["tabs"], edit = True, tabLabelIndex = ([1, 'Modules'], [2, 'Templates']), enable = sceneUnlocked )
        
        
        self.UIElements["lockPublishColumn"] = pm.columnLayout(adjustableColumn = True, columnAlign = 'center', rowSpacing = 3, parent = self.UIElements["topLevelColumn"])
        
        pm.separator(style = 'in', parent = self.UIElements["lockPublishColumn"])
        
        self.UIElements["lockBtn"] = pm.button(label = 'Lock', enable = sceneUnlocked, command = self.Lock, parent = self.UIElements["lockPublishColumn"])
        
        pm.separator(style = 'in', parent = self.UIElements["lockPublishColumn"])
        
        self.UIElements["publishBtn"] = pm.button(label = "Publish", enable = not sceneUnlocked and not scenePublished, command = self.Publish, parent = self.UIElements["lockPublishColumn"])
        
        
        
        # Display window
        pm.showWindow(self.UIElements["window"])
        
        
        self.CreateScriptJob()
    
    
    
    def CreateScriptJob(self):
        self.jobNum = pm.scriptJob(event = ["SelectionChanged", self.ModifySelected], runOnce = True, parent = self.UIElements["window"])
    
    
    
    def DeleteScriptJob(self):
        pm.scriptJob(kill = self.jobNum)
    
    
    def InitializeModuleTab(self, _tabWidth, _tabHeight):
        
        moduleSpecific_scrollHeight = 170
        scrollHeight = _tabHeight - moduleSpecific_scrollHeight - 163
        
        
        self.UIElements["moduleColumn"] = pm.columnLayout(adjustableColumn = True, rowSpacing = 3, parent = self.UIElements["tabs"])
        
        self.UIElements["moduleFrameLayout"] = pm.frameLayout(height = scrollHeight, collapsable = False, borderVisible = False, labelVisible = False, parent = self.UIElements["moduleColumn"])
        
        self.UIElements["moduleList_scroll"] = pm.scrollLayout(horizontalScrollBarThickness = 0, parent = self.UIElements["moduleFrameLayout"])
        
        self.UIElements["moduleList_column"] = pm.columnLayout(columnWidth = self.scrollWidth, adjustableColumn = True, rowSpacing = 2, parent = self.UIElements["moduleList_scroll"])
        
        
        # first separator
        pm.separator(style = 'in', parent = self.UIElements["moduleList_column"])
        
        # Module buttons
        for module in utils.FindAllModules("Modules/Blueprint"):
            self.CreateModuleInstallButton(module)
            pm.separator(style = 'in', parent = self.UIElements["moduleList_column"])
        
        
        # Module manipulation buttons
        pm.separator(style = 'in', parent = self.UIElements["moduleColumn"])
        
        self.UIElements["moduleName_row"] = pm.rowLayout(numberOfColumns = 2, columnAttach = (1, 'right', 0), columnWidth = [(1, 80)], adjustableColumn = 2, parent = self.UIElements["moduleColumn"])
        pm.text(label = "Module Name :", parent = self.UIElements["moduleName_row"])
        self.UIElements["moduleName"] = pm.textField(enable = False, alwaysInvokeEnterCommandOnReturn = True, parent = self.UIElements["moduleName_row"], enterCommand = self.RenameModule)
        
        
        columnWidth = (_tabWidth - 20) / 3
        
        self.UIElements["moduleButtons_rowColumns"] = pm.rowColumnLayout(numberOfColumns = 3, rowOffset = [(1, 'both', 2), (2, 'both', 2), (3, 'both', 2)], columnAttach = [(1, 'both', 3), (2, 'both', 3), (3, 'both', 3)], columnWidth = [(1, columnWidth), (2, columnWidth), (3, columnWidth)], parent = self.UIElements["moduleColumn"])
        
        # First row of buttons
        self.UIElements["rehookBtn"] = pm.button(enable = False, label = "Re-hook", command = self.RehookModule_setup, parent = self.UIElements["moduleButtons_rowColumns"])
        self.UIElements["snapRootBtn"] = pm.button(enable = False, label = "Snap Root > Hook", command = self.SnapRootToHook, parent = self.UIElements["moduleButtons_rowColumns"])
        self.UIElements["constrainBtn"] = pm.button(enable = False, label = "Constrain Root > Hook", command = self.ConstrainRootToHook, parent = self.UIElements["moduleButtons_rowColumns"])
        
        # Second row of buttons
        self.UIElements["groupSelectedBtn"] = pm.button(label = "Group Selected", command = self.GroupSelected, parent = self.UIElements["moduleButtons_rowColumns"])
        self.UIElements["ungroupBtn"] = pm.button(enable = False, label = "Ungroup", command = self.UngroupSelected, parent = self.UIElements["moduleButtons_rowColumns"])
        self.UIElements["mirrorModuleBtn"] = pm.button(enable = False, label = "Mirror Module", command = self.MirrorModule, parent = self.UIElements["moduleButtons_rowColumns"])
        
        # Third row of buttons
        self.UIElements["duplicateModuleBtn"] = pm.button(enable = True, label = "Duplicate Module", command = self.DuplicateModule, parent = self.UIElements["moduleButtons_rowColumns"])
        self.UIElements["deleteModuleBtn"] = pm.button(enable = False, label = "Delete Module", command = self.DeleteModule, parent = self.UIElements["moduleButtons_rowColumns"])
        self.UIElements["symmetryMoveCheckBox"] = pm.checkBox(enable = True, label = "Symmetry Move", onCommand = self.SetupSymmetryMoveExpressions_CheckBox, offCommand = self.DeleteSymmetryMoveExpressions, parent = self.UIElements["moduleButtons_rowColumns"])
        
        pm.separator(style = 'in', parent = self.UIElements["moduleColumn"])
        
        
        
        self.UIElements["moduleSpecificRowColumnLayout"] = pm.rowColumnLayout(numberOfRows = 1, rowAttach = [1, 'both', 0], rowHeight = [1, moduleSpecific_scrollHeight], parent = self.UIElements["moduleColumn"])
        self.UIElements["modueSpecific_scroll"] = pm.scrollLayout(width = _tabWidth - 8, horizontalScrollBarThickness = 0, parent = self.UIElements["moduleSpecificRowColumnLayout"])
        self.UIElements["moduleSpecific_column"] = pm.columnLayout(columnWidth = self.scrollWidth, columnAttach = ['both', 5], rowSpacing = 2, parent = self.UIElements["modueSpecific_scroll"])
        
        
        pm.separator(style = 'in', parent = self.UIElements["moduleColumn"])
    
    
    def InitializeTemplatesTab(self, _tabHeight, _tabWidth):
        
        self.UIElements["templatesColumn"] = pm.columnLayout(adjustableColumn = True, rowSpacing = 3, columnAttach = ["both", 0], parent = self.UIElements["tabs"])
        
        self.UIElements["templatesFrame"] = pm.frameLayout(height = (_tabHeight - 104), collapsable = False, borderVisible = False, labelVisible = False, parent = self.UIElements["templatesColumn"])
        self.UIElements["templateList_scroll"] = pm.scrollLayout(horizontalScrollBarThickness = 0, parent = self.UIElements["templatesFrame"])
        self.UIElements["templateList_column"] = pm.columnLayout(adjustableColumn = True, rowSpacing = 2, parent = self.UIElements["templateList_scroll"])
        
        pm.separator(style = 'in', parent = self.UIElements["templateList_column"])
        
        for template in utils.FindAllMayaFiles("/Templates"):
            
            templateAndPath = "%s/Templates/%s.ma" %(os.environ["RIGGING_TOOL_ROOT"], template)
            self.CreateTemplateInstallButton(templateAndPath)
        
        
        pm.separator(style = 'in', parent = self.UIElements["templatesColumn"])
        
        self.UIElements["prepareTemplateBtn"] = pm.button(label = "Prepare for Template", command = self.PrepareForTemplate, parent = self.UIElements["templatesColumn"])
        
        pm.separator(style = 'in', parent = self.UIElements["templatesColumn"])
        
        self.UIElements["saveCurrentBtn"] = pm.button(label = "Save Current as Template", command = self.SaveCurrentAsTemplate, parent = self.UIElements["templatesColumn"])
        
        pm.separator(style = 'in', parent = self.UIElements["templatesColumn"])
    
    
    
    def CreateModuleInstallButton(self, _module):
        
        mod = __import__("Blueprint.%s" %_module, (), (), [_module])
        reload(mod)
        
        title = mod.TITLE
        description = mod.DESCRIPTION
        icon = mod.ICON
        
        # Create UI
        buttonSize = 64
        row = pm.rowLayout(numberOfColumns = 2, columnWidth = ([1, buttonSize]), adjustableColumn = 2, columnAttach = ([1, 'both', 0], [2, 'both', 5]), parent = self.UIElements["moduleList_column"])
        
        self.UIElements["module_button_%s" %_module] = pm.symbolButton(width = buttonSize, height = buttonSize, image = icon, command = partial(self.InstallModule, _module), parent = row)
        
        textColumn = pm.columnLayout(columnAlign = "center", rowSpacing = 5, parent = row)
        pm.text(align = "center", width = self.scrollWidth - buttonSize - 16, label = title, parent = textColumn)
        
        pm.scrollField(text = description, editable = False, width = self.scrollWidth - buttonSize - 16, height = buttonSize - 16, wordWrap = True, parent = textColumn)
    
    
    def CreateTemplateInstallButton(self, _templateAndPath):
        buttonSize = 64
        
        templateDescriptionFile = "%s.txt" %_templateAndPath.partition(".ma")[0]
        
        with open(templateDescriptionFile, 'r') as file:
            
            title = file.readline()[0:-1]
            description = file.readline()[0:-1]
            icon = file.readline()[0:-1]
        
        row = pm.rowLayout(width = self.scrollWidth, numberOfColumns = 2, columnWidth = ([1, buttonSize], [2, self.scrollWidth - buttonSize]), adjustableColumn = 2, columnAttach = ([1, "both", 0], [2, "both", 5]), parent = self.UIElements["templateList_column"])
        self.UIElements["templat_button_%s" %_templateAndPath] = pm.symbolButton(width = buttonSize, height = buttonSize, image = icon, command = partial(self.InstallTemplate, _templateAndPath), parent = row)
        
        textColumn = pm.columnLayout(columnAlign = "center", parent = row)
        pm.text(align = "center", width = self.scrollWidth - buttonSize - 16, label = title, parent = textColumn)
        pm.scrollField(text = description, editable = False, width = self.scrollWidth - buttonSize - 16, height = buttonSize - 16, wordWrap = True, parent = textColumn)
        
        pm.separator(style = "in", parent = self.UIElements["templateList_column"])
    
    
    def InstallModule(self, _module, *args):
        
        basename = "instance_"
        
        # Set namespace to root and list all namespaces in scene
        pm.namespace(setNamespace = ':')
        namespaces = pm.namespaceInfo(listOnlyNamespaces = True)
        
        
        # Find our module namespace
        for i in range(len(namespaces)):
            if namespaces[i].find("__") != -1:
                namespaces[i] = namespaces[i].rpartition("__")[2]
        
        
        newSuffix = utils.FindHighestTrailingNumber(namespaces, basename) + 1
        
        userSpecName = basename + str(newSuffix)
        
        
        hookObj = self.FindHookObjectFromSelection()
        
        
        # Import our module
        mod = __import__("Blueprint.%s" %_module, (), (), [_module])
        reload(mod)
        
        moduleClass = getattr(mod, mod.CLASS_NAME)
        moduleInstance = moduleClass(userSpecName, hookObj)
        moduleInstance.Install()
        
        # After installation of module, select module transform with move tool
        moduleTranform = "%s__%s:module_transform" %(mod.CLASS_NAME, userSpecName)
        pm.select(moduleTranform, replace = True)
        pm.setToolTo("moveSuperContext")
    
    
    def IsRootTransformInstalled(self):
        pm.namespace(setNamespace = ":")
        namespaces = pm.namespaceInfo(listOnlyNamespaces = True)
        
        for namespace in namespaces:
            if namespace.find("RootTransform__") == 0:
                return True
        
        return False
    
    def Lock(self, *args):
        
        # Recommend creation of root transform if not already implemented
        if not self.IsRootTransformInstalled():
            result = pm.confirmDialog(messageAlign = "center", title = "Lock Character", message = "We have detected that you don't have a root transform (global transform). \nWould you like to go back and edit your blueprint setup? \n\n(It is recommended that all rigs have at least one global control module).", button = ["Yes", "No"], defaultButton = "Yes", dismissString = "Yes")
            
            if result == "Yes":
                return
        
        
        # Give user warning that locking is permanent
        result = pm.confirmDialog(messageAlign = 'center', title = 'Lock Blueprint', button = ['Accept', 'Cancel'], defaultButton = 'Accept', cancelButton = 'Cancel', dismissString = 'Cancel', message = "The action of locking a character will convert the current blueprint modules to joints. \nThis action cannot be undone. \nModifications to the blueprint system cannot be made after this point. \n\nDo you wish to continue?")
        
        if result != 'Accept':
            return
        
        # Clear scene of script jobs
        self.DeleteSymmetryMoveExpressions()
        pm.checkBox(self.UIElements["symmetryMoveCheckBox"], edit = True, value = False)
        self.DeleteScriptJob()
        
        
        moduleInfo = []  # Store (module, userSpecifiedName) pairs
        
        # List all namespaces in scene from root
        pm.namespace(setNamespace = ':')
        namespaces = pm.namespaceInfo(listOnlyNamespaces = True)
        
        moduleNameInfo = utils.FindAllModuleNames("/Modules/Blueprint")
        validModules = moduleNameInfo[0]
        validModuleNames = moduleNameInfo[1]
        
        # Search scene for valid namespaces
        for n in namespaces:
            splitString = n.partition('__')
            
            if splitString[1] != '':
                
                module = splitString[0]
                userSpecifiedName = splitString[2]
                
                # Add valid modules
                if module in validModuleNames:
                    index = validModuleNames.index(module)
                    moduleInfo.append([validModules[index], userSpecifiedName])
        
        
        # Abort locking if no blueprints available
        if len(moduleInfo) == 0:
            pm.confirmDialog(messageAlign = 'center', title = 'Lock Blueprints', message = "There appear to be no blueprint \ninstances in the current scene. \n\nAborting lock.", button = ["Accept"], defaultButton = "Accept")
            return
        
        
        # Lock phase 1
        moduleInstances = []
        for module in moduleInfo:
            mod = __import__("Blueprint.%s" %module[0], {}, {}, [module[0]])
            reload(mod)
            
            moduleClass = getattr(mod, mod.CLASS_NAME)
            moduleInst = moduleClass(module[1], None)
            
            moduleInf = moduleInst.Lock_phase1()
            moduleInstances.append((moduleInst, moduleInf))
        
        
        # Lock phase 2
        for module in moduleInstances:
            module[0].Lock_phase2(module[1])
        
        
        # Lock phase 3
        for module in moduleInstances:
            hookObject = module[1][4]
            module[0].Lock_phase3(hookObject)
        
        
        # Scene completely locked
        sceneLockedLocator = pm.spaceLocator(name = "Scene_Locked")
        pm.setAttr("%s.visibility" %sceneLockedLocator, 0)
        pm.lockNode(sceneLockedLocator, lock = True, lockUnpublished = True)
        
        # Force update scene
        pm.select(clear = True)
        self.ModifySelected()
        
        pm.tabLayout(self.UIElements["tabs"], edit = True, enable = False)
        pm.button(self.UIElements["lockBtn"], edit = True, enable = False)
        pm.button(self.UIElements["publishBtn"], edit = True, enable = True)
    
    
    def ModifySelected(self, *args):
        
        # Only proceed if the scene haven't been locked down
        if not pm.objExists("Scene_Locked"):
            
            if pm.checkBox(self.UIElements["symmetryMoveCheckBox"], query = True, value = True):
                self.DeleteSymmetryMoveExpressions()
                self.SetupSymmetryMoveExpressions()
            
            
            selectedNodes = pm.ls(selection = True)
            
            if len(selectedNodes) <= 1:
                self.moduleInstance = None
                selectedModuleNamespace = None
                currentModuleFile = None
                
                pm.button(self.UIElements["ungroupBtn"], edit = True, enable = False)
                pm.button(self.UIElements["mirrorModuleBtn"], edit = True, enable = False)
                
                if len(selectedNodes) == 1:
                    lastSelected = selectedNodes[0]
                    
                    # Enable ungroup button if selected node is a group node
                    if lastSelected.find("Group__") == 0:
                        pm.button(self.UIElements["ungroupBtn"], edit = True, enable = True)
                        pm.button(self.UIElements["mirrorModuleBtn"], edit = True, enable = True, label = "Mirror Group")
                    
                    namespaceAndNode = utils.StripLeadingNamespace(lastSelected)
                    
                    if namespaceAndNode != None:
                        namespace = namespaceAndNode[0]
                        
                        moduleNameInfo = utils.FindAllModuleNames("/Modules/Blueprint")
                        validModules = moduleNameInfo[0]
                        validModuleNames = moduleNameInfo[1]
                        
                        index = 0
                        for moduleName in validModuleNames:
                            moduleNameIncSuffix = "%s__" %moduleName
                            
                            if namespace.find(moduleNameIncSuffix) == 0:
                                currentModuleFile = validModules[index]
                                selectedModuleNamespace = namespace
                                break
                            
                            index += 1
            
                controlEnable = False
                userSpecifiedName = ''
                constrainCommand = self.ConstrainRootToHook
                constrainLabel = "Constrain Root > Hook"
                
                if selectedModuleNamespace != None:
                    controlEnable = True
                    userSpecifiedName = selectedModuleNamespace.partition('__')[2]
                    
                    
                    mod = __import__("Blueprint.%s" %currentModuleFile, {}, {}, [currentModuleFile])
                    reload(mod)
                    
                    moduleClass = getattr(mod, mod.CLASS_NAME)
                    self.moduleInstance = moduleClass(userSpecifiedName, None)
                    
                    
                    pm.button(self.UIElements["mirrorModuleBtn"], edit = True, enable = True, label = "Mirror Module")
                    
                    if self.moduleInstance.IsRootConstrained():
                        constrainCommand = self.UnconstrainRootFromHook
                        constrainLabel = "Unconstrain Root"
                
                
                pm.button(self.UIElements["rehookBtn"], edit = True, enable = controlEnable)
                pm.button(self.UIElements["snapRootBtn"], edit = True, enable = controlEnable)
                pm.button(self.UIElements["constrainBtn"], edit = True, enable = controlEnable, label = constrainLabel, command = constrainCommand)
                
                pm.button(self.UIElements["deleteModuleBtn"], edit = True, enable = controlEnable, command = self.DeleteModule)
                
                pm.textField(self.UIElements["moduleName"], edit = True, enable = controlEnable, text = userSpecifiedName)
                
                
                self.CreateModuleSpecificControls()
            
            
            self.CreateScriptJob()
    
    
    
    def CreateModuleSpecificControls(self):
        
        existingControls = pm.columnLayout(self.UIElements["moduleSpecific_column"], query = True, childArray = True)
        
        if existingControls != None:
            pm.deleteUI(existingControls)
        
        pm.setParent(self.UIElements["moduleSpecific_column"])
        
        if self.moduleInstance != None:
            self.moduleInstance.UI(self, self.UIElements["moduleSpecific_column"])
    
    
    def DeleteModule(self, *args):
        symmetryMove = pm.checkBox(self.UIElements["symmetryMoveCheckBox"], query = True, value = True)
        if symmetryMove:
            self.DeleteSymmetryMoveExpressions()
        
        self.moduleInstance.Delete()
        pm.select(clear = True)
        
        if symmetryMove:
            self.SetupSymmetryMoveExpressions_CheckBox()
    
    
    def RenameModule(self, *args):
        newName = pm.textField(self.UIElements["moduleName"], query = True, text = True)
        
        symmetryMove = pm.checkBox(self.UIElements["symmetryMoveCheckBox"], query = True, value = True)
        if symmetryMove:
            self.DeleteSymmetryMoveExpressions()
        
        self.moduleInstance.RenameModuleInstance(newName)
        
        if symmetryMove:
            self.SetupSymmetryMoveExpressions_CheckBox()
        
        previousSelected = pm.ls(selection = True)
        
        if len(previousSelected) > 0:
            pm.select(previousSelected, replace = True)
        
        else:
            pm.select(clear = True)
    
    
    
    def FindHookObjectFromSelection(self, *args):
        
        selectedObjects = pm.ls(selection = True, transforms = True)
        numberOfObjects = len(selectedObjects)
        hookObj = None
        
        if numberOfObjects != 0:
            hookObj = selectedObjects[numberOfObjects - 1]
        
        return hookObj
    
    
    
    def RehookModule_setup(self, *args):
        
        selectedNodes = pm.ls(selection = True, transforms = True)
        
        if len(selectedNodes) == 2:
            newHook = self.FindHookObjectFromSelection()
            self.moduleInstance.Rehook(newHook)
        
        else:
            self.DeleteScriptJob()
            
            currentSelection = pm.ls(selection = True)
            
            pm.headsUpMessage("Please select the joint you wish to re-hook to. Clear selection to un-hook.")
            
            pm.scriptJob(event = ['SelectionChanged', partial(self.RehookModule_callback, currentSelection)], runOnce = True)
    
    
    
    
    def RehookModule_callback(self, _currentSelection):
        newHook = self.FindHookObjectFromSelection()
        
        self.moduleInstance.Rehook(newHook)
        
        if len(_currentSelection) > 0:
            pm.select(_currentSelection, replace = True)
        else:
            pm.select(clear = True)
        
        
        self.CreateScriptJob()
    
    
    
    def SnapRootToHook(self, *args):
        self.moduleInstance.SnapRootToHook()
    
    
    def ConstrainRootToHook(self, *args):
        self.moduleInstance.ConstrainRootToHook()
        
        pm.button(self.UIElements["constrainBtn"], edit = True, label = "Unconstrain Root", command = self.UnconstrainRootFromHook)
    
    
    def UnconstrainRootFromHook(self, *args):
        self.moduleInstance.UnconstrainRootFromHook()
        
        pm.button(self.UIElements["constrainBtn"], edit = True, label = "Constrain Root > Hook", command = self.ConstrainRootToHook)
    
    
    def GroupSelected(self, *args):
        import System.groupSelected as group
        reload(group)
        
        group.GroupSelected().ShowUI()
    
    
    def UngroupSelected(self, *args):
        import System.groupSelected as group
        reload(group)
        
        group.UngroupSelected()
    
    
    
    def MirrorModule(self, *args):
        
        import System.mirrorModule as mirror
        reload(mirror)
        
        mirror.MirrorModule()
    
    
    def SetupSymmetryMoveExpressions_CheckBox(self, *args):
        self.DeleteScriptJob()
        
        self.SetupSymmetryMoveExpressions()
        
        self.CreateScriptJob()
    
    
    
    def SetupSymmetryMoveExpressions(self, *args):
        pm.namespace(setNamespace = ":")
        selection = pm.ls(selection = True, transforms = True)
        
        expressionContainer = pm.container(name = "symmetryMove_container")
        
        if len(selection) == 0:
            return
        
        linkedObjs = []
        for obj in selection:
            if obj in linkedObjs:
                continue
            
            # Apply symmetry to group
            if obj.find("Group__") == 0:
                if pm.attributeQuery("mirrorLinks", node = obj, exists = True):
                    mirrorLinks = pm.getAttr("%s.mirrorLinks" %obj)
                    groupInfo = mirrorLinks.rpartition("__")
                    mirrorObj = groupInfo[0]
                    axis = groupInfo[2]
                    
                    linkedObjs.append(mirrorObj)
                    
                    self.SetupSymmetryMoveForObject(obj, mirrorObj, axis, _translation = True, _orientation = True, _globalScale = True)
            
            else:
                objNamespaceInfo = utils.StripLeadingNamespace(obj)
                
                if objNamespaceInfo != None:
                    if pm.attributeQuery("mirrorLinks", node = "%s:module_grp" %objNamespaceInfo[0], exists = True):
                        mirrorLinks = pm.getAttr("%s:module_grp.mirrorLinks" %objNamespaceInfo[0])
                        
                        moduleInfo = mirrorLinks.rpartition("__")
                        module = moduleInfo[0]
                        axis = moduleInfo[2]
                        
                        # Apply symmetry to translation control
                        if objNamespaceInfo[1].find("translation_control") != -1:
                            mirrorObj = "%s:%s" %(module, objNamespaceInfo[1])
                            linkedObjs.append(mirrorObj)
                            self.SetupSymmetryMoveForObject(obj, mirrorObj, axis, _translation = True, _orientation = False, _globalScale = False)
                        
                        # Apply symmetry to module transform
                        elif objNamespaceInfo[1].find("module_transform") == 0:
                            mirrorObj = "%s:module_transform" %module
                            linkedObjs.append(mirrorObj)
                            self.SetupSymmetryMoveForObject(obj, mirrorObj, axis, _translation = True, _orientation = True, _globalScale = True)
                        
                        # Apply symmetry to rotation control
                        elif objNamespaceInfo[1].find("orientation_control") != -1:
                            mirrorObj = "%s:%s" %(module, objNamespaceInfo[1])
                            linkedObjs.append(mirrorObj)
                            
                            expressionString = "%s.rotateX = %s.rotateX;\n" %(mirrorObj, obj)
                            expression = pm.expression(name = "%s_symmetryMoveExpression" %mirrorObj, string = expressionString)
                            utils.AddNodeToContainer(expressionContainer, expression)
                        
                        # Apply symmetry to single orientation control
                        elif objNamespaceInfo[1].find("singleJointOrientation_control") != -1:
                            mirrorObj = "%s:%s" %(module, objNamespaceInfo[1])
                            linkedObjs.append(mirrorObj)
                            
                            expressionString = "%s.rotateX = %s.rotateX;\n" %(mirrorObj, obj)
                            expressionString += "%s.rotateY = %s.rotateY;\n" %(mirrorObj, obj)
                            expressionString += "%s.rotateZ = %s.rotateZ;\n" %(mirrorObj, obj)
                            
                            expression = pm.expression(name = "%s_symmetryMoveExpression" %mirrorObj, string = expressionString)
                            utils.AddNodeToContainer(expressionContainer, expression)
        
        pm.lockNode(expressionContainer, lock = True)
        pm.select(selection, replace = True)
    
    
    
    def SetupSymmetryMoveForObject(self, _obj, _mirrorObj, _axis, _translation = False, _orientation = False, _globalScale = False):
        
        duplicateObject = pm.duplicate(_obj, parentOnly = True, inputConnections = True, name = "%s_mirrorHelper" %_obj)[0]
        
        emptyGroup = pm.group(empty = True, name = "%smirror_scale_grp" %_obj)
        pm.parent(duplicateObject, emptyGroup, absolute = True)
        
        scaleAttribute = ".scale%s" %_axis
        pm.setAttr("%s%s" %(emptyGroup, scaleAttribute), -1)
        
        # mel expression 'namespace -setNamespace ":";' causes update errors post Maya 2010
        expressionString = ''
        if _translation:
            expressionString += '$worldSpacePos = `xform -query -worldSpace -translation %s`;\n' %_obj
        if _orientation:
            expressionString += '$worldSpaceOrient = `xform -query -worldSpace -rotation %s`;\n' %_obj
        
        
        attrs = []
        if _translation:
            attrs.extend([".translateX", ".translateY", ".translateZ"])
        if _orientation:
            attrs.extend([".rotateX", ".rotateY", ".rotateZ"])
        
        
        # Force an update of the expression
        for attr in attrs:
            expressionString += "%s%s = %s%s;\n" %(duplicateObject, attr, _obj, attr)
        
        
        i = 0
        for axis in ["X", "Y", "Z"]:
            if _translation:
                expressionString += "%s.translate%s = $worldSpacePos[%d];\n" %(duplicateObject, axis, i)
            if _orientation:
                expressionString += "%s.rotate%s = $worldSpaceOrient[%d];\n" %(duplicateObject, axis, i)
            
            i += 1
        
        
        if _globalScale:
            expressionString += "%s.globalScale = %s.globalScale;\n" %(duplicateObject, _obj)
        
        # Create unique expression name from namespace
        expressionNames = utils.StripLeadingNamespace(duplicateObject)
        expName = ''
        
        if expressionNames == None:
            expName = '%s' %duplicateObject
        else:
            expName = "%s__%s" %(expressionNames[0], expressionNames[1])
        
        expression = pm.expression(name = "%s__symmetryMoveExpression" %expName, string = expressionString)
        
        
        constraint = ''
        if _translation and _orientation:
            constraint = pm.parentConstraint(duplicateObject, _mirrorObj, maintainOffset = False, name = "%s_symmetryMoveConstraint" %_mirrorObj)
        elif _translation:
            constraint = pm.pointConstraint(duplicateObject, _mirrorObj, maintainOffset = False, name = "%s_symmetryMoveConstraint" %_mirrorObj)
        elif _orientation:
            constraint = pm.orientConstraint(duplicateObject, _mirrorObj, maintainOffset = False, name = "%s_symmetryMoveConstraint" %_mirrorObj)
        
        if _globalScale:
            pm.connectAttr("%s.globalScale" %duplicateObject, "%s.globalScale" %_mirrorObj)
        
        
        utils.AddNodeToContainer("symmetryMove_container", [duplicateObject, emptyGroup, expression, constraint], True)
    
    
    def DeleteSymmetryMoveExpressions(self, *args):
        container = "symmetryMove_container"
        
        if pm.objExists(container):
            pm.lockNode(container, lock = False)
            
            nodes = pm.container(container, query = True, nodeList = True)
            nodes = pm.ls(nodes, type = ["parentConstraint", "pointConstraint", "orientConstraint"])
            
            if len(nodes) > 0:
                pm.delete(nodes)
            
            pm.delete(container)
    
    
    def PrepareForTemplate(self, *args):
        
        pm.select(all = True)
        rootLevelNodes = pm.ls(selection = True, transforms = True)
        
        filteredNodes = []
        for node in rootLevelNodes:
            
            if node.find("Group__") == 0:
                filteredNodes.append(node)
            else:
                nodeNamespaceInfo = utils.StripAllNamespaces(node)
                
                if nodeNamespaceInfo != None:
                    if nodeNamespaceInfo[1] == "module_transform":
                        filteredNodes.append(node)
        
        
        pm.select(filteredNodes, replace = True)
        self.GroupSelected()
    
    
    def SaveCurrentAsTemplate(self, *args):
        
        self.saveTemplateUIElements = {}
        
        if pm.window("saveTemplate_UI_window", exists = True):
            pm.deleteUI("saveTemplate_UI_window")
        
        windowWidth = 300
        windowHeight = 152
        self.saveTemplateUIElements["window"] = pm.window("saveTemplate_UI_window", width = windowWidth, height = windowHeight, title = "Save Current as Template", sizeable = False)
        
        self.saveTemplateUIElements["topLevelColumn"] = pm.columnLayout(adjustableColumn = True, columnAlign = "center", rowSpacing = 3, parent = self.saveTemplateUIElements["window"])
        self.saveTemplateUIElements["templateName_rowColumn"] = pm.rowColumnLayout(numberOfColumns = 2, columnAttach = (1, 'right', 0), columnWidth = [(1, 90), (2, windowWidth - 100)], parent = self.saveTemplateUIElements["topLevelColumn"])
        
        pm.text(label = "Template Name: ", parent = self.saveTemplateUIElements["templateName_rowColumn"])
        self.saveTemplateUIElements["templateName"] = pm.textField(text = '([a-z][A-Z][0-9] and _ only)', parent = self.saveTemplateUIElements["templateName_rowColumn"])
        
        pm.text(label = "Title: ", parent = self.saveTemplateUIElements["templateName_rowColumn"])
        self.saveTemplateUIElements["templateTitle"] = pm.textField(text = 'Title', parent = self.saveTemplateUIElements["templateName_rowColumn"])
    
        pm.text(label = "Description: ", parent = self.saveTemplateUIElements["templateName_rowColumn"])
        self.saveTemplateUIElements["templateDescription"] = pm.textField(text = 'Description', parent = self.saveTemplateUIElements["templateName_rowColumn"])
        
        pm.text(label = "Icon: ", parent = self.saveTemplateUIElements["templateName_rowColumn"])
        self.saveTemplateUIElements["templateIcon"] = pm.textField(text = '[programRoot]/Icons/_icon.xpm', parent = self.saveTemplateUIElements["templateName_rowColumn"])
        
        
        pm.separator(style = "in", parent = self.saveTemplateUIElements["topLevelColumn"])
        
        columnWidth = (windowWidth / 2) - 5
        self.saveTemplateUIElements["button_row"] = pm.rowLayout(numberOfColumns = 2, columnWidth = [(1, columnWidth), (2, columnWidth)], columnAttach = [(1, "both", 10), (2, "both", 10)], columnAlign = [(1, "center"), (2, "center")], parent = self.saveTemplateUIElements["topLevelColumn"])
        
        pm.button(label = "Accept", command = self.SaveCurrentAsTemplate_AcceptWindow, parent = self.saveTemplateUIElements["button_row"])
        pm.button(label = "Cancel", command = self.SaveCurrentAsTemplate_CancelWindow, parent = self.saveTemplateUIElements["button_row"])
        
        pm.showWindow(self.saveTemplateUIElements["window"])
    
    
    def SaveCurrentAsTemplate_CancelWindow(self, *args):
        pm.deleteUI(self.saveTemplateUIElements["window"])
    
    
    def SaveCurrentAsTemplate_AcceptWindow(self, *args):
        templateName = pm.textField(self.saveTemplateUIElements["templateName"], query = True, text = True)
        
        programRoot = os.environ["RIGGING_TOOL_ROOT"]
        templateFileName = "%s/Templates/%s.ma" %(programRoot, templateName)
        
        if os.path.exists(templateFileName):
            pm.confirmDialog(title = "Save Current as Template", message = "Template already exists with that name. Aborting save.", button = ["Accept"], defaultButton = "Accept")
            return
        
        if pm.objExists("Group_container"):
            pm.select("Group_container", replace = True)
        else:
            pm.select(clear = True)
        
        pm.namespace(setNamespace = ":")
        namespaces = pm.namespaceInfo(listOnlyNamespaces = True)
        
        for n in namespaces:
            if n.find("__") != -1:
                pm.select("%s:module_container" %n, add = True)
        
        pm.exportSelected(templateFileName, type = "mayaAscii")
        pm.select(clear = True)
        
        title = pm.textField(self.saveTemplateUIElements["templateTitle"], query = True, text = True)
        description = pm.textField(self.saveTemplateUIElements["templateDescription"], query = True, text = True)
        icon = pm.textField(self.saveTemplateUIElements["templateIcon"], query = True, text = True)
        
        
        if icon.find("[programRoot]") != -1:
            icon = "%s%s" %(programRoot, icon.partition("[programRoot]")[2])
        
        
        templateDescriptionFileName = "%s/Templates/%s.txt" %(programRoot, templateName)
        with open(templateDescriptionFileName, 'w') as file:
            
            file.write("%s\n" %title)
            file.write("%s\n" %description)
            file.write("%s\n" %icon)
        
        
        self.CreateTemplateInstallButton(templateFileName)
        pm.showWindow(self.UIElements["window"])
        
        pm.deleteUI(self.saveTemplateUIElements["window"])
    
    
    
    def InstallTemplate(self, _templateAndPath, *args):
        pm.importFile(_templateAndPath, namespace = "TEMPLATE_1")
        
        self.ResolveNamespaceClashes("TEMPLATE_1")
        
        groupContainer = "TEMPLATE_1:group_container"
        if pm.objExists(groupContainer):
            self.ResolveGroupNameClashes("TEMPLATE_1")
            
            pm.lockNode(groupContainer, lock = False, lockUnpublished = False)
            
            oldGroupContainer = "Group_container"
            if pm.objExists(oldGroupContainer):
                pm.lockNode(oldGroupContainer, lock = False, lockUnpublished = False)
                
                nodeList = pm.containe(groupContainer, query = True, nodeList = True)
                utils.AddNodeToContainer(oldGroupContainer, nodeList, _force = True)
                
                pm.delete(groupContainer)
            else:
                pm.rename(groupContainer, oldGroupContainer)
            
            pm.lockNode("Group_container", lock = True, lockUnpublished = True)
        
        # Clean up temporary namespace
        pm.namespace(setNamespace = ":")
        pm.namespace(moveNamespace = ("TEMPLATE_1", ":"), force = True)
        pm.namespace(removeNamespace = "TEMPLATE_1")
    
    
    def ResolveNamespaceClashes(self, _tempNamespace):
        returnNames = []
        
        pm.namespace(setNamespace = _tempNamespace)
        namespaces = pm.namespaceInfo(listOnlyNamespaces = True)
        
        pm.namespace(setNamespace = ":")
        existingNamespaces = pm.namespaceInfo(listOnlyNamespaces = True)
        
        
        for i in range(len(namespaces)):
            namespaces[i] = namespaces[i].partition("%s:" %_tempNamespace)[2]
        
        for name in namespaces:
            newName = str(name)
            oldName = "%s:%s" %(_tempNamespace, name)
            
            if name in existingNamespaces:
                highestSuffix = utils.FindHighestTrailingNumber(existingNamespaces, "%s_" %name)
                highestSuffix += 1
                
                newName = "%s_%d" %(name, highestSuffix)
            
            returnNames.append([oldName, newName])
        
        
        self.ResolveNameChangeMirrorLinks(returnNames, _tempNamespace)
        
        
        self.RenameNamespaces(returnNames)
        
        return returnNames
    
    
    def ResolveGroupNameClashes(self, _tempNamespace):
        pm.namespace(setNamespace = _tempNamespace)
        dependencyNodes = pm.namespaceInfo(listOnlyDependencyNodes = True)
    
        pm.namespace(setNamespace = ":")
    
        transforms = pm.ls(dependencyNodes, transforms = True)
    
        groups = []
        for node in transforms:
            if node.find("%s:Group__"% _tempNamespace) == 0:
                groups.append(node)
    
        if len(groups) == 0:
            return groups
    
        groupNames = []
        for group in groups:
            groupName = group.partition("%s:" %_tempNamespace)[2]
            newGroupName = str(groupName)
    
            if pm.objExists(newGroupName):
                existingGroups = pm.ls("Group__*", transforms = True)
    
                highestSuffix = utils.FindHighestTrailingNumber(existingGroups, "%s_" %groupName)
                highestSuffix += 1
    
                newGroupName = "%s_%d" %(groupName, highestSuffix)
    
            groupNames.append([group, newGroupName])
    
    
        self.ResolveNameChangeMirrorLinks(groupNames, _tempNamespace)
    
        groupContainer = "%s:Group_container" %_tempNamespace
        if pm.objExists(groupContainer):
            pm.lockNode(groupContainer, lock = False, lockUnpublished = False)
    
        for name in groupNames:
            pm.rename(name[0], name[1])
    
        if pm.objExists(groupContainer):
            pm.lockNode(groupContainer, lock = True, lockUnpublished = True)
    
    
        return groupNames
    
    
    
    def RenameNamespaces(self, _names):
        
        for name in _names:
            oldName = name[0]
            newName = name[1]
            
            pm.namespace(setNamespace = ":")
            pm.namespace(add = newName)
            pm.namespace(moveNamespace = [oldName, newName])
            pm.namespace(removeNamespace = oldName)
    
    
    def ResolveNameChangeMirrorLinks(self, _names, _tempNamespace):
        
        moduleNamespaces = False
        firstOldNode = _names[0][0]
        
        if utils.StripLeadingNamespace(firstOldNode)[1].find("Group__") == -1:
            moduleNamespaces = True
        
        for n in _names:
            oldNode = n[0]
            
            if moduleNamespaces:
                oldNode += ":module_grp"
            
            if pm.attributeQuery("mirrorLinks", node = oldNode, exists = True):
                mirrorLink = pm.getAttr("%s.mirrorLinks" %oldNode)
                mirrorLinkInfo = mirrorLink.rpartition("__")

                mirrorNode = mirrorLinkInfo[0]
                mirrorAxis = mirrorLinkInfo[2]
                
                found = False
                container = ""
                
                if moduleNamespaces:
                    oldNodeNamespace = n[0]
                    container = "%s:module_container" %oldNodeNamespace
                else:
                    container = "%s:Group_container" %_tempNamespace
                
                for nm in _names:
                    oldLink = nm[0].partition("%s:" %_tempNamespace)[2]
                    
                    if oldLink == mirrorNode:
                        newLink = nm[1]
                        
                        if pm.objExists(container):
                            pm.lockNode(container, lock = False, lockUnpublished = False)
                        
                        pm.setAttr("%s.mirrorLinks" %oldNode, "%s__%s" %(newLink, mirrorAxis), type = "string")
                        
                        if pm.objExists(container):
                            pm.lockNode(container, lock = True, lockUnpublished = True)
                        
                        found = True
                        break
                
                if not found:
                    if pm.objExists(container):
                        pm.lockNode(container, lock = False, lockUnpublished = False)
                    
                    pm.deleteAttr(oldNode, attribute = "mirrorLinks")
                    
                    if pm.objExists(container):
                        pm.lockNode(container, lock = True, lockUnpublished = True)
    
    
    def DuplicateModule(self, *args):
        
        modules = set([])
        groups = set([])
        
        selection = pm.ls(selection = True, transforms = True)
        
        if len(selection) == 0:
            return
        
        for node in selection:
            selectionNamespaceInfo = utils.StripLeadingNamespace(node)
            
            if selectionNamespaceInfo != None:
                if selectionNamespaceInfo[0].find("__") != -1:
                    modules.add(selectionNamespaceInfo[0])
            
            else:
                if node.find("Group__") == 0:
                    groups.add(node)
        
        
        for group in groups:
            moduleInfo = self.DuplicateModule_processGroup(group)
            
            for module in moduleInfo:
                modules.add(module)
        
        
        if len(groups) > 0:
            groupSelection = list(groups)
            pm.select(groupSelection, replace = True)
        
        else:
            pm.select(clear = True)
        
        
        for module in modules:
            pm.select("%s:module_container" %module, add = True)
        
        
        if len(groups) > 0:
            pm.lockNode("Group_container", lock = False, lockUnpublished = True)
        
        elif len(modules) == 0:
            return
        
        
        duplicateFileName = "%s/__duplicateCache.ma" %os.environ["RIGGING_TOOL_ROOT"]
        pm.exportSelected(duplicateFileName, type = "mayaAscii", force = True)
        
        if len(groups) > 0:
            pm.lockNode("Group_container", lock = True, lockUnpublished = True)
        
        
        self.InstallDuplicate(duplicateFileName, selection)
        
        pm.setToolTo("moveSuperContext")
    
    
    def InstallDuplicate(self, _duplicatePath, _selection, *args):
        pm.importFile(_duplicatePath, namespace = "TEMPLATE_1")
        
        moduleNames = self.ResolveNamespaceClashes("TEMPLATE_1")
        groupNames = self.ResolveGroupNameClashes("TEMPLATE_1")
        
        groups = []
        for name in groupNames:
            groups.append(name[1])
        
        if len(groups) > 0:
            sceneGroupContainer = "Group_container"
            pm.lockNode(sceneGroupContainer, lock = False, lockUnpublished = False)
            
            utils.AddNodeToContainer(sceneGroupContainer, groups, _includeShapes = True, _force = True)
            
            for group in groups:
                groupNiceName = group.partition("__")[2]
                pm.container(sceneGroupContainer, edit = True, publishAndBind = ["%s.translate" %group, "%s_t" %groupNiceName])
                pm.container(sceneGroupContainer, edit = True, publishAndBind = ["%s.rotate" %group, "%s_r" %groupNiceName])
                pm.container(sceneGroupContainer, edit = True, publishAndBind = ["%s.globalScale" %group, "%s_globalScale" %groupNiceName])
            
            pm.lockNode(sceneGroupContainer, lock = True, lockUnpublished = True)
        
        pm.namespace(setNamespace = ":")
        
        pm.namespace(moveNamespace = ("TEMPLATE_1", ":"), force = True)
        pm.namespace(removeNamespace = "TEMPLATE_1")
        
        newSelection = []
        for node in _selection:
            found = False
            
            for group in groupNames:
                oldName = group[0].partition("TEMPLATE_1:")[2]
                newName = group[1]
                
                if node == oldName:
                    newSelection.append(newName)
                    found = True
                    break
            
            if not found:
                nodeNamespaceInfo = utils.StripLeadingNamespace(node)
                
                if nodeNamespaceInfo != None:
                    nodeNamespace = nodeNamespaceInfo[0]
                    nodeName = nodeNamespaceInfo[1]
                    
                    searchName = "TEMPLATE_1:%s" %nodeNamespace
                    
                    for module in moduleNames:
                        if module[0] == searchName:
                            newSelection.append("%s:%s" %(module[1], nodeName))
        
        if len(newSelection) > 0:
            pm.select(newSelection, replace = True)
    
    
    
    def DuplicateModule_processGroup(self, _group):
        
        returnModules = []
        
        children = pm.listRelatives(_group, children = True, type = "transform")
        
        for c in children:
            selectionNamespaceInfo = utils.StripLeadingNamespace(c)
            
            if selectionNamespaceInfo != None:
                returnModules.append(selectionNamespaceInfo[0])
            
            else:
                if c.find("Group__") == 0:
                    returnModules.extend(self.DuplicateModule_processGroup(c))
        
        return returnModules
    
    
    def Publish(self, *args):
        
        result = pm.confirmDialog(messageAlign = "center", title = "Publish Character", message = "The action of publishing cannot be undone. \nAre you sure you wish to continue?", button = ["Accept", "Cancel"], defaultButton = "Accept", cancelButton = "Cancel", dismissString = "Cancel")
        
        if result != "Accept":
            return
        
        # Name character to be published
        result = pm.promptDialog(title = "Publish Character", message = "Please specify a character name ([a-z][A-Z][0-9] and _ only)", button = ["Accept", "Cancel"], defaultButton = "Accept", cancelButton = "Cancel", dismissString = "Cancel")
        if result == "Accept":
            
            characterName = pm.promptDialog(query = True, text = True)
            characterFileName = "%s/Characters/%s.ma" %(os.environ["RIGGING_TOOL_ROOT"], characterName)
            
            if os.path.exists(characterFileName):
                pm.confirmDialog(title = "Publish Character", message = "Character already exists with that name. Aborting publish.", button = ["Accept"], defaultButton = "Accept")
                return
            
            pm.lockNode("Scene_Locked", lock = False, lockUnpublished = False)
            pm.delete("Scene_Locked")
            
            pm.namespace(setNamespace = ":")
            namespaces = pm.namespaceInfo(listOnlyNamespaces = True)
            
            # Collect valid module names
            moduleNameInfo = utils.FindAllModuleNames("/Modules/Blueprint")
            validModules = moduleNameInfo[0]
            validModuleNames = moduleNameInfo[1]
            
            # Compare module(s) for validity
            foundModuleInstances = []
            for n in namespaces:
                splitString = n.partition("__")
                
                if splitString[1] != '':
                    module = splitString[0]
                    
                    if module in validModuleNames:
                        foundModuleInstances.append(n)
            
            
            moduleGroups = []
            moduleContainers = []
            
            # Collect module groups and containers
            for moduleInstance in foundModuleInstances:
                moduleGroups.append("%s:module_grp" %moduleInstance)
                moduleContainers.append("%s:module_container" %moduleInstance)
            
            # Unlock containers
            for container in moduleContainers:
                pm.lockNode(container, lock = False, lockUnpublished = False)
            
            # Group modules together as a character
            characterGroup = pm.group(empty = True, name = "character_grp")
            for group in moduleGroups:
                pm.parent(group, characterGroup, absolute = True)
            
            
            pm.select(characterGroup, replace = True)
            pm.addAttr(attributeType = "bool", defaultValue = 0, keyable = False, longName = "moduleMaintenanceVisibility")
            pm.addAttr(attributeType = "bool", defaultValue = 1, keyable = True, longName = "animationControlVisibility")
            
            invertModuleMaintenanceVisibility = pm.shadingNode("reverse", name = "reverse_moduleMaintenanceVisibility", asUtility = True)
            pm.connectAttr("%s.moduleMaintenanceVisibility" %characterGroup, "%s.inputX" %invertModuleMaintenanceVisibility, force = True)
            
            moduleVisibilityMultiply = pm.shadingNode("multiplyDivide", name = "moduleVisibilityMultiply", asUtility = True)
            pm.connectAttr("%s.outputX" %invertModuleMaintenanceVisibility, "%s.input1X" %moduleVisibilityMultiply)
            pm.connectAttr("%s.animationControlVisibility" %characterGroup, "%s.input2X" %moduleVisibilityMultiply)
            
            # Create a list containing all of the character nodes
            characterNodes = list(moduleContainers)
            for c in (characterGroup, characterGroup, characterGroup):
                characterNodes.append(c)
            
            # Add list to a character container
            characterContainer = pm.container(name = "character_container")
            utils.AddNodeToContainer(characterContainer, characterNodes)
            
            pm.container(characterContainer, edit = True, publishAndBind = ["%s.animationControlVisibility" %characterGroup, "animationControlVisibility"])
            
            # Publish the module containers attributes to the character container
            for container in moduleContainers:
                moduleNamespace = utils.StripLeadingNamespace(container)[0]
                blueprintJointsGrp = "%s:blueprint_joints_grp" %moduleNamespace
                
                pm.connectAttr("%s.moduleMaintenanceVisibility" %characterGroup, "%s.visibility" %blueprintJointsGrp)
                pm.setAttr("%s.overrideEnabled" %blueprintJointsGrp, 1)
                
                publishedNames = pm.container(container, query = True, publishName = True)
                userSpecifiedName = moduleNamespace.partition("__")[2]
                
                for name in publishedNames:
                    pm.container(characterContainer, edit = True, publishAndBind = ["%s.%s" %(container, name), "%s_%s" %(userSpecifiedName, name)])
            
            
            characterContainers = list(moduleContainers)
            characterContainers.append(characterContainer)
            
            # Select top level transforms in scene
            pm.select(all = True)
            topLevelTransforms = pm.ls(selection = True, transforms = True)
            pm.select(clear = True)
            
            topLevelTransforms.remove(characterGroup)
            
            # Create visibility attributes and add to character container
            if len(topLevelTransforms) != 0:
                nonBlueprintGroup = pm.group(topLevelTransforms, absolute = True, parent = characterGroup, name = "non_blueprint_grp")
                pm.setAttr("%s.overrideEnabled" %nonBlueprintGroup, 1)
                pm.setAttr("%s.overrideDisplayType" %nonBlueprintGroup, 2) # Reference display type
                
                pm.select(nonBlueprintGroup, replace = True)
                pm.addAttr(attributeType = "bool", defaultValue = 1, longName = "display", keyable = True)
                
                visibilityMultiply = pm.shadingNode("multiplyDivide", name = "non_blueprint_visibilityMultiply", asUtility = True)
                pm.connectAttr("%s.outputX" %invertModuleMaintenanceVisibility, "%s.input1X" %visibilityMultiply, force = True)
                pm.connectAttr("%s.display" %nonBlueprintGroup, "%s.input2X" %visibilityMultiply, force = True)
                pm.connectAttr("%s.outputX" %visibilityMultiply, "%s.visibility" %nonBlueprintGroup, force = True)
                
                nonBlueprintContainer = pm.container(addNode = nonBlueprintGroup, includeHierarchyBelow = True, includeNetwork = True, includeShapes = True, name = "non_blueprint_container")
                utils.AddNodeToContainer(characterContainer, nonBlueprintContainer)
                characterContainers.append(nonBlueprintContainer)
                
                publishedName = "displayNonBlueprintNodes"
                pm.container(nonBlueprintContainer, edit = True, publishAndBind = ["%s.display" %nonBlueprintGroup, publishedName])
                pm.container(characterContainer, edit = True, publishAndBind = ["%s.%s" %(nonBlueprintContainer, publishedName), publishedName])
            
            # Lock character container
            for container in characterContainers:
                pm.lockNode(container, lock = True, lockUnpublished = True)
            
            
            # Export character as a .ma file
            pm.select(characterContainer, replace = True)
            pm.exportSelected(characterFileName, type = "mayaAscii")
            
            # Create locator to mark scene as published
            scenePublished = pm.spaceLocator(name = "Scene_Published")
            pm.setAttr("%s.visibility" %scenePublished, 0)
            pm.lockNode(scenePublished, lock = True, lockUnpublished = True)
            
            
            pm.select(clear = True)
            
            pm.button(self.UIElements["publishBtn"], edit = True, enable = False)