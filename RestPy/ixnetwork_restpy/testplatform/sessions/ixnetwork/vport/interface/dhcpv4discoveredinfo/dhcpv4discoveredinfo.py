
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


class DhcpV4DiscoveredInfo(Base):
	"""The DhcpV4DiscoveredInfo class encapsulates a required dhcpV4DiscoveredInfo node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the DhcpV4DiscoveredInfo property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'dhcpV4DiscoveredInfo'

	def __init__(self, parent):
		super(DhcpV4DiscoveredInfo, self).__init__(parent)

	@property
	def Gateway(self):
		"""(Read only) A learned/allocated IPv4 Gateway address for this interface on the router that connects to the network segment on which the source host is located.

		Returns:
			str
		"""
		return self._get_attribute('gateway')

	@property
	def Ipv4Address(self):
		"""(Read only) A learned/allocated IPv4 address for this interface,

		Returns:
			str
		"""
		return self._get_attribute('ipv4Address')

	@property
	def Ipv4Mask(self):
		"""(Read only) A 32-bit address mask used in IP to indicate the bits of an IP address that are being used for the subnet address.

		Returns:
			number
		"""
		return self._get_attribute('ipv4Mask')

	@property
	def IsDhcpV4LearnedInfoRefreshed(self):
		"""(Read Only) When true, the DHCPv4 discovered information is refreshed automatically.

		Returns:
			bool
		"""
		return self._get_attribute('isDhcpV4LearnedInfoRefreshed')

	@property
	def LeaseDuration(self):
		"""(Read Only) The user-specified value and the lease timer (from the DHCP Server) are compared. The lowest value is used as the release/renew timer. After this time period has elapsed, the address will be renewed.

		Returns:
			number
		"""
		return self._get_attribute('leaseDuration')

	@property
	def ProtocolInterface(self):
		"""(Read only) An Ixia protocol interface that is negotiating with the DHCP Server.

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface)
		"""
		return self._get_attribute('protocolInterface')

	@property
	def Tlv(self):
		"""(Read only) Type Length Value for DHCPv4.

		Returns:
			list(dict(arg1:number,arg2:str))
		"""
		return self._get_attribute('tlv')
