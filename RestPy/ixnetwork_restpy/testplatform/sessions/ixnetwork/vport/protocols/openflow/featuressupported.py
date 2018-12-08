
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


class FeaturesSupported(Base):
	"""The FeaturesSupported class encapsulates a required featuresSupported node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the FeaturesSupported property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'featuresSupported'

	def __init__(self, parent):
		super(FeaturesSupported, self).__init__(parent)

	@property
	def ApplyActions(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('applyActions')
	@ApplyActions.setter
	def ApplyActions(self, value):
		self._set_attribute('applyActions', value)

	@property
	def ApplyActionsMiss(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('applyActionsMiss')
	@ApplyActionsMiss.setter
	def ApplyActionsMiss(self, value):
		self._set_attribute('applyActionsMiss', value)

	@property
	def ApplySetField(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('applySetField')
	@ApplySetField.setter
	def ApplySetField(self, value):
		self._set_attribute('applySetField', value)

	@property
	def ApplySetFieldMiss(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('applySetFieldMiss')
	@ApplySetFieldMiss.setter
	def ApplySetFieldMiss(self, value):
		self._set_attribute('applySetFieldMiss', value)

	@property
	def Experimenter(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('experimenter')
	@Experimenter.setter
	def Experimenter(self, value):
		self._set_attribute('experimenter', value)

	@property
	def ExperimenterMiss(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('experimenterMiss')
	@ExperimenterMiss.setter
	def ExperimenterMiss(self, value):
		self._set_attribute('experimenterMiss', value)

	@property
	def Instruction(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('instruction')
	@Instruction.setter
	def Instruction(self, value):
		self._set_attribute('instruction', value)

	@property
	def InstructionMiss(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('instructionMiss')
	@InstructionMiss.setter
	def InstructionMiss(self, value):
		self._set_attribute('instructionMiss', value)

	@property
	def Match(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('match')
	@Match.setter
	def Match(self, value):
		self._set_attribute('match', value)

	@property
	def NextTable(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('nextTable')
	@NextTable.setter
	def NextTable(self, value):
		self._set_attribute('nextTable', value)

	@property
	def NextTableMiss(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('nextTableMiss')
	@NextTableMiss.setter
	def NextTableMiss(self, value):
		self._set_attribute('nextTableMiss', value)

	@property
	def Wildcards(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('wildcards')
	@Wildcards.setter
	def Wildcards(self, value):
		self._set_attribute('wildcards', value)

	@property
	def WriteActions(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('writeActions')
	@WriteActions.setter
	def WriteActions(self, value):
		self._set_attribute('writeActions', value)

	@property
	def WriteActionsMiss(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('writeActionsMiss')
	@WriteActionsMiss.setter
	def WriteActionsMiss(self, value):
		self._set_attribute('writeActionsMiss', value)

	@property
	def WriteSetField(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('writeSetField')
	@WriteSetField.setter
	def WriteSetField(self, value):
		self._set_attribute('writeSetField', value)

	@property
	def WriteSetFieldMiss(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('writeSetFieldMiss')
	@WriteSetFieldMiss.setter
	def WriteSetFieldMiss(self, value):
		self._set_attribute('writeSetFieldMiss', value)
