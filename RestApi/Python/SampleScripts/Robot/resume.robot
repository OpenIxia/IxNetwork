# https://stackoverflow.com/questions/27603242/how-to-import-and-use-user-defined-classes-in-robot-framework-with-python/27604076

# Description
#    Configure IxNetwork basic L2L3 in NGPF.
#
#    This script is the same script from SampleScripts/l2l3Ngpf.py, but this is written in Robot syntaxes.
#
#    This script uses object oriented programming techniques.  The first thing you see in the *** Test Case *** is 
#    that it will extend the main ${ixnObj} object to all the instantiated classes.
#    The reason is because all the common functions like GET, POST, PATCH, and many more are located in IxNetRestApi.Connect.

*** Settings ***
Documentation  Configure IxNetwork basic L2L3 in NGPF
Metadata  Script_Author  Hubert Gee
Metadata  Script_Date    3/10/2018
 
Library  BuiltIn
Library  Collections

# Robot doesn't like including full path when using Python Classes. Must add path to PYTHONPATH.
Library  IxNetRestApi.Connect  ${apiServerIp}  ${apiServerPort}  ${apiServerOs}  WITH NAME  ixnObj
Library  IxNetRestApiPortMgmt.PortMgmt      WITH NAME  portMgmtObj  
Library  IxNetRestApiTraffic.Traffic        WITH NAME  trafficObj
Library  IxNetRestApiProtocol.Protocol      WITH NAME  protocolObj
Library  IxNetRestApiStatistics.Statistics  WITH NAME  statisticObj

*** Variables ***
${apiServerIp} =  192.168.70.3
${apiServerPort} =  11009
${apiServerOs} =  windows
${forceTakePortOwnership} =  True
${releasePortsWhenDone} =  False
${enableDebugTracing} =  True
${deleteSessionAfterTest} =  True
${licenseIsInChassis} =  False
${licenseServerIp} =  192.168.70.5
@{licenseServerIpList} =  ${licenseServerIp}
${licenseModel} =  subscription
${licenseTier} =  tier3  

${ixChassisIp} =  192.168.70.11

# Creating a list and nested list
@{port_1_1} =  ${ixChassisIp}  1  1
@{port_2_1} =  ${ixChassisIp}  2  1
@{portList} =  ${port_1_1}  ${port_2_1}
@{topology1Port} =  ${port_1_1}
@{topology2Port} =  ${port_2_1}
@{trackBy} =  flowGroup0  

# Create a dictionary
&{ethMacAddr1} =  start=00:01:01:00:00:01  direction=increment  step=00:00:00:00:00:01
&{ethMacAddr2} =  start=00:02:01:00:00:01  direction=increment  step=00:00:00:00:00:01
&{ipv41} =        start=1.1.1.1  direction=increment  step=0.0.0.1
&{ipv42} =        start=1.1.1.2  direction=increment  step=0.0.0.1
&{ipv4Gateway1} =  start=1.1.1.2  direction=increment  step=0.0.0.1
&{ipv4Gateway2} =  start=1.1.1.1  direction=increment  step=0.0.0.1
&{trafficItem1} =  name=Topo1-to-Topo2  trafficType=ipv4  biDirectional=True  srcDestMesh=one-to-one routeMesh=oneToOne  allowSelfDestined=False  trackBy=${trackBy}
&{configElements} =  transmissionType=continuous  frameRate=88  frameRateType=percentLineRate  frameSize=128

*** Test Cases ***
Configuring L2L3 NGPF Protocol stacks

    # Extending the main ${ixnObj} object to all the instantiated classes
    ${ixnObj} =       ixnObj.getSelfObject
    ${portMgmtObj} =  portMgmtObj.getSelfObject
    portMgmtObj.setMainObject    ${ixnObj}
    protocolObj.setMainObject    ${ixnObj}
    trafficObj.setMainObject     ${ixnObj}   
    statisticObj.setMainObject   ${ixnObj}

    #portMgmtObj.connectIxChassis  ${ixChassisIp}

    #${result} =  portMgmtObj.arePortsAvailable  portList=${portList}  raiseException=${False}
    #Run Keyword If  ("${result}"!=0) and ("${forceTakePortOwnership}"=="True")  Run Keywords
    #...  portMgmtObj.releasePorts  ${portList}
    #...  AND  portMgmtObj.clearPortOwnership  ${portList}
    #...  ELSE  Fail  Port are still owned

    #ixnObj.newBlankConfig

    ${value}  Get From Dictionary  ${ethMacAddr1}  start
    Log To Console  value: ${value}
    
    #${port_1_1}  Evaluate  type($port_1_1)
    #Log To Console  type is: ${port_1_1}

    #Run Keyword If  "${licenseIsInChassis}"=="False"  Run Keywords
    #...  portMgmtObj.releasePorts  portList=${portList}
    #...  AND  ixnObj.configLicenseServerDetails  ${licenseServerIpList}  ${licenseModel}  ${licenseTier}
