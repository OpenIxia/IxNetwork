"""
Description
     Demonstrate how to use Python class inheritance to leverage OpenIxia
     library and extend the OpenIxia library with your own library.

     Create your own classes and inherit the corresponding OpenIxia class.
     Your scripts will be instantiating objects using your classes.
     With inheritance, this allows your scripts to use all of OpenIxia functions
     and use your added functions in your classes.
     This allows you to keep getting OpenIxia updates without interferring with 
     your extended functions.

"""

from IxNetRestApi import *
from IxNetRestApiPortMgmt import PortMgmt
from IxNetRestApiTraffic import Traffic
from IxNetRestApiProtocol import Protocol
from IxNetRestApiStatistics import Statistics
from IxNetRestApiPacketCapture import PacketCapture
from IxNetRestApiQuickTest import QuickTest

class Connection(Connect):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class Port_Mgmt(PortMgmt):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def my_Own_Port_Mgmt_Function(self):
        # Add and create your own function to extend the OpenIxia library.
        pass

    def exportJsonConfig(self):
        # Overwrite the OpenIxia exportJsonConfig function.
        # For enhancement or to fix a bug in exportJsonConfig().
        pass

class Traffic_Config(Traffic):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class Protocol_Config(Protocol):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class Statistics_View(Statistics):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
