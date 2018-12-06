
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


class IxNetCodeOptions(Base):
	"""The IxNetCodeOptions class encapsulates a required ixNetCodeOptions node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the IxNetCodeOptions property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'ixNetCodeOptions'

	def __init__(self, parent):
		super(IxNetCodeOptions, self).__init__(parent)

	@property
	def IncludeAvailableHardware(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('includeAvailableHardware')
	@IncludeAvailableHardware.setter
	def IncludeAvailableHardware(self, value):
		self._set_attribute('includeAvailableHardware', value)

	@property
	def IncludeConnect(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('includeConnect')
	@IncludeConnect.setter
	def IncludeConnect(self, value):
		self._set_attribute('includeConnect', value)

	@property
	def IncludeDefaultValues(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('includeDefaultValues')
	@IncludeDefaultValues.setter
	def IncludeDefaultValues(self, value):
		self._set_attribute('includeDefaultValues', value)

	@property
	def IncludeQuickTest(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('includeQuickTest')
	@IncludeQuickTest.setter
	def IncludeQuickTest(self, value):
		self._set_attribute('includeQuickTest', value)

	@property
	def IncludeStatistic(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('includeStatistic')
	@IncludeStatistic.setter
	def IncludeStatistic(self, value):
		self._set_attribute('includeStatistic', value)

	@property
	def IncludeTAPSettings(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('includeTAPSettings')
	@IncludeTAPSettings.setter
	def IncludeTAPSettings(self, value):
		self._set_attribute('includeTAPSettings', value)

	@property
	def IncludeTestComposer(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('includeTestComposer')
	@IncludeTestComposer.setter
	def IncludeTestComposer(self, value):
		self._set_attribute('includeTestComposer', value)

	@property
	def IncludeTraffic(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('includeTraffic')
	@IncludeTraffic.setter
	def IncludeTraffic(self, value):
		self._set_attribute('includeTraffic', value)

	@property
	def IncludeTrafficFlowGroup(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('includeTrafficFlowGroup')
	@IncludeTrafficFlowGroup.setter
	def IncludeTrafficFlowGroup(self, value):
		self._set_attribute('includeTrafficFlowGroup', value)

	@property
	def IncludeTrafficStack(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('includeTrafficStack')
	@IncludeTrafficStack.setter
	def IncludeTrafficStack(self, value):
		self._set_attribute('includeTrafficStack', value)
