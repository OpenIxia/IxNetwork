
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


class Interfaces(Base):
	"""The Interfaces class encapsulates a required interfaces node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Interfaces property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'interfaces'

	def __init__(self, parent):
		super(Interfaces, self).__init__(parent)

	@property
	def ArpOnLinkup(self):
		"""If true, automatically enables ARP and PING when the interfaces is associated with a port.

		Returns:
			bool
		"""
		return self._get_attribute('arpOnLinkup')
	@ArpOnLinkup.setter
	def ArpOnLinkup(self, value):
		self._set_attribute('arpOnLinkup', value)

	@property
	def NsOnLinkup(self):
		"""If true, automatically enables NS when the interfaces is associated with a port.

		Returns:
			bool
		"""
		return self._get_attribute('nsOnLinkup')
	@NsOnLinkup.setter
	def NsOnLinkup(self, value):
		self._set_attribute('nsOnLinkup', value)

	@property
	def SendSingleArpPerGateway(self):
		"""If true, only a single ARP is sent via each defined gateway address.

		Returns:
			bool
		"""
		return self._get_attribute('sendSingleArpPerGateway')
	@SendSingleArpPerGateway.setter
	def SendSingleArpPerGateway(self, value):
		self._set_attribute('sendSingleArpPerGateway', value)

	@property
	def SendSingleNsPerGateway(self):
		"""If true, only a single NS is sent via each defined gateway address.

		Returns:
			bool
		"""
		return self._get_attribute('sendSingleNsPerGateway')
	@SendSingleNsPerGateway.setter
	def SendSingleNsPerGateway(self, value):
		self._set_attribute('sendSingleNsPerGateway', value)
