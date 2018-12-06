
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


class TrillPingOam(Base):
	"""The TrillPingOam class encapsulates a required trillPingOam node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the TrillPingOam property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'trillPingOam'

	def __init__(self, parent):
		super(TrillPingOam, self).__init__(parent)

	@property
	def AlertFlag(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('alertFlag')
	@AlertFlag.setter
	def AlertFlag(self, value):
		self._set_attribute('alertFlag', value)

	@property
	def DestinationNickname(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('destinationNickname')
	@DestinationNickname.setter
	def DestinationNickname(self, value):
		self._set_attribute('destinationNickname', value)

	@property
	def EtherType(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('etherType')
	@EtherType.setter
	def EtherType(self, value):
		self._set_attribute('etherType', value)

	@property
	def HopCount(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('hopCount')
	@HopCount.setter
	def HopCount(self, value):
		self._set_attribute('hopCount', value)

	@property
	def NativeFlag(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('nativeFlag')
	@NativeFlag.setter
	def NativeFlag(self, value):
		self._set_attribute('nativeFlag', value)

	@property
	def NoOfPingRequests(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('noOfPingRequests')
	@NoOfPingRequests.setter
	def NoOfPingRequests(self, value):
		self._set_attribute('noOfPingRequests', value)

	@property
	def SilentFlag(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('silentFlag')
	@SilentFlag.setter
	def SilentFlag(self, value):
		self._set_attribute('silentFlag', value)

	@property
	def SourceNickname(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('sourceNickname')
	@SourceNickname.setter
	def SourceNickname(self, value):
		self._set_attribute('sourceNickname', value)

	@property
	def TimeOut(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('timeOut')
	@TimeOut.setter
	def TimeOut(self, value):
		self._set_attribute('timeOut', value)
