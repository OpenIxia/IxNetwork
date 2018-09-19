from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class IsisSRTunnelList(Base):
	"""The IsisSRTunnelList class encapsulates a required isisSRTunnelList node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the IsisSRTunnelList property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'isisSRTunnelList'

	def __init__(self, parent):
		super(IsisSRTunnelList, self).__init__(parent)

	@property
	def IsisSegmentList(self):
		"""An instance of the IsisSegmentList class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.isissegmentlist.IsisSegmentList)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.isissegmentlist import IsisSegmentList
		return IsisSegmentList(self)

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
	def NumberOfSegments(self):
		"""Number of Segments

		Returns:
			number
		"""
		return self._get_attribute('numberOfSegments')
	@NumberOfSegments.setter
	def NumberOfSegments(self, value):
		self._set_attribute('numberOfSegments', value)

	@property
	def SourceIpv4(self):
		"""Source IPv4

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('sourceIpv4')

	@property
	def SourceIpv6(self):
		"""Source IPv6

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('sourceIpv6')

	@property
	def TunnelDescription(self):
		"""Tunnel Description

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('tunnelDescription')

	@property
	def UsingHeadEndNodePrefix(self):
		"""Using head end Node prefix

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('usingHeadEndNodePrefix')
