from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class MeterConfigStatsLearnedInformation(Base):
	"""The MeterConfigStatsLearnedInformation class encapsulates a system managed meterConfigStatsLearnedInformation node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the MeterConfigStatsLearnedInformation property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'meterConfigStatsLearnedInformation'

	def __init__(self, parent):
		super(MeterConfigStatsLearnedInformation, self).__init__(parent)

	@property
	def MeterConfigStatsBandLearnedInformation(self):
		"""An instance of the MeterConfigStatsBandLearnedInformation class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.meterconfigstatsbandlearnedinformation.MeterConfigStatsBandLearnedInformation)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.meterconfigstatsbandlearnedinformation import MeterConfigStatsBandLearnedInformation
		return MeterConfigStatsBandLearnedInformation(self)

	@property
	def DataPathId(self):
		"""The Data Path identifier of the OpenFlow Controller.

		Returns:
			number
		"""
		return self._get_attribute('dataPathId')

	@property
	def DataPathIdAsHex(self):
		"""The Data Path identifier of the OpenFlow Controller in hexadecimal format.

		Returns:
			str
		"""
		return self._get_attribute('dataPathIdAsHex')

	@property
	def ErrorCode(self):
		"""The error code of the received error.

		Returns:
			str
		"""
		return self._get_attribute('errorCode')

	@property
	def ErrorType(self):
		"""The type of the error received.

		Returns:
			str
		"""
		return self._get_attribute('errorType')

	@property
	def Flags(self):
		"""Select the meter configuration flags from the list.

		Returns:
			str
		"""
		return self._get_attribute('flags')

	@property
	def LastErrorCode(self):
		"""The Last error code of the received error.

		Returns:
			str
		"""
		return self._get_attribute('lastErrorCode')

	@property
	def LastErrorType(self):
		"""The type of the Last error received.

		Returns:
			str
		"""
		return self._get_attribute('lastErrorType')

	@property
	def Latency(self):
		"""The latency measurement for the OpenFlow channel in microseconds.

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
	def MeterId(self):
		"""Specifies Meter ID

		Returns:
			number
		"""
		return self._get_attribute('meterId')

	@property
	def NegotiatedVersion(self):
		"""Version of the protocol that has been negotiated between OpenFLow Controller and Switch.

		Returns:
			str
		"""
		return self._get_attribute('negotiatedVersion')

	@property
	def NumberOfBands(self):
		"""Specify the number of Bands for this controller configuration. The default value is 1.

		Returns:
			number
		"""
		return self._get_attribute('numberOfBands')

	@property
	def RemoteIp(self):
		"""The Remote IP address of the selected interface.

		Returns:
			str
		"""
		return self._get_attribute('remoteIp')

	@property
	def ReplyState(self):
		"""The state of reply for the Open Flow channel.

		Returns:
			str
		"""
		return self._get_attribute('replyState')

	def find(self, DataPathId=None, DataPathIdAsHex=None, ErrorCode=None, ErrorType=None, Flags=None, LastErrorCode=None, LastErrorType=None, Latency=None, LocalIp=None, MeterId=None, NegotiatedVersion=None, NumberOfBands=None, RemoteIp=None, ReplyState=None):
		"""Finds and retrieves meterConfigStatsLearnedInformation data from the server.

		All named parameters support regex and can be used to selectively retrieve meterConfigStatsLearnedInformation data from the server.
		By default the find method takes no parameters and will retrieve all meterConfigStatsLearnedInformation data from the server.

		Args:
			DataPathId (number): The Data Path identifier of the OpenFlow Controller.
			DataPathIdAsHex (str): The Data Path identifier of the OpenFlow Controller in hexadecimal format.
			ErrorCode (str): The error code of the received error.
			ErrorType (str): The type of the error received.
			Flags (str): Select the meter configuration flags from the list.
			LastErrorCode (str): The Last error code of the received error.
			LastErrorType (str): The type of the Last error received.
			Latency (number): The latency measurement for the OpenFlow channel in microseconds.
			LocalIp (str): Indicates the local IP of the Controller.
			MeterId (number): Specifies Meter ID
			NegotiatedVersion (str): Version of the protocol that has been negotiated between OpenFLow Controller and Switch.
			NumberOfBands (number): Specify the number of Bands for this controller configuration. The default value is 1.
			RemoteIp (str): The Remote IP address of the selected interface.
			ReplyState (str): The state of reply for the Open Flow channel.

		Returns:
			self: This instance with matching meterConfigStatsLearnedInformation data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of meterConfigStatsLearnedInformation data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the meterConfigStatsLearnedInformation data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
