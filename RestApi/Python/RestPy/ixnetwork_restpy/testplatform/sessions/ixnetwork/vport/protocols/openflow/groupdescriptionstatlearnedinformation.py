from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class GroupDescriptionStatLearnedInformation(Base):
	"""The GroupDescriptionStatLearnedInformation class encapsulates a system managed groupDescriptionStatLearnedInformation node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the GroupDescriptionStatLearnedInformation property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'groupDescriptionStatLearnedInformation'

	def __init__(self, parent):
		super(GroupDescriptionStatLearnedInformation, self).__init__(parent)

	@property
	def GroupBucketDescStatLearnedInformation(self):
		"""An instance of the GroupBucketDescStatLearnedInformation class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.groupbucketdescstatlearnedinformation.GroupBucketDescStatLearnedInformation)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.groupbucketdescstatlearnedinformation import GroupBucketDescStatLearnedInformation
		return GroupBucketDescStatLearnedInformation(self)

	@property
	def DataPathId(self):
		"""The Data Path ID of the connected switch.

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
	def ErrorCode(self):
		"""The error code of the error received.

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
	def GroupId(self):
		"""A 32-bit integer uniquely identifying the group.

		Returns:
			number
		"""
		return self._get_attribute('groupId')

	@property
	def GroupType(self):
		"""Specify the group types supported by Switch.

		Returns:
			str
		"""
		return self._get_attribute('groupType')

	@property
	def Latency(self):
		"""The latency measurement for the OpenFlow channel.

		Returns:
			number
		"""
		return self._get_attribute('latency')

	@property
	def LocalIp(self):
		"""The local IP address of the selected interface.

		Returns:
			str
		"""
		return self._get_attribute('localIp')

	@property
	def NegotiatedVersion(self):
		"""The OpenFlow version supported by this configuration.

		Returns:
			str
		"""
		return self._get_attribute('negotiatedVersion')

	@property
	def NumberOfBucketStats(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('numberOfBucketStats')

	@property
	def RemoteIp(self):
		"""The Remote IP address of the selected interface.

		Returns:
			str
		"""
		return self._get_attribute('remoteIp')

	@property
	def ReplyState(self):
		"""The reply state of the OF Channel.

		Returns:
			str
		"""
		return self._get_attribute('replyState')

	def find(self, DataPathId=None, DataPathIdAsHex=None, ErrorCode=None, ErrorType=None, GroupId=None, GroupType=None, Latency=None, LocalIp=None, NegotiatedVersion=None, NumberOfBucketStats=None, RemoteIp=None, ReplyState=None):
		"""Finds and retrieves groupDescriptionStatLearnedInformation data from the server.

		All named parameters support regex and can be used to selectively retrieve groupDescriptionStatLearnedInformation data from the server.
		By default the find method takes no parameters and will retrieve all groupDescriptionStatLearnedInformation data from the server.

		Args:
			DataPathId (str): The Data Path ID of the connected switch.
			DataPathIdAsHex (str): The Data Path ID of the OpenFlow switch in hexadecimal format.
			ErrorCode (str): The error code of the error received.
			ErrorType (str): The type of the error received.
			GroupId (number): A 32-bit integer uniquely identifying the group.
			GroupType (str): Specify the group types supported by Switch.
			Latency (number): The latency measurement for the OpenFlow channel.
			LocalIp (str): The local IP address of the selected interface.
			NegotiatedVersion (str): The OpenFlow version supported by this configuration.
			NumberOfBucketStats (str): NOT DEFINED
			RemoteIp (str): The Remote IP address of the selected interface.
			ReplyState (str): The reply state of the OF Channel.

		Returns:
			self: This instance with matching groupDescriptionStatLearnedInformation data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of groupDescriptionStatLearnedInformation data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the groupDescriptionStatLearnedInformation data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
