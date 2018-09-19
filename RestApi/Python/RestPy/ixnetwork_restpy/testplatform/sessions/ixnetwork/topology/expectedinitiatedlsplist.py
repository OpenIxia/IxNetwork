from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class ExpectedInitiatedLspList(Base):
	"""The ExpectedInitiatedLspList class encapsulates a required expectedInitiatedLspList node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the ExpectedInitiatedLspList property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'expectedInitiatedLspList'

	def __init__(self, parent):
		super(ExpectedInitiatedLspList, self).__init__(parent)

	@property
	def Tag(self):
		"""An instance of the Tag class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.tag.Tag)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.tag import Tag
		return Tag(self)

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
	def InsertIpv6ExplicitNull(self):
		"""Insert IPv6 Explicit Null MPLS header if the traffic type is of type IPv6

		Returns:
			bool
		"""
		return self._get_attribute('insertIpv6ExplicitNull')
	@InsertIpv6ExplicitNull.setter
	def InsertIpv6ExplicitNull(self, value):
		self._set_attribute('insertIpv6ExplicitNull', value)

	@property
	def MaxExpectedSegmentCount(self):
		"""This control is used to set the maximum Segment count/ MPLS labels that would be present in the generted traffic.

		Returns:
			number
		"""
		return self._get_attribute('maxExpectedSegmentCount')
	@MaxExpectedSegmentCount.setter
	def MaxExpectedSegmentCount(self, value):
		self._set_attribute('maxExpectedSegmentCount', value)

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
	def SourceIpv4Address(self):
		"""This is used to set the Source IPv4 address in the IP header of the generated traffic.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('sourceIpv4Address')

	@property
	def SourceIpv6Address(self):
		"""This is used to set the Source IPv6 address in the IP header of the generated traffic.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('sourceIpv6Address')

	@property
	def SymbolicPathName(self):
		"""This is used for generating the traffic for those LSPs from PCE for which the Symbolic Path Name is configured and matches the value.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('symbolicPathName')
