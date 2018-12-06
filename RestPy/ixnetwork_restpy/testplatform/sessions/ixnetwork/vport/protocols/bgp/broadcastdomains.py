
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


class BroadcastDomains(Base):
	"""The BroadcastDomains class encapsulates a user managed broadcastDomains node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the BroadcastDomains property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'broadcastDomains'

	def __init__(self, parent):
		super(BroadcastDomains, self).__init__(parent)

	@property
	def CMacRange(self):
		"""An instance of the CMacRange class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.cmacrange.CMacRange)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.cmacrange import CMacRange
		return CMacRange(self)

	@property
	def AdRouteLabel(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('adRouteLabel')
	@AdRouteLabel.setter
	def AdRouteLabel(self, value):
		self._set_attribute('adRouteLabel', value)

	@property
	def BVlanId(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('bVlanId')
	@BVlanId.setter
	def BVlanId(self, value):
		self._set_attribute('bVlanId', value)

	@property
	def BVlanPriority(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('bVlanPriority')
	@BVlanPriority.setter
	def BVlanPriority(self, value):
		self._set_attribute('bVlanPriority', value)

	@property
	def BVlanTpId(self):
		"""

		Returns:
			str(0x8100|0x9100|0x9200|0x88A8)
		"""
		return self._get_attribute('bVlanTpId')
	@BVlanTpId.setter
	def BVlanTpId(self, value):
		self._set_attribute('bVlanTpId', value)

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
	def EthernetTagId(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('ethernetTagId')
	@EthernetTagId.setter
	def EthernetTagId(self, value):
		self._set_attribute('ethernetTagId', value)

	def add(self, AdRouteLabel=None, BVlanId=None, BVlanPriority=None, BVlanTpId=None, Enabled=None, EthernetTagId=None):
		"""Adds a new broadcastDomains node on the server and retrieves it in this instance.

		Args:
			AdRouteLabel (number): 
			BVlanId (number): 
			BVlanPriority (number): 
			BVlanTpId (str(0x8100|0x9100|0x9200|0x88A8)): 
			Enabled (bool): 
			EthernetTagId (number): 

		Returns:
			self: This instance with all currently retrieved broadcastDomains data using find and the newly added broadcastDomains data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the broadcastDomains data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, AdRouteLabel=None, BVlanId=None, BVlanPriority=None, BVlanTpId=None, Enabled=None, EthernetTagId=None):
		"""Finds and retrieves broadcastDomains data from the server.

		All named parameters support regex and can be used to selectively retrieve broadcastDomains data from the server.
		By default the find method takes no parameters and will retrieve all broadcastDomains data from the server.

		Args:
			AdRouteLabel (number): 
			BVlanId (number): 
			BVlanPriority (number): 
			BVlanTpId (str(0x8100|0x9100|0x9200|0x88A8)): 
			Enabled (bool): 
			EthernetTagId (number): 

		Returns:
			self: This instance with matching broadcastDomains data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of broadcastDomains data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the broadcastDomains data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)

	def AdvertiseAliasing(self):
		"""Executes the advertiseAliasing operation on the server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=broadcastDomains)): The method internally sets Arg1 to the current href for this instance

		Returns:
			str: 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('AdvertiseAliasing', payload=locals(), response_object=None)

	def WithdrawAliasing(self):
		"""Executes the withdrawAliasing operation on the server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=broadcastDomains)): The method internally sets Arg1 to the current href for this instance

		Returns:
			str: 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('WithdrawAliasing', payload=locals(), response_object=None)
