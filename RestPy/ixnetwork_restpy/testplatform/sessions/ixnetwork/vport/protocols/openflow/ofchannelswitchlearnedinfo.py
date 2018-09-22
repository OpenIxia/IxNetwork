from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class OfChannelSwitchLearnedInfo(Base):
	"""The OfChannelSwitchLearnedInfo class encapsulates a system managed ofChannelSwitchLearnedInfo node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the OfChannelSwitchLearnedInfo property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'ofChannelSwitchLearnedInfo'

	def __init__(self, parent):
		super(OfChannelSwitchLearnedInfo, self).__init__(parent)

	@property
	def OfChannelPortsSwitchLearnedInfo(self):
		"""An instance of the OfChannelPortsSwitchLearnedInfo class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.ofchannelportsswitchlearnedinfo.OfChannelPortsSwitchLearnedInfo)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.ofchannelportsswitchlearnedinfo import OfChannelPortsSwitchLearnedInfo
		return OfChannelPortsSwitchLearnedInfo(self)

	@property
	def OfChannelSessionPeersLearnedInformation(self):
		"""An instance of the OfChannelSessionPeersLearnedInformation class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.ofchannelsessionpeerslearnedinformation.OfChannelSessionPeersLearnedInformation)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.ofchannelsessionpeerslearnedinformation import OfChannelSessionPeersLearnedInformation
		return OfChannelSessionPeersLearnedInformation(self)

	@property
	def ActionsSupported(self):
		"""This describes the actions supported by the switch.

		Returns:
			str
		"""
		return self._get_attribute('actionsSupported')

	@property
	def AveragePacketInReplyDelay(self):
		"""This describes the average delay between Packet-In sent from Switch and reply received from Controller.

		Returns:
			number
		"""
		return self._get_attribute('averagePacketInReplyDelay')
	@AveragePacketInReplyDelay.setter
	def AveragePacketInReplyDelay(self, value):
		self._set_attribute('averagePacketInReplyDelay', value)

	@property
	def Capabilities(self):
		"""This describes the OF Channel capabilities of the switch.

		Returns:
			str
		"""
		return self._get_attribute('capabilities')

	@property
	def ConfigFlags(self):
		"""This describes the Flags for fragmentation handling.

		Returns:
			str
		"""
		return self._get_attribute('configFlags')

	@property
	def ConfiguredPacketInReplyCount(self):
		"""This describes the Packet-In sent from Switch from configured Packet-In Ranges.

		Returns:
			number
		"""
		return self._get_attribute('configuredPacketInReplyCount')
	@ConfiguredPacketInReplyCount.setter
	def ConfiguredPacketInReplyCount(self, value):
		self._set_attribute('configuredPacketInReplyCount', value)

	@property
	def ConfiguredPacketInSentCount(self):
		"""This describes the Packet-In reply received from Controller for Packet-In sent.

		Returns:
			number
		"""
		return self._get_attribute('configuredPacketInSentCount')
	@ConfiguredPacketInSentCount.setter
	def ConfiguredPacketInSentCount(self, value):
		self._set_attribute('configuredPacketInSentCount', value)

	@property
	def DataPathId(self):
		"""This describes the datapath ID of the switch.

		Returns:
			str
		"""
		return self._get_attribute('dataPathId')

	@property
	def DataPathIdAsHex(self):
		"""This describes the datapath ID, in hexadecimal format, of the switch.

		Returns:
			str
		"""
		return self._get_attribute('dataPathIdAsHex')

	@property
	def FlowRate(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('flowRate')

	@property
	def GenerationId(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('generationId')

	@property
	def LastErrorCode(self):
		"""This describes the code for the last error received.

		Returns:
			str
		"""
		return self._get_attribute('lastErrorCode')

	@property
	def LastErrorType(self):
		"""This describes the type of error for the last error received.

		Returns:
			str
		"""
		return self._get_attribute('lastErrorType')

	@property
	def LocalIp(self):
		"""This describes the local IP address of the switch.

		Returns:
			str
		"""
		return self._get_attribute('localIp')

	@property
	def MaxBufferSize(self):
		"""This describes the maximum number of packets that can be stored in the buffer of the switch at a time.

		Returns:
			number
		"""
		return self._get_attribute('maxBufferSize')

	@property
	def MaxPacketInBytes(self):
		"""This describes the max amount of data to be sent in the Packet-In message.

		Returns:
			number
		"""
		return self._get_attribute('maxPacketInBytes')

	@property
	def NegotiatedVersion(self):
		"""This describes the OpenFlow version supported by this configuration.

		Returns:
			number
		"""
		return self._get_attribute('negotiatedVersion')

	@property
	def NumberOfAuxiliaryConnection(self):
		"""This describes the number of auxiliary connections.

		Returns:
			number
		"""
		return self._get_attribute('numberOfAuxiliaryConnection')
	@NumberOfAuxiliaryConnection.setter
	def NumberOfAuxiliaryConnection(self, value):
		self._set_attribute('numberOfAuxiliaryConnection', value)

	@property
	def NumberOfErrorsSent(self):
		"""This describes the number of errors received by the switch.

		Returns:
			number
		"""
		return self._get_attribute('numberOfErrorsSent')

	@property
	def NumberOfPorts(self):
		"""This describes the number of ports in the switch.

		Returns:
			number
		"""
		return self._get_attribute('numberOfPorts')

	@property
	def NumberofTable(self):
		"""This describes the number of tables in the switch.

		Returns:
			number
		"""
		return self._get_attribute('numberofTable')

	@property
	def RemoteIp(self):
		"""This describes the IP address of the remote end of the OF Channel.

		Returns:
			str
		"""
		return self._get_attribute('remoteIp')

	@property
	def RemotePortNumber(self):
		"""This describes the TCP port number of the remote end of the OF Channel.

		Returns:
			number
		"""
		return self._get_attribute('remotePortNumber')
	@RemotePortNumber.setter
	def RemotePortNumber(self, value):
		self._set_attribute('remotePortNumber', value)

	@property
	def SessionType(self):
		"""This describes the type of OpenFlow session.

		Returns:
			str
		"""
		return self._get_attribute('sessionType')

	def find(self, ActionsSupported=None, AveragePacketInReplyDelay=None, Capabilities=None, ConfigFlags=None, ConfiguredPacketInReplyCount=None, ConfiguredPacketInSentCount=None, DataPathId=None, DataPathIdAsHex=None, FlowRate=None, GenerationId=None, LastErrorCode=None, LastErrorType=None, LocalIp=None, MaxBufferSize=None, MaxPacketInBytes=None, NegotiatedVersion=None, NumberOfAuxiliaryConnection=None, NumberOfErrorsSent=None, NumberOfPorts=None, NumberofTable=None, RemoteIp=None, RemotePortNumber=None, SessionType=None):
		"""Finds and retrieves ofChannelSwitchLearnedInfo data from the server.

		All named parameters support regex and can be used to selectively retrieve ofChannelSwitchLearnedInfo data from the server.
		By default the find method takes no parameters and will retrieve all ofChannelSwitchLearnedInfo data from the server.

		Args:
			ActionsSupported (str): This describes the actions supported by the switch.
			AveragePacketInReplyDelay (number): This describes the average delay between Packet-In sent from Switch and reply received from Controller.
			Capabilities (str): This describes the OF Channel capabilities of the switch.
			ConfigFlags (str): This describes the Flags for fragmentation handling.
			ConfiguredPacketInReplyCount (number): This describes the Packet-In sent from Switch from configured Packet-In Ranges.
			ConfiguredPacketInSentCount (number): This describes the Packet-In reply received from Controller for Packet-In sent.
			DataPathId (str): This describes the datapath ID of the switch.
			DataPathIdAsHex (str): This describes the datapath ID, in hexadecimal format, of the switch.
			FlowRate (number): NOT DEFINED
			GenerationId (number): NOT DEFINED
			LastErrorCode (str): This describes the code for the last error received.
			LastErrorType (str): This describes the type of error for the last error received.
			LocalIp (str): This describes the local IP address of the switch.
			MaxBufferSize (number): This describes the maximum number of packets that can be stored in the buffer of the switch at a time.
			MaxPacketInBytes (number): This describes the max amount of data to be sent in the Packet-In message.
			NegotiatedVersion (number): This describes the OpenFlow version supported by this configuration.
			NumberOfAuxiliaryConnection (number): This describes the number of auxiliary connections.
			NumberOfErrorsSent (number): This describes the number of errors received by the switch.
			NumberOfPorts (number): This describes the number of ports in the switch.
			NumberofTable (number): This describes the number of tables in the switch.
			RemoteIp (str): This describes the IP address of the remote end of the OF Channel.
			RemotePortNumber (number): This describes the TCP port number of the remote end of the OF Channel.
			SessionType (str): This describes the type of OpenFlow session.

		Returns:
			self: This instance with matching ofChannelSwitchLearnedInfo data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of ofChannelSwitchLearnedInfo data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the ofChannelSwitchLearnedInfo data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)

	def AddRecordForTrigger(self):
		"""Executes the addRecordForTrigger operation on the server.

		API to add record for trigger to be sent.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=ofChannelSwitchLearnedInfo)): The method internally set Arg1 to the current href for this instance

		Returns:
			bool: NOT DEFINED

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('AddRecordForTrigger', payload=locals(), response_object=None)
