
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


class DceTopologyRange(Base):
	"""The DceTopologyRange class encapsulates a user managed dceTopologyRange node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the DceTopologyRange property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'dceTopologyRange'

	def __init__(self, parent):
		super(DceTopologyRange, self).__init__(parent)

	@property
	def DceInterestedVlanRange(self):
		"""An instance of the DceInterestedVlanRange class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.dceinterestedvlanrange.DceInterestedVlanRange)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.dceinterestedvlanrange import DceInterestedVlanRange
		return DceInterestedVlanRange(self)

	@property
	def EnableFtag(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableFtag')
	@EnableFtag.setter
	def EnableFtag(self, value):
		self._set_attribute('enableFtag', value)

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
	def NicknameList(self):
		"""

		Returns:
			list(dict(arg1:number,arg2:number,arg3:number))
		"""
		return self._get_attribute('nicknameList')
	@NicknameList.setter
	def NicknameList(self, value):
		self._set_attribute('nicknameList', value)

	@property
	def NoOfTreesToCompute(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('noOfTreesToCompute')
	@NoOfTreesToCompute.setter
	def NoOfTreesToCompute(self, value):
		self._set_attribute('noOfTreesToCompute', value)

	@property
	def StartFtagValue(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('startFtagValue')
	@StartFtagValue.setter
	def StartFtagValue(self, value):
		self._set_attribute('startFtagValue', value)

	@property
	def TopologyCount(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('topologyCount')
	@TopologyCount.setter
	def TopologyCount(self, value):
		self._set_attribute('topologyCount', value)

	@property
	def TopologyId(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('topologyId')
	@TopologyId.setter
	def TopologyId(self, value):
		self._set_attribute('topologyId', value)

	@property
	def TopologyIdStep(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('topologyIdStep')
	@TopologyIdStep.setter
	def TopologyIdStep(self, value):
		self._set_attribute('topologyIdStep', value)

	def add(self, EnableFtag=None, Enabled=None, NicknameList=None, NoOfTreesToCompute=None, StartFtagValue=None, TopologyCount=None, TopologyId=None, TopologyIdStep=None):
		"""Adds a new dceTopologyRange node on the server and retrieves it in this instance.

		Args:
			EnableFtag (bool): 
			Enabled (bool): 
			NicknameList (list(dict(arg1:number,arg2:number,arg3:number))): 
			NoOfTreesToCompute (number): 
			StartFtagValue (number): 
			TopologyCount (number): 
			TopologyId (number): 
			TopologyIdStep (number): 

		Returns:
			self: This instance with all currently retrieved dceTopologyRange data using find and the newly added dceTopologyRange data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the dceTopologyRange data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, EnableFtag=None, Enabled=None, NicknameList=None, NoOfTreesToCompute=None, StartFtagValue=None, TopologyCount=None, TopologyId=None, TopologyIdStep=None):
		"""Finds and retrieves dceTopologyRange data from the server.

		All named parameters support regex and can be used to selectively retrieve dceTopologyRange data from the server.
		By default the find method takes no parameters and will retrieve all dceTopologyRange data from the server.

		Args:
			EnableFtag (bool): 
			Enabled (bool): 
			NicknameList (list(dict(arg1:number,arg2:number,arg3:number))): 
			NoOfTreesToCompute (number): 
			StartFtagValue (number): 
			TopologyCount (number): 
			TopologyId (number): 
			TopologyIdStep (number): 

		Returns:
			self: This instance with matching dceTopologyRange data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of dceTopologyRange data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the dceTopologyRange data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
