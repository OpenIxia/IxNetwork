
*** Settings ***
Documentation  Load a saved configuration file
 
Library  BuiltIn
Library  Collections

Library  rtpKeywords.py

*** Variables ***
${apiServerIp} =  192.168.70.3
${apiServerPort} =  11009
${apiServerOs} =  windows
${ixChassisIp} =  192.168.70.11
${bgpConfigFile} =  /home/hgee/Dropbox/MyIxiaWork/OpenIxiaGit/IxNetwork/RestApi/Python/SampleScripts/bgp_ngpf_8.30.ixncfg

*** Test Cases ***
Load Config

     Ixia Connect To Rest Server  ${apiServerIp}  ${apiServerPort}  ${ixChassisIp}
     Ixia Load Config  ${bgpConfigFile}
     Ixia Start Protocols
     Ixia Start Traffic
