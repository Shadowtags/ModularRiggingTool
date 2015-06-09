import pymel.core as pm
from functools import partial

import System.utils as utils

reload(utils)

class Blueprint_UI:
    
    def __init__(self):
        
        self.moduleInstance = None
        
        # Store UI elements in a dictionary
        self.UIElements = {}
        
        if pm.window("blueprint_UI_window", exists = True):
            pm.deleteUI("blueprint_UI_window")
        
        
        windowWidth = 400
        windowHeight = 598
        
        self.UIElements["window"] = pm.window("blueprint_UI_window", width = windowWidth, height = windowHeight, title = "Blueprint Modue UI", sizeable = False)
        
        self.UIElements["topLevelColumn"] = pm.columnLayout(adjustableColumn = True, columnAlign = "center", parent = self.UIElements["window"])
        
        # setup tabs
        tabHeight = 500
        self.UIElements["tabs"] = pm.tabLayout(width = windowWidth, height = tabHeight, innerMarginWidth = 5, innerMarginHeight = 5, parent = self.UIElements["topLevelColumn"])
        
        tabWidth = pm.tabLayout(self.UIElements["tabs"], query = True, width = True)
        self.scrollWidth = tabWidth - 40
        
        self.InitializeModuleTab(tabWidth, tabHeight)
        
        pm.tabLayout(self.UIElements["tabs"], edit = True, tabLabelIndex = ([1, 'Modules']) )
        
        
        self.UIElements["lockPublishColumn"] = pm.columnLayout(adjustableColumn = True, columnAlign = 'center', rowSpacing = 3, parent = self.UIElements["topLevelColumn"])
        
        pm.separator(style = 'in', parent = self.UIElements["lockPublishColumn"])
        
        self.UIElements["lockBtn"] = pm.button(label = 'Lock', command = self.Lock, parent = self.UIElements["lockPublishColumn"])
        
        pm.separator(style = 'in', parent = self.UIElements["lockPublishColumn"])
        
        self.UIElements["publishBtn"] = pm.button(label = "Publish", parent = self.UIElements["lockPublishColumn"])
        
        
        
        # Display window
        pm.showWindow(self.UIElements["window"])
        
        
        self.CreateScriptJob()
    
    
    
    def CreateScriptJob(self):
        self.jobNum = pm.scriptJob(event = ["SelectionChanged", self.ModifySelected], runOnce = True, parent = self.UIElements["window"])
    
    
    
    def DeleteScriptJob(self):
        pm.scriptJob(kill = self.jobNum)
    
    
    def InitializeModuleTab(self, _tabWidth, _tabHeight):
        
        moduleSpecific_scrollHeight = 120
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
        self.UIElements["rehookBtn"] = pm.button(enable = False, label = "Re-hook", parent = self.UIElements["moduleButtons_rowColumns"])
        self.UIElements["snapRootBtn"] = pm.button(enable = False, label = "Snap Root > Hook", parent = self.UIElements["moduleButtons_rowColumns"])
        self.UIElements["constrainBtn"] = pm.button(enable = False, label = "Constrain Root > Hook", parent = self.UIElements["moduleButtons_rowColumns"])
        
        # Second row of buttons
        self.UIElements["groupSelectedBtn"] = pm.button(label = "Group Selected", parent = self.UIElements["moduleButtons_rowColumns"])
        self.UIElements["ungroupBtn"] = pm.button(enable = False, label = "Ungroup", parent = self.UIElements["moduleButtons_rowColumns"])
        self.UIElements["mirrorModuleBtn"] = pm.button(enable = False, label = "Mirror Module", parent = self.UIElements["moduleButtons_rowColumns"])
        
        # Third row of buttons
        pm.text(label = '', parent = self.UIElements["moduleButtons_rowColumns"])
        self.UIElements["deleteModuleBtn"] = pm.button(enable = False, label = "Delete Module", command = self.DeleteModule, parent = self.UIElements["moduleButtons_rowColumns"])
        self.UIElements["symmetryMoveCheckBox"] = pm.checkBox(enable = True, label = "Symmetry Move", parent = self.UIElements["moduleButtons_rowColumns"])
        
        pm.separator(style = 'in', parent = self.UIElements["moduleColumn"])
        
        
        
        self.UIElements["moduleSpecificRowColumnLayout"] = pm.rowColumnLayout(numberOfRows = 1, rowAttach = [1, 'both', 0], rowHeight = [1, moduleSpecific_scrollHeight], parent = self.UIElements["moduleColumn"])
        self.UIElements["modueSpecific_scroll"] = pm.scrollLayout(width = _tabWidth - 8, horizontalScrollBarThickness = 0, parent = self.UIElements["moduleSpecificRowColumnLayout"])
        self.UIElements["moduleSpecific_column"] = pm.columnLayout(columnWidth = self.scrollWidth, columnAttach = ['both', 5], rowSpacing = 2, parent = self.UIElements["modueSpecific_scroll"])
        
        
        pm.separator(style = 'in', parent = self.UIElements["moduleColumn"])
    
    
    
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
    
    
    def Lock(self, *args):
        
        # Give user warning that locking is permanent
        result = pm.confirmDialog(messageAlign = 'center', title = 'Lock Blueprint', button = ['Accept', 'Cancel'], defaultButton = 'Accept', cancelButton = 'Cancel', dismissString = 'Cancel', message = "The action of locking a character will convert the current blueprint modules to joints. \nThis action cannot be undone. \nModifications to the blueprint system cannot be made after this point. \n\nDo you wish to continue?")
        
        if result != 'Accept':
            return
        
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
        
        
        if len(moduleInfo) == 0:
            pm.confirmDialog(messageAlign = 'center', title = 'Lock Blueprints', message = "There appear to be no blueprint \ninstances in the current scene. \n\nAborting lock.", button = ["Accept"], defaultButton = "Accept")
            return
        
        
        moduleInstances = []
        for module in moduleInfo:
            mod = __import__("Blueprint.%s" %module[0], {}, {}, [module[0]])
            reload(mod)
            
            moduleClass = getattr(mod, mod.CLASS_NAME)
            moduleInst = moduleClass(module[1], None)
            
            moduleInfo = moduleInst.Lock_phase1()
            
            moduleInstances.append((moduleInst, moduleInfo))
        
        
        for module in moduleInstances:
            module[0].Lock_phase2(module[1])
    
    
    
    def ModifySelected(self, *args):
        selectedNodes = pm.ls(selection = True)
        
        if len(selectedNodes) <= 1:
            self.moduleInstance = None
            selectedModuleNamespace = None
            currentModule = None
            
            if len(selectedNodes) == 1:
                lastSelected = selectedNodes[0]
                
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
            
            if selectedModuleNamespace != None:
                controlEnable = True
                userSpecifiedName = selectedModuleNamespace.partition('__')[2]
                
                mod = __import__("Blueprint.%s" %currentModuleFile, {}, {}, [currentModuleFile])
                reload(mod)
                
                
                moduleClass = getattr(mod, mod.CLASS_NAME)
                self.moduleInstance = moduleClass(userSpecifiedName, None)
            
            pm.button(self.UIElements["mirrorModuleBtn"], edit = True, enable = controlEnable)
            
            pm.button(self.UIElements["rehookBtn"], edit = True, enable = controlEnable)
            pm.button(self.UIElements["snapRootBtn"], edit = True, enable = controlEnable)
            pm.button(self.UIElements["constrainBtn"], edit = True, enable = controlEnable)
            
            pm.button(self.UIElements["deleteModuleBtn"], edit = True, enable = controlEnable)
            
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
        self.moduleInstance.Delete()
        
        pm.select(clear = True)
    
    
    def RenameModule(self, *args):
        newName = pm.textField(self.UIElements["moduleName"], query = True, text = True)
        
        self.moduleInstance.RenameModuleInstance(newName)
        
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