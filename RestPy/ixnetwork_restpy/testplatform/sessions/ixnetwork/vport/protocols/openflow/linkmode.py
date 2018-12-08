
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


class LinkMode(Base):
	"""The LinkMode class encapsulates a required linkMode node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the LinkMode property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'linkMode'

	def __init__(self, parent):
		super(LinkMode, self).__init__(parent)

	@property
	def Ofppf100GbFd(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('ofppf100GbFd')
	@Ofppf100GbFd.setter
	def Ofppf100GbFd(self, value):
		self._set_attribute('ofppf100GbFd', value)

	@property
	def Ofppf100MbFd(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('ofppf100MbFd')
	@Ofppf100MbFd.setter
	def Ofppf100MbFd(self, value):
		self._set_attribute('ofppf100MbFd', value)

	@property
	def Ofppf100MbHd(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('ofppf100MbHd')
	@Ofppf100MbHd.setter
	def Ofppf100MbHd(self, value):
		self._set_attribute('ofppf100MbHd', value)

	@property
	def Ofppf10GbFd(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('ofppf10GbFd')
	@Ofppf10GbFd.setter
	def Ofppf10GbFd(self, value):
		self._set_attribute('ofppf10GbFd', value)

	@property
	def Ofppf10MbFd(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('ofppf10MbFd')
	@Ofppf10MbFd.setter
	def Ofppf10MbFd(self, value):
		self._set_attribute('ofppf10MbFd', value)

	@property
	def Ofppf10MbHd(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('ofppf10MbHd')
	@Ofppf10MbHd.setter
	def Ofppf10MbHd(self, value):
		self._set_attribute('ofppf10MbHd', value)

	@property
	def Ofppf1GbFd(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('ofppf1GbFd')
	@Ofppf1GbFd.setter
	def Ofppf1GbFd(self, value):
		self._set_attribute('ofppf1GbFd', value)

	@property
	def Ofppf1GbHd(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('ofppf1GbHd')
	@Ofppf1GbHd.setter
	def Ofppf1GbHd(self, value):
		self._set_attribute('ofppf1GbHd', value)

	@property
	def Ofppf1TbFd(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('ofppf1TbFd')
	@Ofppf1TbFd.setter
	def Ofppf1TbFd(self, value):
		self._set_attribute('ofppf1TbFd', value)

	@property
	def Ofppf40GbFd(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('ofppf40GbFd')
	@Ofppf40GbFd.setter
	def Ofppf40GbFd(self, value):
		self._set_attribute('ofppf40GbFd', value)

	@property
	def OfppfOther(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('ofppfOther')
	@OfppfOther.setter
	def OfppfOther(self, value):
		self._set_attribute('ofppfOther', value)
