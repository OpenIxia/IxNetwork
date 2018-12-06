
# Copyright 1997 - 2018 by IXIA Keysight
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
    
from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Vport(Base):
	"""The Vport class encapsulates a user managed vport node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Vport property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'vport'

	def __init__(self, parent):
		super(Vport, self).__init__(parent)

	@property
	def Capture(self):
		"""An instance of the Capture class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.capture.capture.Capture)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.capture.capture import Capture
		return Capture(self)._select()

	@property
	def DiscoveredNeighbor(self):
		"""An instance of the DiscoveredNeighbor class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.discoveredneighbor.discoveredneighbor.DiscoveredNeighbor)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.discoveredneighbor.discoveredneighbor import DiscoveredNeighbor
		return DiscoveredNeighbor(self)

	@property
	def Interface(self):
		"""An instance of the Interface class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.interface.interface.Interface)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.interface.interface import Interface
		return Interface(self)

	@property
	def InterfaceDiscoveredAddress(self):
		"""An instance of the InterfaceDiscoveredAddress class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.interfacediscoveredaddress.interfacediscoveredaddress.InterfaceDiscoveredAddress)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.interfacediscoveredaddress.interfacediscoveredaddress import InterfaceDiscoveredAddress
		return InterfaceDiscoveredAddress(self)._select()

	@property
	def L1Config(self):
		"""An instance of the L1Config class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.l1config.l1config.L1Config)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.l1config.l1config import L1Config
		return L1Config(self)._select()

	@property
	def Protocols(self):
		"""An instance of the Protocols class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.protocols.Protocols)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.protocols import Protocols
		return Protocols(self)

	@property
	def RateControlParameters(self):
		"""An instance of the RateControlParameters class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.ratecontrolparameters.ratecontrolparameters.RateControlParameters)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.ratecontrolparameters.ratecontrolparameters import RateControlParameters
		return RateControlParameters(self)._select()

	@property
	def ActualSpeed(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('actualSpeed')

	@property
	def AssignedTo(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('assignedTo')

	@property
	def ConnectedTo(self):
		"""

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/availableHardware?deepchild=port)
		"""
		return self._get_attribute('connectedTo')
	@ConnectedTo.setter
	def ConnectedTo(self, value):
		self._set_attribute('connectedTo', value)

	@property
	def ConnectionInfo(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('connectionInfo')

	@property
	def ConnectionState(self):
		"""Consolidated state of the vport. This combines the connection state with link state.

		Returns:
			str(assignedInUseByOther|assignedUnconnected|connectedLinkDown|connectedLinkUp|connecting|unassigned)
		"""
		return self._get_attribute('connectionState')

	@property
	def ConnectionStatus(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('connectionStatus')

	@property
	def InternalId(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('internalId')

	@property
	def IsAvailable(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('isAvailable')

	@property
	def IsConnected(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('isConnected')

	@property
	def IsMapped(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('isMapped')

	@property
	def IsPullOnly(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('isPullOnly')
	@IsPullOnly.setter
	def IsPullOnly(self, value):
		self._set_attribute('isPullOnly', value)

	@property
	def IsVMPort(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('isVMPort')

	@property
	def IxnChassisVersion(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('ixnChassisVersion')

	@property
	def IxnClientVersion(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('ixnClientVersion')

	@property
	def IxosChassisVersion(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('ixosChassisVersion')

	@property
	def Licenses(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('licenses')

	@property
	def Name(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('name')
	@Name.setter
	def Name(self, value):
		self._set_attribute('name', value)

	@property
	def RxMode(self):
		"""

		Returns:
			str(capture|captureAndMeasure|measure|packetImpairment)
		"""
		return self._get_attribute('rxMode')
	@RxMode.setter
	def RxMode(self, value):
		self._set_attribute('rxMode', value)

	@property
	def State(self):
		"""

		Returns:
			str(busy|down|unassigned|up|versionMismatch)
		"""
		return self._get_attribute('state')

	@property
	def StateDetail(self):
		"""

		Returns:
			str(busy|cpuNotReady|idle|inActive|l1ConfigFailed|protocolsNotSupported|versionMismatched|waitingForCPUStatus)
		"""
		return self._get_attribute('stateDetail')

	@property
	def TransmitIgnoreLinkStatus(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('transmitIgnoreLinkStatus')
	@TransmitIgnoreLinkStatus.setter
	def TransmitIgnoreLinkStatus(self, value):
		self._set_attribute('transmitIgnoreLinkStatus', value)

	@property
	def TxGapControlMode(self):
		"""

		Returns:
			str(averageMode|fixedMode)
		"""
		return self._get_attribute('txGapControlMode')
	@TxGapControlMode.setter
	def TxGapControlMode(self, value):
		self._set_attribute('txGapControlMode', value)

	@property
	def TxMode(self):
		"""

		Returns:
			str(interleaved|interleavedCoarse|packetImpairment|sequential|sequentialCoarse)
		"""
		return self._get_attribute('txMode')
	@TxMode.setter
	def TxMode(self, value):
		self._set_attribute('txMode', value)

	@property
	def Type(self):
		"""

		Returns:
			str(atlasFourHundredGigLan|atlasFourHundredGigLanFcoe|atm|ethernet|ethernetFcoe|ethernetImpairment|ethernetvm|fc|fortyGigLan|fortyGigLanFcoe|hundredGigLan|hundredGigLanFcoe|krakenFourHundredGigLan|novusHundredGigLan|novusHundredGigLanFcoe|novusTenGigLan|novusTenGigLanFcoe|pos|tenFortyHundredGigLan|tenFortyHundredGigLanFcoe|tenGigLan|tenGigLanFcoe|tenGigWan|tenGigWanFcoe)
		"""
		return self._get_attribute('type')
	@Type.setter
	def Type(self, value):
		self._set_attribute('type', value)

	@property
	def ValidTxModes(self):
		"""

		Returns:
			list(str[interleaved|interleavedCoarse|packetImpairment|sequential|sequentialCoarse])
		"""
		return self._get_attribute('validTxModes')

	def add(self, ConnectedTo=None, IsPullOnly=None, Name=None, RxMode=None, TransmitIgnoreLinkStatus=None, TxGapControlMode=None, TxMode=None, Type=None):
		"""Adds a new vport node on the server and retrieves it in this instance.

		Args:
			ConnectedTo (str(None|/api/v1/sessions/1/ixnetwork/availableHardware?deepchild=port)): 
			IsPullOnly (bool): 
			Name (str): 
			RxMode (str(capture|captureAndMeasure|measure|packetImpairment)): 
			TransmitIgnoreLinkStatus (bool): 
			TxGapControlMode (str(averageMode|fixedMode)): 
			TxMode (str(interleaved|interleavedCoarse|packetImpairment|sequential|sequentialCoarse)): 
			Type (str(atlasFourHundredGigLan|atlasFourHundredGigLanFcoe|atm|ethernet|ethernetFcoe|ethernetImpairment|ethernetvm|fc|fortyGigLan|fortyGigLanFcoe|hundredGigLan|hundredGigLanFcoe|krakenFourHundredGigLan|novusHundredGigLan|novusHundredGigLanFcoe|novusTenGigLan|novusTenGigLanFcoe|pos|tenFortyHundredGigLan|tenFortyHundredGigLanFcoe|tenGigLan|tenGigLanFcoe|tenGigWan|tenGigWanFcoe)): 

		Returns:
			self: This instance with all currently retrieved vport data using find and the newly added vport data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the vport data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, ActualSpeed=None, AssignedTo=None, ConnectedTo=None, ConnectionInfo=None, ConnectionState=None, ConnectionStatus=None, InternalId=None, IsAvailable=None, IsConnected=None, IsMapped=None, IsPullOnly=None, IsVMPort=None, IxnChassisVersion=None, IxnClientVersion=None, IxosChassisVersion=None, Licenses=None, Name=None, RxMode=None, State=None, StateDetail=None, TransmitIgnoreLinkStatus=None, TxGapControlMode=None, TxMode=None, Type=None, ValidTxModes=None):
		"""Finds and retrieves vport data from the server.

		All named parameters support regex and can be used to selectively retrieve vport data from the server.
		By default the find method takes no parameters and will retrieve all vport data from the server.

		Args:
			ActualSpeed (number): 
			AssignedTo (str): 
			ConnectedTo (str(None|/api/v1/sessions/1/ixnetwork/availableHardware?deepchild=port)): 
			ConnectionInfo (str): 
			ConnectionState (str(assignedInUseByOther|assignedUnconnected|connectedLinkDown|connectedLinkUp|connecting|unassigned)): Consolidated state of the vport. This combines the connection state with link state.
			ConnectionStatus (str): 
			InternalId (number): 
			IsAvailable (bool): 
			IsConnected (bool): 
			IsMapped (bool): 
			IsPullOnly (bool): 
			IsVMPort (bool): 
			IxnChassisVersion (str): 
			IxnClientVersion (str): 
			IxosChassisVersion (str): 
			Licenses (str): 
			Name (str): 
			RxMode (str(capture|captureAndMeasure|measure|packetImpairment)): 
			State (str(busy|down|unassigned|up|versionMismatch)): 
			StateDetail (str(busy|cpuNotReady|idle|inActive|l1ConfigFailed|protocolsNotSupported|versionMismatched|waitingForCPUStatus)): 
			TransmitIgnoreLinkStatus (bool): 
			TxGapControlMode (str(averageMode|fixedMode)): 
			TxMode (str(interleaved|interleavedCoarse|packetImpairment|sequential|sequentialCoarse)): 
			Type (str(atlasFourHundredGigLan|atlasFourHundredGigLanFcoe|atm|ethernet|ethernetFcoe|ethernetImpairment|ethernetvm|fc|fortyGigLan|fortyGigLanFcoe|hundredGigLan|hundredGigLanFcoe|krakenFourHundredGigLan|novusHundredGigLan|novusHundredGigLanFcoe|novusTenGigLan|novusTenGigLanFcoe|pos|tenFortyHundredGigLan|tenFortyHundredGigLanFcoe|tenGigLan|tenGigLanFcoe|tenGigWan|tenGigWanFcoe)): 
			ValidTxModes (list(str[interleaved|interleavedCoarse|packetImpairment|sequential|sequentialCoarse])): 

		Returns:
			self: This instance with matching vport data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of vport data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the vport data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)

	def AddQuickFlowGroups(self, Arg2):
		"""Executes the addQuickFlowGroups operation on the server.

		Add quick flow traffic items to the configuration.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/lag|/api/v1/sessions/1/ixnetwork/vport])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			Arg2 (number): The number of quick flow groups to add.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('AddQuickFlowGroups', payload=locals(), response_object=None)

	def ClearNeighborSolicitation(self):
		"""Executes the clearNeighborSolicitation operation on the server.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/vport])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('ClearNeighborSolicitation', payload=locals(), response_object=None)

	def ClearNeighborSolicitation(self):
		"""Executes the clearNeighborSolicitation operation on the server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport)): The method internally sets Arg1 to the current href for this instance

		Returns:
			bool: 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('ClearNeighborSolicitation', payload=locals(), response_object=None)

	def ClearNeighborTable(self):
		"""Executes the clearNeighborTable operation on the server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport)): The method internally sets Arg1 to the current href for this instance

		Returns:
			bool: 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('ClearNeighborTable', payload=locals(), response_object=None)

	def ClearPortTransmitDuration(self):
		"""Executes the clearPortTransmitDuration operation on the server.

		Clear the port transmit duration.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/lag|/api/v1/sessions/1/ixnetwork/vport])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('ClearPortTransmitDuration', payload=locals(), response_object=None)

	def ConnectPort(self):
		"""Executes the connectPort operation on the server.

		Connect a list of ports.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/vport])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('ConnectPort', payload=locals(), response_object=None)

	def ConnectPorts(self):
		"""Executes the connectPorts operation on the server.

		Connect a list of ports.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/vport])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('ConnectPorts', payload=locals(), response_object=None)

	def EnableOAM(self, Arg2):
		"""Executes the enableOAM operation on the server.

		Enable/Disable OAM on a list of ports.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/vport])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			Arg2 (bool): If true, it will enable OAM. Otherwise, it will disable OAM.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('EnableOAM', payload=locals(), response_object=None)

	def IgmpJoin(self, Arg2):
		"""Executes the igmpJoin operation on the server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport)): The method internally sets Arg1 to the current href for this instance
			Arg2 (str): 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('IgmpJoin', payload=locals(), response_object=None)

	def IgmpJoin(self, Arg2, Arg3):
		"""Executes the igmpJoin operation on the server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport)): The method internally sets Arg1 to the current href for this instance
			Arg2 (str): 
			Arg3 (number): 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('IgmpJoin', payload=locals(), response_object=None)

	def IgmpLeave(self, Arg2):
		"""Executes the igmpLeave operation on the server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport)): The method internally sets Arg1 to the current href for this instance
			Arg2 (str): 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('IgmpLeave', payload=locals(), response_object=None)

	def IgmpLeave(self, Arg2, Arg3):
		"""Executes the igmpLeave operation on the server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport)): The method internally sets Arg1 to the current href for this instance
			Arg2 (str): 
			Arg3 (number): 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('IgmpLeave', payload=locals(), response_object=None)

	def Import(self, Arg2):
		"""Executes the import operation on the server.

		Imports the port file (also supports legacy port files).

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport)): The method internally sets Arg1 to the current href for this instance
			Arg2 (obj(ixnetwork_restpy.files.Files)): The file to be imported.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		self._check_arg_type(Arg2, Files)
		return self._execute('Import', payload=locals(), response_object=None)

	def LinkUpDn(self, Arg2):
		"""Executes the linkUpDn operation on the server.

		Simulate port link up/down.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/vport])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			Arg2 (str(down|up)): A valid enum value as specified by the restriction.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('LinkUpDn', payload=locals(), response_object=None)

	def PullPort(self):
		"""Executes the pullPort operation on the server.

		Pulls config onto vport or group of vports.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport)): The method internally sets Arg1 to the current href for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('PullPort', payload=locals(), response_object=None)

	def RefreshUnresolvedNeighbors(self):
		"""Executes the refreshUnresolvedNeighbors operation on the server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport)): The method internally sets Arg1 to the current href for this instance

		Returns:
			bool: 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('RefreshUnresolvedNeighbors', payload=locals(), response_object=None)

	def ReleasePort(self):
		"""Executes the releasePort operation on the server.

		Release a hardware port.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/vport])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('ReleasePort', payload=locals(), response_object=None)

	def ResetPortCpu(self):
		"""Executes the resetPortCpu operation on the server.

		Reboot port CPU.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/vport])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('ResetPortCpu', payload=locals(), response_object=None)

	def ResetPortCpuAndFactoryDefault(self):
		"""Executes the resetPortCpuAndFactoryDefault operation on the server.

		Reboots the port CPU and restores the default settings.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/vport])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('ResetPortCpuAndFactoryDefault', payload=locals(), response_object=None)

	def RestartPppNegotiation(self):
		"""Executes the restartPppNegotiation operation on the server.

		Restarts the PPP negotiation on the port.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport)): The method internally sets Arg1 to the current href for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('RestartPppNegotiation', payload=locals(), response_object=None)

	def SendArp(self):
		"""Executes the sendArp operation on the server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport)): The method internally sets Arg1 to the current href for this instance

		Returns:
			bool: 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('SendArp', payload=locals(), response_object=None)

	def SendArp(self, Arg2):
		"""Executes the sendArp operation on the server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport)): The method internally sets Arg1 to the current href for this instance
			Arg2 (list(str[None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface])): 

		Returns:
			bool: 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('SendArp', payload=locals(), response_object=None)

	def SendArpAll(self):
		"""Executes the sendArpAll operation on the server.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/vport])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('SendArpAll', payload=locals(), response_object=None)

	def SendNs(self):
		"""Executes the sendNs operation on the server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport)): The method internally sets Arg1 to the current href for this instance

		Returns:
			bool: 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('SendNs', payload=locals(), response_object=None)

	def SendNs(self, Arg2):
		"""Executes the sendNs operation on the server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport)): The method internally sets Arg1 to the current href for this instance
			Arg2 (list(str[None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface])): 

		Returns:
			bool: 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('SendNs', payload=locals(), response_object=None)

	def SendNsAll(self):
		"""Executes the sendNsAll operation on the server.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/vport])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('SendNsAll', payload=locals(), response_object=None)

	def SendRs(self):
		"""Executes the sendRs operation on the server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport)): The method internally sets Arg1 to the current href for this instance

		Returns:
			bool: 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('SendRs', payload=locals(), response_object=None)

	def SendRs(self, Arg2):
		"""Executes the sendRs operation on the server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport)): The method internally sets Arg1 to the current href for this instance
			Arg2 (list(str[None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface])): 

		Returns:
			bool: 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('SendRs', payload=locals(), response_object=None)

	def SendRsAll(self):
		"""Executes the sendRsAll operation on the server.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/vport])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('SendRsAll', payload=locals(), response_object=None)

	def SetFactoryDefaults(self):
		"""Executes the setFactoryDefaults operation on the server.

		Set default values for port settings.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/vport])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('SetFactoryDefaults', payload=locals(), response_object=None)

	def StartStatelessTraffic(self):
		"""Executes the startStatelessTraffic operation on the server.

		Start the traffic configuration for stateless traffic items only.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/lag|/api/v1/sessions/1/ixnetwork/traffic|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficItem|/api/v1/sessions/1/ixnetwork/traffic?deepchild=highLevelStream|/api/v1/sessions/1/ixnetwork/vport])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('StartStatelessTraffic', payload=locals(), response_object=None)

	def StartStatelessTrafficBlocking(self):
		"""Executes the startStatelessTrafficBlocking operation on the server.

		Start the traffic configuration for stateless traffic items only. This will block until traffic is fully started.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/lag|/api/v1/sessions/1/ixnetwork/traffic|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficItem|/api/v1/sessions/1/ixnetwork/traffic?deepchild=highLevelStream|/api/v1/sessions/1/ixnetwork/vport])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('StartStatelessTrafficBlocking', payload=locals(), response_object=None)

	def StopStatelessTraffic(self):
		"""Executes the stopStatelessTraffic operation on the server.

		Stop the stateless traffic items.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/lag|/api/v1/sessions/1/ixnetwork/traffic|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficItem|/api/v1/sessions/1/ixnetwork/traffic?deepchild=highLevelStream|/api/v1/sessions/1/ixnetwork/vport])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('StopStatelessTraffic', payload=locals(), response_object=None)

	def StopStatelessTrafficBlocking(self):
		"""Executes the stopStatelessTrafficBlocking operation on the server.

		Stop the traffic configuration for stateless traffic items only. This will block until traffic is fully stopped.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/lag|/api/v1/sessions/1/ixnetwork/traffic|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficItem|/api/v1/sessions/1/ixnetwork/traffic?deepchild=highLevelStream|/api/v1/sessions/1/ixnetwork/vport])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('StopStatelessTrafficBlocking', payload=locals(), response_object=None)

	def UnassignPorts(self, Arg2):
		"""Executes the unassignPorts operation on the server.

		Unassign hardware ports.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/vport])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			Arg2 (bool): If true, virtual ports will be deleted.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('UnassignPorts', payload=locals(), response_object=None)
