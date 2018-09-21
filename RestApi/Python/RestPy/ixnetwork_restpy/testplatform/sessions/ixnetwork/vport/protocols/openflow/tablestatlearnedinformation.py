from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class TableStatLearnedInformation(Base):
	"""The TableStatLearnedInformation class encapsulates a system managed tableStatLearnedInformation node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the TableStatLearnedInformation property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'tableStatLearnedInformation'

	def __init__(self, parent):
		super(TableStatLearnedInformation, self).__init__(parent)

	@property
	def ActiveCount(self):
		"""Indicates the number of active entries.

		Returns:
			number
		"""
		return self._get_attribute('activeCount')

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
	def ErrorCode(self):
		"""Signifies the error code of the error received

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
	def LookupCount(self):
		"""Indicates the number of packets looked up in table.

		Returns:
			str
		"""
		return self._get_attribute('lookupCount')

	@property
	def MatchedCount(self):
		"""Indicates the number of packets that hit table.

		Returns:
			str
		"""
		return self._get_attribute('matchedCount')

	@property
	def MaxEntries(self):
		"""Indicates the maximum number of entries supported.

		Returns:
			number
		"""
		return self._get_attribute('maxEntries')

	@property
	def NegotiatedVersion(self):
		"""Version of the protocol that has been negotiated between OpenFLow Controller and Switch.

		Returns:
			str
		"""
		return self._get_attribute('negotiatedVersion')

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
	def TableId(self):
		"""Indicates the Identifier of table.

		Returns:
			str
		"""
		return self._get_attribute('tableId')

	@property
	def TableName(self):
		"""Indicates a name of the table.

		Returns:
			str
		"""
		return self._get_attribute('tableName')

	@property
	def Wildcards(self):
		"""Indicates the Wildcards that are supported by the table.

		Returns:
			str
		"""
		return self._get_attribute('wildcards')

	def find(self, ActiveCount=None, DataPathId=None, DataPathIdAsHex=None, ErrorCode=None, ErrorType=None, Latency=None, LocalIp=None, LookupCount=None, MatchedCount=None, MaxEntries=None, NegotiatedVersion=None, RemoteIp=None, ReplyState=None, TableId=None, TableName=None, Wildcards=None):
		"""Finds and retrieves tableStatLearnedInformation data from the server.

		All named parameters support regex and can be used to selectively retrieve tableStatLearnedInformation data from the server.
		By default the find method takes no parameters and will retrieve all tableStatLearnedInformation data from the server.

		Args:
			ActiveCount (number): Indicates the number of active entries.
			DataPathId (str): Indicates the Datapath ID of the switch.
			DataPathIdAsHex (str): Indicates the Datapath ID, in hexadecimal format, of the switch.
			ErrorCode (str): Signifies the error code of the error received
			ErrorType (str): Signifies the type of the error received.
			Latency (number): Indicates the duration elapsed (in microsecond) between the learned info request and response.
			LocalIp (str): Indicates the local IP of the Controller.
			LookupCount (str): Indicates the number of packets looked up in table.
			MatchedCount (str): Indicates the number of packets that hit table.
			MaxEntries (number): Indicates the maximum number of entries supported.
			NegotiatedVersion (str): Version of the protocol that has been negotiated between OpenFLow Controller and Switch.
			RemoteIp (str): Indicates the IP of the remote end of the OF Channel.
			ReplyState (str): Indicates the reply state of the switch.
			TableId (str): Indicates the Identifier of table.
			TableName (str): Indicates a name of the table.
			Wildcards (str): Indicates the Wildcards that are supported by the table.

		Returns:
			self: This instance with matching tableStatLearnedInformation data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of tableStatLearnedInformation data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the tableStatLearnedInformation data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
