
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


class Instruction(Base):
	"""The Instruction class encapsulates a required instruction node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Instruction property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'instruction'

	def __init__(self, parent):
		super(Instruction, self).__init__(parent)

	@property
	def ApplyActions(self):
		"""If selected, applies the actions associated with a flow immediately.

		Returns:
			bool
		"""
		return self._get_attribute('applyActions')
	@ApplyActions.setter
	def ApplyActions(self, value):
		self._set_attribute('applyActions', value)

	@property
	def ClearActions(self):
		"""If selected, clears the actions attached with the flow.

		Returns:
			bool
		"""
		return self._get_attribute('clearActions')
	@ClearActions.setter
	def ClearActions(self, value):
		self._set_attribute('clearActions', value)

	@property
	def Experimenter(self):
		"""Set the Experimenter details.

		Returns:
			bool
		"""
		return self._get_attribute('experimenter')
	@Experimenter.setter
	def Experimenter(self, value):
		self._set_attribute('experimenter', value)

	@property
	def GoToTable(self):
		"""If selected, forwards the packet to the next table in the pipeline.

		Returns:
			bool
		"""
		return self._get_attribute('goToTable')
	@GoToTable.setter
	def GoToTable(self, value):
		self._set_attribute('goToTable', value)

	@property
	def Meter(self):
		"""If selected, directs a flow to a particular meter.

		Returns:
			bool
		"""
		return self._get_attribute('meter')
	@Meter.setter
	def Meter(self, value):
		self._set_attribute('meter', value)

	@property
	def WriteActions(self):
		"""If selected, appends actions to the existing action set of the packet.

		Returns:
			bool
		"""
		return self._get_attribute('writeActions')
	@WriteActions.setter
	def WriteActions(self, value):
		self._set_attribute('writeActions', value)

	@property
	def WriteMetadata(self):
		"""If selected, writes the masked metadata field to the match.

		Returns:
			bool
		"""
		return self._get_attribute('writeMetadata')
	@WriteMetadata.setter
	def WriteMetadata(self, value):
		self._set_attribute('writeMetadata', value)
