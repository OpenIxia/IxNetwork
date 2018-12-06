
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


class SwitchHostRangeLearnedInfoTriggerAttributes(Base):
	"""The SwitchHostRangeLearnedInfoTriggerAttributes class encapsulates a required switchHostRangeLearnedInfoTriggerAttributes node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the SwitchHostRangeLearnedInfoTriggerAttributes property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'switchHostRangeLearnedInfoTriggerAttributes'

	def __init__(self, parent):
		super(SwitchHostRangeLearnedInfoTriggerAttributes, self).__init__(parent)

	@property
	def CustomPacket(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('customPacket')
	@CustomPacket.setter
	def CustomPacket(self, value):
		self._set_attribute('customPacket', value)

	@property
	def DestinationCustom(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('destinationCustom')
	@DestinationCustom.setter
	def DestinationCustom(self, value):
		self._set_attribute('destinationCustom', value)

	@property
	def DestinationCustomIpv4Address(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('destinationCustomIpv4Address')
	@DestinationCustomIpv4Address.setter
	def DestinationCustomIpv4Address(self, value):
		self._set_attribute('destinationCustomIpv4Address', value)

	@property
	def DestinationCustomIpv4AddressStep(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('destinationCustomIpv4AddressStep')
	@DestinationCustomIpv4AddressStep.setter
	def DestinationCustomIpv4AddressStep(self, value):
		self._set_attribute('destinationCustomIpv4AddressStep', value)

	@property
	def DestinationCustomMacAddress(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('destinationCustomMacAddress')
	@DestinationCustomMacAddress.setter
	def DestinationCustomMacAddress(self, value):
		self._set_attribute('destinationCustomMacAddress', value)

	@property
	def DestinationCustomMacAddressStep(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('destinationCustomMacAddressStep')
	@DestinationCustomMacAddressStep.setter
	def DestinationCustomMacAddressStep(self, value):
		self._set_attribute('destinationCustomMacAddressStep', value)

	@property
	def DestinationHostList(self):
		"""

		Returns:
			list(str[None|/api/v1/sessions/1/ixnetwork/vport?deepchild=switchHostRanges])
		"""
		return self._get_attribute('destinationHostList')
	@DestinationHostList.setter
	def DestinationHostList(self, value):
		self._set_attribute('destinationHostList', value)

	@property
	def MeshingType(self):
		"""

		Returns:
			str(fullyMesh)
		"""
		return self._get_attribute('meshingType')
	@MeshingType.setter
	def MeshingType(self, value):
		self._set_attribute('meshingType', value)

	@property
	def PacketType(self):
		"""

		Returns:
			str(arp|ping|custom)
		"""
		return self._get_attribute('packetType')
	@PacketType.setter
	def PacketType(self, value):
		self._set_attribute('packetType', value)

	@property
	def PeriodIntervalInMs(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('periodIntervalInMs')
	@PeriodIntervalInMs.setter
	def PeriodIntervalInMs(self, value):
		self._set_attribute('periodIntervalInMs', value)

	@property
	def Periodic(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('periodic')
	@Periodic.setter
	def Periodic(self, value):
		self._set_attribute('periodic', value)

	@property
	def PeriodicIterationNumber(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('periodicIterationNumber')
	@PeriodicIterationNumber.setter
	def PeriodicIterationNumber(self, value):
		self._set_attribute('periodicIterationNumber', value)

	@property
	def ResponseTimeout(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('responseTimeout')
	@ResponseTimeout.setter
	def ResponseTimeout(self, value):
		self._set_attribute('responseTimeout', value)

	@property
	def SourceHostList(self):
		"""

		Returns:
			list(str[None|/api/v1/sessions/1/ixnetwork/vport?deepchild=switchHostRanges])
		"""
		return self._get_attribute('sourceHostList')
	@SourceHostList.setter
	def SourceHostList(self, value):
		self._set_attribute('sourceHostList', value)
