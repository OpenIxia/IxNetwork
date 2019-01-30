
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


class VendorStatLearnedInformation(Base):
	"""The VendorStatLearnedInformation class encapsulates a system managed vendorStatLearnedInformation node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the VendorStatLearnedInformation property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'vendorStatLearnedInformation'

	def __init__(self, parent):
		super(VendorStatLearnedInformation, self).__init__(parent)

	@property
	def DataPathId(self):
		"""Signifies the datapath ID of the OpenFlow switch.

		Returns:
			str
		"""
		return self._get_attribute('dataPathId')

	@property
	def DataPathIdAsHex(self):
		"""Signifies the datapath ID of the OpenFlow switch in hexadecimal format.

		Returns:
			str
		"""
		return self._get_attribute('dataPathIdAsHex')

	@property
	def ErrorCode(self):
		"""Signifies the error code of the error received

		Returns:
			str
		"""
		return self._get_attribute('errorCode')

	@property
	def ErrorType(self):
		"""Signifies the type of the error received.

		Returns:
			str
		"""
		return self._get_attribute('errorType')

	@property
	def ExperimenterType(self):
		"""Type of experimenter.

		Returns:
			number
		"""
		return self._get_attribute('experimenterType')

	@property
	def Latency(self):
		"""Signifies the latency measurement for the OpenFlow channel in microseconds.

		Returns:
			number
		"""
		return self._get_attribute('latency')

	@property
	def LocalIp(self):
		"""Signifies the local IP address of the selected interface.

		Returns:
			str
		"""
		return self._get_attribute('localIp')

	@property
	def MessageLength(self):
		"""Signifies the length of the message transmitted.

		Returns:
			number
		"""
		return self._get_attribute('messageLength')

	@property
	def NegotiatedVersion(self):
		"""Version of the protocol that has been negotiated between OpenFLow Controller and Switch.

		Returns:
			str
		"""
		return self._get_attribute('negotiatedVersion')

	@property
	def RemoteIp(self):
		"""The IP address of the DUT at the other end of the Open Flow channel.

		Returns:
			str
		"""
		return self._get_attribute('remoteIp')

	@property
	def ReplyState(self):
		"""Signifies the reply state of the OF Channel.

		Returns:
			str
		"""
		return self._get_attribute('replyState')

	@property
	def VendorId(self):
		"""Signifies the vendor identifier.

		Returns:
			number
		"""
		return self._get_attribute('vendorId')

	@property
	def VendorMessage(self):
		"""Signifies the vendor message value.

		Returns:
			str
		"""
		return self._get_attribute('vendorMessage')

	def find(self, DataPathId=None, DataPathIdAsHex=None, ErrorCode=None, ErrorType=None, ExperimenterType=None, Latency=None, LocalIp=None, MessageLength=None, NegotiatedVersion=None, RemoteIp=None, ReplyState=None, VendorId=None, VendorMessage=None):
		"""Finds and retrieves vendorStatLearnedInformation data from the server.

		All named parameters support regex and can be used to selectively retrieve vendorStatLearnedInformation data from the server.
		By default the find method takes no parameters and will retrieve all vendorStatLearnedInformation data from the server.

		Args:
			DataPathId (str): Signifies the datapath ID of the OpenFlow switch.
			DataPathIdAsHex (str): Signifies the datapath ID of the OpenFlow switch in hexadecimal format.
			ErrorCode (str): Signifies the error code of the error received
			ErrorType (str): Signifies the type of the error received.
			ExperimenterType (number): Type of experimenter.
			Latency (number): Signifies the latency measurement for the OpenFlow channel in microseconds.
			LocalIp (str): Signifies the local IP address of the selected interface.
			MessageLength (number): Signifies the length of the message transmitted.
			NegotiatedVersion (str): Version of the protocol that has been negotiated between OpenFLow Controller and Switch.
			RemoteIp (str): The IP address of the DUT at the other end of the Open Flow channel.
			ReplyState (str): Signifies the reply state of the OF Channel.
			VendorId (number): Signifies the vendor identifier.
			VendorMessage (str): Signifies the vendor message value.

		Returns:
			self: This instance with matching vendorStatLearnedInformation data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of vendorStatLearnedInformation data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the vendorStatLearnedInformation data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
