"""
tapsettings_ApplicationSelect.py:

    - Connect to the API server
    - In this test, do the following:
        - Add two real ports 
        - Add two vports
        - Assign two real ports in to vports
        - Find the transceiverOptions from vport tapsettings
        - Update reqAppSel attributes of transceiverOptions

     
Supports IxNetwork API servers:
   - Windows, Windows Connection Mgr and Linux
   
Requirements:
   - Minimum IxNetwork 10.00
   - Python 2.7 and 3+
   - pip install requests
   - pip install ixnetwork_restpy
   
RestPy Doc:
    https://openixia.github.io/ixnetwork_restpy/#/overview

Usage:
   - Enter: python <script>
   
"""

from ixnetwork_restpy import SessionAssistant

session_assistant = SessionAssistant(
    IpAddress="<chassis-ip>",
    RestPort="<rest-port>",
    UserName="admin",
    Password="admin",
    LogLevel=SessionAssistant.LOGLEVEL_INFO,
    ClearConfig=True,
)

ixnetwork = session_assistant.Ixnetwork

# mapping the ports
port_map = session_assistant.PortMapAssistant()
port_map.Map(Location="<chassis-ip>;<card>;<port>", Name="Port 1")
port_map.Map(Location="<chassis-ip>;<card>;<port>", Name="Port 2")

# using the map connect test port locations and vports
port_map.Connect(ForceOwnership=True, HostReadyTimeout=20, LinkUpTimeout=60)
vport1 = ixnetwork.Vport.find(Name="Port 1")
vport2 = ixnetwork.Vport.find(Name="Port 2")

# Get Tap Settings options
vport1.GetTapSettings()
tapsettings = vport1.TapSettings.find()

# Transceiver Options Configuration 
v1_trans = vport1.TapSettings.find().TransceiverOptions
appselMatch = v1_trans.AppselMatch.find()
availableApp = v1_trans.AvailableApplications.find()
v1_trans.ReqAppSel = "appSel1"
vport1.SetTapSettings()