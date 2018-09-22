from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class VpnParameter(Base):
	"""The VpnParameter class encapsulates a user managed vpnParameter node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the VpnParameter property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'vpnParameter'

	def __init__(self, parent):
		super(VpnParameter, self).__init__(parent)

	@property
	def Count(self):
		"""Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group

		Returns:
			number
		"""
		return self._get_attribute('count')

	@property
	def SiteId(self):
		"""VPN Site Identifier

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('siteId')

	@property
	def UseVpnParameters(self):
		"""Flag to determine whether optional VPN parameters are provided.

		Returns:
			bool
		"""
		return self._get_attribute('useVpnParameters')
	@UseVpnParameters.setter
	def UseVpnParameters(self, value):
		self._set_attribute('useVpnParameters', value)

	def add(self, UseVpnParameters=None):
		"""Adds a new vpnParameter node on the server and retrieves it in this instance.

		Args:
			UseVpnParameters (bool): Flag to determine whether optional VPN parameters are provided.

		Returns:
			self: This instance with all currently retrieved vpnParameter data using find and the newly added vpnParameter data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the vpnParameter data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, Count=None, UseVpnParameters=None):
		"""Finds and retrieves vpnParameter data from the server.

		All named parameters support regex and can be used to selectively retrieve vpnParameter data from the server.
		By default the find method takes no parameters and will retrieve all vpnParameter data from the server.

		Args:
			Count (number): Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group
			UseVpnParameters (bool): Flag to determine whether optional VPN parameters are provided.

		Returns:
			self: This instance with matching vpnParameter data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of vpnParameter data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the vpnParameter data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
