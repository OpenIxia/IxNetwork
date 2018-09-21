from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class GroupBucketDescStatLearnedInformation(Base):
	"""The GroupBucketDescStatLearnedInformation class encapsulates a system managed groupBucketDescStatLearnedInformation node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the GroupBucketDescStatLearnedInformation property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'groupBucketDescStatLearnedInformation'

	def __init__(self, parent):
		super(GroupBucketDescStatLearnedInformation, self).__init__(parent)

	@property
	def ActionCount(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('actionCount')

	@property
	def DataPathId(self):
		"""The Data Path ID of the OpenFlow switch.

		Returns:
			str
		"""
		return self._get_attribute('dataPathId')

	@property
	def DataPathIdAsHex(self):
		"""The Data Path ID of the OpenFlow switch in hexadecimal format.

		Returns:
			str
		"""
		return self._get_attribute('dataPathIdAsHex')

	@property
	def GroupId(self):
		"""A 32-bit integer uniquely identifying the group.

		Returns:
			number
		"""
		return self._get_attribute('groupId')

	@property
	def LocalIp(self):
		"""The Data Path ID of the OpenFlow switch.

		Returns:
			str
		"""
		return self._get_attribute('localIp')

	@property
	def RemoteIp(self):
		"""The Remote IP address of the selected interface.

		Returns:
			str
		"""
		return self._get_attribute('remoteIp')

	@property
	def WatchGroup(self):
		"""A group whose state determines whether this bucket is live or not. Default value OFPG_ANY(4,294,967,295) indicates that Watch Group is not specified in ofp_group_mod packets.

		Returns:
			number
		"""
		return self._get_attribute('watchGroup')

	@property
	def WatchPort(self):
		"""A Port whose state determines whether this bucket is live or not. Default value OFPP_ANY(4,294,967,295) indicates that Watch Port is not specified in ofp_group_mod packets.

		Returns:
			number
		"""
		return self._get_attribute('watchPort')

	@property
	def Weight(self):
		"""Specify the weight of buckets. The range allowed is 0-65535.

		Returns:
			number
		"""
		return self._get_attribute('weight')

	def find(self, ActionCount=None, DataPathId=None, DataPathIdAsHex=None, GroupId=None, LocalIp=None, RemoteIp=None, WatchGroup=None, WatchPort=None, Weight=None):
		"""Finds and retrieves groupBucketDescStatLearnedInformation data from the server.

		All named parameters support regex and can be used to selectively retrieve groupBucketDescStatLearnedInformation data from the server.
		By default the find method takes no parameters and will retrieve all groupBucketDescStatLearnedInformation data from the server.

		Args:
			ActionCount (number): NOT DEFINED
			DataPathId (str): The Data Path ID of the OpenFlow switch.
			DataPathIdAsHex (str): The Data Path ID of the OpenFlow switch in hexadecimal format.
			GroupId (number): A 32-bit integer uniquely identifying the group.
			LocalIp (str): The Data Path ID of the OpenFlow switch.
			RemoteIp (str): The Remote IP address of the selected interface.
			WatchGroup (number): A group whose state determines whether this bucket is live or not. Default value OFPG_ANY(4,294,967,295) indicates that Watch Group is not specified in ofp_group_mod packets.
			WatchPort (number): A Port whose state determines whether this bucket is live or not. Default value OFPP_ANY(4,294,967,295) indicates that Watch Port is not specified in ofp_group_mod packets.
			Weight (number): Specify the weight of buckets. The range allowed is 0-65535.

		Returns:
			self: This instance with matching groupBucketDescStatLearnedInformation data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of groupBucketDescStatLearnedInformation data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the groupBucketDescStatLearnedInformation data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
