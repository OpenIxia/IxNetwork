
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


class Fcoe(Base):
	"""The Fcoe class encapsulates a required fcoe node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Fcoe property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'fcoe'

	def __init__(self, parent):
		super(Fcoe, self).__init__(parent)

	@property
	def EnablePFCPauseDelay(self):
		"""If true, PFC pause delay is enabled.

		Returns:
			bool
		"""
		return self._get_attribute('enablePFCPauseDelay')
	@EnablePFCPauseDelay.setter
	def EnablePFCPauseDelay(self, value):
		self._set_attribute('enablePFCPauseDelay', value)

	@property
	def FlowControlType(self):
		"""The type of flow control to be selected.

		Returns:
			str(ieee802.1Qbb|ieee802.3x)
		"""
		return self._get_attribute('flowControlType')
	@FlowControlType.setter
	def FlowControlType(self, value):
		self._set_attribute('flowControlType', value)

	@property
	def PfcPauseDelay(self):
		"""If selected, enables to increase the number of frames that is sent when a pause frame is received.

		Returns:
			number
		"""
		return self._get_attribute('pfcPauseDelay')
	@PfcPauseDelay.setter
	def PfcPauseDelay(self, value):
		self._set_attribute('pfcPauseDelay', value)

	@property
	def PfcPriorityGroups(self):
		"""When you select 802.1Qbb as the flowControlType, you can use the PFC/Priority settings to map each of the eight PFC priorities to one of the eight Priority Groups (or to None). The PFCs are numbered 0-7.

		Returns:
			list(str)
		"""
		return self._get_attribute('pfcPriorityGroups')
	@PfcPriorityGroups.setter
	def PfcPriorityGroups(self, value):
		self._set_attribute('pfcPriorityGroups', value)

	@property
	def PriorityGroupSize(self):
		"""The maximum size of a Priority Group.

		Returns:
			str(priorityGroupSize-4|priorityGroupSize-8)
		"""
		return self._get_attribute('priorityGroupSize')
	@PriorityGroupSize.setter
	def PriorityGroupSize(self, value):
		self._set_attribute('priorityGroupSize', value)

	@property
	def SupportDataCenterMode(self):
		"""If true, this mode automatically sets Transmit Mode to Interleaved Streams.

		Returns:
			bool
		"""
		return self._get_attribute('supportDataCenterMode')
	@SupportDataCenterMode.setter
	def SupportDataCenterMode(self, value):
		self._set_attribute('supportDataCenterMode', value)
