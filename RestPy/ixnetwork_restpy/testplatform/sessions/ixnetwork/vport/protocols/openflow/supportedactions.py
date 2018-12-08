
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


class SupportedActions(Base):
	"""The SupportedActions class encapsulates a required supportedActions node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the SupportedActions property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'supportedActions'

	def __init__(self, parent):
		super(SupportedActions, self).__init__(parent)

	@property
	def Enqueue(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enqueue')
	@Enqueue.setter
	def Enqueue(self, value):
		self._set_attribute('enqueue', value)

	@property
	def EthernetDestination(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('ethernetDestination')
	@EthernetDestination.setter
	def EthernetDestination(self, value):
		self._set_attribute('ethernetDestination', value)

	@property
	def EthernetSource(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('ethernetSource')
	@EthernetSource.setter
	def EthernetSource(self, value):
		self._set_attribute('ethernetSource', value)

	@property
	def IpDscp(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('ipDscp')
	@IpDscp.setter
	def IpDscp(self, value):
		self._set_attribute('ipDscp', value)

	@property
	def Ipv4Destination(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('ipv4Destination')
	@Ipv4Destination.setter
	def Ipv4Destination(self, value):
		self._set_attribute('ipv4Destination', value)

	@property
	def Ipv4Source(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('ipv4Source')
	@Ipv4Source.setter
	def Ipv4Source(self, value):
		self._set_attribute('ipv4Source', value)

	@property
	def Output(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('output')
	@Output.setter
	def Output(self, value):
		self._set_attribute('output', value)

	@property
	def StripVlanHeader(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('stripVlanHeader')
	@StripVlanHeader.setter
	def StripVlanHeader(self, value):
		self._set_attribute('stripVlanHeader', value)

	@property
	def TransportDestination(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('transportDestination')
	@TransportDestination.setter
	def TransportDestination(self, value):
		self._set_attribute('transportDestination', value)

	@property
	def TransportSource(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('transportSource')
	@TransportSource.setter
	def TransportSource(self, value):
		self._set_attribute('transportSource', value)

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
