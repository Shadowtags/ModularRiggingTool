import pymel.core as pm
import System.utils as utils
reload(utils)

class MirrorModule:
    
    def __init__(self):
        
        # Class variables
        self.modules = []
        self.moduleNames = []
        self.moduleInfo = []
        
        self.UIElements = {}
        
        self.group = None
        self.sameMirrorSettingsForAll = False
        
        
        
        selection = pm.ls(selection = True, transforms = True)
        
        if len(selection) == 0:
            return
        
        
        firstSelected = selection[0]
        
        if firstSelected.find("Group__") == 0:
            self.group = firstSelected
            self.modules = self.FindSubModules(firstSelected)
        
        else:
            moduleNamespaceInfo = utils.StripLeadingNamespace(firstSelected)
            
            if moduleNamespaceInfo != None:
                self.modules.append(moduleNamespaceInfo[0])
        
        
        tempModuleList = []
        for module in self.modules:
            if self.IsModuleAMirror(module):
                pm.confirmDialog(title = "Mirror Module(s)", message = "Cannot mirror a previously mirrored module. \nAborting mirror.", button = ["Accept"], defaultButton = "Accept")
                return
            
            if not self.CanModuleBeMirrored(module):
                print 'Module "%s" is of a module type that cannot be mirrored... skipping module.' %module
            
            else:
                tempModuleList.append(module)
        
        self.modules = tempModuleList
        
        if len(self.modules) > 0:
            self.MirrorModule_UI()
    
    
    
    def FindSubModules(self, _group):
        returnModules = []
        
        children = pm.listRelatives(_group, children = True)
        children = pm.ls(children, transforms = True)
        
        for child in children:
            if child.find("Group__") == 0:
                returnModules.extend(self.FindSubModules(child))
            
            else:
                namespaceInfo = utils.StripAllNamespaces(child)
                
                if namespaceInfo != None and namespaceInfo[1] == "module_transform":
                    module = namespaceInfo[0]
                    returnModules.append(module)
        
        return returnModules
    
    
    def IsModuleAMirror(self, _module):
        moduleGroup = "%s:module_grp" %_module
        return pm.attributeQuery("mirrorLinks", node = moduleGroup, exists = True)
    
    
    def CanModuleBeMirrored(self, _module):
        moduleNameInfo = utils.FindAllModuleNames("/Modules/Blueprint")
        validModules = moduleNameInfo[0]
        validModuleNames = moduleNameInfo[1]
        
        moduleName = _module.partition("__")[0]
        
        if not moduleName in validModuleNames:
            return False;
        
        index = validModuleNames.index(moduleName)
        mod = __import__("Blueprint.%s" %validModules[index], {}, {}, validModules[index])
        reload(mod)
        
        moduleClass = getattr(mod, mod.CLASS_NAME)
        moduleInst = moduleClass("null", None)
        
        return moduleInst.CanModuleBeMirrored()
    
    
    def MirrorModule_UI(self):
        
        for module in self.modules:
            self.moduleNames.append(module.partition("__")[2])
        
        if len(self.modules) > 1:
            result = pm.confirmDialog(title = "Mirror Multiple Modules", message = "%d modules selected for mirror. \nHow would you like to apply mirror settings?" %len(self.modules), button = ["Same for All", "Individually", "Cancel"], defaultButton = "Same for All", cancelButton = "Cancel", dismissString = "Cancel")
            
            if result == 'Cancel':
                return
            
            if result == 'Same for All':
                self.sameMirrorSettingsForAll = True
        
        
        # Refresh UI
        if pm.window("mirrorModule_UI_window", exists = True):
            pm.deleteUI("mirrorModule_UI_window")
        
        
        # Create UI
        windowWidth = 300
        windowHeight = 400
        self.UIElements["window"] = pm.window("mirrorModule_UI_window", width = windowWidth, height = windowHeight, title = "Mirror Module(s)", sizeable = False)
        
        self.UIElements["scrollLayout"] = pm.scrollLayout(horizontalScrollBarThickness = 0, parent = self.UIElements["window"])
        self.UIElements["topColumnLayout"] = pm.columnLayout(adjustableColumn = True, rowSpacing = 3, parent = self.UIElements["scrollLayout"])
        
        scrollWidth = windowWidth - 30
        
        mirrorPlane_textWidth = 80
        mirrorPlane_columnWidth = (scrollWidth - mirrorPlane_textWidth) / 3
        
        self.UIElements["mirrorPlane_rowColumn"] = pm.rowColumnLayout(numberOfColumns = 4, columnAttach = (1, 'right', 0), columnWidth = [(1, mirrorPlane_textWidth), (2, mirrorPlane_columnWidth), (3, mirrorPlane_columnWidth), (4, mirrorPlane_columnWidth)], parent = self.UIElements["topColumnLayout"])
        
        pm.text(label = "Mirror Plane: ", parent = self.UIElements["mirrorPlane_rowColumn"])
        
        self.UIElements["mirrorPlane_radioCollection"] = pm.radioCollection(parent = self.UIElements["mirrorPlane_rowColumn"])
        pm.radioButton("XY", label = "XY", select = False)
        pm.radioButton("YZ", label = "YZ", select = True)
        pm.radioButton("XZ", label = "XZ", select = False)
        
        pm.separator(style = 'in', parent = self.UIElements["topColumnLayout"])
        
        pm.text(label = "Mirrored Name(s): ", parent = self.UIElements["topColumnLayout"])
        
        columnWidth = scrollWidth / 2
        self.UIElements["moduleName_rowColumn"] = pm.rowColumnLayout(numberOfColumns = 2, columnAttach = (1, 'right', 0), columnWidth = [(1, columnWidth), (2, columnWidth)], parent = self.UIElements["topColumnLayout"])
        
        for module in self.moduleNames:
            pm.text(label = "%s >> " %module, parent = self.UIElements["moduleName_rowColumn"])
            self.UIElements["moduleName_%s" %module] = pm.textField(enable = True, text = "%s_mirror" %module, parent = self.UIElements["moduleName_rowColumn"])
        
        pm.separator(style = 'in', parent = self.UIElements["topColumnLayout"])
        
        
        if self.sameMirrorSettingsForAll:
            self.GenerateMirrorFunctionControls(None, scrollWidth)
        else:
            for module in self.moduleNames:
                self.GenerateMirrorFunctionControls(module, scrollWidth)
        
        pm.separator(style = 'in', parent = self.UIElements["topColumnLayout"])
        
        
        self.UIElements["button_row"] = pm.rowLayout(numberOfColumns = 2, columnWidth = [(1, columnWidth), (2, columnWidth)], columnAttach = [(1, 'both', 10), (2, 'both', 10)], columnAlign = [(1, 'center'), (2, 'center')], parent = self.UIElements["topColumnLayout"])
        pm.button(label = "Accept", command = self.AcceptWindow, parent = self.UIElements["button_row"])
        pm.button(label = "Cancel", command = self.CancelWindow, parent = self.UIElements["button_row"])
        
        
        pm.showWindow(self.UIElements["window"])
    
    
    
    def GenerateMirrorFunctionControls(self, _moduleName, _scrollWidth):
        
        rotationRadioCollection = "rotation_radioCollection_all"
        translationRadioCollection = "translation_radioCollection_all"
        textLabel = "Mirror Settings:"
        
        behaviourName = "behaviour__"
        orientationName = "orientation__"
        mirroredName = "mirrored__"
        worldSpaceName = "worldSpace__"
        mirrorRowColumn = "mirrorFunctionRowColumn__"
        
        if _moduleName != None:
            rotationRadioCollection = "rotation_radioCollection_%s" %_moduleName
            translationRadioCollection = "translation_radioCollection_%s" %_moduleName
            textLabel = "%s Mirror Settings:" %_moduleName
            mirrorRowColumn = "mirrorFunctionRowColumn__%s" %_moduleName
            
            behaviourName = "behaviour__%s" %_moduleName
            orientationName = "orientation__%s" %_moduleName
            mirroredName = "mirrored__%s" %_moduleName
            worldSpaceName = "worldSpace__%s" %_moduleName
        
        pm.text(label = textLabel, parent = self.UIElements["topColumnLayout"])
        
        mirrorSettings_textWidth = 80
        mirrorSettings_columnWidth = (_scrollWidth - mirrorSettings_textWidth) / 2
        
        pm.rowColumnLayout(mirrorRowColumn, numberOfColumns = 3, columnAttach = (1, 'right', 0), columnWidth = [(1, mirrorSettings_textWidth), (2, mirrorSettings_columnWidth), (3, mirrorSettings_columnWidth)], parent = self.UIElements["topColumnLayout"])
        
        pm.text(label = "Rotation: ", parent = mirrorRowColumn)
        
        self.UIElements[rotationRadioCollection] = pm.radioCollection(parent = mirrorRowColumn)
        pm.radioButton(behaviourName, label = "Behaviour", select = True)
        pm.radioButton(orientationName, label = "orientation", select = False)
        
        pm.text(label = "Translation: ", parent = mirrorRowColumn)
        
        self.UIElements[translationRadioCollection] = pm.radioCollection(parent = mirrorRowColumn)
        pm.radioButton(mirroredName, label = "Mirrored", select = True)
        pm.radioButton(worldSpaceName, label = "World Space", select = False)
        
        pm.text(label = '')
    
    
    def CancelWindow(self, *args):
        pm.deleteUI(self.UIElements["window"])
    
        
    def AcceptWindow(self, *args):
        
        # a moduleInf entry = (originalModuleName, mirroredModuleName, mirrorPlane, rotationFunction, translationFunction)
        
        self.mirrorPlane = pm.radioCollection(self.UIElements["mirrorPlane_radioCollection"], query = True, select = True)
        
        for i in range(len(self.modules)):
            originalModule = self.modules[i]
            originalModuleName = self.moduleNames[i]
            
            originalModulePrefix = originalModule.partition("__")[0]
            mirroredModuleUserSpecifiedName = pm.textField(self.UIElements["moduleName_%s" %originalModuleName], query = True, text = True)
            mirroredModuleName = "%s__%s" %(originalModulePrefix, mirroredModuleUserSpecifiedName)
            
            # Catch name conflicts
            if utils.DoesBlueprintUserSpecifiedNameExist(mirroredModuleUserSpecifiedName):
                pm.confirmDialog(title = "Name Conflict", message = 'Name "%s" already exists. \nAborting mirror.' %mirroredModuleUserSpecifiedName, button = ["Accept"], defaultButton = "Accept")
                return
            
            
            rotationFunction = ''
            translationFunction = ''
            
            if self.sameMirrorSettingsForAll == True:
                rotationFunction = pm.radioCollection(self.UIElements["rotation_radioCollection_all"], query = True, select = True)
                translationFunction = pm.radioCollection(self.UIElements["translation_radioCollection_all"], query = True, select = True)
            
            else:
                rotationFunction = pm.radioCollection(self.UIElements["rotation_radioCollection_%s" %originalModuleName], query = True, select = True)
                translationFunction = pm.radioCollection(self.UIElements["translation_radioCollection_%s" %originalModuleName], query = True, select = True)
            
            
            rotationFunction = rotationFunction.partition("__")[0]
            translationFunction = translationFunction.partition("__")[0]
            
            self.moduleInfo.append([originalModule, mirroredModuleName, self.mirrorPlane, rotationFunction, translationFunction])
        
        
        pm.deleteUI(self.UIElements["window"])
        
        
        self.MirrorModules()
    
    
    
    def MirrorModules(self):
        mirrorModulesProgress_UI = pm.progressWindow(title = "Mirror Module(s)", status = "This may take a few minutes...", isInterruptable = False)
        mirrorModulesProgress = 0
        
        mirrorModulesProgress_stage1_proportion = 15
        mirrorModulesProgress_stage2_proportion = 70
        mirrorModulesProgress_stage3_proportion = 10
        
        moduleNameInfo = utils.FindAllModuleNames("/Modules/Blueprint")
        validModules = moduleNameInfo[0]
        validModuleNames = moduleNameInfo[1]
        
        for module in self.moduleInfo:
            moduleName = module[0].partition("__")[0]
            
            if moduleName in validModuleNames:
                index = validModuleNames.index(moduleName)
                module.append(validModules[index])
        
        
        # COLLECT DATA FOR MIRRORING
        mirrorModulesProgress_progressIncrement = mirrorModulesProgress_stage1_proportion / len(self.moduleInfo)
        for module in self.moduleInfo:
            userSpecifiedName = module[0].partition("__")[2]
            
            mod = __import__("Blueprint.%s" %module[5], {}, {}, [module[5]])
            reload(mod)
            
            moduleClass = getattr(mod, mod.CLASS_NAME)
            moduleInst = moduleClass(userSpecifiedName, None)
            
            hookObject = moduleInst.FindHookObject()
            
            newHookObject = None
            hookModule = utils.StripLeadingNamespace(hookObject)[0]
            
            hookFound = False
            for m in self.moduleInfo:
                if hookModule == m[0]:
                    hookFound = True
                    
                    if m == module:
                        continue
                    
                    hookObjectName = utils.StripLeadingNamespace(hookObject)[1]
                    newHookObject = "%s:%s" %(m[1], hookObjectName)
            
            if not hookFound:
                newHookObject = hookObject
            
            module.append(newHookObject)
            
            hookConstrained = moduleInst.IsRootConstrained()
            module.append(hookConstrained)
            
            
            # Increment progress bar
            mirrorModulesProgress += mirrorModulesProgress_progressIncrement
            pm.progressWindow(mirrorModulesProgress_UI, edit = True, progress = mirrorModulesProgress)
        
        
        
        
        # MIRROR MODULE
        mirrorModulesProgress_progressIncrement = mirrorModulesProgress_stage2_proportion / len(self.moduleInfo)
        for module in self.moduleInfo:
            newUserSpecifiedName = module[1].partition("__")[2]
            
            mod = __import__("Blueprint.%s" %module[5], {}, {}, [module[5]])
            reload(mod)
        
            moduleClass = getattr(mod, mod.CLASS_NAME)
            moduleInst = moduleClass(newUserSpecifiedName, None)
            
            moduleInst.Mirror(module[0], module[2], module[3], module[4])
            
            # Increment progress bar
            mirrorModulesProgress += mirrorModulesProgress_progressIncrement
            pm.progressWindow(mirrorModulesProgress_UI, edit = True, progress = mirrorModulesProgress)
        
        
        
        
        # MIRROR HOOKED RELATIONS
        mirrorModulesProgress_progressIncrement = mirrorModulesProgress_stage3_proportion / len (self.moduleInfo)
        for module in self.moduleInfo:
            newUserSpecifiedName = module[1].partition("__")[2]
            
            mod = __import__("Blueprint.%s" %module[5], {}, {}, [module[5]])
            reload(mod)
            
            moduleClass = getattr(mod, mod.CLASS_NAME)
            moduleInst = moduleClass(newUserSpecifiedName, None)
            
            moduleInst.Rehook(module[6])
            
            hookConstrained = module[7]
            if hookConstrained:
                moduleInst.ConstrainRootToHook()
            
            mirrorModulesProgress += mirrorModulesProgress_progressIncrement
            pm.progressWindow(mirrorModulesProgress_UI, edit = True, progress = mirrorModulesProgress)
        
        
        
        if self.group != None:
            pm.lockNode("Group_container", lock = False, lockUnpublished = False)
            
            groupParent = pm.listRelatives(self.group, parent = True)
            
            if groupParent != []:
                groupParent = groupParent = [0]
            
            self.ProcessGroup(self.group, groupParent)
            
            pm.lockNode("Group_container", lock = True, lockUnpublished = True)
            
            pm.select(clear = True)
        
        
        pm.progressWindow(mirrorModulesProgress_UI, edit = True, endProgress = True)
        
        utils.ForceSceneUpdate()
    
    
    def ProcessGroup(self, _group, _groupParent):
        
        import System.groupSelected as groupSelected
        reload(groupSelected)
        
        tempGroup = pm.duplicate(_group, parentOnly = True, inputConnections = True)[0]
        emptyGroup = pm.group(empty = True)
        pm.parent(tempGroup, emptyGroup, absolute = True)
        
        scaleAxis = ".scaleX"
        if self.mirrorPlane == "XZ":
            scaleAxis = ".scaleY"
        elif self.mirrorPlane == "XY":
            scaleAxis = ".scaleZ"
        
        pm.setAttr("%s%s" %(emptyGroup, scaleAxis), -1)
        
        instance = groupSelected.GroupSelected()
        groupSuffix = _group.partition("__")[2]
        newGroup = instance.CreateGroupAtSpecified("%s_mirror" %groupSuffix, tempGroup, _groupParent)
        
        pm.lockNode("Group_container", lock = False, lockUnpublished = False)
        pm.delete(emptyGroup)
        
        for moduleLink in ( (_group, newGroup), (newGroup, _group) ):
            attributeValue = "%s__" %moduleLink[1]
            
            if self.mirrorPlane == "YZ":
                attributeValue += "X"
            elif self.mirrorPlane == "XZ":
                attributeValue += "Y"
            elif self.mirrorPlane == "XY":
                attributeValue += "Z"
        
            pm.select(moduleLink[0], replace = True)
        
            pm.addAttr(dataType = "string", longName = "mirrorLinks", keyable = False)
            pm.setAttr("%s.mirrorLinks" %moduleLink[0], attributeValue, type = "string")
        
        pm.select(clear = True)
        
        children = pm.listRelatives(_group, children = True)
        children = pm.ls(children, transforms = True)
        
        # Recursively process group heirarchy
        for child in children:
            if child.find("Group__") == 0:
                self.ProcessGroup(child, newGroup)
            else:
                childNamespaces = utils.StripAllNamespaces(child)
                
                if childNamespaces != None and childNamespaces[1] == "module_transform":
                    for module in self.moduleInfo:
                        if childNamespaces[0] == module[0]:
                            moduleContainer = "%s:module_container" %module[1]
                            pm.lockNode(moduleContainer, lock = False, lockUnpublished = False)
                            
                            moduleTransform = "%s:module_transform" %module[1]
                            pm.parent(moduleTransform, newGroup, absolute = True)
                            
                            pm.lockNode(moduleContainer, lock = True, lockUnpublished = True)