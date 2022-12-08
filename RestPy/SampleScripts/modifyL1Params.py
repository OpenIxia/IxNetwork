"""
modifyL1Params.py:
    Test Script to modify VPort L1 Parameters
    Tested with two back-2-back Ixia ports...
        - Connect to the API server
    
    Vport L1 Parametes that will be considered for modification in script are
    1. LinkUp/Dowm
    2. LaserOn/Off
    3. Change LoopBack Status
    4. Inserting Local/Remote Faults
    5. Enable Transmit deviation frequency Increments
    
    Config File Used: bgp_ngpf.9.00.ixcnfg (Standard 2 topology BGP NGPF setup)
    Card Used: NovusHundredGigLan
    
    Supports IxNetwork API servers:
    - Windows, Windows Connection Mgr and Linux
    
    Requirements:
    - Minimum IxNetwork 8.50
    - Python 3+
    - pip install requests
    - pip install ixnetwork_restpy (minimum version 1.0.51)
    RestPy Doc:
        https://www.openixia.github.io/ixnetwork_restpy/#/
    Usage:
    - Enter: python <script>
"""

import traceback
from ixnetwork_restpy import SessionAssistant


apiServerIp = '10.36.236.121'

# windows|connection_manager|linux
osPlatform = 'linux'

# For Linux API server only
user='admin'
password='admin'

# Since we can have multiple sessions on Linux based chassis, we need to select a session id/name 
sessionId='12'

# Set to False so as not to clean up and build up session every time the script is run
clearConfig = False

try:

    # Create session object
    session = SessionAssistant(IpAddress=apiServerIp, UserName=user, Password=password,
                                LogLevel=SessionAssistant.LOGLEVEL_INFO,
                                ClearConfig=clearConfig,
                                SessionId=sessionId)
    
    ixNetwork = session.Ixnetwork
    
    # List of Vports available
    
    vportsList = list()

    for vportItem in ixNetwork.Vport.find():
        vportsList.append(vportItem.Name)
    
    # Display vports on topology.
    print(vportsList)
    
    for vportName in vportsList:
        
        vport = ixNetwork.Vport.find(Name = vportName)   
        vport_properties_object = vport.L1Config.find().NovusHundredGigLan.find()
        
        #  ====== 1 LinkUp/Dowm ========
        
        vport.LinkUpDn(Arg2='down')
        print (f"{vportName} turned DOWN")
        vport.LinkUpDn(Arg2='up')
        print (f"{vportName} turned UP")
        
        
        # ====== 2 Laser ON/OFF ========
        
        vport.L1Config.NovusHundredGigLan.LaserOn = False
        print (f"{vportName} Laser ON:  {vport.L1Config.NovusHundredGigLan.LaserOn}")
        vport.L1Config.NovusHundredGigLan.LaserOn = True
        print (f"{vportName} Laser ON:  {vport.L1Config.NovusHundredGigLan.LaserOn}")
        
    
        # ======= 3 Changing Loopbank Status =========
        
        vport_properties_object.LoopbackMode = "internalLoopback" # 3 Options: none | lineLoopback | internalLoopback
        print (f"{vportName} Loopback Mode:  {vport.L1Config.NovusHundredGigLan.LoopbackMode}")
    
        # ====== 4 Inserting Local/Remote Faults ========
    
        # Fault Types: localFault | remoteFault
        vport_properties_object.TypeAOrderedSets = 'localFault'
        vport_properties_object.TypeBOrderedSets = 'remoteFault'
        
        # Send Stats Mode: alternate | typeAOnly | typeBOnly
        vport_properties_object.SendSetsMode = 'typeAOnly' # TypeAOnly means geneate fault only on A side of topo
        vport_properties_object.StartErrorInsertion = True
        
        # ====== 5 Enable Transmit deviation frequency Increments ========
        
        vport_properties_object.EnablePPM = True
        print(f"PPM Enabled: {vport.L1Config.NovusHundredGigLan.EnablePPM}")
        
        vport_properties_object.Ppm = 50 #PPM increment should be > value already set.
        
        print (f"#=========== {vportName} Statistics ==========")
        print( vport.L1Config.NovusHundredGigLan)
        
    
except Exception as errMsg:
    print('\nError: %s' % traceback.format_exc())
    print('\nrestPy.Exception:', errMsg)

    
    
