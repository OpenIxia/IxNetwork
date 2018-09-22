from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Atm(Base):
	"""The Atm class encapsulates a user managed atm node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Atm property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'atm'

	def __init__(self, parent):
		super(Atm, self).__init__(parent)

	@property
	def AtmEncapsulation(self):
		"""The type of ATM encapsulation to use for this ATM Name.

		Returns:
			str(llcRoutedSnap|llcBridged802p3WithFcs|llcBridged802p3WithOutFcs|ppp|vcMultiplexedPpp|vcMultiRouted|vcMultiBridged802p3WithFcs|vcMultiBridged802p3WithOutFcs)
		"""
		return self._get_attribute('atmEncapsulation')
	@AtmEncapsulation.setter
	def AtmEncapsulation(self, value):
		self._set_attribute('atmEncapsulation', value)

	@property
	def Count(self):
		"""The total number of VPI/VCI pairs to create.

		Returns:
			number
		"""
		return self._get_attribute('count')
	@Count.setter
	def Count(self, value):
		self._set_attribute('count', value)

	@property
	def Enabled(self):
		"""Enables this ATM VPI/VCI entry.

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def IncrementVci(self):
		"""Creates multiple VCIs. Each additional VCI will be incremented by 1.

		Returns:
			number
		"""
		return self._get_attribute('incrementVci')
	@IncrementVci.setter
	def IncrementVci(self, value):
		self._set_attribute('incrementVci', value)

	@property
	def IncrementVpi(self):
		"""Creates multiple VPIs. Each additional VPI will be incremented by 1.

		Returns:
			number
		"""
		return self._get_attribute('incrementVpi')
	@IncrementVpi.setter
	def IncrementVpi(self, value):
		self._set_attribute('incrementVpi', value)

	@property
	def Name(self):
		"""The identifier associated with this ATM VPI/VCI entry.

		Returns:
			str
		"""
		return self._get_attribute('name')
	@Name.setter
	def Name(self, value):
		self._set_attribute('name', value)

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

	@property
	def Vci(self):
		"""The value for the first ATM Virtual Circuit Identifier (VCI). The VCI value is used with a VPI value - a VPI/VCI pair - to identify a specific ATM link.

		Returns:
			number
		"""
		return self._get_attribute('vci')
	@Vci.setter
	def Vci(self, value):
		self._set_attribute('vci', value)

	@property
	def Vpi(self):
		"""The value for the first ATM Virtual Port Identifier (VPI). The VPI value is used with a VCI value - a VPI/VCI pair - to identify a specific ATM virtual link.

		Returns:
			number
		"""
		return self._get_attribute('vpi')
	@Vpi.setter
	def Vpi(self, value):
		self._set_attribute('vpi', value)

	def add(self, AtmEncapsulation=None, Count=None, Enabled=None, IncrementVci=None, IncrementVpi=None, Name=None, TrafficGroupId=None, Vci=None, Vpi=None):
		"""Adds a new atm node on the server and retrieves it in this instance.

		Args:
			AtmEncapsulation (str(llcRoutedSnap|llcBridged802p3WithFcs|llcBridged802p3WithOutFcs|ppp|vcMultiplexedPpp|vcMultiRouted|vcMultiBridged802p3WithFcs|vcMultiBridged802p3WithOutFcs)): The type of ATM encapsulation to use for this ATM Name.
			Count (number): The total number of VPI/VCI pairs to create.
			Enabled (bool): Enables this ATM VPI/VCI entry.
			IncrementVci (number): Creates multiple VCIs. Each additional VCI will be incremented by 1.
			IncrementVpi (number): Creates multiple VPIs. Each additional VPI will be incremented by 1.
			Name (str): The identifier associated with this ATM VPI/VCI entry.
			TrafficGroupId (str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficGroup)): The name of the group to which this port is assigned, for the purpose of creating traffic streams among source/destination members of the group.
			Vci (number): The value for the first ATM Virtual Circuit Identifier (VCI). The VCI value is used with a VPI value - a VPI/VCI pair - to identify a specific ATM link.
			Vpi (number): The value for the first ATM Virtual Port Identifier (VPI). The VPI value is used with a VCI value - a VPI/VCI pair - to identify a specific ATM virtual link.

		Returns:
			self: This instance with all currently retrieved atm data using find and the newly added atm data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the atm data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, AtmEncapsulation=None, Count=None, Enabled=None, IncrementVci=None, IncrementVpi=None, Name=None, TrafficGroupId=None, Vci=None, Vpi=None):
		"""Finds and retrieves atm data from the server.

		All named parameters support regex and can be used to selectively retrieve atm data from the server.
		By default the find method takes no parameters and will retrieve all atm data from the server.

		Args:
			AtmEncapsulation (str(llcRoutedSnap|llcBridged802p3WithFcs|llcBridged802p3WithOutFcs|ppp|vcMultiplexedPpp|vcMultiRouted|vcMultiBridged802p3WithFcs|vcMultiBridged802p3WithOutFcs)): The type of ATM encapsulation to use for this ATM Name.
			Count (number): The total number of VPI/VCI pairs to create.
			Enabled (bool): Enables this ATM VPI/VCI entry.
			IncrementVci (number): Creates multiple VCIs. Each additional VCI will be incremented by 1.
			IncrementVpi (number): Creates multiple VPIs. Each additional VPI will be incremented by 1.
			Name (str): The identifier associated with this ATM VPI/VCI entry.
			TrafficGroupId (str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficGroup)): The name of the group to which this port is assigned, for the purpose of creating traffic streams among source/destination members of the group.
			Vci (number): The value for the first ATM Virtual Circuit Identifier (VCI). The VCI value is used with a VPI value - a VPI/VCI pair - to identify a specific ATM link.
			Vpi (number): The value for the first ATM Virtual Port Identifier (VPI). The VPI value is used with a VCI value - a VPI/VCI pair - to identify a specific ATM virtual link.

		Returns:
			self: This instance with matching atm data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of atm data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the atm data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
