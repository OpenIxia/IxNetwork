
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


class Capabilities(Base):
	"""The Capabilities class encapsulates a required capabilities node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Capabilities property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'capabilities'

	def __init__(self, parent):
		super(Capabilities, self).__init__(parent)

	@property
	def AdVpls(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('adVpls')
	@AdVpls.setter
	def AdVpls(self, value):
		self._set_attribute('adVpls', value)

	@property
	def Evpn(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('evpn')
	@Evpn.setter
	def Evpn(self, value):
		self._set_attribute('evpn', value)

	@property
	def FetchDetailedIpV4UnicastInfo(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('fetchDetailedIpV4UnicastInfo')
	@FetchDetailedIpV4UnicastInfo.setter
	def FetchDetailedIpV4UnicastInfo(self, value):
		self._set_attribute('fetchDetailedIpV4UnicastInfo', value)

	@property
	def FetchDetailedIpV6UnicastInfo(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('fetchDetailedIpV6UnicastInfo')
	@FetchDetailedIpV6UnicastInfo.setter
	def FetchDetailedIpV6UnicastInfo(self, value):
		self._set_attribute('fetchDetailedIpV6UnicastInfo', value)

	@property
	def IpV4Mpls(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('ipV4Mpls')
	@IpV4Mpls.setter
	def IpV4Mpls(self, value):
		self._set_attribute('ipV4Mpls', value)

	@property
	def IpV4MplsVpn(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('ipV4MplsVpn')
	@IpV4MplsVpn.setter
	def IpV4MplsVpn(self, value):
		self._set_attribute('ipV4MplsVpn', value)

	@property
	def IpV4Multicast(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('ipV4Multicast')
	@IpV4Multicast.setter
	def IpV4Multicast(self, value):
		self._set_attribute('ipV4Multicast', value)

	@property
	def IpV4MulticastMplsVpn(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('ipV4MulticastMplsVpn')
	@IpV4MulticastMplsVpn.setter
	def IpV4MulticastMplsVpn(self, value):
		self._set_attribute('ipV4MulticastMplsVpn', value)

	@property
	def IpV4MulticastVpn(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('ipV4MulticastVpn')
	@IpV4MulticastVpn.setter
	def IpV4MulticastVpn(self, value):
		self._set_attribute('ipV4MulticastVpn', value)

	@property
	def IpV4Unicast(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('ipV4Unicast')
	@IpV4Unicast.setter
	def IpV4Unicast(self, value):
		self._set_attribute('ipV4Unicast', value)

	@property
	def IpV6Mpls(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('ipV6Mpls')
	@IpV6Mpls.setter
	def IpV6Mpls(self, value):
		self._set_attribute('ipV6Mpls', value)

	@property
	def IpV6MplsVpn(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('ipV6MplsVpn')
	@IpV6MplsVpn.setter
	def IpV6MplsVpn(self, value):
		self._set_attribute('ipV6MplsVpn', value)

	@property
	def IpV6Multicast(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('ipV6Multicast')
	@IpV6Multicast.setter
	def IpV6Multicast(self, value):
		self._set_attribute('ipV6Multicast', value)

	@property
	def IpV6MulticastMplsVpn(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('ipV6MulticastMplsVpn')
	@IpV6MulticastMplsVpn.setter
	def IpV6MulticastMplsVpn(self, value):
		self._set_attribute('ipV6MulticastMplsVpn', value)

	@property
	def IpV6MulticastVpn(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('ipV6MulticastVpn')
	@IpV6MulticastVpn.setter
	def IpV6MulticastVpn(self, value):
		self._set_attribute('ipV6MulticastVpn', value)

	@property
	def IpV6Unicast(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('ipV6Unicast')
	@IpV6Unicast.setter
	def IpV6Unicast(self, value):
		self._set_attribute('ipV6Unicast', value)

	@property
	def Vpls(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('vpls')
	@Vpls.setter
	def Vpls(self, value):
		self._set_attribute('vpls', value)
