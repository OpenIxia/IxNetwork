from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class PbbEVpnParameter(Base):
	"""The PbbEVpnParameter class encapsulates a user managed pbbEVpnParameter node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the PbbEVpnParameter property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'pbbEVpnParameter'

	def __init__(self, parent):
		super(PbbEVpnParameter, self).__init__(parent)

	@property
	def BMac(self):
		"""Broadcast MAC addresses of the devices

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('bMac')

	@property
	def Count(self):
		"""Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group

		Returns:
			number
		"""
		return self._get_attribute('count')

	@property
	def UsePbbEVpnParameters(self):
		"""Flag to determine whether optional PBB EVPN parameters are provided.

		Returns:
			bool
		"""
		return self._get_attribute('usePbbEVpnParameters')
	@UsePbbEVpnParameters.setter
	def UsePbbEVpnParameters(self, value):
		self._set_attribute('usePbbEVpnParameters', value)

	def add(self, UsePbbEVpnParameters=None):
		"""Adds a new pbbEVpnParameter node on the server and retrieves it in this instance.

		Args:
			UsePbbEVpnParameters (bool): Flag to determine whether optional PBB EVPN parameters are provided.

		Returns:
			self: This instance with all currently retrieved pbbEVpnParameter data using find and the newly added pbbEVpnParameter data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the pbbEVpnParameter data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, Count=None, UsePbbEVpnParameters=None):
		"""Finds and retrieves pbbEVpnParameter data from the server.

		All named parameters support regex and can be used to selectively retrieve pbbEVpnParameter data from the server.
		By default the find method takes no parameters and will retrieve all pbbEVpnParameter data from the server.

		Args:
			Count (number): Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group
			UsePbbEVpnParameters (bool): Flag to determine whether optional PBB EVPN parameters are provided.

		Returns:
			self: This instance with matching pbbEVpnParameter data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of pbbEVpnParameter data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the pbbEVpnParameter data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
