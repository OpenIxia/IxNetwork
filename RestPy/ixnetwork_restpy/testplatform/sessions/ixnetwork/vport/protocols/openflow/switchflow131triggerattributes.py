
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


class SwitchFlow131TriggerAttributes(Base):
	"""The SwitchFlow131TriggerAttributes class encapsulates a required switchFlow131TriggerAttributes node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the SwitchFlow131TriggerAttributes property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'switchFlow131TriggerAttributes'

	def __init__(self, parent):
		super(SwitchFlow131TriggerAttributes, self).__init__(parent)

	@property
	def OutGroup(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('outGroup')
	@OutGroup.setter
	def OutGroup(self, value):
		self._set_attribute('outGroup', value)

	@property
	def OutGroupInputMode(self):
		"""

		Returns:
			str(allGroups|anyGroup|outGroupCustom)
		"""
		return self._get_attribute('outGroupInputMode')
	@OutGroupInputMode.setter
	def OutGroupInputMode(self, value):
		self._set_attribute('outGroupInputMode', value)

	@property
	def OutPort(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('outPort')
	@OutPort.setter
	def OutPort(self, value):
		self._set_attribute('outPort', value)

	@property
	def OutPortInputMode(self):
		"""

		Returns:
			str(ofppInPort|ofppNormal|ofppFlood|ofppAll|ofppController|ofppLocal|ofppAny|outPortCustom)
		"""
		return self._get_attribute('outPortInputMode')
	@OutPortInputMode.setter
	def OutPortInputMode(self, value):
		self._set_attribute('outPortInputMode', value)

	@property
	def TableId(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('tableId')
	@TableId.setter
	def TableId(self, value):
		self._set_attribute('tableId', value)

	@property
	def TableIdInputMode(self):
		"""

		Returns:
			str(allTables|emergency|custom)
		"""
		return self._get_attribute('tableIdInputMode')
	@TableIdInputMode.setter
	def TableIdInputMode(self, value):
		self._set_attribute('tableIdInputMode', value)
