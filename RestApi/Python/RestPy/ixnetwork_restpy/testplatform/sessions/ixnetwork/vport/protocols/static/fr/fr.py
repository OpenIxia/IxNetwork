from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Fr(Base):
	"""The Fr class encapsulates a user managed fr node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Fr property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'fr'

	def __init__(self, parent):
		super(Fr, self).__init__(parent)

	@property
	def Count(self):
		"""The total number of DLCIs to create for this range.

		Returns:
			number
		"""
		return self._get_attribute('count')
	@Count.setter
	def Count(self, value):
		self._set_attribute('count', value)

	@property
	def Dlci(self):
		"""The Data Link Connection Identifier (DLCI) value.

		Returns:
			number
		"""
		return self._get_attribute('dlci')
	@Dlci.setter
	def Dlci(self, value):
		self._set_attribute('dlci', value)

	@property
	def EnableIncrement(self):
		"""Creates a range of DLCIs for this entry. Each additional DLCI value will be incremented by 1.

		Returns:
			bool
		"""
		return self._get_attribute('enableIncrement')
	@EnableIncrement.setter
	def EnableIncrement(self, value):
		self._set_attribute('enableIncrement', value)

	@property
	def Enabled(self):
		"""Check this box to enable this Frame Relay (FR) DLCI entry.

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def TrafficGroupId(self):
		"""The name of the group to which this port is assigned, for the purpose of creating traffic streams among source/destination members of the group.

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficGroup)
		"""
		return self._get_attribute('trafficGroupId')
	@TrafficGroupId.setter
	def TrafficGroupId(self, value):
		self._set_attribute('trafficGroupId', value)

	def add(self, Count=None, Dlci=None, EnableIncrement=None, Enabled=None, TrafficGroupId=None):
		"""Adds a new fr node on the server and retrieves it in this instance.

		Args:
			Count (number): The total number of DLCIs to create for this range.
			Dlci (number): The Data Link Connection Identifier (DLCI) value.
			EnableIncrement (bool): Creates a range of DLCIs for this entry. Each additional DLCI value will be incremented by 1.
			Enabled (bool): Check this box to enable this Frame Relay (FR) DLCI entry.
			TrafficGroupId (str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficGroup)): The name of the group to which this port is assigned, for the purpose of creating traffic streams among source/destination members of the group.

		Returns:
			self: This instance with all currently retrieved fr data using find and the newly added fr data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the fr data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, Count=None, Dlci=None, EnableIncrement=None, Enabled=None, TrafficGroupId=None):
		"""Finds and retrieves fr data from the server.

		All named parameters support regex and can be used to selectively retrieve fr data from the server.
		By default the find method takes no parameters and will retrieve all fr data from the server.

		Args:
			Count (number): The total number of DLCIs to create for this range.
			Dlci (number): The Data Link Connection Identifier (DLCI) value.
			EnableIncrement (bool): Creates a range of DLCIs for this entry. Each additional DLCI value will be incremented by 1.
			Enabled (bool): Check this box to enable this Frame Relay (FR) DLCI entry.
			TrafficGroupId (str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficGroup)): The name of the group to which this port is assigned, for the purpose of creating traffic streams among source/destination members of the group.

		Returns:
			self: This instance with matching fr data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of fr data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the fr data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
