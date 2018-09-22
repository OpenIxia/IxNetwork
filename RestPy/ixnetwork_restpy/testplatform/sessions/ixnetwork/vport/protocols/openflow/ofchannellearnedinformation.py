from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class OfChannelLearnedInformation(Base):
	"""The OfChannelLearnedInformation class encapsulates a system managed ofChannelLearnedInformation node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the OfChannelLearnedInformation property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'ofChannelLearnedInformation'

	def __init__(self, parent):
		super(OfChannelLearnedInformation, self).__init__(parent)

	@property
	def ControllerAuxiliaryConnectionLearnedInfo(self):
		"""An instance of the ControllerAuxiliaryConnectionLearnedInfo class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.controllerauxiliaryconnectionlearnedinfo.ControllerAuxiliaryConnectionLearnedInfo)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.controllerauxiliaryconnectionlearnedinfo import ControllerAuxiliaryConnectionLearnedInfo
		return ControllerAuxiliaryConnectionLearnedInfo(self)

	@property
	def OfChannelPortsLearnedInformation(self):
		"""An instance of the OfChannelPortsLearnedInformation class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.ofchannelportslearnedinformation.OfChannelPortsLearnedInformation)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.ofchannelportslearnedinformation import OfChannelPortsLearnedInformation
		return OfChannelPortsLearnedInformation(self)

	@property
	def ActionsSupported(self):
		"""Signifies the types of actions supported by the switch.

		Returns:
			str
		"""
		return self._get_attribute('actionsSupported')

	@property
	def Capabilities(self):
		"""Signifies the capabilities of the switch.

		Returns:
			str
		"""
		return self._get_attribute('capabilities')

	@property
	def DataPathId(self):
		"""Indicates the datapath ID of the OpenFlow switch.

		Returns:
			str
		"""
		return self._get_attribute('dataPathId')

	@property
	def DataPathIdAsHex(self):
		"""Indicates the datapath ID of the OpenFlow switch in hexadecimal format.

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
		"""The generation ID number.

		Returns:
			str
		"""
		return self._get_attribute('generationId')

	@property
	def LastErrorCode(self):
		"""Signifies the error code of the last error received.

		Returns:
			str
		"""
		return self._get_attribute('lastErrorCode')

	@property
	def LastErrorType(self):
		"""Signifies the type of the last error received.

		Returns:
			str
		"""
		return self._get_attribute('lastErrorType')

	@property
	def LocalIp(self):
		"""Signifies the local IP address of the selected interface.

		Returns:
			str
		"""
		return self._get_attribute('localIp')

	@property
	def LocalPortNumber(self):
		"""Signifies the local port number identifier.

		Returns:
			number
		"""
		return self._get_attribute('localPortNumber')

	@property
	def MaxBufferSize(self):
		"""Signifies the maximum configurable buffer size.

		Returns:
			number
		"""
		return self._get_attribute('maxBufferSize')

	@property
	def NegotiatedVersion(self):
		"""Version of the protocol that has been negotiated between OpenFLow Controller and Switch.

		Returns:
			number
		"""
		return self._get_attribute('negotiatedVersion')

	@property
	def NumberOfErrorsReceived(self):
		"""Signifies the total number of errors received from the emulation start time.

		Returns:
			number
		"""
		return self._get_attribute('numberOfErrorsReceived')

	@property
	def NumberOfPorts(self):
		"""Signifies the number of ports used.

		Returns:
			number
		"""
		return self._get_attribute('numberOfPorts')

	@property
	def NumberOfTables(self):
		"""Signifies the number of tables supported.

		Returns:
			number
		"""
		return self._get_attribute('numberOfTables')

	@property
	def RemoteIp(self):
		"""Signifies the Remote IP address of the selected interface.

		Returns:
			str
		"""
		return self._get_attribute('remoteIp')

	@property
	def RemotePortNumber(self):
		"""Signifies the remote port number identifier.

		Returns:
			number
		"""
		return self._get_attribute('remotePortNumber')

	@property
	def ReplyState(self):
		"""Signifies the reply state of the OF Channel.

		Returns:
			str
		"""
		return self._get_attribute('replyState')

	@property
	def Role(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('role')

	@property
	def SessionType(self):
		"""Signifies the type of OpenFlow session supported by the switch.

		Returns:
			str
		"""
		return self._get_attribute('sessionType')

	def find(self, ActionsSupported=None, Capabilities=None, DataPathId=None, DataPathIdAsHex=None, FlowRate=None, GenerationId=None, LastErrorCode=None, LastErrorType=None, LocalIp=None, LocalPortNumber=None, MaxBufferSize=None, NegotiatedVersion=None, NumberOfErrorsReceived=None, NumberOfPorts=None, NumberOfTables=None, RemoteIp=None, RemotePortNumber=None, ReplyState=None, Role=None, SessionType=None):
		"""Finds and retrieves ofChannelLearnedInformation data from the server.

		All named parameters support regex and can be used to selectively retrieve ofChannelLearnedInformation data from the server.
		By default the find method takes no parameters and will retrieve all ofChannelLearnedInformation data from the server.

		Args:
			ActionsSupported (str): Signifies the types of actions supported by the switch.
			Capabilities (str): Signifies the capabilities of the switch.
			DataPathId (str): Indicates the datapath ID of the OpenFlow switch.
			DataPathIdAsHex (str): Indicates the datapath ID of the OpenFlow switch in hexadecimal format.
			FlowRate (number): NOT DEFINED
			GenerationId (str): The generation ID number.
			LastErrorCode (str): Signifies the error code of the last error received.
			LastErrorType (str): Signifies the type of the last error received.
			LocalIp (str): Signifies the local IP address of the selected interface.
			LocalPortNumber (number): Signifies the local port number identifier.
			MaxBufferSize (number): Signifies the maximum configurable buffer size.
			NegotiatedVersion (number): Version of the protocol that has been negotiated between OpenFLow Controller and Switch.
			NumberOfErrorsReceived (number): Signifies the total number of errors received from the emulation start time.
			NumberOfPorts (number): Signifies the number of ports used.
			NumberOfTables (number): Signifies the number of tables supported.
			RemoteIp (str): Signifies the Remote IP address of the selected interface.
			RemotePortNumber (number): Signifies the remote port number identifier.
			ReplyState (str): Signifies the reply state of the OF Channel.
			Role (str): NOT DEFINED
			SessionType (str): Signifies the type of OpenFlow session supported by the switch.

		Returns:
			self: This instance with matching ofChannelLearnedInformation data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of ofChannelLearnedInformation data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the ofChannelLearnedInformation data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)

	def AddRecordForTrigger(self):
		"""Executes the addRecordForTrigger operation on the server.

		This describes the record added for trigger settings.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=ofChannelLearnedInformation)): The method internally set Arg1 to the current href for this instance

		Returns:
			bool: NOT DEFINED

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('AddRecordForTrigger', payload=locals(), response_object=None)

	def ConfigureOfChannel(self):
		"""Executes the configureOfChannel operation on the server.

		It is a command that will configure controller OF channel from controller OF channel learned information.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=ofChannelLearnedInformation)): The method internally set Arg1 to the current href for this instance

		Returns:
			bool: NOT DEFINED

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('ConfigureOfChannel', payload=locals(), response_object=None)
