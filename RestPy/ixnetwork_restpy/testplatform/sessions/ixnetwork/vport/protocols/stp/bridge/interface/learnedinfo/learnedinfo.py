
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


class LearnedInfo(Base):
	"""The LearnedInfo class encapsulates a required learnedInfo node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the LearnedInfo property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'learnedInfo'

	def __init__(self, parent):
		super(LearnedInfo, self).__init__(parent)

	@property
	def DesignatedCost(self):
		"""Root Path Cost. The administrative cost for the shortest path from this bridge to the Root bridge. A 4-byte unsigned integer. The default is 0.

		Returns:
			number
		"""
		return self._get_attribute('designatedCost')

	@property
	def DesignatedMac(self):
		"""(Read-only) The 6-byte MAC address of the designated bridge on the LAN segment.

		Returns:
			str
		"""
		return self._get_attribute('designatedMac')

	@property
	def DesignatedPortId(self):
		"""(Read-only) The port ID of the designated bridge's designated port on the LAN segment.

		Returns:
			number
		"""
		return self._get_attribute('designatedPortId')

	@property
	def DesignatedPriority(self):
		"""(Read-only) The priority of the designated bridge on the LAN segment.

		Returns:
			number
		"""
		return self._get_attribute('designatedPriority')

	@property
	def InterfaceDesc(self):
		"""(Read-only) The descriptive identifier of the protocol interface.

		Returns:
			str
		"""
		return self._get_attribute('interfaceDesc')

	@property
	def InterfaceRole(self):
		"""(Read-only) The role of the Interface. One of the following options: Disabled, Root, Designated, Alternate, or Backup.

		Returns:
			str
		"""
		return self._get_attribute('interfaceRole')

	@property
	def InterfaceState(self):
		"""Read-only) The state of the interface. One of the following options: Discarding, learning, or forwarding.

		Returns:
			str
		"""
		return self._get_attribute('interfaceState')

	@property
	def RootMac(self):
		"""(Read-only) The 6-byte MAC address of the root bridge.

		Returns:
			str
		"""
		return self._get_attribute('rootMac')

	@property
	def RootPriority(self):
		"""(Read-only) The priority of the root bridge.

		Returns:
			number
		"""
		return self._get_attribute('rootPriority')
