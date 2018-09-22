from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Range(Base):
	"""The Range class encapsulates a system managed range node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Range property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'range'

	def __init__(self, parent):
		super(Range, self).__init__(parent)

	@property
	def From(self):
		"""Start range value.

		Returns:
			number
		"""
		return self._get_attribute('from')
	@From.setter
	def From(self, value):
		self._set_attribute('from', value)

	@property
	def MaxValue(self):
		"""(Read only) Maximum supported value for parameter range.

		Returns:
			number
		"""
		return self._get_attribute('maxValue')

	@property
	def MinValue(self):
		"""(Read only) Minimum supported value for parameter range.

		Returns:
			number
		"""
		return self._get_attribute('minValue')

	@property
	def To(self):
		"""End range value.

		Returns:
			number
		"""
		return self._get_attribute('to')
	@To.setter
	def To(self, value):
		self._set_attribute('to', value)

	def find(self, From=None, MaxValue=None, MinValue=None, To=None):
		"""Finds and retrieves range data from the server.

		All named parameters support regex and can be used to selectively retrieve range data from the server.
		By default the find method takes no parameters and will retrieve all range data from the server.

		Args:
			From (number): Start range value.
			MaxValue (number): (Read only) Maximum supported value for parameter range.
			MinValue (number): (Read only) Minimum supported value for parameter range.
			To (number): End range value.

		Returns:
			self: This instance with matching range data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of range data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the range data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
