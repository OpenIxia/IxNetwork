
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


class Router(Base):
	"""The Router class encapsulates a user managed router node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Router property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'router'

	def __init__(self, parent):
		super(Router, self).__init__(parent)

	@property
	def Interface(self):
		"""An instance of the Interface class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.pimsm.router.interface.interface.Interface)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.pimsm.router.interface.interface import Interface
		return Interface(self)

	@property
	def DataMdtInterval(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('dataMdtInterval')
	@DataMdtInterval.setter
	def DataMdtInterval(self, value):
		self._set_attribute('dataMdtInterval', value)

	@property
	def DataMdtTimeOut(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('dataMdtTimeOut')
	@DataMdtTimeOut.setter
	def DataMdtTimeOut(self, value):
		self._set_attribute('dataMdtTimeOut', value)

	@property
	def DrPriority(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('drPriority')
	@DrPriority.setter
	def DrPriority(self, value):
		self._set_attribute('drPriority', value)

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
	def JoinPruneHoldTime(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('joinPruneHoldTime')
	@JoinPruneHoldTime.setter
	def JoinPruneHoldTime(self, value):
		self._set_attribute('joinPruneHoldTime', value)

	@property
	def JoinPruneInterval(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('joinPruneInterval')
	@JoinPruneInterval.setter
	def JoinPruneInterval(self, value):
		self._set_attribute('joinPruneInterval', value)

	@property
	def RouterId(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('routerId')
	@RouterId.setter
	def RouterId(self, value):
		self._set_attribute('routerId', value)

	@property
	def RpDiscoveryMode(self):
		"""

		Returns:
			str(manual|auto)
		"""
		return self._get_attribute('rpDiscoveryMode')
	@RpDiscoveryMode.setter
	def RpDiscoveryMode(self, value):
		self._set_attribute('rpDiscoveryMode', value)

	@property
	def TrafficGroupId(self):
		"""

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficGroup)
		"""
		return self._get_attribute('trafficGroupId')
	@TrafficGroupId.setter
	def TrafficGroupId(self, value):
		self._set_attribute('trafficGroupId', value)

	def add(self, DataMdtInterval=None, DataMdtTimeOut=None, DrPriority=None, Enabled=None, JoinPruneHoldTime=None, JoinPruneInterval=None, RouterId=None, RpDiscoveryMode=None, TrafficGroupId=None):
		"""Adds a new router node on the server and retrieves it in this instance.

		Args:
			DataMdtInterval (number): 
			DataMdtTimeOut (number): 
			DrPriority (number): 
			Enabled (bool): 
			JoinPruneHoldTime (number): 
			JoinPruneInterval (number): 
			RouterId (str): 
			RpDiscoveryMode (str(manual|auto)): 
			TrafficGroupId (str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficGroup)): 

		Returns:
			self: This instance with all currently retrieved router data using find and the newly added router data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the router data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, DataMdtInterval=None, DataMdtTimeOut=None, DrPriority=None, Enabled=None, JoinPruneHoldTime=None, JoinPruneInterval=None, RouterId=None, RpDiscoveryMode=None, TrafficGroupId=None):
		"""Finds and retrieves router data from the server.

		All named parameters support regex and can be used to selectively retrieve router data from the server.
		By default the find method takes no parameters and will retrieve all router data from the server.

		Args:
			DataMdtInterval (number): 
			DataMdtTimeOut (number): 
			DrPriority (number): 
			Enabled (bool): 
			JoinPruneHoldTime (number): 
			JoinPruneInterval (number): 
			RouterId (str): 
			RpDiscoveryMode (str(manual|auto)): 
			TrafficGroupId (str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficGroup)): 

		Returns:
			self: This instance with matching router data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of router data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the router data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
