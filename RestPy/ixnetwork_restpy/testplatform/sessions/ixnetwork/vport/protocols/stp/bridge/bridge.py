from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Bridge(Base):
	"""The Bridge class encapsulates a user managed bridge node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Bridge property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'bridge'

	def __init__(self, parent):
		super(Bridge, self).__init__(parent)

	@property
	def Cist(self):
		"""An instance of the Cist class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.stp.bridge.cist.cist.Cist)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.stp.bridge.cist.cist import Cist
		return Cist(self)._select()

	@property
	def Interface(self):
		"""An instance of the Interface class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.stp.bridge.interface.interface.Interface)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.stp.bridge.interface.interface import Interface
		return Interface(self)

	@property
	def LearnedInfo(self):
		"""An instance of the LearnedInfo class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.stp.bridge.learnedinfo.learnedinfo.LearnedInfo)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.stp.bridge.learnedinfo.learnedinfo import LearnedInfo
		return LearnedInfo(self)._select()

	@property
	def Msti(self):
		"""An instance of the Msti class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.stp.bridge.msti.msti.Msti)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.stp.bridge.msti.msti import Msti
		return Msti(self)

	@property
	def Vlan(self):
		"""An instance of the Vlan class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.stp.bridge.vlan.vlan.Vlan)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.stp.bridge.vlan.vlan import Vlan
		return Vlan(self)

	@property
	def AutoPickBridgeMac(self):
		"""If enabled, the MAC address for one of the STP interfaces will be automatically assigned as the MAC address for this bridge.

		Returns:
			bool
		"""
		return self._get_attribute('autoPickBridgeMac')
	@AutoPickBridgeMac.setter
	def AutoPickBridgeMac(self, value):
		self._set_attribute('autoPickBridgeMac', value)

	@property
	def BridgeMac(self):
		"""The 6-byte MAC address assigned to this bridge. Part of the bridge identifier (bridge ID).

		Returns:
			str
		"""
		return self._get_attribute('bridgeMac')
	@BridgeMac.setter
	def BridgeMac(self, value):
		self._set_attribute('bridgeMac', value)

	@property
	def BridgePriority(self):
		"""The Bridge Priority for this bridge.The valid range is 0 to 61,440, in multiples of 4,096. (default = 32,768)

		Returns:
			str(0|4096|8192|12288|16384|20480|24576|28672|32768|36864|40960|45056|49152|53248|57344|61440)
		"""
		return self._get_attribute('bridgePriority')
	@BridgePriority.setter
	def BridgePriority(self, value):
		self._set_attribute('bridgePriority', value)

	@property
	def BridgeSystemId(self):
		"""The System ID for the bridge. The valid range is 0 to 4,095. (default = 0)

		Returns:
			number
		"""
		return self._get_attribute('bridgeSystemId')
	@BridgeSystemId.setter
	def BridgeSystemId(self, value):
		self._set_attribute('bridgeSystemId', value)

	@property
	def BridgeType(self):
		"""NOT DEFINED

		Returns:
			str(bridges|providerBridges)
		"""
		return self._get_attribute('bridgeType')
	@BridgeType.setter
	def BridgeType(self, value):
		self._set_attribute('bridgeType', value)

	@property
	def CistRegRootCost(self):
		"""(For use with PVST+ and RPVST+ only) The Common Spanning Tree (CST) root path cost. The valid range is 0 to 4294967295. (default = 0)

		Returns:
			number
		"""
		return self._get_attribute('cistRegRootCost')
	@CistRegRootCost.setter
	def CistRegRootCost(self, value):
		self._set_attribute('cistRegRootCost', value)

	@property
	def CistRegRootMac(self):
		"""(For use with PVST+ and RPVST+ only) The Common Spanning Tree (CST) 6-byte root MAC address. (default = 00:00:00:00:00:00)

		Returns:
			str
		"""
		return self._get_attribute('cistRegRootMac')
	@CistRegRootMac.setter
	def CistRegRootMac(self, value):
		self._set_attribute('cistRegRootMac', value)

	@property
	def CistRegRootPriority(self):
		"""(For use with PVST+ and RPVST+ only) The Common Spanning Tree (CST) priority of the root. The valid range is 0 to 61,440, in increments of 4,096. (default = 32,768)

		Returns:
			str(0|4096|8192|12288|16384|20480|24576|28672|32768|36864|40960|45056|49152|53248|57344|61440)
		"""
		return self._get_attribute('cistRegRootPriority')
	@CistRegRootPriority.setter
	def CistRegRootPriority(self, value):
		self._set_attribute('cistRegRootPriority', value)

	@property
	def CistRemainingHop(self):
		"""(For use with MSTP only) The number of additional bridge-to-bridge hops that will be allowed for the MSTP BPDUs. The root sets the maximum hop count, and each subsequent bridge decrements this value by 1. The valid range is 1 to 255. (default = 20)

		Returns:
			number
		"""
		return self._get_attribute('cistRemainingHop')
	@CistRemainingHop.setter
	def CistRemainingHop(self, value):
		self._set_attribute('cistRemainingHop', value)

	@property
	def Enabled(self):
		"""Enables or disables the bridge's simulation. (default = disabled)

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def ExternalRootCost(self):
		"""Common and Internal Spanning Tree (CIST) external root path cost. A 4-byte unsigned integer. The default is 0.

		Returns:
			number
		"""
		return self._get_attribute('externalRootCost')
	@ExternalRootCost.setter
	def ExternalRootCost(self, value):
		self._set_attribute('externalRootCost', value)

	@property
	def ExternalRootMac(self):
		"""Common and Internal Spanning Tree (CIST) external root MAC address. A 6-byte MAC address.The default is 00 00 00 00 00 00.

		Returns:
			str
		"""
		return self._get_attribute('externalRootMac')
	@ExternalRootMac.setter
	def ExternalRootMac(self, value):
		self._set_attribute('externalRootMac', value)

	@property
	def ExternalRootPriority(self):
		"""(For use with MSTP only) The priority value of the root bridge for the CIST/MSTP region (external). Part of the CIST External Root Identifier. The valid range is 0 to 61,440, in increments of 4096. (default = 32,768)

		Returns:
			str(0|4096|8192|12288|16384|20480|24576|28672|32768|36864|40960|45056|49152|53248|57344|61440)
		"""
		return self._get_attribute('externalRootPriority')
	@ExternalRootPriority.setter
	def ExternalRootPriority(self, value):
		self._set_attribute('externalRootPriority', value)

	@property
	def ForwardDelay(self):
		"""The delay used for a port's change to the Forwarding state. (in milliseconds) The valid range is 500 msec to 255 sec. (default = 15,000 msec (15 sec)

		Returns:
			number
		"""
		return self._get_attribute('forwardDelay')
	@ForwardDelay.setter
	def ForwardDelay(self, value):
		self._set_attribute('forwardDelay', value)

	@property
	def HelloInterval(self):
		"""The length of time between transmission of Hello messages from the root bridge (in milliseconds). The valid range is 500 msec to 255 sec. (default = 2,000 msec (2 sec)

		Returns:
			number
		"""
		return self._get_attribute('helloInterval')
	@HelloInterval.setter
	def HelloInterval(self, value):
		self._set_attribute('helloInterval', value)

	@property
	def IsRefreshComplete(self):
		"""If true, this causes the STP bridge to update.

		Returns:
			bool
		"""
		return self._get_attribute('isRefreshComplete')

	@property
	def MaxAge(self):
		"""The maximum Configuration message aging time. (in milliseconds) The valid range is 500 msec to 255 sec. (default = 20,000 msec (20 sec)

		Returns:
			number
		"""
		return self._get_attribute('maxAge')
	@MaxAge.setter
	def MaxAge(self, value):
		self._set_attribute('maxAge', value)

	@property
	def MessageAge(self):
		"""The message age time parameter in the BPDU (in milliseconds). (It should be less than the Max. Age.) The valid range is 500 msec to 255 sec. (default = 0)

		Returns:
			number
		"""
		return self._get_attribute('messageAge')
	@MessageAge.setter
	def MessageAge(self, value):
		self._set_attribute('messageAge', value)

	@property
	def Mode(self):
		"""The version of the STP protocol that is being used on the Bridge.

		Returns:
			str(stp|rstp|mstp|pvst|rpvst|pvstp)
		"""
		return self._get_attribute('mode')
	@Mode.setter
	def Mode(self, value):
		self._set_attribute('mode', value)

	@property
	def MstcName(self):
		"""(For use with MSTP only) The name of the Multiple Spanning Tree Configuration being used. Format = MSTC ID-n (editable by user).

		Returns:
			str
		"""
		return self._get_attribute('mstcName')
	@MstcName.setter
	def MstcName(self, value):
		self._set_attribute('mstcName', value)

	@property
	def MstcRevisionNumber(self):
		"""(For use with MSTP only) The Revision Number of the Multiple Spanning Tree Configuration being used. A 2-byte unsigned integer. (default = 0)

		Returns:
			number
		"""
		return self._get_attribute('mstcRevisionNumber')
	@MstcRevisionNumber.setter
	def MstcRevisionNumber(self, value):
		self._set_attribute('mstcRevisionNumber', value)

	@property
	def PortPriority(self):
		"""The port priority. The valid range is to 240, in multiples of 16. (default = 0)

		Returns:
			str(0|16|32|48|64|80|96|112|128|144|160|176|192|208|224|240)
		"""
		return self._get_attribute('portPriority')
	@PortPriority.setter
	def PortPriority(self, value):
		self._set_attribute('portPriority', value)

	@property
	def PvstpMode(self):
		"""The version of the pvSTP protocol that is being used on the Bridge.

		Returns:
			str(stp|rstp)
		"""
		return self._get_attribute('pvstpMode')
	@PvstpMode.setter
	def PvstpMode(self, value):
		self._set_attribute('pvstpMode', value)

	@property
	def RootCost(self):
		"""(For STP and RSTP) The administrative cost for the shortest path from this bridge to the Root Bridge. The valid range is 0 to 4294967295. (default = 0)

		Returns:
			number
		"""
		return self._get_attribute('rootCost')
	@RootCost.setter
	def RootCost(self, value):
		self._set_attribute('rootCost', value)

	@property
	def RootMac(self):
		"""(For STP and RSTP) The 6-byte MAC Address for the Root Bridge. (default = 00:00:00:00:00:00)

		Returns:
			str
		"""
		return self._get_attribute('rootMac')
	@RootMac.setter
	def RootMac(self, value):
		self._set_attribute('rootMac', value)

	@property
	def RootPriority(self):
		"""(For STP and RSTP) The Bridge Priority for the root bridge. The valid range is 0 to 61,440, in increments of 4096. (default = 32,768)

		Returns:
			str(0|4096|8192|12288|16384|20480|24576|28672|32768|36864|40960|45056|49152|53248|57344|61440)
		"""
		return self._get_attribute('rootPriority')
	@RootPriority.setter
	def RootPriority(self, value):
		self._set_attribute('rootPriority', value)

	@property
	def RootSystemId(self):
		"""(For STP and RSTP) The System ID for the root bridge. The valid range is 0 to 4,095. (default = 0)

		Returns:
			number
		"""
		return self._get_attribute('rootSystemId')
	@RootSystemId.setter
	def RootSystemId(self, value):
		self._set_attribute('rootSystemId', value)

	@property
	def UpdateRequired(self):
		"""Indicates that an updated is required.

		Returns:
			number
		"""
		return self._get_attribute('updateRequired')
	@UpdateRequired.setter
	def UpdateRequired(self, value):
		self._set_attribute('updateRequired', value)

	@property
	def VlanPortPriority(self):
		"""(For use with PVST+ and RPVST+ only) The Common Spanning Tree (CST) VLAN port priority. The valid range is 0 to 63. (default = 32)

		Returns:
			number
		"""
		return self._get_attribute('vlanPortPriority')
	@VlanPortPriority.setter
	def VlanPortPriority(self, value):
		self._set_attribute('vlanPortPriority', value)

	@property
	def VlanRootMac(self):
		"""Common and Internal Spanning Tree (CIST) Regional (external) MAC address. Part of the CIST External Root Identifier. A 6-byte MAC address.

		Returns:
			str
		"""
		return self._get_attribute('vlanRootMac')
	@VlanRootMac.setter
	def VlanRootMac(self, value):
		self._set_attribute('vlanRootMac', value)

	@property
	def VlanRootPathCost(self):
		"""Common and Internal Spanning Tree (CIST) regional (external) root path cost.

		Returns:
			number
		"""
		return self._get_attribute('vlanRootPathCost')
	@VlanRootPathCost.setter
	def VlanRootPathCost(self, value):
		self._set_attribute('vlanRootPathCost', value)

	@property
	def VlanRootPriority(self):
		"""The priority value of the root bridge for the Common Spanning Tree (CST).

		Returns:
			str(0|4096|8192|12288|16384|20480|24576|28672|32768|36864|40960|45056|49152|53248|57344|61440)
		"""
		return self._get_attribute('vlanRootPriority')
	@VlanRootPriority.setter
	def VlanRootPriority(self, value):
		self._set_attribute('vlanRootPriority', value)

	def add(self, AutoPickBridgeMac=None, BridgeMac=None, BridgePriority=None, BridgeSystemId=None, BridgeType=None, CistRegRootCost=None, CistRegRootMac=None, CistRegRootPriority=None, CistRemainingHop=None, Enabled=None, ExternalRootCost=None, ExternalRootMac=None, ExternalRootPriority=None, ForwardDelay=None, HelloInterval=None, MaxAge=None, MessageAge=None, Mode=None, MstcName=None, MstcRevisionNumber=None, PortPriority=None, PvstpMode=None, RootCost=None, RootMac=None, RootPriority=None, RootSystemId=None, UpdateRequired=None, VlanPortPriority=None, VlanRootMac=None, VlanRootPathCost=None, VlanRootPriority=None):
		"""Adds a new bridge node on the server and retrieves it in this instance.

		Args:
			AutoPickBridgeMac (bool): If enabled, the MAC address for one of the STP interfaces will be automatically assigned as the MAC address for this bridge.
			BridgeMac (str): The 6-byte MAC address assigned to this bridge. Part of the bridge identifier (bridge ID).
			BridgePriority (str(0|4096|8192|12288|16384|20480|24576|28672|32768|36864|40960|45056|49152|53248|57344|61440)): The Bridge Priority for this bridge.The valid range is 0 to 61,440, in multiples of 4,096. (default = 32,768)
			BridgeSystemId (number): The System ID for the bridge. The valid range is 0 to 4,095. (default = 0)
			BridgeType (str(bridges|providerBridges)): NOT DEFINED
			CistRegRootCost (number): (For use with PVST+ and RPVST+ only) The Common Spanning Tree (CST) root path cost. The valid range is 0 to 4294967295. (default = 0)
			CistRegRootMac (str): (For use with PVST+ and RPVST+ only) The Common Spanning Tree (CST) 6-byte root MAC address. (default = 00:00:00:00:00:00)
			CistRegRootPriority (str(0|4096|8192|12288|16384|20480|24576|28672|32768|36864|40960|45056|49152|53248|57344|61440)): (For use with PVST+ and RPVST+ only) The Common Spanning Tree (CST) priority of the root. The valid range is 0 to 61,440, in increments of 4,096. (default = 32,768)
			CistRemainingHop (number): (For use with MSTP only) The number of additional bridge-to-bridge hops that will be allowed for the MSTP BPDUs. The root sets the maximum hop count, and each subsequent bridge decrements this value by 1. The valid range is 1 to 255. (default = 20)
			Enabled (bool): Enables or disables the bridge's simulation. (default = disabled)
			ExternalRootCost (number): Common and Internal Spanning Tree (CIST) external root path cost. A 4-byte unsigned integer. The default is 0.
			ExternalRootMac (str): Common and Internal Spanning Tree (CIST) external root MAC address. A 6-byte MAC address.The default is 00 00 00 00 00 00.
			ExternalRootPriority (str(0|4096|8192|12288|16384|20480|24576|28672|32768|36864|40960|45056|49152|53248|57344|61440)): (For use with MSTP only) The priority value of the root bridge for the CIST/MSTP region (external). Part of the CIST External Root Identifier. The valid range is 0 to 61,440, in increments of 4096. (default = 32,768)
			ForwardDelay (number): The delay used for a port's change to the Forwarding state. (in milliseconds) The valid range is 500 msec to 255 sec. (default = 15,000 msec (15 sec)
			HelloInterval (number): The length of time between transmission of Hello messages from the root bridge (in milliseconds). The valid range is 500 msec to 255 sec. (default = 2,000 msec (2 sec)
			MaxAge (number): The maximum Configuration message aging time. (in milliseconds) The valid range is 500 msec to 255 sec. (default = 20,000 msec (20 sec)
			MessageAge (number): The message age time parameter in the BPDU (in milliseconds). (It should be less than the Max. Age.) The valid range is 500 msec to 255 sec. (default = 0)
			Mode (str(stp|rstp|mstp|pvst|rpvst|pvstp)): The version of the STP protocol that is being used on the Bridge.
			MstcName (str): (For use with MSTP only) The name of the Multiple Spanning Tree Configuration being used. Format = MSTC ID-n (editable by user).
			MstcRevisionNumber (number): (For use with MSTP only) The Revision Number of the Multiple Spanning Tree Configuration being used. A 2-byte unsigned integer. (default = 0)
			PortPriority (str(0|16|32|48|64|80|96|112|128|144|160|176|192|208|224|240)): The port priority. The valid range is to 240, in multiples of 16. (default = 0)
			PvstpMode (str(stp|rstp)): The version of the pvSTP protocol that is being used on the Bridge.
			RootCost (number): (For STP and RSTP) The administrative cost for the shortest path from this bridge to the Root Bridge. The valid range is 0 to 4294967295. (default = 0)
			RootMac (str): (For STP and RSTP) The 6-byte MAC Address for the Root Bridge. (default = 00:00:00:00:00:00)
			RootPriority (str(0|4096|8192|12288|16384|20480|24576|28672|32768|36864|40960|45056|49152|53248|57344|61440)): (For STP and RSTP) The Bridge Priority for the root bridge. The valid range is 0 to 61,440, in increments of 4096. (default = 32,768)
			RootSystemId (number): (For STP and RSTP) The System ID for the root bridge. The valid range is 0 to 4,095. (default = 0)
			UpdateRequired (number): Indicates that an updated is required.
			VlanPortPriority (number): (For use with PVST+ and RPVST+ only) The Common Spanning Tree (CST) VLAN port priority. The valid range is 0 to 63. (default = 32)
			VlanRootMac (str): Common and Internal Spanning Tree (CIST) Regional (external) MAC address. Part of the CIST External Root Identifier. A 6-byte MAC address.
			VlanRootPathCost (number): Common and Internal Spanning Tree (CIST) regional (external) root path cost.
			VlanRootPriority (str(0|4096|8192|12288|16384|20480|24576|28672|32768|36864|40960|45056|49152|53248|57344|61440)): The priority value of the root bridge for the Common Spanning Tree (CST).

		Returns:
			self: This instance with all currently retrieved bridge data using find and the newly added bridge data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the bridge data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, AutoPickBridgeMac=None, BridgeMac=None, BridgePriority=None, BridgeSystemId=None, BridgeType=None, CistRegRootCost=None, CistRegRootMac=None, CistRegRootPriority=None, CistRemainingHop=None, Enabled=None, ExternalRootCost=None, ExternalRootMac=None, ExternalRootPriority=None, ForwardDelay=None, HelloInterval=None, IsRefreshComplete=None, MaxAge=None, MessageAge=None, Mode=None, MstcName=None, MstcRevisionNumber=None, PortPriority=None, PvstpMode=None, RootCost=None, RootMac=None, RootPriority=None, RootSystemId=None, UpdateRequired=None, VlanPortPriority=None, VlanRootMac=None, VlanRootPathCost=None, VlanRootPriority=None):
		"""Finds and retrieves bridge data from the server.

		All named parameters support regex and can be used to selectively retrieve bridge data from the server.
		By default the find method takes no parameters and will retrieve all bridge data from the server.

		Args:
			AutoPickBridgeMac (bool): If enabled, the MAC address for one of the STP interfaces will be automatically assigned as the MAC address for this bridge.
			BridgeMac (str): The 6-byte MAC address assigned to this bridge. Part of the bridge identifier (bridge ID).
			BridgePriority (str(0|4096|8192|12288|16384|20480|24576|28672|32768|36864|40960|45056|49152|53248|57344|61440)): The Bridge Priority for this bridge.The valid range is 0 to 61,440, in multiples of 4,096. (default = 32,768)
			BridgeSystemId (number): The System ID for the bridge. The valid range is 0 to 4,095. (default = 0)
			BridgeType (str(bridges|providerBridges)): NOT DEFINED
			CistRegRootCost (number): (For use with PVST+ and RPVST+ only) The Common Spanning Tree (CST) root path cost. The valid range is 0 to 4294967295. (default = 0)
			CistRegRootMac (str): (For use with PVST+ and RPVST+ only) The Common Spanning Tree (CST) 6-byte root MAC address. (default = 00:00:00:00:00:00)
			CistRegRootPriority (str(0|4096|8192|12288|16384|20480|24576|28672|32768|36864|40960|45056|49152|53248|57344|61440)): (For use with PVST+ and RPVST+ only) The Common Spanning Tree (CST) priority of the root. The valid range is 0 to 61,440, in increments of 4,096. (default = 32,768)
			CistRemainingHop (number): (For use with MSTP only) The number of additional bridge-to-bridge hops that will be allowed for the MSTP BPDUs. The root sets the maximum hop count, and each subsequent bridge decrements this value by 1. The valid range is 1 to 255. (default = 20)
			Enabled (bool): Enables or disables the bridge's simulation. (default = disabled)
			ExternalRootCost (number): Common and Internal Spanning Tree (CIST) external root path cost. A 4-byte unsigned integer. The default is 0.
			ExternalRootMac (str): Common and Internal Spanning Tree (CIST) external root MAC address. A 6-byte MAC address.The default is 00 00 00 00 00 00.
			ExternalRootPriority (str(0|4096|8192|12288|16384|20480|24576|28672|32768|36864|40960|45056|49152|53248|57344|61440)): (For use with MSTP only) The priority value of the root bridge for the CIST/MSTP region (external). Part of the CIST External Root Identifier. The valid range is 0 to 61,440, in increments of 4096. (default = 32,768)
			ForwardDelay (number): The delay used for a port's change to the Forwarding state. (in milliseconds) The valid range is 500 msec to 255 sec. (default = 15,000 msec (15 sec)
			HelloInterval (number): The length of time between transmission of Hello messages from the root bridge (in milliseconds). The valid range is 500 msec to 255 sec. (default = 2,000 msec (2 sec)
			IsRefreshComplete (bool): If true, this causes the STP bridge to update.
			MaxAge (number): The maximum Configuration message aging time. (in milliseconds) The valid range is 500 msec to 255 sec. (default = 20,000 msec (20 sec)
			MessageAge (number): The message age time parameter in the BPDU (in milliseconds). (It should be less than the Max. Age.) The valid range is 500 msec to 255 sec. (default = 0)
			Mode (str(stp|rstp|mstp|pvst|rpvst|pvstp)): The version of the STP protocol that is being used on the Bridge.
			MstcName (str): (For use with MSTP only) The name of the Multiple Spanning Tree Configuration being used. Format = MSTC ID-n (editable by user).
			MstcRevisionNumber (number): (For use with MSTP only) The Revision Number of the Multiple Spanning Tree Configuration being used. A 2-byte unsigned integer. (default = 0)
			PortPriority (str(0|16|32|48|64|80|96|112|128|144|160|176|192|208|224|240)): The port priority. The valid range is to 240, in multiples of 16. (default = 0)
			PvstpMode (str(stp|rstp)): The version of the pvSTP protocol that is being used on the Bridge.
			RootCost (number): (For STP and RSTP) The administrative cost for the shortest path from this bridge to the Root Bridge. The valid range is 0 to 4294967295. (default = 0)
			RootMac (str): (For STP and RSTP) The 6-byte MAC Address for the Root Bridge. (default = 00:00:00:00:00:00)
			RootPriority (str(0|4096|8192|12288|16384|20480|24576|28672|32768|36864|40960|45056|49152|53248|57344|61440)): (For STP and RSTP) The Bridge Priority for the root bridge. The valid range is 0 to 61,440, in increments of 4096. (default = 32,768)
			RootSystemId (number): (For STP and RSTP) The System ID for the root bridge. The valid range is 0 to 4,095. (default = 0)
			UpdateRequired (number): Indicates that an updated is required.
			VlanPortPriority (number): (For use with PVST+ and RPVST+ only) The Common Spanning Tree (CST) VLAN port priority. The valid range is 0 to 63. (default = 32)
			VlanRootMac (str): Common and Internal Spanning Tree (CIST) Regional (external) MAC address. Part of the CIST External Root Identifier. A 6-byte MAC address.
			VlanRootPathCost (number): Common and Internal Spanning Tree (CIST) regional (external) root path cost.
			VlanRootPriority (str(0|4096|8192|12288|16384|20480|24576|28672|32768|36864|40960|45056|49152|53248|57344|61440)): The priority value of the root bridge for the Common Spanning Tree (CST).

		Returns:
			self: This instance with matching bridge data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of bridge data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the bridge data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)

	def BridgeTopologyChange(self):
		"""Executes the bridgeTopologyChange operation on the server.

		This commands checks to see if there has been a topology change in the specified STP bridge.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=bridge)): The method internally set Arg1 to the current href for this instance

		Returns:
			bool: NOT DEFINED

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('BridgeTopologyChange', payload=locals(), response_object=None)

	def CistTopologyChange(self):
		"""Executes the cistTopologyChange operation on the server.

		This command checks to see if a topology change has occurred on the specified STP bridge CIST.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=bridge)): The method internally set Arg1 to the current href for this instance

		Returns:
			bool: NOT DEFINED

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('CistTopologyChange', payload=locals(), response_object=None)

	def RefreshLearnedInfo(self):
		"""Executes the refreshLearnedInfo operation on the server.

		This exec refreshes the STP learned information from the DUT.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=bridge)): The method internally set Arg1 to the current href for this instance

		Returns:
			bool: NOT DEFINED

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('RefreshLearnedInfo', payload=locals(), response_object=None)

	def UpdateParameters(self):
		"""Executes the updateParameters operation on the server.

		Updates the current STP parameters for the STP bridge.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=bridge)): The method internally set Arg1 to the current href for this instance

		Returns:
			bool: NOT DEFINED

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('UpdateParameters', payload=locals(), response_object=None)
