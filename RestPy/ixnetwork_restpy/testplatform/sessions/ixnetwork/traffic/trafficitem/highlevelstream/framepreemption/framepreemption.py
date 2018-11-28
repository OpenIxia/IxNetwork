
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


class FramePreemption(Base):
	"""The FramePreemption class encapsulates a required framePreemption node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the FramePreemption property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'framePreemption'

	def __init__(self, parent):
		super(FramePreemption, self).__init__(parent)

	@property
	def AutoFragmentCount(self):
		"""Let the fragments be auto counted

		Returns:
			bool
		"""
		return self._get_attribute('autoFragmentCount')
	@AutoFragmentCount.setter
	def AutoFragmentCount(self, value):
		self._set_attribute('autoFragmentCount', value)

	@property
	def Enable(self):
		"""Enable frame preemption on the given stream. Disabled indicates an express frame

		Returns:
			bool
		"""
		return self._get_attribute('enable')
	@Enable.setter
	def Enable(self, value):
		self._set_attribute('enable', value)

	@property
	def FragmentCount(self):
		"""Set the fragment count (a value between 0 and 3)

		Returns:
			number
		"""
		return self._get_attribute('fragmentCount')
	@FragmentCount.setter
	def FragmentCount(self, value):
		self._set_attribute('fragmentCount', value)

	@property
	def FrameType(self):
		"""Select the frame type

		Returns:
			str(control|fragment|invalid|wholeFrame)
		"""
		return self._get_attribute('frameType')
	@FrameType.setter
	def FrameType(self, value):
		self._set_attribute('frameType', value)

	@property
	def LastFragment(self):
		"""Indicates if this is the last fragment of the preemptable packet

		Returns:
			bool
		"""
		return self._get_attribute('lastFragment')
	@LastFragment.setter
	def LastFragment(self, value):
		self._set_attribute('lastFragment', value)

	@property
	def SmdType(self):
		"""Select the SMD type

		Returns:
			str(autoSMDC|autoSMDS|invalidSMD|smdC0|smdC1|smdC2|smdC3|smdE|smdR|smdS0|smdS1|smdS2|smdS3|smdV)
		"""
		return self._get_attribute('smdType')
	@SmdType.setter
	def SmdType(self, value):
		self._set_attribute('smdType', value)
