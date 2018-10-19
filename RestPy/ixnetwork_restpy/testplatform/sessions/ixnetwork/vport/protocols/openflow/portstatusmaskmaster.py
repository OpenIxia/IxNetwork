
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


class PortStatusMaskMaster(Base):
	"""The PortStatusMaskMaster class encapsulates a required portStatusMaskMaster node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the PortStatusMaskMaster property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'portStatusMaskMaster'

	def __init__(self, parent):
		super(PortStatusMaskMaster, self).__init__(parent)

	@property
	def PortAdd(self):
		"""This indicates that a port is added.

		Returns:
			bool
		"""
		return self._get_attribute('portAdd')
	@PortAdd.setter
	def PortAdd(self, value):
		self._set_attribute('portAdd', value)

	@property
	def PortDelete(self):
		"""This indicates that a port is removed.

		Returns:
			bool
		"""
		return self._get_attribute('portDelete')
	@PortDelete.setter
	def PortDelete(self, value):
		self._set_attribute('portDelete', value)

	@property
	def PortModify(self):
		"""This indicates that some attributes of the port is changed.

		Returns:
			bool
		"""
		return self._get_attribute('portModify')
	@PortModify.setter
	def PortModify(self, value):
		self._set_attribute('portModify', value)
