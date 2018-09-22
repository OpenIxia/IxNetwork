from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class HighLevelStream(Base):
	"""The HighLevelStream class encapsulates a system managed highLevelStream node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the HighLevelStream property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'highLevelStream'

	def __init__(self, parent):
		super(HighLevelStream, self).__init__(parent)

	@property
	def FramePayload(self):
		"""An instance of the FramePayload class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.highlevelstream.framepayload.framepayload.FramePayload)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.highlevelstream.framepayload.framepayload import FramePayload
		return FramePayload(self)._select()

	@property
	def FrameRate(self):
		"""An instance of the FrameRate class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.highlevelstream.framerate.framerate.FrameRate)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.highlevelstream.framerate.framerate import FrameRate
		return FrameRate(self)._select()

	@property
	def FrameSize(self):
		"""An instance of the FrameSize class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.highlevelstream.framesize.framesize.FrameSize)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.highlevelstream.framesize.framesize import FrameSize
		return FrameSize(self)._select()

	@property
	def Stack(self):
		"""An instance of the Stack class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.highlevelstream.stack.stack.Stack)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.highlevelstream.stack.stack import Stack
		return Stack(self)

	@property
	def StackLink(self):
		"""An instance of the StackLink class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.highlevelstream.stacklink.stacklink.StackLink)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.highlevelstream.stacklink.stacklink import StackLink
		return StackLink(self)

	@property
	def TableUdf(self):
		"""An instance of the TableUdf class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.highlevelstream.tableudf.tableudf.TableUdf)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.highlevelstream.tableudf.tableudf import TableUdf
		return TableUdf(self)

	@property
	def TransmissionControl(self):
		"""An instance of the TransmissionControl class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.highlevelstream.transmissioncontrol.transmissioncontrol.TransmissionControl)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.highlevelstream.transmissioncontrol.transmissioncontrol import TransmissionControl
		return TransmissionControl(self)._select()

	@property
	def Udf(self):
		"""An instance of the Udf class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.highlevelstream.udf.udf.Udf)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.highlevelstream.udf.udf import Udf
		return Udf(self)

	@property
	def AppliedFrameSize(self):
		"""(Read only) Indicates the applied frame size of the high level stream.

		Returns:
			str
		"""
		return self._get_attribute('appliedFrameSize')

	@property
	def AppliedPacketCount(self):
		"""(Read only) Indicates the aplied packet count of the high level stream.

		Returns:
			number
		"""
		return self._get_attribute('appliedPacketCount')

	@property
	def Crc(self):
		"""The Cyclic Redundancy Check frame of the configured high level stream.

		Returns:
			str(badCrc|goodCrc)
		"""
		return self._get_attribute('crc')
	@Crc.setter
	def Crc(self, value):
		self._set_attribute('crc', value)

	@property
	def CurrentPacketCount(self):
		"""(Read only) Denotes the number of packets.

		Returns:
			number
		"""
		return self._get_attribute('currentPacketCount')

	@property
	def DestinationMacMode(self):
		"""The mode in which the Destination MAC Address is configured, either manual or ARP.

		Returns:
			str(arp|manual)
		"""
		return self._get_attribute('destinationMacMode')
	@DestinationMacMode.setter
	def DestinationMacMode(self, value):
		self._set_attribute('destinationMacMode', value)

	@property
	def Distributions(self):
		"""Denotes the distribution of the high level stream.

		Returns:
			list(dict(arg1:str,arg2:str))
		"""
		return self._get_attribute('distributions')

	@property
	def Enabled(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def EncapsulationName(self):
		"""Name of the configured encapsulation type.

		Returns:
			str
		"""
		return self._get_attribute('encapsulationName')

	@property
	def EndpointSetId(self):
		"""The ID of the configured endpoint set.

		Returns:
			number
		"""
		return self._get_attribute('endpointSetId')

	@property
	def Name(self):
		"""An alphanumeric string that returns the name of the field.

		Returns:
			str
		"""
		return self._get_attribute('name')
	@Name.setter
	def Name(self, value):
		self._set_attribute('name', value)

	@property
	def OverSubscribed(self):
		"""If true, the rate is oversubscribed.

		Returns:
			bool
		"""
		return self._get_attribute('overSubscribed')

	@property
	def Pause(self):
		"""If true then pause is enabled.

		Returns:
			bool
		"""
		return self._get_attribute('pause')
	@Pause.setter
	def Pause(self, value):
		self._set_attribute('pause', value)

	@property
	def PreambleCustomSize(self):
		"""Customizes the preamble size of the frame.

		Returns:
			number
		"""
		return self._get_attribute('preambleCustomSize')
	@PreambleCustomSize.setter
	def PreambleCustomSize(self, value):
		self._set_attribute('preambleCustomSize', value)

	@property
	def PreambleFrameSizeMode(self):
		"""The starting size of the frame.

		Returns:
			str(auto|custom)
		"""
		return self._get_attribute('preambleFrameSizeMode')
	@PreambleFrameSizeMode.setter
	def PreambleFrameSizeMode(self, value):
		self._set_attribute('preambleFrameSizeMode', value)

	@property
	def RxPortIds(self):
		"""A list of virtual ports that are the receiving ports

		Returns:
			list(str[None|/api/v1/sessions/1/ixnetwork/lag|/api/v1/sessions/1/ixnetwork/vport])
		"""
		return self._get_attribute('rxPortIds')
	@RxPortIds.setter
	def RxPortIds(self, value):
		self._set_attribute('rxPortIds', value)

	@property
	def RxPortNames(self):
		"""A list of names from the receiving virtual ports.

		Returns:
			list(str)
		"""
		return self._get_attribute('rxPortNames')

	@property
	def State(self):
		"""(Read only) Denotes the current state of the stream.

		Returns:
			str
		"""
		return self._get_attribute('state')

	@property
	def Suspend(self):
		"""Suspends all traffic on this high level stream.

		Returns:
			bool
		"""
		return self._get_attribute('suspend')
	@Suspend.setter
	def Suspend(self, value):
		self._set_attribute('suspend', value)

	@property
	def TxPortId(self):
		"""The virtual port that is the transmitting port.

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/lag|/api/v1/sessions/1/ixnetwork/vport)
		"""
		return self._get_attribute('txPortId')
	@TxPortId.setter
	def TxPortId(self, value):
		self._set_attribute('txPortId', value)

	@property
	def TxPortName(self):
		"""The name of the virtual port that is the transmitting port.

		Returns:
			str
		"""
		return self._get_attribute('txPortName')

	def find(self, AppliedFrameSize=None, AppliedPacketCount=None, Crc=None, CurrentPacketCount=None, DestinationMacMode=None, Distributions=None, Enabled=None, EncapsulationName=None, EndpointSetId=None, Name=None, OverSubscribed=None, Pause=None, PreambleCustomSize=None, PreambleFrameSizeMode=None, RxPortIds=None, RxPortNames=None, State=None, Suspend=None, TxPortId=None, TxPortName=None):
		"""Finds and retrieves highLevelStream data from the server.

		All named parameters support regex and can be used to selectively retrieve highLevelStream data from the server.
		By default the find method takes no parameters and will retrieve all highLevelStream data from the server.

		Args:
			AppliedFrameSize (str): (Read only) Indicates the applied frame size of the high level stream.
			AppliedPacketCount (number): (Read only) Indicates the aplied packet count of the high level stream.
			Crc (str(badCrc|goodCrc)): The Cyclic Redundancy Check frame of the configured high level stream.
			CurrentPacketCount (number): (Read only) Denotes the number of packets.
			DestinationMacMode (str(arp|manual)): The mode in which the Destination MAC Address is configured, either manual or ARP.
			Distributions (list(dict(arg1:str,arg2:str))): Denotes the distribution of the high level stream.
			Enabled (bool): 
			EncapsulationName (str): Name of the configured encapsulation type.
			EndpointSetId (number): The ID of the configured endpoint set.
			Name (str): An alphanumeric string that returns the name of the field.
			OverSubscribed (bool): If true, the rate is oversubscribed.
			Pause (bool): If true then pause is enabled.
			PreambleCustomSize (number): Customizes the preamble size of the frame.
			PreambleFrameSizeMode (str(auto|custom)): The starting size of the frame.
			RxPortIds (list(str[None|/api/v1/sessions/1/ixnetwork/lag|/api/v1/sessions/1/ixnetwork/vport])): A list of virtual ports that are the receiving ports
			RxPortNames (list(str)): A list of names from the receiving virtual ports.
			State (str): (Read only) Denotes the current state of the stream.
			Suspend (bool): Suspends all traffic on this high level stream.
			TxPortId (str(None|/api/v1/sessions/1/ixnetwork/lag|/api/v1/sessions/1/ixnetwork/vport)): The virtual port that is the transmitting port.
			TxPortName (str): The name of the virtual port that is the transmitting port.

		Returns:
			self: This instance with matching highLevelStream data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of highLevelStream data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the highLevelStream data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)

	def DeleteQuickFlowGroups(self):
		"""Executes the deleteQuickFlowGroups operation on the server.

		Deletes a list of quick flow groups.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=highLevelStream])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('DeleteQuickFlowGroups', payload=locals(), response_object=None)

	def PreviewFlowPackets(self, Arg2, Arg3):
		"""Executes the previewFlowPackets operation on the server.

		Preview packets for selected highLevelstream

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=highLevelStream)): The method internally set Arg1 to the current href for this instance
			Arg2 (number): 
			Arg3 (number): 

		Returns:
			dict(arg1:number,arg2:number,arg3:list[str],arg4:list[list[str]]): No return value.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('PreviewFlowPackets', payload=locals(), response_object=None)

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
