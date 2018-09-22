from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class BgpAsPathSegmentList(Base):
	"""The BgpAsPathSegmentList class encapsulates a system managed bgpAsPathSegmentList node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the BgpAsPathSegmentList property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'bgpAsPathSegmentList'

	def __init__(self, parent):
		super(BgpAsPathSegmentList, self).__init__(parent)

	@property
	def BgpAsNumberList(self):
		"""An instance of the BgpAsNumberList class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgpasnumberlist.BgpAsNumberList)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bgpasnumberlist import BgpAsNumberList
		return BgpAsNumberList(self)

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
	def EnableASPathSegment(self):
		"""Enable AS Path Segment

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableASPathSegment')

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
	def NumberOfAsNumberInSegment(self):
		"""Number of AS Number In Segment

		Returns:
			number
		"""
		return self._get_attribute('numberOfAsNumberInSegment')
	@NumberOfAsNumberInSegment.setter
	def NumberOfAsNumberInSegment(self, value):
		self._set_attribute('numberOfAsNumberInSegment', value)

	@property
	def SegmentType(self):
		"""SegmentType

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('segmentType')

	def find(self, Count=None, DescriptiveName=None, Name=None, NumberOfAsNumberInSegment=None):
		"""Finds and retrieves bgpAsPathSegmentList data from the server.

		All named parameters support regex and can be used to selectively retrieve bgpAsPathSegmentList data from the server.
		By default the find method takes no parameters and will retrieve all bgpAsPathSegmentList data from the server.

		Args:
			Count (number): Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario
			NumberOfAsNumberInSegment (number): Number of AS Number In Segment

		Returns:
			self: This instance with matching bgpAsPathSegmentList data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of bgpAsPathSegmentList data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the bgpAsPathSegmentList data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
