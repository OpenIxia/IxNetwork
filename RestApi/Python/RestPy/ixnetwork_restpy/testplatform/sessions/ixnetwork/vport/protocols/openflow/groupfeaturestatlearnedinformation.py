from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class GroupFeatureStatLearnedInformation(Base):
	"""The GroupFeatureStatLearnedInformation class encapsulates a system managed groupFeatureStatLearnedInformation node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the GroupFeatureStatLearnedInformation property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'groupFeatureStatLearnedInformation'

	def __init__(self, parent):
		super(GroupFeatureStatLearnedInformation, self).__init__(parent)

	@property
	def ActionsAll(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('actionsAll')

	@property
	def ActionsFastFailOver(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('actionsFastFailOver')

	@property
	def ActionsIndirect(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('actionsIndirect')

	@property
	def ActionsSelect(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('actionsSelect')

	@property
	def DataPathIdAsHex(self):
		"""The Data Path ID of the OpenFlow switch in hexadecimal format.

		Returns:
			str
		"""
		return self._get_attribute('dataPathIdAsHex')

	@property
	def DatapathId(self):
		"""The Data Path ID of the connected switch.

		Returns:
			str
		"""
		return self._get_attribute('datapathId')

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
	def GroupCapabilities(self):
		"""Specify the group capabilities supported by Switch.

		Returns:
			str
		"""
		return self._get_attribute('groupCapabilities')

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
	def MaxGroupsAll(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('maxGroupsAll')

	@property
	def MaxGroupsFastFailOver(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('maxGroupsFastFailOver')

	@property
	def MaxGroupsIndirect(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('maxGroupsIndirect')

	@property
	def MaxGroupsSelect(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('maxGroupsSelect')

	@property
	def NegotiatedVersion(self):
		"""The OpenFlow version supported by this configuration.

		Returns:
			str
		"""
		return self._get_attribute('negotiatedVersion')

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

	def find(self, ActionsAll=None, ActionsFastFailOver=None, ActionsIndirect=None, ActionsSelect=None, DataPathIdAsHex=None, DatapathId=None, ErrorCode=None, ErrorType=None, GroupCapabilities=None, GroupType=None, Latency=None, LocalIp=None, MaxGroupsAll=None, MaxGroupsFastFailOver=None, MaxGroupsIndirect=None, MaxGroupsSelect=None, NegotiatedVersion=None, RemoteIp=None, ReplyState=None):
		"""Finds and retrieves groupFeatureStatLearnedInformation data from the server.

		All named parameters support regex and can be used to selectively retrieve groupFeatureStatLearnedInformation data from the server.
		By default the find method takes no parameters and will retrieve all groupFeatureStatLearnedInformation data from the server.

		Args:
			ActionsAll (str): NOT DEFINED
			ActionsFastFailOver (str): NOT DEFINED
			ActionsIndirect (str): NOT DEFINED
			ActionsSelect (str): NOT DEFINED
			DataPathIdAsHex (str): The Data Path ID of the OpenFlow switch in hexadecimal format.
			DatapathId (str): The Data Path ID of the connected switch.
			ErrorCode (str): The error code of the error received.
			ErrorType (str): The type of the error received.
			GroupCapabilities (str): Specify the group capabilities supported by Switch.
			GroupType (str): Specify the group types supported by Switch.
			Latency (number): The latency measurement for the OpenFlow channel.
			LocalIp (str): The local IP address of the selected interface.
			MaxGroupsAll (number): NOT DEFINED
			MaxGroupsFastFailOver (number): NOT DEFINED
			MaxGroupsIndirect (number): NOT DEFINED
			MaxGroupsSelect (number): NOT DEFINED
			NegotiatedVersion (str): The OpenFlow version supported by this configuration.
			RemoteIp (str): The Remote IP address of the selected interface.
			ReplyState (str): The reply state of the OF Channel.

		Returns:
			self: This instance with matching groupFeatureStatLearnedInformation data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of groupFeatureStatLearnedInformation data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the groupFeatureStatLearnedInformation data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
