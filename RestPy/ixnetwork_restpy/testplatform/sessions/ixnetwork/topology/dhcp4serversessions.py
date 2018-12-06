
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

	def get_device_ids(self, PortNames=None, DefaultLeaseTime=None, EchoRelayInfo=None, IpAddress=None, IpAddressIncrement=None, IpDns1=None, IpDns2=None, IpGateway=None, IpPrefix=None, PoolSize=None):
		"""Base class infrastructure that gets a list of dhcp4ServerSessions device ids encapsulated by this object.

		Use the optional regex parameters in the method to refine the list of device ids encapsulated by this object.

		Args:
			PortNames (str): optional regex of port names
			DefaultLeaseTime (str): optional regex of defaultLeaseTime
			EchoRelayInfo (str): optional regex of echoRelayInfo
			IpAddress (str): optional regex of ipAddress
			IpAddressIncrement (str): optional regex of ipAddressIncrement
			IpDns1 (str): optional regex of ipDns1
			IpDns2 (str): optional regex of ipDns2
			IpGateway (str): optional regex of ipGateway
			IpPrefix (str): optional regex of ipPrefix
			PoolSize (str): optional regex of poolSize

		Returns:
			list(int): A list of device ids that meets the regex criteria provided in the method parameters

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._get_ngpf_device_ids(locals())
