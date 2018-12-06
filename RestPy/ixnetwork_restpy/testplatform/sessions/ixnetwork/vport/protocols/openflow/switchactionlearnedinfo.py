
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


class SwitchActionLearnedInfo(Base):
	"""The SwitchActionLearnedInfo class encapsulates a system managed switchActionLearnedInfo node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the SwitchActionLearnedInfo property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'switchActionLearnedInfo'

	def __init__(self, parent):
		super(SwitchActionLearnedInfo, self).__init__(parent)

	@property
	def ActionType(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('actionType')

	@property
	def EthernetDestination(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('ethernetDestination')

	@property
	def EthernetSource(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('ethernetSource')

	@property
	def IpDscp(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('ipDscp')

	@property
	def Ipv4Destination(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('ipv4Destination')

	@property
	def Ipv4Source(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('ipv4Source')

	@property
	def MaxByteLength(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('maxByteLength')

	@property
	def OutputPort(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('outputPort')

	@property
	def QueueId(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('queueId')

	@property
	def TransportDestination(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('transportDestination')

	@property
	def TransportSource(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('transportSource')

	@property
	def VlanId(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('vlanId')

	@property
	def VlanPriority(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('vlanPriority')

	def find(self, ActionType=None, EthernetDestination=None, EthernetSource=None, IpDscp=None, Ipv4Destination=None, Ipv4Source=None, MaxByteLength=None, OutputPort=None, QueueId=None, TransportDestination=None, TransportSource=None, VlanId=None, VlanPriority=None):
		"""Finds and retrieves switchActionLearnedInfo data from the server.

		All named parameters support regex and can be used to selectively retrieve switchActionLearnedInfo data from the server.
		By default the find method takes no parameters and will retrieve all switchActionLearnedInfo data from the server.

		Args:
			ActionType (str): 
			EthernetDestination (str): 
			EthernetSource (str): 
			IpDscp (str): 
			Ipv4Destination (str): 
			Ipv4Source (str): 
			MaxByteLength (number): 
			OutputPort (number): 
			QueueId (number): 
			TransportDestination (number): 
			TransportSource (number): 
			VlanId (number): 
			VlanPriority (number): 

		Returns:
			self: This instance with matching switchActionLearnedInfo data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of switchActionLearnedInfo data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the switchActionLearnedInfo data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
