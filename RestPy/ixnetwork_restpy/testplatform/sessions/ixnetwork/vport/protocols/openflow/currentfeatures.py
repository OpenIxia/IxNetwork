
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


class CurrentFeatures(Base):
	"""The CurrentFeatures class encapsulates a required currentFeatures node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the CurrentFeatures property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'currentFeatures'

	def __init__(self, parent):
		super(CurrentFeatures, self).__init__(parent)

	@property
	def 100MbFd(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('100MbFd')
	@100MbFd.setter
	def 100MbFd(self, value):
		self._set_attribute('100MbFd', value)

	@property
	def 100MbHd(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('100MbHd')
	@100MbHd.setter
	def 100MbHd(self, value):
		self._set_attribute('100MbHd', value)

	@property
	def 10GbFd(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('10GbFd')
	@10GbFd.setter
	def 10GbFd(self, value):
		self._set_attribute('10GbFd', value)

	@property
	def 10MbFd(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('10MbFd')
	@10MbFd.setter
	def 10MbFd(self, value):
		self._set_attribute('10MbFd', value)

	@property
	def 10MbHd(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('10MbHd')
	@10MbHd.setter
	def 10MbHd(self, value):
		self._set_attribute('10MbHd', value)

	@property
	def 1GbFd(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('1GbFd')
	@1GbFd.setter
	def 1GbFd(self, value):
		self._set_attribute('1GbFd', value)

	@property
	def 1GbHd(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('1GbHd')
	@1GbHd.setter
	def 1GbHd(self, value):
		self._set_attribute('1GbHd', value)

	@property
	def AsymmetricPause(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('asymmetricPause')
	@AsymmetricPause.setter
	def AsymmetricPause(self, value):
		self._set_attribute('asymmetricPause', value)

	@property
	def AutoNegotiation(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('autoNegotiation')
	@AutoNegotiation.setter
	def AutoNegotiation(self, value):
		self._set_attribute('autoNegotiation', value)

	@property
	def CopperMedium(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('copperMedium')
	@CopperMedium.setter
	def CopperMedium(self, value):
		self._set_attribute('copperMedium', value)

	@property
	def FiberMedium(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('fiberMedium')
	@FiberMedium.setter
	def FiberMedium(self, value):
		self._set_attribute('fiberMedium', value)

	@property
	def Pause(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('pause')
	@Pause.setter
	def Pause(self, value):
		self._set_attribute('pause', value)
