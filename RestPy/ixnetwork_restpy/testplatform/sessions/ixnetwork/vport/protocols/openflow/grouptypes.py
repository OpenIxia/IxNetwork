
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


class GroupTypes(Base):
	"""The GroupTypes class encapsulates a required groupTypes node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the GroupTypes property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'groupTypes'

	def __init__(self, parent):
		super(GroupTypes, self).__init__(parent)

	@property
	def All(self):
		"""If selected, all buckets in the group are forwarded. This group is used for multicast or broadcast forwarding. The packet is effectively cloned for each bucket. One packet is processed for each bucket of the group.

		Returns:
			bool
		"""
		return self._get_attribute('all')
	@All.setter
	def All(self, value):
		self._set_attribute('all', value)

	@property
	def FastFailover(self):
		"""If selected, the first active bucket is forwarded. Each action bucket is associated with a specific port and/or group that controls its liveness. The buckets are evaluated in the order defined by the group, and the first bucket which is associated with a live port/group is selected. This group type allows the switch to change forwarding without requiring a round trip to the controller. If no buckets are live, packets are dropped.

		Returns:
			bool
		"""
		return self._get_attribute('fastFailover')
	@FastFailover.setter
	def FastFailover(self, value):
		self._set_attribute('fastFailover', value)

	@property
	def Indirect(self):
		"""If selected, the one defined bucket in this group is forwarded. This group supports only a single bucket. It allows multiple flow entries or groups to point to a common group identifier, supporting faster, more efficient convergence. For instance, next hops for IP forwarding.

		Returns:
			bool
		"""
		return self._get_attribute('indirect')
	@Indirect.setter
	def Indirect(self, value):
		self._set_attribute('indirect', value)

	@property
	def Select(self):
		"""If selected, a single bucket in the group is forwarded.

		Returns:
			bool
		"""
		return self._get_attribute('select')
	@Select.setter
	def Select(self, value):
		self._set_attribute('select', value)
