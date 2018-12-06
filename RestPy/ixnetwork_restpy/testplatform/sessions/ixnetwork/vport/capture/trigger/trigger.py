
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


class Trigger(Base):
	"""The Trigger class encapsulates a required trigger node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Trigger property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'trigger'

	def __init__(self, parent):
		super(Trigger, self).__init__(parent)

	@property
	def CaptureTriggerDA(self):
		"""

		Returns:
			str(addr1|addr2|anyAddr|notAddr1|notAddr2)
		"""
		return self._get_attribute('captureTriggerDA')
	@CaptureTriggerDA.setter
	def CaptureTriggerDA(self, value):
		self._set_attribute('captureTriggerDA', value)

	@property
	def CaptureTriggerEnable(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('captureTriggerEnable')
	@CaptureTriggerEnable.setter
	def CaptureTriggerEnable(self, value):
		self._set_attribute('captureTriggerEnable', value)

	@property
	def CaptureTriggerError(self):
		"""

		Returns:
			str(errAnyFrame|errAnyIpTcpUdpChecksumError|errAnySequencekError|errBadCRC|errBadFrame|errBigSequenceError|errDataIntegrityError|errGoodFrame|errInvalidFcoeFrame|errReverseSequenceError|errSmallSequenceError)
		"""
		return self._get_attribute('captureTriggerError')
	@CaptureTriggerError.setter
	def CaptureTriggerError(self, value):
		self._set_attribute('captureTriggerError', value)

	@property
	def CaptureTriggerExpressionString(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('captureTriggerExpressionString')
	@CaptureTriggerExpressionString.setter
	def CaptureTriggerExpressionString(self, value):
		self._set_attribute('captureTriggerExpressionString', value)

	@property
	def CaptureTriggerFrameSizeEnable(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('captureTriggerFrameSizeEnable')
	@CaptureTriggerFrameSizeEnable.setter
	def CaptureTriggerFrameSizeEnable(self, value):
		self._set_attribute('captureTriggerFrameSizeEnable', value)

	@property
	def CaptureTriggerFrameSizeFrom(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('captureTriggerFrameSizeFrom')
	@CaptureTriggerFrameSizeFrom.setter
	def CaptureTriggerFrameSizeFrom(self, value):
		self._set_attribute('captureTriggerFrameSizeFrom', value)

	@property
	def CaptureTriggerFrameSizeTo(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('captureTriggerFrameSizeTo')
	@CaptureTriggerFrameSizeTo.setter
	def CaptureTriggerFrameSizeTo(self, value):
		self._set_attribute('captureTriggerFrameSizeTo', value)

	@property
	def CaptureTriggerPattern(self):
		"""

		Returns:
			str(anyPattern|notPattern1|notPattern2|pattern1|pattern1AndPattern2|pattern2)
		"""
		return self._get_attribute('captureTriggerPattern')
	@CaptureTriggerPattern.setter
	def CaptureTriggerPattern(self, value):
		self._set_attribute('captureTriggerPattern', value)

	@property
	def CaptureTriggerSA(self):
		"""

		Returns:
			str(addr1|addr2|anyAddr|notAddr1|notAddr2)
		"""
		return self._get_attribute('captureTriggerSA')
	@CaptureTriggerSA.setter
	def CaptureTriggerSA(self, value):
		self._set_attribute('captureTriggerSA', value)
