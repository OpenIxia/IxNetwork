
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


class Ppp(Base):
	"""The Ppp class encapsulates a required ppp node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Ppp property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'ppp'

	def __init__(self, parent):
		super(Ppp, self).__init__(parent)

	@property
	def ConfigurationRetries(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('configurationRetries')
	@ConfigurationRetries.setter
	def ConfigurationRetries(self, value):
		self._set_attribute('configurationRetries', value)

	@property
	def EnableAccmNegotiation(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableAccmNegotiation')
	@EnableAccmNegotiation.setter
	def EnableAccmNegotiation(self, value):
		self._set_attribute('enableAccmNegotiation', value)

	@property
	def EnableIpV4(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableIpV4')
	@EnableIpV4.setter
	def EnableIpV4(self, value):
		self._set_attribute('enableIpV4', value)

	@property
	def EnableIpV6(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableIpV6')
	@EnableIpV6.setter
	def EnableIpV6(self, value):
		self._set_attribute('enableIpV6', value)

	@property
	def EnableLqm(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableLqm')
	@EnableLqm.setter
	def EnableLqm(self, value):
		self._set_attribute('enableLqm', value)

	@property
	def EnableMpls(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableMpls')
	@EnableMpls.setter
	def EnableMpls(self, value):
		self._set_attribute('enableMpls', value)

	@property
	def EnableOsi(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableOsi')
	@EnableOsi.setter
	def EnableOsi(self, value):
		self._set_attribute('enableOsi', value)

	@property
	def Enabled(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def LocalIpAddress(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('localIpAddress')
	@LocalIpAddress.setter
	def LocalIpAddress(self, value):
		self._set_attribute('localIpAddress', value)

	@property
	def LocalIpV6IdType(self):
		"""

		Returns:
			str(ipV6|lastNegotiated|macBased|random)
		"""
		return self._get_attribute('localIpV6IdType')
	@LocalIpV6IdType.setter
	def LocalIpV6IdType(self, value):
		self._set_attribute('localIpV6IdType', value)

	@property
	def LocalIpV6Iid(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('localIpV6Iid')
	@LocalIpV6Iid.setter
	def LocalIpV6Iid(self, value):
		self._set_attribute('localIpV6Iid', value)

	@property
	def LocalIpV6MacBasedIid(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('localIpV6MacBasedIid')
	@LocalIpV6MacBasedIid.setter
	def LocalIpV6MacBasedIid(self, value):
		self._set_attribute('localIpV6MacBasedIid', value)

	@property
	def LocalIpV6NegotiationMode(self):
		"""

		Returns:
			str(localMay|localMust|peerMust)
		"""
		return self._get_attribute('localIpV6NegotiationMode')
	@LocalIpV6NegotiationMode.setter
	def LocalIpV6NegotiationMode(self, value):
		self._set_attribute('localIpV6NegotiationMode', value)

	@property
	def LqmReportInterval(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('lqmReportInterval')
	@LqmReportInterval.setter
	def LqmReportInterval(self, value):
		self._set_attribute('lqmReportInterval', value)

	@property
	def PeerIpV6IdType(self):
		"""

		Returns:
			str(ipV6|lastNegotiated|macBased|random)
		"""
		return self._get_attribute('peerIpV6IdType')
	@PeerIpV6IdType.setter
	def PeerIpV6IdType(self, value):
		self._set_attribute('peerIpV6IdType', value)

	@property
	def PeerIpV6Iid(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('peerIpV6Iid')
	@PeerIpV6Iid.setter
	def PeerIpV6Iid(self, value):
		self._set_attribute('peerIpV6Iid', value)

	@property
	def PeerIpV6MacBasedIid(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('peerIpV6MacBasedIid')
	@PeerIpV6MacBasedIid.setter
	def PeerIpV6MacBasedIid(self, value):
		self._set_attribute('peerIpV6MacBasedIid', value)

	@property
	def PeerIpV6NegotiationMode(self):
		"""

		Returns:
			str(localMust|peerMay|peerMust)
		"""
		return self._get_attribute('peerIpV6NegotiationMode')
	@PeerIpV6NegotiationMode.setter
	def PeerIpV6NegotiationMode(self, value):
		self._set_attribute('peerIpV6NegotiationMode', value)

	@property
	def PppLinkState(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('pppLinkState')

	@property
	def RetryTimeout(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('retryTimeout')
	@RetryTimeout.setter
	def RetryTimeout(self, value):
		self._set_attribute('retryTimeout', value)

	@property
	def RxAlignment(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('rxAlignment')
	@RxAlignment.setter
	def RxAlignment(self, value):
		self._set_attribute('rxAlignment', value)

	@property
	def RxMaxReceiveUnit(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('rxMaxReceiveUnit')
	@RxMaxReceiveUnit.setter
	def RxMaxReceiveUnit(self, value):
		self._set_attribute('rxMaxReceiveUnit', value)

	@property
	def TxAlignment(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('txAlignment')
	@TxAlignment.setter
	def TxAlignment(self, value):
		self._set_attribute('txAlignment', value)

	@property
	def TxMaxReceiveUnit(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('txMaxReceiveUnit')
	@TxMaxReceiveUnit.setter
	def TxMaxReceiveUnit(self, value):
		self._set_attribute('txMaxReceiveUnit', value)

	@property
	def UseMagicNumber(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('useMagicNumber')
	@UseMagicNumber.setter
	def UseMagicNumber(self, value):
		self._set_attribute('useMagicNumber', value)
