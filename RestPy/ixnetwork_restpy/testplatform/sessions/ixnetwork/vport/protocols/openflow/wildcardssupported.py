
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


class WildcardsSupported(Base):
	"""The WildcardsSupported class encapsulates a required wildcardsSupported node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the WildcardsSupported property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'wildcardsSupported'

	def __init__(self, parent):
		super(WildcardsSupported, self).__init__(parent)

	@property
	def EthernetDestinationAddress(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('ethernetDestinationAddress')
	@EthernetDestinationAddress.setter
	def EthernetDestinationAddress(self, value):
		self._set_attribute('ethernetDestinationAddress', value)

	@property
	def EthernetFrameType(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('ethernetFrameType')
	@EthernetFrameType.setter
	def EthernetFrameType(self, value):
		self._set_attribute('ethernetFrameType', value)

	@property
	def EthernetSourceAddress(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('ethernetSourceAddress')
	@EthernetSourceAddress.setter
	def EthernetSourceAddress(self, value):
		self._set_attribute('ethernetSourceAddress', value)

	@property
	def IpDestinationAddress(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('ipDestinationAddress')
	@IpDestinationAddress.setter
	def IpDestinationAddress(self, value):
		self._set_attribute('ipDestinationAddress', value)

	@property
	def IpProtocol(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('ipProtocol')
	@IpProtocol.setter
	def IpProtocol(self, value):
		self._set_attribute('ipProtocol', value)

	@property
	def IpSourceAddress(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('ipSourceAddress')
	@IpSourceAddress.setter
	def IpSourceAddress(self, value):
		self._set_attribute('ipSourceAddress', value)

	@property
	def IpTos(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('ipTos')
	@IpTos.setter
	def IpTos(self, value):
		self._set_attribute('ipTos', value)

	@property
	def SwitchInputPort(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('switchInputPort')
	@SwitchInputPort.setter
	def SwitchInputPort(self, value):
		self._set_attribute('switchInputPort', value)

	@property
	def TcpUdpDestinationPort(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('tcpUdpDestinationPort')
	@TcpUdpDestinationPort.setter
	def TcpUdpDestinationPort(self, value):
		self._set_attribute('tcpUdpDestinationPort', value)

	@property
	def TcpUdpSourcePort(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('tcpUdpSourcePort')
	@TcpUdpSourcePort.setter
	def TcpUdpSourcePort(self, value):
		self._set_attribute('tcpUdpSourcePort', value)

	@property
	def VlanId(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('vlanId')
	@VlanId.setter
	def VlanId(self, value):
		self._set_attribute('vlanId', value)

	@property
	def VlanPriority(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('vlanPriority')
	@VlanPriority.setter
	def VlanPriority(self, value):
		self._set_attribute('vlanPriority', value)
