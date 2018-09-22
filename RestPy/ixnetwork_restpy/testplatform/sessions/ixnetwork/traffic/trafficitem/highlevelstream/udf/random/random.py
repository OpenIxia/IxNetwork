from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Random(Base):
	"""The Random class encapsulates a system managed random node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Random property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'random'

	def __init__(self, parent):
		super(Random, self).__init__(parent)

	@property
	def AvailableWidths(self):
		"""Species all the possible widths available for a UDF in particular Type.

		Returns:
			list(str)
		"""
		return self._get_attribute('availableWidths')

	@property
	def Mask(self):
		"""Sets the UDF mask.

		Returns:
			str
		"""
		return self._get_attribute('mask')
	@Mask.setter
	def Mask(self, value):
		self._set_attribute('mask', value)

	@property
	def Width(self):
		"""Specifies the width of the UDF.

		Returns:
			str(16|24|32|8)
		"""
		return self._get_attribute('width')
	@Width.setter
	def Width(self, value):
		self._set_attribute('width', value)

	def find(self, AvailableWidths=None, Mask=None, Width=None):
		"""Finds and retrieves random data from the server.

		All named parameters support regex and can be used to selectively retrieve random data from the server.
		By default the find method takes no parameters and will retrieve all random data from the server.

		Args:
			AvailableWidths (list(str)): Species all the possible widths available for a UDF in particular Type.
			Mask (str): Sets the UDF mask.
			Width (str(16|24|32|8)): Specifies the width of the UDF.

		Returns:
			self: This instance with matching random data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of random data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the random data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
