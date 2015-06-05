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
        
        self.UIElements["topLevelColumn"] = pm.columnLayout(adjustableColumn = True, columnAlign = "center")
        
        # setup tabs
        tabHeight = 500
        self.UIElements["tabs"] = pm.tabLayout(width = windowWidth, height = tabHeight, innerMarginWidth = 5, innerMarginHeight = 5)
        
        tabWidth = pm.tabLayout(self.UIElements["tabs"], query = True, width = True)
        self.scrollWidth = tabWidth - 40
        
        self.InitializeModuleTab(tabWidth, tabHeight)
        
        pm.tabLayout(self.UIElements["tabs"], edit = True, tabLabelIndex = ([1, 'Modules']) )
        
        # Display window
        pm.showWindow(self.UIElements["window"])
    
    
    
    def InitializeModuleTab(self, _tabWidth, _tabHeight):
        
        scrollHeight = _tabHeight
        
        self.UIElements["moduleColumn"] = pm.columnLayout(adjustableColumn = True, rowSpacing = 3)
        
        self.UIElements["moduleFrameLayout"] = pm.frameLayout(height = scrollHeight, collapsable = False, borderVisible = False, labelVisible = False)
        
        self.UIElements["moduleList_scroll"] = pm.scrollLayout(hst = 0)
        
        self.UIElements["moduleList_column"] = pm.columnLayout(columnWidth = self.scrollWidth, adjustableColumn = True, rowSpacing = 2)
        
        
        # first separator
        pm.separator(style = 'in', parent = self.UIElements["moduleList_column"])
        
        for module in utils.FindAllModules("Modules/Blueprint"):
            self.CreateModuleInstallButton(module)
            pm.separator(style = 'in', parent = self.UIElements["moduleList_column"])
    
    
    
    
    def CreateModuleInstallButton(self, _module):
        
        mod = __import__("Blueprint.%s" %_module, (), (), [_module])
        reload(mod)
        
        title = mod.TITLE
        description = mod.DESCRIPTION
        icon = mod.ICON
        
        # Create UI
        buttonSize = 64
        row = pm.rowLayout(numberOfColumns = 2, columnWidth = ([1, buttonSize]), adjustableColumn = 2, columnAttach = ([1, 'both', 0], [2, 'both', 5]), parent = self.UIElements["moduleList_column"])
        
        self.UIElements["module_button_%s" %_module] = pm.symbolButton(width = buttonSize, height = buttonSize, image = icon, command = partial(self.InstallModule, _module))
        
        textColumn = pm.columnLayout(columnAlign = "center")
        pm.text(align = "center", width = self.scrollWidth - buttonSize - 16, label = title)
        
        pm.scrollField(text = description, editable = False, width = self.scrollWidth - buttonSize - 16, height = buttonSize + 16, wordWrap = True, parent = self.UIElements["moduleList_column"])
    
    
    
    def InstallModule(self, _module, *args):
        
        basename = "instance_"
        
        pm.namespace(setNamespace = ':')
        namespaces = pm.namespaceInfo(listOnlyNamespaces = True)
        
        
        for i in range(len(namespaces)):
            if namespaces[i].find("__") != -1:
                namespaces[i] = namespaces[i].rpartition("__")[2]
        
        
        newSuffix = utils.FindHighestTrailingNumber(namespaces, basename) + 1
        
        userSpecName = basename + str(newSuffix)
        
        
        mod = __import__("Blueprint.%s" %_module, (), (), [_module])
        reload(mod)
        
        moduleClass = getattr(mod, mod.CLASS_NAME)
        moduleInstance = moduleClass(userSpecName)
        
        moduleInstance.Install()