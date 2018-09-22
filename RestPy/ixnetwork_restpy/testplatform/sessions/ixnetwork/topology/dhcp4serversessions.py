from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Dhcp4ServerSessions(Base):
	"""The Dhcp4ServerSessions class encapsulates a required dhcp4ServerSessions node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Dhcp4ServerSessions property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'dhcp4ServerSessions'

	def __init__(self, parent):
		super(Dhcp4ServerSessions, self).__init__(parent)

	@property
	def Count(self):
		"""Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group

		Returns:
			number
		"""
		return self._get_attribute('count')

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
	def EchoRelayInfo(self):
		"""Enable echoing of DHCP option 82.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('echoRelayInfo')

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
	def IpDns1(self):
		"""The first DNS address advertised in DHCP Offer and Reply messages.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('ipDns1')

	@property
	def IpDns2(self):
		"""The second DNS address advertised in DHCP Offer and Reply messages.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('ipDns2')

	@property
	def IpGateway(self):
		"""The Router address advertised in DHCP Offer and Reply messages.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('ipGateway')

	@property
	def IpPrefix(self):
		"""The Subnet Address length used to compute the subnetwork the advertised lease is part of.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('ipPrefix')

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
	def PoolSize(self):
		"""The number of leases to be allocated per each server address.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('poolSize')

	@property
	def SessionInfo(self):
		"""Logs additional information about the session state

		Returns:
			list(str[excessiveTlvs|none|poolTooLarge])
		"""
		return self._get_attribute('sessionInfo')
