"""
Description

    This script converts .ixncfg configurations to a JSON config file:

    - All converted filenames are the same names as the original .ixncfg config file with the .json extension.
    - All converted JSON config files are stored in the user defined variable destinationPath.
    - You provide a list of folders containing .ixncfg config files and this script will convert all .ixncfg
      config files in it.
    - You could also provide a list of .ixncfg config files including its path.

    This script could connect to any IxNetwork API servers: Windows or Linux.

        1> It will load each .ixncfg file (Takes approximately a minute to load).
        2> Verify port state because by default after loading a config file, the ports are rebooting.
        3> If ports are not assigned, then the port verification will be skipped.
        4> Export the loaded configuration to a JSON config file.

Variables
    
    destinationPath: The location to store all the converted .json config files

    ixncfgFolder: Provide a list of all the folders with .ixncfg config files.
                  This script will automatically convert all .ixncfg in each folder.
                  Leave variable empty if none.

    ixncfgFiles:  Provide a list of all the .ixncfg files including its path.
                  Leave variable empty if none.

Requirements:
    (This script uses ReST APIs)
    - Written in Python3 and supports Python2
    - The Python "requests" module for ReST API executions.
    - IxNetwork API server.  Chassis and ports are not required.
    - IxNetRestApi* modules in the ../Modules directory.

Usage

    You must set the above variables.

    Command line execution:
        python convertIxncfgToJson or ...
        python convertIxncfgToJson linux|windowsConnectionMgr
"""

import sys, glob, traceback

sys.path.insert(0, '../Modules')
from IxNetRestApi import *
from IxNetRestApiFileMgmt import FileMgmt
from IxNetRestApiPortMgmt import PortMgmt

destinationPath = '/home/hgee/Temp/temp2' ;# User needs to replace this
ixncfgFolders = []
ixncfgFiles = []

# Default the API server to either windows or linux.
connectToApiServer = 'windows'

# For accepting command line parameters: windows or linux
if len(sys.argv) > 1:
    if sys.argv[1] not in ['windows', 'windowsConnectionMgr', 'linux']:
        sys.exit("\nError: %s is not a known option. Choices are 'windows', 'windowsConnectionMgr or 'linux'." % sys.argv[1])
    connectToApiServer = sys.argv[1]

def convertFile():
    ixncfgFileName = eachIxncfgFile.split('/')[-1].split('.')[0]
    exportJsonFilename = ixncfgFileName+'.json'
    fileMgmtObj.loadConfigFile(eachIxncfgFile)
    portObj.verifyPortState()
    fileMgmtObj.exportJsonConfigFile(jsonFileName=destinationPath+'/'+exportJsonFilename)

try:
    #---------- Preference Settings --------------
    enableDebugTracing = True
    deleteSessionAfterTest = True

    if connectToApiServer == 'linux':
        mainObj = Connect(apiServerIp='192.168.70.108',
                                serverIpPort='443',
                                username='admin',
                                password='admin',
                                deleteSessionAfterTest=deleteSessionAfterTest,
                                verifySslCert=False,
                                serverOs='linux')

    if connectToApiServer in ['windows', 'windowsConnectionMgr']:
        mainObj = Connect(apiServerIp='192.168.70.3',
                                serverIpPort='11009',
                                serverOs=connectToApiServer,
                                deleteSessionAfterTest=deleteSessionAfterTest)

    #---------- Preference Settings End --------------

    portObj = PortMgmt(mainObj)
    fileMgmtObj = FileMgmt(mainObj)
    folderNotExists = []
    fileNotExists = []

    if destinationPath == '' or destinationPath == None:
        raise IxNetRestApiException('\nError: You must provide a destination path to store the converted JSON config files.\n')

    if os.path.exists(destinationPath) == False:
        raise IxNetRestApiException('\nError: The destinationPath does not exists: {0}'.format(destinationPath))

    if ixncfgFiles:
        for eachIxncfgFile in ixncfgFiles:
            if not os.path.exists(eachIxncfgFile):
                fileNotExists.append(eachIxncfgFile)
            else:
                print('\nLoading ixncfg: {0}'.format(eachIxncfgFile))
                convertFile()

    if ixncfgFolders:
        for eachFolder in ixncfgFolders:
            if not os.path.exists(eachFolder):
                folderNotExists.append(eachFolder)
            else:
                ixncfgFiles = glob.glob(eachFolder+'/*.ixncfg')
                if ixncfgFiles == []:
                    print('\nWarning: No .ixncfg config file in folder: {0}'.format(eachFolder))
                for eachIxncfgFile in ixncfgFiles:
                    print('\nLoading ixncfg: {0}'.format(eachIxncfgFile))
                    convertFile()

    if folderNotExists != []:
        print('\nWarning: Following folders don\'t exists: {0}'.format(folderNotExists))
    if fileNotExists != []:
        print('\nWarning: Following files don\'t exists: {0}'.format(fileNotExists))

except (IxNetRestApiException, Exception, KeyboardInterrupt) as errMsg:
    if enableDebugTracing:
        if not bool(re.search('ConnectionError', traceback.format_exc())):
            print('\n%s' % traceback.format_exc())
    print('\nException Error! %s\n' % errMsg)
    if 'mainObj' in locals() and connectToApiServer == 'linux':
        if deleteSessionAfterTest:
            mainObj.linuxServerStopAndDeleteSession()
    if 'mainObj' in locals() and connectToApiServer in ['windows', 'windowsConnectionMgr']:
        if connectToApiServer == 'windowsConnectionMgr':
            if deleteSessionAfterTest:
                mainObj.deleteSession()

