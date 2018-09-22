from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class RouterTlv(Base):
	"""The RouterTlv class encapsulates a system managed routerTlv node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the RouterTlv property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'routerTlv'

	def __init__(self, parent):
		super(RouterTlv, self).__init__(parent)

	@property
	def RouterAddress(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('routerAddress')
	@RouterAddress.setter
	def RouterAddress(self, value):
		self._set_attribute('routerAddress', value)

	def find(self, RouterAddress=None):
		"""Finds and retrieves routerTlv data from the server.

		All named parameters support regex and can be used to selectively retrieve routerTlv data from the server.
		By default the find method takes no parameters and will retrieve all routerTlv data from the server.

		Args:
			RouterAddress (str): 

		Returns:
			self: This instance with matching routerTlv data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of routerTlv data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the routerTlv data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
