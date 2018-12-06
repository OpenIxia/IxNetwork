
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


class Gre(Base):
	"""The Gre class encapsulates a required gre node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Gre property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'gre'

	def __init__(self, parent):
		super(Gre, self).__init__(parent)

	@property
	def Dest(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('dest')
	@Dest.setter
	def Dest(self, value):
		self._set_attribute('dest', value)

	@property
	def InKey(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('inKey')
	@InKey.setter
	def InKey(self, value):
		self._set_attribute('inKey', value)

	@property
	def OutKey(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('outKey')
	@OutKey.setter
	def OutKey(self, value):
		self._set_attribute('outKey', value)

	@property
	def Source(self):
		"""

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=ipv4|/api/v1/sessions/1/ixnetwork/vport?deepchild=ipv6)
		"""
		return self._get_attribute('source')
	@Source.setter
	def Source(self, value):
		self._set_attribute('source', value)

	@property
	def UseChecksum(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('useChecksum')
	@UseChecksum.setter
	def UseChecksum(self, value):
		self._set_attribute('useChecksum', value)

	@property
	def UseKey(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('useKey')
	@UseKey.setter
	def UseKey(self, value):
		self._set_attribute('useKey', value)

	@property
	def UseSequence(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('useSequence')
	@UseSequence.setter
	def UseSequence(self, value):
		self._set_attribute('useSequence', value)