"""Sample Output
    
(ixn-venv) ashwjosh@C0HD4NKHCX IxNetwork % /Users/ashwjosh/AshPro/IxNetwork/ixn-venv/bin/python /Users/ashwjosh/AshPro/IxNetwork/ixn-venv/modifyL1params.py
2022-12-08 19:38:21 [ixnetwork_restpy.connection tid:8603411712] [INFO] using python version 3.11.0 (v3.11.0:deaf509e8f, Oct 24 2022, 14:43:23) [Clang 13.0.0 (clang-1300.0.29.30)]
2022-12-08 19:38:21 [ixnetwork_restpy.connection tid:8603411712] [INFO] using ixnetwork-restpy version 1.1.7
2022-12-08 19:38:21 [ixnetwork_restpy.connection tid:8603411712] [WARNING] Verification of certificates is disabled
2022-12-08 19:38:21 [ixnetwork_restpy.connection tid:8603411712] [INFO] Determining the platform and rest_port using the 10.36.236.121 address...
2022-12-08 19:38:23 [ixnetwork_restpy.connection tid:8603411712] [WARNING] Unable to connect to http://10.36.236.121:11009.
2022-12-08 19:38:25 [ixnetwork_restpy.connection tid:8603411712] [WARNING] Unable to connect to https://10.36.236.121:11009.
2022-12-08 19:38:25 [ixnetwork_restpy.connection tid:8603411712] [WARNING] Unable to connect to http://10.36.236.121:443.
2022-12-08 19:38:25 [ixnetwork_restpy.connection tid:8603411712] [INFO] Connection established to `https://10.36.236.121:443 on linux`
2022-12-08 19:38:26 [ixnetwork_restpy.connection tid:8603411712] [INFO] Using IxNetwork api server version 9.20.2201.33
2022-12-08 19:38:26 [ixnetwork_restpy.connection tid:8603411712] [INFO] User info IxNetwork/ixnetworkweb/admin-12-25826
['Port_1', 'Port_2']
Port_1 turned DOWN
Port_1 turned UP
Port_1 Laser ON:  False
Port_1 Laser ON:  True
Port_1 Loopback Mode:  internalLoopback
PPM Enabled: True
#=========== Port_1 Statistics ==========
NovusHundredGigLan[0]: /api/v1/sessions/12/ixnetwork/vport/1/l1Config/novusHundredGigLan
        AutoInstrumentation: endOfFrame
        AvailableSpeeds: ['speed100g']
        BadBlocksNumber: 4
        CanModifySpeed: False
        CanSetMultipleSpeeds: False
        EnableAutoNegotiation: False
        EnablePPM: True
        EnableRsFec: True
        EnableRsFecStats: True
        EnabledFlowControl: True
        FirecodeAdvertise: False
        FirecodeForceOff: False
        FirecodeForceOn: False
        FirecodeRequest: False
        FlowControlDirectedAddress: 01 80 C2 00 00 01
        ForceDisableFEC: False
        GoodBlocksNumber: 0
        IeeeL1Defaults: True
        LaserOn: True
        LinkTraining: False
        LoopContinuously: True
        LoopCountNumber: 1
        Loopback: True
        LoopbackMode: internalLoopback
        Ppm: 70
        RsFecAdvertise: False
        RsFecForceOn: False
        RsFecRequest: False
        SelectedSpeeds: ['speed100g']
        SendSetsMode: typeAOnly
        Speed: speed100g
        StartErrorInsertion: True
        TxIgnoreRxLinkFaults: False
        TypeAOrderedSets: localFault
        TypeBOrderedSets: remoteFault
        UseANResults: False
        

Port_2 turned DOWN
Port_2 turned UP
Port_2 Laser ON:  False
Port_2 Laser ON:  True
Port_2 Loopback Mode:  internalLoopback
PPM Enabled: True
#=========== Port_2 Statistics ==========
NovusHundredGigLan[0]: /api/v1/sessions/12/ixnetwork/vport/2/l1Config/novusHundredGigLan
        AutoInstrumentation: endOfFrame
        AvailableSpeeds: ['speed100g']
        BadBlocksNumber: 4
        CanModifySpeed: False
        CanSetMultipleSpeeds: False
        EnableAutoNegotiation: False
        EnablePPM: True
        EnableRsFec: True
        EnableRsFecStats: True
        EnabledFlowControl: True
        FirecodeAdvertise: False
        FirecodeForceOff: False
        FirecodeForceOn: False
        FirecodeRequest: False
        FlowControlDirectedAddress: 01 80 C2 00 00 01
        ForceDisableFEC: False
        GoodBlocksNumber: 0
        IeeeL1Defaults: True
        LaserOn: True
        LinkTraining: False
        LoopContinuously: True
        LoopCountNumber: 1
        Loopback: True
        LoopbackMode: internalLoopback
        Ppm: 70
        RsFecAdvertise: False
        RsFecForceOn: False
        RsFecRequest: False
        SelectedSpeeds: ['speed100g']
        SendSetsMode: typeAOnly
        Speed: speed100g
        StartErrorInsertion: True
        TxIgnoreRxLinkFaults: False
        TypeAOrderedSets: localFault
        TypeBOrderedSets: remoteFault
        UseANResults: False
"""
