def FindAllModules(_relativeDirectory):
    
    # Search the relative directory for all available modules
    # Return a list of all module names (excluding the ".py" extension)
    returnModules = []
    
    
    allPyFiles = FindAllFiles(_relativeDirectory, ".py")
    
    for f in allPyFiles:
        if f != "__init__":
            returnModules.append(f)
    
    
    return returnModules
    
    

def FindAllFiles(_relativeDirectory, _fileExtension):
    
    # Search the relative directory for all files with the given extension
    # Return a list of all file names, excluding the file extension
    allFiles = []
    returnFiles = []
    
    import os
    
    fileDirectory = "%s/%s/" %(os.environ["RIGGING_TOOL_ROOT"], _relativeDirectory)
    
    allFiles = os.listdir(fileDirectory)
    
    
    # refine all files, listing only those of the specific file extension
    for f in allFiles:
        splitString = str(f).rpartition(_fileExtension)
        
        if not splitString[1] == '' and splitString[2] == '':
            returnFiles.append(splitString[0])
    
    
    return returnFiles