
# Copyright 1997 - 2018 by IXIA Keysight
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
    
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

	def get_device_ids(self, PortNames=None, AddressDuidMask=None, AddressDuidPattern=None, AddressesPerIA=None, CustomRebindTime=None, CustomRenewTime=None, DefaultLeaseTime=None, EnableAddressMatchDuid=None, EnablePrefixMatchDuid=None, IaType=None, Ignore=None, IgnoreMask=None, IgnorePattern=None, IpAddress=None, IpAddressIncrement=None, IpAddressPD=None, IpPrefix=None, IpPrefixIncrement=None, LeaseTimeIncrement=None, Nak=None, NakMask=None, NakPattern=None, PoolPrefixSize=None, PoolSize=None, PrefixDuidIncrement=None, PrefixDuidStart=None, PrefixLength=None, PrefixesPerIA=None, UseCustomTimes=None):
		"""Base class infrastructure that gets a list of dhcp6ServerSessions device ids encapsulated by this object.

		Use the optional regex parameters in the method to refine the list of device ids encapsulated by this object.

		Args:
			PortNames (str): optional regex of port names
			AddressDuidMask (str): optional regex of addressDuidMask
			AddressDuidPattern (str): optional regex of addressDuidPattern
			AddressesPerIA (str): optional regex of addressesPerIA
			CustomRebindTime (str): optional regex of customRebindTime
			CustomRenewTime (str): optional regex of customRenewTime
			DefaultLeaseTime (str): optional regex of defaultLeaseTime
			EnableAddressMatchDuid (str): optional regex of enableAddressMatchDuid
			EnablePrefixMatchDuid (str): optional regex of enablePrefixMatchDuid
			IaType (str): optional regex of iaType
			Ignore (str): optional regex of ignore
			IgnoreMask (str): optional regex of ignoreMask
			IgnorePattern (str): optional regex of ignorePattern
			IpAddress (str): optional regex of ipAddress
			IpAddressIncrement (str): optional regex of ipAddressIncrement
			IpAddressPD (str): optional regex of ipAddressPD
			IpPrefix (str): optional regex of ipPrefix
			IpPrefixIncrement (str): optional regex of ipPrefixIncrement
			LeaseTimeIncrement (str): optional regex of leaseTimeIncrement
			Nak (str): optional regex of nak
			NakMask (str): optional regex of nakMask
			NakPattern (str): optional regex of nakPattern
			PoolPrefixSize (str): optional regex of poolPrefixSize
			PoolSize (str): optional regex of poolSize
			PrefixDuidIncrement (str): optional regex of prefixDuidIncrement
			PrefixDuidStart (str): optional regex of prefixDuidStart
			PrefixLength (str): optional regex of prefixLength
			PrefixesPerIA (str): optional regex of prefixesPerIA
			UseCustomTimes (str): optional regex of useCustomTimes

		Returns:
			list(int): A list of device ids that meets the regex criteria provided in the method parameters

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._get_ngpf_device_ids(locals())
