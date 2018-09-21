from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class LocalEidRange(Base):
	"""The LocalEidRange class encapsulates a user managed localEidRange node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the LocalEidRange property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'localEidRange'

	def __init__(self, parent):
		super(LocalEidRange, self).__init__(parent)

	@property
	def Locator(self):
		"""An instance of the Locator class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.lisp.router.lispinstance.localeidrange.locator.locator.Locator)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.lisp.router.lispinstance.localeidrange.locator.locator import Locator
		return Locator(self)

	@property
	def Count(self):
		"""It gives details about the count

		Returns:
			number
		"""
		return self._get_attribute('count')
	@Count.setter
	def Count(self, value):
		self._set_attribute('count', value)

	@property
	def EnableProxyMapReplyBit(self):
		"""If true, it enables the proxy map reply bit

		Returns:
			bool
		"""
		return self._get_attribute('enableProxyMapReplyBit')
	@EnableProxyMapReplyBit.setter
	def EnableProxyMapReplyBit(self, value):
		self._set_attribute('enableProxyMapReplyBit', value)

	@property
	def EnableWantMapNotifyBit(self):
		"""If true, it enables the Want map Notify bit

		Returns:
			str(always|duringQuickRegistration|never)
		"""
		return self._get_attribute('enableWantMapNotifyBit')
	@EnableWantMapNotifyBit.setter
	def EnableWantMapNotifyBit(self, value):
		self._set_attribute('enableWantMapNotifyBit', value)

	@property
	def Enabled(self):
		"""If true, it enables the protocol

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
	def MaxRecordPerMapRegisterPacket(self):
		"""It gives details about the maximum record per map register packet

		Returns:
			number
		"""
		return self._get_attribute('maxRecordPerMapRegisterPacket')
	@MaxRecordPerMapRegisterPacket.setter
	def MaxRecordPerMapRegisterPacket(self, value):
		self._set_attribute('maxRecordPerMapRegisterPacket', value)

	@property
	def PeriodicRefreshInterval(self):
		"""It gives details about the periodic refresh interval

		Returns:
			number
		"""
		return self._get_attribute('periodicRefreshInterval')
	@PeriodicRefreshInterval.setter
	def PeriodicRefreshInterval(self, value):
		self._set_attribute('periodicRefreshInterval', value)

	@property
	def PrefixLength(self):
		"""it gives details about the prefix length

		Returns:
			number
		"""
		return self._get_attribute('prefixLength')
	@PrefixLength.setter
	def PrefixLength(self, value):
		self._set_attribute('prefixLength', value)

	@property
	def QuickRegistrationPeriod(self):
		"""it gives details about the quick registration period

		Returns:
			number
		"""
		return self._get_attribute('quickRegistrationPeriod')
	@QuickRegistrationPeriod.setter
	def QuickRegistrationPeriod(self, value):
		self._set_attribute('quickRegistrationPeriod', value)

	@property
	def RefreshIntervalInQuickRegistrationPeriod(self):
		"""It refreshs the interval in quick registration periods

		Returns:
			number
		"""
		return self._get_attribute('refreshIntervalInQuickRegistrationPeriod')
	@RefreshIntervalInQuickRegistrationPeriod.setter
	def RefreshIntervalInQuickRegistrationPeriod(self, value):
		self._set_attribute('refreshIntervalInQuickRegistrationPeriod', value)

	@property
	def StartAddress(self):
		"""It gives details about the start address

		Returns:
			str
		"""
		return self._get_attribute('startAddress')
	@StartAddress.setter
	def StartAddress(self, value):
		self._set_attribute('startAddress', value)

	@property
	def SupportSmrGeneration(self):
		"""It supports smr generation

		Returns:
			bool
		"""
		return self._get_attribute('supportSmrGeneration')
	@SupportSmrGeneration.setter
	def SupportSmrGeneration(self, value):
		self._set_attribute('supportSmrGeneration', value)

	@property
	def Ttl(self):
		"""It gives details about the ttl

		Returns:
			number
		"""
		return self._get_attribute('ttl')
	@Ttl.setter
	def Ttl(self, value):
		self._set_attribute('ttl', value)

	@property
	def UseAllInterfaceAddressesAsLocator(self):
		"""If True, it uses all interface address as locator

		Returns:
			bool
		"""
		return self._get_attribute('useAllInterfaceAddressesAsLocator')
	@UseAllInterfaceAddressesAsLocator.setter
	def UseAllInterfaceAddressesAsLocator(self, value):
		self._set_attribute('useAllInterfaceAddressesAsLocator', value)

	def add(self, Count=None, EnableProxyMapReplyBit=None, EnableWantMapNotifyBit=None, Enabled=None, Family=None, MaxRecordPerMapRegisterPacket=None, PeriodicRefreshInterval=None, PrefixLength=None, QuickRegistrationPeriod=None, RefreshIntervalInQuickRegistrationPeriod=None, StartAddress=None, SupportSmrGeneration=None, Ttl=None, UseAllInterfaceAddressesAsLocator=None):
		"""Adds a new localEidRange node on the server and retrieves it in this instance.

		Args:
			Count (number): It gives details about the count
			EnableProxyMapReplyBit (bool): If true, it enables the proxy map reply bit
			EnableWantMapNotifyBit (str(always|duringQuickRegistration|never)): If true, it enables the Want map Notify bit
			Enabled (bool): If true, it enables the protocol
			Family (str(ipv4|ipv6)): It gives details about the family
			MaxRecordPerMapRegisterPacket (number): It gives details about the maximum record per map register packet
			PeriodicRefreshInterval (number): It gives details about the periodic refresh interval
			PrefixLength (number): it gives details about the prefix length
			QuickRegistrationPeriod (number): it gives details about the quick registration period
			RefreshIntervalInQuickRegistrationPeriod (number): It refreshs the interval in quick registration periods
			StartAddress (str): It gives details about the start address
			SupportSmrGeneration (bool): It supports smr generation
			Ttl (number): It gives details about the ttl
			UseAllInterfaceAddressesAsLocator (bool): If True, it uses all interface address as locator

		Returns:
			self: This instance with all currently retrieved localEidRange data using find and the newly added localEidRange data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the localEidRange data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, Count=None, EnableProxyMapReplyBit=None, EnableWantMapNotifyBit=None, Enabled=None, Family=None, MaxRecordPerMapRegisterPacket=None, PeriodicRefreshInterval=None, PrefixLength=None, QuickRegistrationPeriod=None, RefreshIntervalInQuickRegistrationPeriod=None, StartAddress=None, SupportSmrGeneration=None, Ttl=None, UseAllInterfaceAddressesAsLocator=None):
		"""Finds and retrieves localEidRange data from the server.

		All named parameters support regex and can be used to selectively retrieve localEidRange data from the server.
		By default the find method takes no parameters and will retrieve all localEidRange data from the server.

		Args:
			Count (number): It gives details about the count
			EnableProxyMapReplyBit (bool): If true, it enables the proxy map reply bit
			EnableWantMapNotifyBit (str(always|duringQuickRegistration|never)): If true, it enables the Want map Notify bit
			Enabled (bool): If true, it enables the protocol
			Family (str(ipv4|ipv6)): It gives details about the family
			MaxRecordPerMapRegisterPacket (number): It gives details about the maximum record per map register packet
			PeriodicRefreshInterval (number): It gives details about the periodic refresh interval
			PrefixLength (number): it gives details about the prefix length
			QuickRegistrationPeriod (number): it gives details about the quick registration period
			RefreshIntervalInQuickRegistrationPeriod (number): It refreshs the interval in quick registration periods
			StartAddress (str): It gives details about the start address
			SupportSmrGeneration (bool): It supports smr generation
			Ttl (number): It gives details about the ttl
			UseAllInterfaceAddressesAsLocator (bool): If True, it uses all interface address as locator

		Returns:
			self: This instance with matching localEidRange data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of localEidRange data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the localEidRange data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
