"""
Description
    Samples on JSON config import and export

    - How to export a configuration into a JSON format file.
    - How to import/load a JSON config file.

    How to import JSON data object.
        (This does not write to the JSON config file. This imports the data object.)
        - How to use XPATH to modify IxNetwork configurations.
        - How to modify multiple configurations simultaneously.
        - How to add a new Traffic Item by importing just the code fragments object.

    How to write modifications on the JSON config file:
        - How to modify configurations using dictionary style.
        - How to write modications to the JSON config file.
        - How to add additional configurations to a JSON config file:
            - Such as adding additional Traffic Items.

Instructions
    - Uncomment out the topic area one at a time to try each out.
    - To view the actual ReST APIs and steps, view the functions inside
      the file IxNetRestApi.py.

Requirements
    IxNetRestApi.py
    An Exported JSON configuration file
"""

import sys, traceback, time

sys.path.insert(0, '../Modules/Main')
from IxNetRestApi import *
from IxNetRestApiFileMgmt import FileMgmt

# The path to your exported JSON config file:
jsonConfigFile = 'bgpSimplified.json'
exportJsonConfigFile = '/home/hgee/exportedJsonConfig.json'

try:
    restObj = Connect(apiServerIp='192.168.70.3', serverIpPort='11009')
    fileMgmtObj = FileMgmt(restObj)

    # How to export a configuration into a JSON format file.
    #    This will export your current configuration into a specified json filename.
    fileMgmtObj.exportJsonConfigFile(jsonFileName=exportJsonConfigFile)

    # How to load a complete json config file
    fileMgmtObj.importJsonConfigFile(jsonConfigFile, type='newConfig')


    # Read a JSON config file and store all the datas into an object.
    # Use the jsonData object to make your modifications.
    jsonData = fileMgmtObj.jsonReadConfig(exportJsonConfigFile)


    # How to use XPATH to modify IxNetwork configurations.
    xpathObj = [{"xpath": "/multivalue[@source = '/topology[1]/deviceGroup[1]/ethernet[1]/ipv4[1]/bgpIpv4Peer[1] flap']/singleValue",
                 "value": "true"},
               {"xpath": "/multivalue[@source = '/topology[1]/deviceGroup[1]/ethernet[1]/ipv4[1]/bgpIpv4Peer[1] uptimeInSec']/singleValue",
                 "value": "28"},
               {"xpath": "/multivalue[@source = '/topology[1]/deviceGroup[1]/ethernet[1]/ipv4[1]/bgpIpv4Peer[1] downtimeInSec']/singleValue",
                 "value": "68"}
             ]
    fileMgmtObj.importJsonConfigObj(dataObj=xpathObj, type='modify')


    # How to add a new Traffic Item without touching the JSON config file.
    #     Assuming that there are two Traffic Items already.
    #     You must know the existing amount of Traffic Items in order to specify the next number.
    jsonData = [{
        "xpath": "/traffic/trafficItem[1]",
        "name": 'New Traffic Item 1'
    }]
    fileMgmtObj.importJsonConfigObj(dataObj=jsonData, type='modify')


    # How to modify multiple configurations simultaneously:
    jsonData = [{
        "xpath": "/traffic/trafficItem[1]",
        "name": 'New Traffic Item 1'
    },
    {
        "xpath": "/topology[1]",
        "name": 'New Topology 1'
    }]
    fileMgmtObj.importJsonConfigObj(dataObj=jsonData, type='modify')


    # How to write the modication to the JSON config file.
    fileMgmtObj.jsonWriteToFile(jsonData, jsonConfigFile)


    # How to add additional configurations to a JSON config file:
    #    This example shows how to add additional Traffic Item.
    #    This method applies to all other configurations.
    #       1> Get a copy of an existing Traffic Item in the list.
    #       2> Replace the XPATH ID with the next incremental ID.
    #       3> Append the copied codes to the Traffic Item list.
    #       4> Write to the JSON config file.
    currentTotalTrafficItems = len(jsonData['traffic']['trafficItem'])
    copy = jsonData["traffic"]["trafficItem"][0]
    copy['xpath'] = '/traffic/trafficItem[%s]' % str(currentTotalTrafficItems+1)
    jsonData["traffic"]["trafficItem"].append(copy)
    fileMgmtObj.jsonWriteToFile(jsonData, jsonConfigFile)


except (IxNetRestApiException, Exception, KeyboardInterrupt) as errMsg:
    print('\nTest failed! {0}\n'.format(traceback.print_exc()))
    print(errMsg)
