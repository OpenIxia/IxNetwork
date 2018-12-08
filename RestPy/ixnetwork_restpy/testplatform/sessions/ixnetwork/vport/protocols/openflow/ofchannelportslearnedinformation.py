
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


class OfChannelPortsLearnedInformation(Base):
	"""The OfChannelPortsLearnedInformation class encapsulates a system managed ofChannelPortsLearnedInformation node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the OfChannelPortsLearnedInformation property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'ofChannelPortsLearnedInformation'

	def __init__(self, parent):
		super(OfChannelPortsLearnedInformation, self).__init__(parent)

	@property
	def AdvertisedFeatures(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('advertisedFeatures')

	@property
	def Config(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('config')

	@property
	def CurrentFeatures(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('currentFeatures')

	@property
	def CurrentSpeed(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('currentSpeed')

	@property
	def DataPathId(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('dataPathId')

	@property
	def DataPathIdAsHex(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('dataPathIdAsHex')

	@property
	def EthernetAddress(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('ethernetAddress')

	@property
	def LocalIp(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('localIp')

	@property
	def MaximumSpeed(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('maximumSpeed')

	@property
	def Name(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('name')

	@property
	def PeerAdvertisedFeatures(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('peerAdvertisedFeatures')

	@property
	def PortNumber(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('portNumber')

	@property
	def RemoteIp(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('remoteIp')

	@property
	def State(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('state')

	@property
	def SupportedFeatures(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('supportedFeatures')

	def find(self, AdvertisedFeatures=None, Config=None, CurrentFeatures=None, CurrentSpeed=None, DataPathId=None, DataPathIdAsHex=None, EthernetAddress=None, LocalIp=None, MaximumSpeed=None, Name=None, PeerAdvertisedFeatures=None, PortNumber=None, RemoteIp=None, State=None, SupportedFeatures=None):
		"""Finds and retrieves ofChannelPortsLearnedInformation data from the server.

		All named parameters support regex and can be used to selectively retrieve ofChannelPortsLearnedInformation data from the server.
		By default the find method takes no parameters and will retrieve all ofChannelPortsLearnedInformation data from the server.

		Args:
			AdvertisedFeatures (str): 
			Config (str): 
			CurrentFeatures (str): 
			CurrentSpeed (number): 
			DataPathId (number): 
			DataPathIdAsHex (str): 
			EthernetAddress (str): 
			LocalIp (str): 
			MaximumSpeed (number): 
			Name (str): 
			PeerAdvertisedFeatures (str): 
			PortNumber (number): 
			RemoteIp (str): 
			State (str): 
			SupportedFeatures (str): 

		Returns:
			self: This instance with matching ofChannelPortsLearnedInformation data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of ofChannelPortsLearnedInformation data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the ofChannelPortsLearnedInformation data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
