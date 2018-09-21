from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Locator(Base):
	"""The Locator class encapsulates a user managed locator node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Locator property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'locator'

	def __init__(self, parent):
		super(Locator, self).__init__(parent)

	@property
	def Address(self):
		"""It gives details about the Ip

		Returns:
			str
		"""
		return self._get_attribute('address')
	@Address.setter
	def Address(self, value):
		self._set_attribute('address', value)

	@property
	def Enabled(self):
		"""It True, it enables the protocol

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def Family(self):
		"""It gives details about the family

		Returns:
			str(ipv4|ipv6)
		"""
		return self._get_attribute('family')
	@Family.setter
	def Family(self, value):
		self._set_attribute('family', value)

	@property
	def LispInterfaceId(self):
		"""It gives details about the LISP interface id

		Returns:
			number
		"""
		return self._get_attribute('lispInterfaceId')
	@LispInterfaceId.setter
	def LispInterfaceId(self, value):
		self._set_attribute('lispInterfaceId', value)

	@property
	def LocalLocator(self):
		"""If True, It gives the address of the local locator

		Returns:
			bool
		"""
		return self._get_attribute('localLocator')
	@LocalLocator.setter
	def LocalLocator(self, value):
		self._set_attribute('localLocator', value)

	@property
	def MPriority(self):
		"""It denotes the m priority

		Returns:
			number
		"""
		return self._get_attribute('mPriority')
	@MPriority.setter
	def MPriority(self, value):
		self._set_attribute('mPriority', value)

	@property
	def MWeight(self):
		"""It denotes the m weight

		Returns:
			number
		"""
		return self._get_attribute('mWeight')
	@MWeight.setter
	def MWeight(self, value):
		self._set_attribute('mWeight', value)

	@property
	def Priority(self):
		"""It gives the priority

		Returns:
			number
		"""
		return self._get_attribute('priority')
	@Priority.setter
	def Priority(self, value):
		self._set_attribute('priority', value)

	@property
	def ProtocolInterfaceIpItemId(self):
		"""It gives details about the protocol interface ip item id

		Returns:
			number
		"""
		return self._get_attribute('protocolInterfaceIpItemId')
	@ProtocolInterfaceIpItemId.setter
	def ProtocolInterfaceIpItemId(self, value):
		self._set_attribute('protocolInterfaceIpItemId', value)

	@property
	def Reachability(self):
		"""If true, it defines the reachability

		Returns:
			bool
		"""
		return self._get_attribute('reachability')
	@Reachability.setter
	def Reachability(self, value):
		self._set_attribute('reachability', value)

	@property
	def Weight(self):
		"""It gives details about the weight

		Returns:
			number
		"""
		return self._get_attribute('weight')
	@Weight.setter
	def Weight(self, value):
		self._set_attribute('weight', value)

	def add(self, Address=None, Enabled=None, Family=None, LispInterfaceId=None, LocalLocator=None, MPriority=None, MWeight=None, Priority=None, ProtocolInterfaceIpItemId=None, Reachability=None, Weight=None):
		"""Adds a new locator node on the server and retrieves it in this instance.

		Args:
			Address (str): It gives details about the Ip
			Enabled (bool): It True, it enables the protocol
			Family (str(ipv4|ipv6)): It gives details about the family
			LispInterfaceId (number): It gives details about the LISP interface id
			LocalLocator (bool): If True, It gives the address of the local locator
			MPriority (number): It denotes the m priority
			MWeight (number): It denotes the m weight
			Priority (number): It gives the priority
			ProtocolInterfaceIpItemId (number): It gives details about the protocol interface ip item id
			Reachability (bool): If true, it defines the reachability
			Weight (number): It gives details about the weight

		Returns:
			self: This instance with all currently retrieved locator data using find and the newly added locator data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the locator data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, Address=None, Enabled=None, Family=None, LispInterfaceId=None, LocalLocator=None, MPriority=None, MWeight=None, Priority=None, ProtocolInterfaceIpItemId=None, Reachability=None, Weight=None):
		"""Finds and retrieves locator data from the server.

		All named parameters support regex and can be used to selectively retrieve locator data from the server.
		By default the find method takes no parameters and will retrieve all locator data from the server.

		Args:
			Address (str): It gives details about the Ip
			Enabled (bool): It True, it enables the protocol
			Family (str(ipv4|ipv6)): It gives details about the family
			LispInterfaceId (number): It gives details about the LISP interface id
			LocalLocator (bool): If True, It gives the address of the local locator
			MPriority (number): It denotes the m priority
			MWeight (number): It denotes the m weight
			Priority (number): It gives the priority
			ProtocolInterfaceIpItemId (number): It gives details about the protocol interface ip item id
			Reachability (bool): If true, it defines the reachability
			Weight (number): It gives details about the weight

		Returns:
			self: This instance with matching locator data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of locator data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the locator data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
