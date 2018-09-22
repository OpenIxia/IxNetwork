from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class GroupStatBucketLearnedInformation(Base):
	"""The GroupStatBucketLearnedInformation class encapsulates a system managed groupStatBucketLearnedInformation node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the GroupStatBucketLearnedInformation property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'groupStatBucketLearnedInformation'

	def __init__(self, parent):
		super(GroupStatBucketLearnedInformation, self).__init__(parent)

	@property
	def ByteCount(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('byteCount')

	@property
	def DataPathId(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('dataPathId')

	@property
	def DataPathIdAsHex(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('dataPathIdAsHex')

	@property
	def GroupId(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('groupId')

	@property
	def LocalIp(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('localIp')

	@property
	def PacketCount(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('packetCount')

	@property
	def RemoteIp(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('remoteIp')

	def find(self, ByteCount=None, DataPathId=None, DataPathIdAsHex=None, GroupId=None, LocalIp=None, PacketCount=None, RemoteIp=None):
		"""Finds and retrieves groupStatBucketLearnedInformation data from the server.

		All named parameters support regex and can be used to selectively retrieve groupStatBucketLearnedInformation data from the server.
		By default the find method takes no parameters and will retrieve all groupStatBucketLearnedInformation data from the server.

		Args:
			ByteCount (str): NOT DEFINED
			DataPathId (str): NOT DEFINED
			DataPathIdAsHex (str): NOT DEFINED
			GroupId (str): NOT DEFINED
			LocalIp (str): NOT DEFINED
			PacketCount (str): NOT DEFINED
			RemoteIp (str): NOT DEFINED

		Returns:
			self: This instance with matching groupStatBucketLearnedInformation data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of groupStatBucketLearnedInformation data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the groupStatBucketLearnedInformation data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
