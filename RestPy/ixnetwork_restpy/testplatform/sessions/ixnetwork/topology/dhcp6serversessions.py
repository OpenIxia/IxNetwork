from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Dhcp6ServerSessions(Base):
	"""The Dhcp6ServerSessions class encapsulates a required dhcp6ServerSessions node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Dhcp6ServerSessions property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'dhcp6ServerSessions'

	def __init__(self, parent):
		super(Dhcp6ServerSessions, self).__init__(parent)

	@property
	def AddressDuidMask(self):
		"""The mask based on which the DUIDs are chosen for address assignment.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('addressDuidMask')

	@property
	def AddressDuidPattern(self):
		"""The pattern based on which the DUIDs are chosen for address assignment.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('addressDuidPattern')

	@property
	def AddressesPerIA(self):
		"""Number of addresses to be advertised in a single IANA option.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('addressesPerIA')

	@property
	def Count(self):
		"""Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group

		Returns:
			number
		"""
		return self._get_attribute('count')

	@property
	def CustomRebindTime(self):
		"""The Time (in seconds) after the client will start rebinding the leases from the server.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('customRebindTime')

	@property
	def CustomRenewTime(self):
		"""The Time (in seconds) after the client will start renewing the leases from the server.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('customRenewTime')

	@property
	def DefaultLeaseTime(self):
		"""The Life Time length in seconds that will be assigned to a lease if the requesting DHCP Client does not specify a specific expiration time.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('defaultLeaseTime')

	@property
	def DescriptiveName(self):
		"""Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context

		Returns:
			str
		"""
		return self._get_attribute('descriptiveName')

	@property
	def EnableAddressMatchDuid(self):
		"""If enabled, the requests with DUIDs matching the mask and pattern will be assigned addresses from this pool.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableAddressMatchDuid')

	@property
	def EnablePrefixMatchDuid(self):
		"""If enabled, the requests with DUIDs matching DUID start and increment will be given a specific prefix from this pool.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enablePrefixMatchDuid')

	@property
	def IaType(self):
		"""The Identity Association type supported by IPv6 address pools .

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('iaType')

	@property
	def Ignore(self):
		"""If enabled, the requests with DUIDs matching the mask and pattern will be ignored by the Server.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('ignore')

	@property
	def IgnoreMask(self):
		"""The mask based on which the DUIDs of ignored addresses are chosen.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('ignoreMask')

	@property
	def IgnorePattern(self):
		"""The pattern based on which the DUIDs of ignored addresses are chosen.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('ignorePattern')

	@property
	def IpAddress(self):
		"""The IP address of the first lease pool.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('ipAddress')

	@property
	def IpAddressIncrement(self):
		"""The increment value for the lease address within the lease pool.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('ipAddressIncrement')

	@property
	def IpAddressPD(self):
		"""The prefix of the first lease pool.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('ipAddressPD')

	@property
	def IpPrefix(self):
		"""The Subnet Address length used to compute the subnetwork the advertised lease is part of.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('ipPrefix')

	@property
	def IpPrefixIncrement(self):
		"""The increment value for the lease prefix within the lease pool.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('ipPrefixIncrement')

	@property
	def LeaseTimeIncrement(self):
		"""Increment step for Lease Time.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('leaseTimeIncrement')

	@property
	def Nak(self):
		"""If enabled, the requests with DUIDs matching the mask and pattern will be NAKed by the Server.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('nak')

	@property
	def NakMask(self):
		"""The mask based on which the DUIDs of NAKed addresses are chosen.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('nakMask')

	@property
	def NakPattern(self):
		"""The pattern based on which the DUIDs of NAKed addresses are chosen.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('nakPattern')

	@property
	def Name(self):
		"""Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			str
		"""
		return self._get_attribute('name')
	@Name.setter
	def Name(self, value):
		self._set_attribute('name', value)

	@property
	def PoolPrefixSize(self):
		"""The number of leases to be allocated per each server prefix.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('poolPrefixSize')

	@property
	def PoolSize(self):
		"""The number of leases to be allocated per each server address.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('poolSize')

	@property
	def PrefixDuidIncrement(self):
		"""The increment used to generate the DUIDs which will be chosen for prefix assignment.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('prefixDuidIncrement')

	@property
	def PrefixDuidStart(self):
		"""The first DUID which will be chosen for prefix assignment.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('prefixDuidStart')

	@property
	def PrefixLength(self):
		"""The subnet address length advertised in DHCP Offer and Reply messages.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('prefixLength')

	@property
	def PrefixesPerIA(self):
		"""Number of prefixes to be advertised in a single IANA option.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('prefixesPerIA')

	@property
	def UseCustomTimes(self):
		""">Use Custom Renew/Rebind Times instead of the ones computed from the valability times of the leases.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('useCustomTimes')
