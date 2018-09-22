from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class QueueStatLearnedInformation(Base):
	"""The QueueStatLearnedInformation class encapsulates a system managed queueStatLearnedInformation node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the QueueStatLearnedInformation property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'queueStatLearnedInformation'

	def __init__(self, parent):
		super(QueueStatLearnedInformation, self).__init__(parent)

	@property
	def BytesTx(self):
		"""Indicates the number of transmitted bytes.

		Returns:
			str
		"""
		return self._get_attribute('bytesTx')

	@property
	def DataPathId(self):
		"""Indicates the Datapath ID of the switch.

		Returns:
			str
		"""
		return self._get_attribute('dataPathId')

	@property
	def DataPathIdAsHex(self):
		"""Indicates the Datapath ID, in hexadecimal format, of the switch.

		Returns:
			str
		"""
		return self._get_attribute('dataPathIdAsHex')

	@property
	def Duration(self):
		"""The time in seconds, for which the queue has been alive.

		Returns:
			number
		"""
		return self._get_attribute('duration')

	@property
	def DurationInNsec(self):
		"""The time in nanoseconds, for which the queue has been alive beyond Duration (sec).

		Returns:
			number
		"""
		return self._get_attribute('durationInNsec')

	@property
	def ErrorCode(self):
		"""Signifies the error code of the error received.

		Returns:
			str
		"""
		return self._get_attribute('errorCode')

	@property
	def ErrorType(self):
		"""Signifies the type of the error received.

		Returns:
			str
		"""
		return self._get_attribute('errorType')

	@property
	def Latency(self):
		"""Indicates the duration elapsed (in microsecond) between the learned info request and response.

		Returns:
			number
		"""
		return self._get_attribute('latency')

	@property
	def LocalIp(self):
		"""Indicates the local IP of the Controller.

		Returns:
			str
		"""
		return self._get_attribute('localIp')

	@property
	def NegotiatedVersion(self):
		"""Version of the protocol that has been negotiated between OpenFLow Controller and Switch.

		Returns:
			str
		"""
		return self._get_attribute('negotiatedVersion')

	@property
	def PacketsTx(self):
		"""Indicates the number of transmitted packets.

		Returns:
			str
		"""
		return self._get_attribute('packetsTx')

	@property
	def PortNumber(self):
		"""Indicates the port to which the queue belongs.

		Returns:
			number
		"""
		return self._get_attribute('portNumber')

	@property
	def QueueId(self):
		"""Indicates the Identifier of the queue.

		Returns:
			number
		"""
		return self._get_attribute('queueId')

	@property
	def RemoteIp(self):
		"""Indicates the IP of the remote end of the OF Channel.

		Returns:
			str
		"""
		return self._get_attribute('remoteIp')

	@property
	def ReplyState(self):
		"""Indicates the reply state of the switch.

		Returns:
			str
		"""
		return self._get_attribute('replyState')

	@property
	def TxErrors(self):
		"""Indicates the number of packets dropped due to overrun.

		Returns:
			str
		"""
		return self._get_attribute('txErrors')

	def find(self, BytesTx=None, DataPathId=None, DataPathIdAsHex=None, Duration=None, DurationInNsec=None, ErrorCode=None, ErrorType=None, Latency=None, LocalIp=None, NegotiatedVersion=None, PacketsTx=None, PortNumber=None, QueueId=None, RemoteIp=None, ReplyState=None, TxErrors=None):
		"""Finds and retrieves queueStatLearnedInformation data from the server.

		All named parameters support regex and can be used to selectively retrieve queueStatLearnedInformation data from the server.
		By default the find method takes no parameters and will retrieve all queueStatLearnedInformation data from the server.

		Args:
			BytesTx (str): Indicates the number of transmitted bytes.
			DataPathId (str): Indicates the Datapath ID of the switch.
			DataPathIdAsHex (str): Indicates the Datapath ID, in hexadecimal format, of the switch.
			Duration (number): The time in seconds, for which the queue has been alive.
			DurationInNsec (number): The time in nanoseconds, for which the queue has been alive beyond Duration (sec).
			ErrorCode (str): Signifies the error code of the error received.
			ErrorType (str): Signifies the type of the error received.
			Latency (number): Indicates the duration elapsed (in microsecond) between the learned info request and response.
			LocalIp (str): Indicates the local IP of the Controller.
			NegotiatedVersion (str): Version of the protocol that has been negotiated between OpenFLow Controller and Switch.
			PacketsTx (str): Indicates the number of transmitted packets.
			PortNumber (number): Indicates the port to which the queue belongs.
			QueueId (number): Indicates the Identifier of the queue.
			RemoteIp (str): Indicates the IP of the remote end of the OF Channel.
			ReplyState (str): Indicates the reply state of the switch.
			TxErrors (str): Indicates the number of packets dropped due to overrun.

		Returns:
			self: This instance with matching queueStatLearnedInformation data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of queueStatLearnedInformation data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the queueStatLearnedInformation data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
