
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


class DhcpV6DiscoveredInfo(Base):
	"""The DhcpV6DiscoveredInfo class encapsulates a required dhcpV6DiscoveredInfo node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the DhcpV6DiscoveredInfo property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'dhcpV6DiscoveredInfo'

	def __init__(self, parent):
		super(DhcpV6DiscoveredInfo, self).__init__(parent)

	@property
	def IaRebindTime(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('iaRebindTime')

	@property
	def IaRenewTime(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('iaRenewTime')

	@property
	def Ipv6Address(self):
		"""

		Returns:
			list(str)
		"""
		return self._get_attribute('ipv6Address')

	@property
	def IsDhcpV6LearnedInfoRefreshed(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('isDhcpV6LearnedInfoRefreshed')

	@property
	def ProtocolInterface(self):
		"""

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface)
		"""
		return self._get_attribute('protocolInterface')

	@property
	def Tlvs(self):
		"""

		Returns:
			list(dict(arg1:number,arg2:str))
		"""
		return self._get_attribute('tlvs')
