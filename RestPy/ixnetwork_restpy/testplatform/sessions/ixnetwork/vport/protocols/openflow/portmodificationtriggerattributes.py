
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


class PortModificationTriggerAttributes(Base):
	"""The PortModificationTriggerAttributes class encapsulates a required portModificationTriggerAttributes node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the PortModificationTriggerAttributes property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'portModificationTriggerAttributes'

	def __init__(self, parent):
		super(PortModificationTriggerAttributes, self).__init__(parent)

	@property
	def LinkFeature(self):
		"""An instance of the LinkFeature class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.linkfeature.LinkFeature)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.linkfeature import LinkFeature
		return LinkFeature(self)._select()

	@property
	def LinkMode(self):
		"""An instance of the LinkMode class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.linkmode.LinkMode)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.linkmode import LinkMode
		return LinkMode(self)._select()

	@property
	def LinkType(self):
		"""An instance of the LinkType class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.linktype.LinkType)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.linktype import LinkType
		return LinkType(self)._select()

	@property
	def AdvertisedFeatures(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('advertisedFeatures')
	@AdvertisedFeatures.setter
	def AdvertisedFeatures(self, value):
		self._set_attribute('advertisedFeatures', value)

	@property
	def DoNotSendPacketIn(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('doNotSendPacketIn')
	@DoNotSendPacketIn.setter
	def DoNotSendPacketIn(self, value):
		self._set_attribute('doNotSendPacketIn', value)

	@property
	def DropAllPackets(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('dropAllPackets')
	@DropAllPackets.setter
	def DropAllPackets(self, value):
		self._set_attribute('dropAllPackets', value)

	@property
	def DropForwardedPackets(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('dropForwardedPackets')
	@DropForwardedPackets.setter
	def DropForwardedPackets(self, value):
		self._set_attribute('dropForwardedPackets', value)

	@property
	def EnableAdvertiseFeature(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableAdvertiseFeature')
	@EnableAdvertiseFeature.setter
	def EnableAdvertiseFeature(self, value):
		self._set_attribute('enableAdvertiseFeature', value)

	@property
	def EnableEthernetAddress(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableEthernetAddress')
	@EnableEthernetAddress.setter
	def EnableEthernetAddress(self, value):
		self._set_attribute('enableEthernetAddress', value)

	@property
	def EnablePortConfig(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enablePortConfig')
	@EnablePortConfig.setter
	def EnablePortConfig(self, value):
		self._set_attribute('enablePortConfig', value)

	@property
	def EnablePortModPortFeatures(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enablePortModPortFeatures')
	@EnablePortModPortFeatures.setter
	def EnablePortModPortFeatures(self, value):
		self._set_attribute('enablePortModPortFeatures', value)

	@property
	def EnablePortNumber(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enablePortNumber')
	@EnablePortNumber.setter
	def EnablePortNumber(self, value):
		self._set_attribute('enablePortNumber', value)

	@property
	def EthernetAddress(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('ethernetAddress')
	@EthernetAddress.setter
	def EthernetAddress(self, value):
		self._set_attribute('ethernetAddress', value)

	@property
	def PortAdministrativelyDown(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('portAdministrativelyDown')
	@PortAdministrativelyDown.setter
	def PortAdministrativelyDown(self, value):
		self._set_attribute('portAdministrativelyDown', value)

	@property
	def PortConfig(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('portConfig')
	@PortConfig.setter
	def PortConfig(self, value):
		self._set_attribute('portConfig', value)

	@property
	def PortConfigMask(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('portConfigMask')
	@PortConfigMask.setter
	def PortConfigMask(self, value):
		self._set_attribute('portConfigMask', value)

	@property
	def PortNumber(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('portNumber')
	@PortNumber.setter
	def PortNumber(self, value):
		self._set_attribute('portNumber', value)
