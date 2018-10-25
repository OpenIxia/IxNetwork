
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


class GenerateRoutesParams(Base):
	"""The GenerateRoutesParams class encapsulates a required generateRoutesParams node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the GenerateRoutesParams property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'generateRoutesParams'

	def __init__(self, parent):
		super(GenerateRoutesParams, self).__init__(parent)

	@property
	def AddressRangesToSkip(self):
		"""Address Ranges that will be skipped. You can provide multiple ranges separated by ','. Example: 192.0.0.0 - 192.255.255.255

		Returns:
			str
		"""
		return self._get_attribute('addressRangesToSkip')
	@AddressRangesToSkip.setter
	def AddressRangesToSkip(self, value):
		self._set_attribute('addressRangesToSkip', value)

	@property
	def CustomDistributionFile(self):
		"""Source file having custom distribution information.

		Returns:
			obj(ixnetwork_restpy.files.Files)
		"""
		return self._get_attribute('customDistributionFile')
	@CustomDistributionFile.setter
	def CustomDistributionFile(self, value):
		self._set_attribute('customDistributionFile', value)

	@property
	def DuplicateRoutesAsPathSuffix(self):
		"""AS Path Suffix for Duplicate Routes

		Returns:
			str
		"""
		return self._get_attribute('duplicateRoutesAsPathSuffix')
	@DuplicateRoutesAsPathSuffix.setter
	def DuplicateRoutesAsPathSuffix(self, value):
		self._set_attribute('duplicateRoutesAsPathSuffix', value)

	@property
	def DuplicateRoutesPerDevicePercent(self):
		"""Percentage to Duplicate Primary Routes per Device.

		Returns:
			number
		"""
		return self._get_attribute('duplicateRoutesPerDevicePercent')
	@DuplicateRoutesPerDevicePercent.setter
	def DuplicateRoutesPerDevicePercent(self, value):
		self._set_attribute('duplicateRoutesPerDevicePercent', value)

	@property
	def NetworkAddressStart(self):
		"""Network Address Start Value.

		Returns:
			str
		"""
		return self._get_attribute('networkAddressStart')
	@NetworkAddressStart.setter
	def NetworkAddressStart(self, value):
		self._set_attribute('networkAddressStart', value)

	@property
	def NetworkAddressStep(self):
		"""Network Address Step Value.

		Returns:
			str
		"""
		return self._get_attribute('networkAddressStep')
	@NetworkAddressStep.setter
	def NetworkAddressStep(self, value):
		self._set_attribute('networkAddressStep', value)

	@property
	def PrefixLengthDistributionScope(self):
		"""Prefix Length Distribution Scope.

		Returns:
			str(perDevice|perPort|perTopology)
		"""
		return self._get_attribute('prefixLengthDistributionScope')
	@PrefixLengthDistributionScope.setter
	def PrefixLengthDistributionScope(self, value):
		self._set_attribute('prefixLengthDistributionScope', value)

	@property
	def PrefixLengthDistributionType(self):
		"""Prefix Length Distribution Type.

		Returns:
			str(custom|even|exponential|fixed|internet|random)
		"""
		return self._get_attribute('prefixLengthDistributionType')
	@PrefixLengthDistributionType.setter
	def PrefixLengthDistributionType(self, value):
		self._set_attribute('prefixLengthDistributionType', value)

	@property
	def PrefixLengthEnd(self):
		"""Prefix Length End Value. Applicable only for Even and Exponential distribution type.

		Returns:
			number
		"""
		return self._get_attribute('prefixLengthEnd')
	@PrefixLengthEnd.setter
	def PrefixLengthEnd(self, value):
		self._set_attribute('prefixLengthEnd', value)

	@property
	def PrefixLengthStart(self):
		"""Prefix Length Start Value. Applicable only for Fixed, Even and Exponential distribution type.

		Returns:
			number
		"""
		return self._get_attribute('prefixLengthStart')
	@PrefixLengthStart.setter
	def PrefixLengthStart(self, value):
		self._set_attribute('prefixLengthStart', value)

	@property
	def PrimaryRoutesAsPathSuffix(self):
		"""AS Path Suffix for Primary Routes

		Returns:
			str
		"""
		return self._get_attribute('primaryRoutesAsPathSuffix')
	@PrimaryRoutesAsPathSuffix.setter
	def PrimaryRoutesAsPathSuffix(self, value):
		self._set_attribute('primaryRoutesAsPathSuffix', value)

	@property
	def PrimaryRoutesPerDevice(self):
		"""Number of Primary Routes per Device.

		Returns:
			number
		"""
		return self._get_attribute('primaryRoutesPerDevice')
	@PrimaryRoutesPerDevice.setter
	def PrimaryRoutesPerDevice(self, value):
		self._set_attribute('primaryRoutesPerDevice', value)

	@property
	def PrimaryRoutesPerRange(self):
		"""Number of Routes per Route Range.

		Returns:
			number
		"""
		return self._get_attribute('primaryRoutesPerRange')
	@PrimaryRoutesPerRange.setter
	def PrimaryRoutesPerRange(self, value):
		self._set_attribute('primaryRoutesPerRange', value)

	@property
	def SkipLoopback(self):
		"""Do not include Loopback Address in the generated Address Range

		Returns:
			bool
		"""
		return self._get_attribute('skipLoopback')
	@SkipLoopback.setter
	def SkipLoopback(self, value):
		self._set_attribute('skipLoopback', value)

	@property
	def SkipMcast(self):
		"""Do not include Multicast Address in the generated Address Range

		Returns:
			bool
		"""
		return self._get_attribute('skipMcast')
	@SkipMcast.setter
	def SkipMcast(self, value):
		self._set_attribute('skipMcast', value)

	def GenerateRoutes(self):
		"""Executes the generateRoutes operation on the server.

		Generate Primary and Duplicate Routes with advanced prefix length distribution options.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally sets Arg1 to the current href for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('GenerateRoutes', payload=locals(), response_object=None)
