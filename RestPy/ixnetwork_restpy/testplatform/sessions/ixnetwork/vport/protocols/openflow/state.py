
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


class State(Base):
	"""The State class encapsulates a required state node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the State property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'state'

	def __init__(self, parent):
		super(State, self).__init__(parent)

	@property
	def LinkDown(self):
		"""Indicates that, no physical link is present.

		Returns:
			bool
		"""
		return self._get_attribute('linkDown')
	@LinkDown.setter
	def LinkDown(self, value):
		self._set_attribute('linkDown', value)

	@property
	def StpBlock(self):
		"""Indicates that the port is not part of spanning tree.

		Returns:
			bool
		"""
		return self._get_attribute('stpBlock')
	@StpBlock.setter
	def StpBlock(self, value):
		self._set_attribute('stpBlock', value)

	@property
	def StpForward(self):
		"""Indicates that the port is learning and relaying frames.

		Returns:
			bool
		"""
		return self._get_attribute('stpForward')
	@StpForward.setter
	def StpForward(self, value):
		self._set_attribute('stpForward', value)

	@property
	def StpLearn(self):
		"""Indicates that the port is learning but not relaying frames.

		Returns:
			bool
		"""
		return self._get_attribute('stpLearn')
	@StpLearn.setter
	def StpLearn(self, value):
		self._set_attribute('stpLearn', value)

	@property
	def StpListen(self):
		"""Indicates that the port is not learning or relaying frames.

		Returns:
			bool
		"""
		return self._get_attribute('stpListen')
	@StpListen.setter
	def StpListen(self, value):
		self._set_attribute('stpListen', value)
