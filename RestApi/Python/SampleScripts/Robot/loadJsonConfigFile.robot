
# Description
#    Import a saved BGP JSON config file to IxNetwork API server.
#
# Notes
#    This script is the same script as ../SampleScripts/loadJsonConfigFile.py.
#
#    This script uses object oriented programming techniques.  The first thing you see in the *** Test Case *** is 
#    that it will extend the main ${ixnObj} object to all the instantiated classes.
#    The reason is because all the common functions like GET, POST, PATCH, and many more are located in IxNetRestApi.Connect.
#
#    Tested with two back-to-back Ixia ports

*** Settings ***
Documentation  Import a JSON config file to IxNetwork API server that configures BGP in NGPF.
Metadata  Script_Author  Hubert Gee
Metadata  Script_Date    3/10/2018
 
Library  BuiltIn
Library  Collections

# Must add the ../../Modules path to PYTHONPATH.
Library  IxNetRestApi.Connect  ${apiServerIp}  ${apiServerPort}  ${apiServerOs}  WITH NAME  ixnObj
Library  IxNetRestApiPortMgmt.PortMgmt      WITH NAME  portMgmtObj  
Library  IxNetRestApiFileMgmt.FileMgmt      WITH NAME  fileMgmtObj  
Library  IxNetRestApiTraffic.Traffic        WITH NAME  trafficObj
Library  IxNetRestApiProtocol.Protocol      WITH NAME  protocolObj
Library  IxNetRestApiStatistics.Statistics  WITH NAME  statisticObj

*** Variables ***
${jsonConfigFile} =  ../../SampleScripts/bgp.json
${apiServerIp} =  192.168.70.3
${apiServerPort} =  11009
${apiServerOs} =  windows
${forceTakePortOwnership} =  True
${releasePortsWhenDone} =  False
${deleteSessionAfterTest} =  True
${licenseServerIp} =  192.168.70.3
${licenseModel} =  subscription
${licenseTier} =  tier3  

${ixChassisIp} =  192.168.70.11

# Creating a list and nested list
@{port_1_1} =  ${ixChassisIp}  1  1
@{port_2_1} =  ${ixChassisIp}  2  1
@{portList} =  ${port_1_1}  ${port_2_1}


*** Test Cases ***
Load a JSON config file

    # Extending the main ${ixnObj} object to all the instantiated classes
    ${ixnObj} =  ixnObj.getSelfObject
    portMgmtObj.setMainObject   ${ixnObj}
    fileMgmtObj.setMainObject   ${ixnObj}
    protocolObj.setMainObject   ${ixnObj}
    trafficObj.setMainObject    ${ixnObj}   
    statisticObj.setMainObject  ${ixnObj}

    Log To Console  Connecting to chassis ...
    portMgmtObj.ConnectIxChassis  ${ixChassisIp}

    # Verify if ports are available. Take over if forceTakePortOwnership == True
    ${result} =  portMgmtObj.arePortsAvailable  portList=${portList}  raiseException=${False}
    Run Keyword If  ("${result}"!=0) and ("${forceTakePortOwnership}"=="True")  Run Keywords
    ...  portMgmtObj.releasePorts  ${portList}
    ...  AND  portMgmtObj.clearPortOwnership  ${portList}
    ...  ELSE  Fail  Ports are still owned

    ${jsonData} =  fileMgmtObj.jsonReadConfig  ${jsonConfigFile}

    Log To Console  Loading JSON config file to API server
    ${newConfig}  Evaluate  str('newConfig')
    fileMgmtObj.importJsonConfigFile  jsonFileName=${jsonConfigFile}  option=${newConfig}

    Log To Console  Assigning ports
    ${assignPortTimeout} =  Convert To Integer  300
    fileMgmtObj.jsonAssignPorts  ${jsonData}  ${portList}  timeout=${assignPortTimeout}
    portMgmtObj.verifyPortState

    Log To Console  Start all protocols
    protocolObj.startAllProtocols

    Log To Console  Verifying protocol sessions
    protocolObj.verifyArp  ipType=ipv4
    protocolObj.verifyProtocolSessionsUp  protocolViewName=BGP Peer Per Port
    trafficObj.regenerateTrafficItems

    Log To Console  Starting traffic
    trafficObj.startTraffic  

    sleep  10

    Log To Console  Getting stats
    ${stats} =  statisticObj.getStats  viewName=Flow Statistics

    Log To Console  ${stats}

    
