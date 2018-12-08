
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


class LearnedFilter(Base):
	"""The LearnedFilter class encapsulates a required learnedFilter node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the LearnedFilter property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'learnedFilter'

	def __init__(self, parent):
		super(LearnedFilter, self).__init__(parent)

	@property
	def EnableFilter(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableFilter')
	@EnableFilter.setter
	def EnableFilter(self, value):
		self._set_attribute('enableFilter', value)

	@property
	def EnableIpv4FecAddress(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableIpv4FecAddress')
	@EnableIpv4FecAddress.setter
	def EnableIpv4FecAddress(self, value):
		self._set_attribute('enableIpv4FecAddress', value)

	@property
	def EnableIpv4FecMask(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableIpv4FecMask')
	@EnableIpv4FecMask.setter
	def EnableIpv4FecMask(self, value):
		self._set_attribute('enableIpv4FecMask', value)

	@property
	def EnableIpv4RootAddress(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableIpv4RootAddress')
	@EnableIpv4RootAddress.setter
	def EnableIpv4RootAddress(self, value):
		self._set_attribute('enableIpv4RootAddress', value)

	@property
	def EnableLabel(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableLabel')
	@EnableLabel.setter
	def EnableLabel(self, value):
		self._set_attribute('enableLabel', value)

	@property
	def EnableMartiniDescription(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableMartiniDescription')
	@EnableMartiniDescription.setter
	def EnableMartiniDescription(self, value):
		self._set_attribute('enableMartiniDescription', value)

	@property
	def EnableMartiniGroupId(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableMartiniGroupId')
	@EnableMartiniGroupId.setter
	def EnableMartiniGroupId(self, value):
		self._set_attribute('enableMartiniGroupId', value)

	@property
	def EnableMartiniVcId(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableMartiniVcId')
	@EnableMartiniVcId.setter
	def EnableMartiniVcId(self, value):
		self._set_attribute('enableMartiniVcId', value)

	@property
	def EnableMartiniVcType(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableMartiniVcType')
	@EnableMartiniVcType.setter
	def EnableMartiniVcType(self, value):
		self._set_attribute('enableMartiniVcType', value)

	@property
	def EnablePeerAddress(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enablePeerAddress')
	@EnablePeerAddress.setter
	def EnablePeerAddress(self, value):
		self._set_attribute('enablePeerAddress', value)

	@property
	def EnablePeerMask(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enablePeerMask')
	@EnablePeerMask.setter
	def EnablePeerMask(self, value):
		self._set_attribute('enablePeerMask', value)

	@property
	def Ipv4FecAddress(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('ipv4FecAddress')
	@Ipv4FecAddress.setter
	def Ipv4FecAddress(self, value):
		self._set_attribute('ipv4FecAddress', value)

	@property
	def Ipv4FecMask(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('ipv4FecMask')
	@Ipv4FecMask.setter
	def Ipv4FecMask(self, value):
		self._set_attribute('ipv4FecMask', value)

	@property
	def Ipv4FecMaskMatch(self):
		"""

		Returns:
			str(exactMatch|looseMatch)
		"""
		return self._get_attribute('ipv4FecMaskMatch')
	@Ipv4FecMaskMatch.setter
	def Ipv4FecMaskMatch(self, value):
		self._set_attribute('ipv4FecMaskMatch', value)

	@property
	def Label(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('label')
	@Label.setter
	def Label(self, value):
		self._set_attribute('label', value)

	@property
	def MartiniDescription(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('martiniDescription')
	@MartiniDescription.setter
	def MartiniDescription(self, value):
		self._set_attribute('martiniDescription', value)

	@property
	def MartiniGroupId(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('martiniGroupId')
	@MartiniGroupId.setter
	def MartiniGroupId(self, value):
		self._set_attribute('martiniGroupId', value)

	@property
	def MartiniVcId(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('martiniVcId')
	@MartiniVcId.setter
	def MartiniVcId(self, value):
		self._set_attribute('martiniVcId', value)

	@property
	def MartiniVcType(self):
		"""

		Returns:
			str(frameRelay|atmaal5|atmxCell|vlan|ethernet|hdlc|ppp|cem|atmvcc|atmvpc|ip)
		"""
		return self._get_attribute('martiniVcType')
	@MartiniVcType.setter
	def MartiniVcType(self, value):
		self._set_attribute('martiniVcType', value)

	@property
	def PeerAddress(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('peerAddress')
	@PeerAddress.setter
	def PeerAddress(self, value):
		self._set_attribute('peerAddress', value)

	@property
	def PeerMask(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('peerMask')
	@PeerMask.setter
	def PeerMask(self, value):
		self._set_attribute('peerMask', value)

	@property
	def RootAddress(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('rootAddress')
	@RootAddress.setter
	def RootAddress(self, value):
		self._set_attribute('rootAddress', value)
