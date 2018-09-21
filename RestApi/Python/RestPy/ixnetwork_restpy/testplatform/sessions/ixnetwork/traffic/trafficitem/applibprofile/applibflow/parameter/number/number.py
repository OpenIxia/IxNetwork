from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Number(Base):
	"""The Number class encapsulates a system managed number node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Number property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'number'

	def __init__(self, parent):
		super(Number, self).__init__(parent)

	@property
	def Default(self):
		"""(Read only) Parameter default value.

		Returns:
			number
		"""
		return self._get_attribute('default')

	@property
	def MaxValue(self):
		"""(Read only) Maximum supported value for parameter.

		Returns:
			number
		"""
		return self._get_attribute('maxValue')

	@property
	def MinValue(self):
		"""(Read only) Minimum supported value for parameter.

		Returns:
			number
		"""
		return self._get_attribute('minValue')

	@property
	def Value(self):
		"""Parameter integer value.

		Returns:
			number
		"""
		return self._get_attribute('value')
	@Value.setter
	def Value(self, value):
		self._set_attribute('value', value)

	def find(self, Default=None, MaxValue=None, MinValue=None, Value=None):
		"""Finds and retrieves number data from the server.

		All named parameters support regex and can be used to selectively retrieve number data from the server.
		By default the find method takes no parameters and will retrieve all number data from the server.

		Args:
			Default (number): (Read only) Parameter default value.
			MaxValue (number): (Read only) Maximum supported value for parameter.
			MinValue (number): (Read only) Minimum supported value for parameter.
			Value (number): Parameter integer value.

		Returns:
			self: This instance with matching number data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of number data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the number data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
