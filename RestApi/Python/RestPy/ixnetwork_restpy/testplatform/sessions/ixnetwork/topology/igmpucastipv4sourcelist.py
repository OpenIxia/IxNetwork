from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class IgmpUcastIPv4SourceList(Base):
	"""The IgmpUcastIPv4SourceList class encapsulates a required igmpUcastIPv4SourceList node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the IgmpUcastIPv4SourceList property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'igmpUcastIPv4SourceList'

	def __init__(self, parent):
		super(IgmpUcastIPv4SourceList, self).__init__(parent)

	@property
	def Active(self):
		"""Activate/Deactivate Configuration

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('active')

	@property
	def Count(self):
		"""Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group

		Returns:
			number
		"""
		return self._get_attribute('count')

	@property
	def DescriptiveName(self):
		"""Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context

		Returns:
			str
		"""
		return self._get_attribute('descriptiveName')

	@property
	def Name(self):
		"""Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			str
		"""
		return self._get_attribute('name')
	@Name.setter
	def Name(self, value):
		self._set_attribute('name', value)

	@property
	def StartUcastAddr(self):
		"""Start Multicast Address

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('startUcastAddr')

	@property
	def State(self):
		"""Indicates the state of the groups in the range

		Returns:
			list(str[iptv|joined|notJoined|notStarted])
		"""
		return self._get_attribute('state')

	@property
	def UcastAddrIncr(self):
		"""Source Address Increment

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('ucastAddrIncr')

	@property
	def UcastSrcAddrCnt(self):
		"""Source Address Count

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('ucastSrcAddrCnt')

	def IgmpJoinSource(self):
		"""Executes the igmpJoinSource operation on the server.

		Join Source

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('IgmpJoinSource', payload=locals(), response_object=None)

	def IgmpJoinSource(self, SessionIndices):
		"""Executes the igmpJoinSource operation on the server.

		Join Source

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('IgmpJoinSource', payload=locals(), response_object=None)

	def IgmpJoinSource(self, SessionIndices):
		"""Executes the igmpJoinSource operation on the server.

		Join Source

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('IgmpJoinSource', payload=locals(), response_object=None)

	def IgmpLeaveSource(self):
		"""Executes the igmpLeaveSource operation on the server.

		Leave Source

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('IgmpLeaveSource', payload=locals(), response_object=None)

	def IgmpLeaveSource(self, SessionIndices):
		"""Executes the igmpLeaveSource operation on the server.

		Leave Source

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('IgmpLeaveSource', payload=locals(), response_object=None)

	def IgmpLeaveSource(self, SessionIndices):
		"""Executes the igmpLeaveSource operation on the server.

		Leave Source

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('IgmpLeaveSource', payload=locals(), response_object=None)

	def Join(self, Arg2):
		"""Executes the join operation on the server.

		Sends a Join on selected Source Ranges

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally set Arg1 to the current href for this instance
			Arg2 (list(number)): List of indices into the source range grid

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('Join', payload=locals(), response_object=None)

	def Leave(self, Arg2):
		"""Executes the leave operation on the server.

		Sends a Leave on selected Source Range

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally set Arg1 to the current href for this instance
			Arg2 (list(number)): List of indices into the source range grid

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('Leave', payload=locals(), response_object=None)
