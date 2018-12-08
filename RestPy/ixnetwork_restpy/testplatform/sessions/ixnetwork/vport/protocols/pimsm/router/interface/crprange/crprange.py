
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


class CrpRange(Base):
	"""The CrpRange class encapsulates a user managed crpRange node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the CrpRange property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'crpRange'

	def __init__(self, parent):
		super(CrpRange, self).__init__(parent)

	@property
	def AdvertisementHoldTime(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('advertisementHoldTime')
	@AdvertisementHoldTime.setter
	def AdvertisementHoldTime(self, value):
		self._set_attribute('advertisementHoldTime', value)

	@property
	def BackOffInterval(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('backOffInterval')
	@BackOffInterval.setter
	def BackOffInterval(self, value):
		self._set_attribute('backOffInterval', value)

	@property
	def CrpAddress(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('crpAddress')
	@CrpAddress.setter
	def CrpAddress(self, value):
		self._set_attribute('crpAddress', value)

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
	def GroupAddress(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('groupAddress')
	@GroupAddress.setter
	def GroupAddress(self, value):
		self._set_attribute('groupAddress', value)

	@property
	def GroupCount(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('groupCount')
	@GroupCount.setter
	def GroupCount(self, value):
		self._set_attribute('groupCount', value)

	@property
	def GroupMaskLen(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('groupMaskLen')
	@GroupMaskLen.setter
	def GroupMaskLen(self, value):
		self._set_attribute('groupMaskLen', value)

	@property
	def MeshingType(self):
		"""

		Returns:
			str(fullyMeshed|oneToOne)
		"""
		return self._get_attribute('meshingType')
	@MeshingType.setter
	def MeshingType(self, value):
		self._set_attribute('meshingType', value)

	@property
	def PeriodicAdvertisementInterval(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('periodicAdvertisementInterval')
	@PeriodicAdvertisementInterval.setter
	def PeriodicAdvertisementInterval(self, value):
		self._set_attribute('periodicAdvertisementInterval', value)

	@property
	def PriorityChangeInterval(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('priorityChangeInterval')
	@PriorityChangeInterval.setter
	def PriorityChangeInterval(self, value):
		self._set_attribute('priorityChangeInterval', value)

	@property
	def PriorityType(self):
		"""

		Returns:
			str(same|incremental|random)
		"""
		return self._get_attribute('priorityType')
	@PriorityType.setter
	def PriorityType(self, value):
		self._set_attribute('priorityType', value)

	@property
	def PriorityValue(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('priorityValue')
	@PriorityValue.setter
	def PriorityValue(self, value):
		self._set_attribute('priorityValue', value)

	@property
	def RouterCount(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('routerCount')
	@RouterCount.setter
	def RouterCount(self, value):
		self._set_attribute('routerCount', value)

	@property
	def TriggeredCrpMessageCount(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('triggeredCrpMessageCount')
	@TriggeredCrpMessageCount.setter
	def TriggeredCrpMessageCount(self, value):
		self._set_attribute('triggeredCrpMessageCount', value)

	def add(self, AdvertisementHoldTime=None, BackOffInterval=None, CrpAddress=None, Enabled=None, GroupAddress=None, GroupCount=None, GroupMaskLen=None, MeshingType=None, PeriodicAdvertisementInterval=None, PriorityChangeInterval=None, PriorityType=None, PriorityValue=None, RouterCount=None, TriggeredCrpMessageCount=None):
		"""Adds a new crpRange node on the server and retrieves it in this instance.

		Args:
			AdvertisementHoldTime (number): 
			BackOffInterval (number): 
			CrpAddress (str): 
			Enabled (bool): 
			GroupAddress (str): 
			GroupCount (number): 
			GroupMaskLen (number): 
			MeshingType (str(fullyMeshed|oneToOne)): 
			PeriodicAdvertisementInterval (number): 
			PriorityChangeInterval (number): 
			PriorityType (str(same|incremental|random)): 
			PriorityValue (number): 
			RouterCount (number): 
			TriggeredCrpMessageCount (number): 

		Returns:
			self: This instance with all currently retrieved crpRange data using find and the newly added crpRange data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the crpRange data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, AdvertisementHoldTime=None, BackOffInterval=None, CrpAddress=None, Enabled=None, GroupAddress=None, GroupCount=None, GroupMaskLen=None, MeshingType=None, PeriodicAdvertisementInterval=None, PriorityChangeInterval=None, PriorityType=None, PriorityValue=None, RouterCount=None, TriggeredCrpMessageCount=None):
		"""Finds and retrieves crpRange data from the server.

		All named parameters support regex and can be used to selectively retrieve crpRange data from the server.
		By default the find method takes no parameters and will retrieve all crpRange data from the server.

		Args:
			AdvertisementHoldTime (number): 
			BackOffInterval (number): 
			CrpAddress (str): 
			Enabled (bool): 
			GroupAddress (str): 
			GroupCount (number): 
			GroupMaskLen (number): 
			MeshingType (str(fullyMeshed|oneToOne)): 
			PeriodicAdvertisementInterval (number): 
			PriorityChangeInterval (number): 
			PriorityType (str(same|incremental|random)): 
			PriorityValue (number): 
			RouterCount (number): 
			TriggeredCrpMessageCount (number): 

		Returns:
			self: This instance with matching crpRange data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of crpRange data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the crpRange data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
