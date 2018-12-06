
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


class PacketInHeaders(Base):
	"""The PacketInHeaders class encapsulates a required packetInHeaders node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the PacketInHeaders property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'packetInHeaders'

	def __init__(self, parent):
		super(PacketInHeaders, self).__init__(parent)

	@property
	def EthernetDestinationAddress(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('ethernetDestinationAddress')

	@property
	def EthernetSourceAddress(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('ethernetSourceAddress')

	@property
	def EthernetType(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('ethernetType')

	@property
	def Ipv4DestinationAddress(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('ipv4DestinationAddress')

	@property
	def Ipv4Protocol(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('ipv4Protocol')

	@property
	def Ipv4SourceAddress(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('ipv4SourceAddress')

	@property
	def Ipv6DestinationAddress(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('ipv6DestinationAddress')

	@property
	def Ipv6FlowLabel(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('ipv6FlowLabel')

	@property
	def Ipv6SourceAddress(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('ipv6SourceAddress')

	@property
	def TcpDestinationPort(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('tcpDestinationPort')

	@property
	def TcpSourcePort(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('tcpSourcePort')

	@property
	def UdpDestinationPort(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('udpDestinationPort')

	@property
	def UdpSourcePort(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('udpSourcePort')

	@property
	def UniquePacketCount(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('uniquePacketCount')

	@property
	def VlanId(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('vlanId')

	@property
	def VlanPriority(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('vlanPriority')
