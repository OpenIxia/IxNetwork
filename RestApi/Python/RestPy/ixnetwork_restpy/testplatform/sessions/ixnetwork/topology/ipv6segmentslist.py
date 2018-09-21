from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class IPv6SegmentsList(Base):
	"""The IPv6SegmentsList class encapsulates a system managed IPv6SegmentsList node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the IPv6SegmentsList property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'IPv6SegmentsList'

	def __init__(self, parent):
		super(IPv6SegmentsList, self).__init__(parent)

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
	def SID(self):
		"""Segment Item Address

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('sID')

	@property
	def SIDEnable(self):
		"""Enable This Segment

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('sIDEnable')

	def find(self, Count=None, DescriptiveName=None, Name=None):
		"""Finds and retrieves IPv6SegmentsList data from the server.

		All named parameters support regex and can be used to selectively retrieve IPv6SegmentsList data from the server.
		By default the find method takes no parameters and will retrieve all IPv6SegmentsList data from the server.

		Args:
			Count (number): Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			self: This instance with matching IPv6SegmentsList data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of IPv6SegmentsList data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the IPv6SegmentsList data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
