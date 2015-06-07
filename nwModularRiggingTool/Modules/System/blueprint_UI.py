import pymel.core as pm
from functools import partial

import System.utils as utils

reload(utils)

class Blueprint_UI:
    
    def __init__(self):
        
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
        
        self.UIElements["lockBtn"] = pm.button(label = 'Lock', parent = self.UIElements["lockPublishColumn"])
        
        pm.separator(style = 'in', parent = self.UIElements["lockPublishColumn"])
        
        self.UIElements["publishBtn"] = pm.button(label = "Publish", parent = self.UIElements["lockPublishColumn"])
        
        
        
        # Display window
        pm.showWindow(self.UIElements["window"])
    
    
    
    def InitializeModuleTab(self, _tabWidth, _tabHeight):
        
        scrollHeight = _tabHeight - 150
        
        self.UIElements["moduleColumn"] = pm.columnLayout(adjustableColumn = True, rowSpacing = 3, parent = self.UIElements["tabs"])
        
        self.UIElements["moduleFrameLayout"] = pm.frameLayout(height = scrollHeight, collapsable = False, borderVisible = False, labelVisible = False, parent = self.UIElements["moduleColumn"])
        
        self.UIElements["moduleList_scroll"] = pm.scrollLayout(hst = 0, parent = self.UIElements["moduleFrameLayout"])
        
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
        self.UIElements["moduleName"] = pm.textField(enable = False, alwaysInvokeEnterCommandOnReturn = True, parent = self.UIElements["moduleName_row"])
        
        
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
        self.UIElements["deleteModuleBtn"] = pm.button(enable = False, label = "Delete Module", parent = self.UIElements["moduleButtons_rowColumns"])
        self.UIElements["symmetryMoveCheckBox"] = pm.checkBox(enable = True, label = "Symmetry Move", parent = self.UIElements["moduleButtons_rowColumns"])
        
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
        
        # Import our module
        mod = __import__("Blueprint.%s" %_module, (), (), [_module])
        reload(mod)
        
        moduleClass = getattr(mod, mod.CLASS_NAME)
        moduleInstance = moduleClass(userSpecName)
        moduleInstance.Install()
        
        # After installation of module, select module transform with move tool
        moduleTranform = "%s__%s:module_transform" %(mod.CLASS_NAME, userSpecName)
        pm.select(moduleTranform, replace = True)
        pm.setToolTo("moveSuperContext")