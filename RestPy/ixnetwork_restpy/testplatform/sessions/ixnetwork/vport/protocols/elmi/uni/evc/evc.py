
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


class Evc(Base):
	"""The Evc class encapsulates a user managed evc node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Evc property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'evc'

	def __init__(self, parent):
		super(Evc, self).__init__(parent)

	@property
	def BwProfile(self):
		"""An instance of the BwProfile class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.elmi.uni.evc.bwprofile.bwprofile.BwProfile)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.elmi.uni.evc.bwprofile.bwprofile import BwProfile
		return BwProfile(self)

	@property
	def CeVlanIdRange(self):
		"""An instance of the CeVlanIdRange class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.elmi.uni.evc.cevlanidrange.cevlanidrange.CeVlanIdRange)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.elmi.uni.evc.cevlanidrange.cevlanidrange import CeVlanIdRange
		return CeVlanIdRange(self)

	@property
	def DefaultEvc(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('defaultEvc')
	@DefaultEvc.setter
	def DefaultEvc(self, value):
		self._set_attribute('defaultEvc', value)

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
	def EvcIdentifier(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('evcIdentifier')
	@EvcIdentifier.setter
	def EvcIdentifier(self, value):
		self._set_attribute('evcIdentifier', value)

	@property
	def EvcIdentifierLength(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('evcIdentifierLength')
	@EvcIdentifierLength.setter
	def EvcIdentifierLength(self, value):
		self._set_attribute('evcIdentifierLength', value)

	@property
	def EvcStatus(self):
		"""

		Returns:
			str(notActive|newAndNotActive|active|newAndActive|partiallyActive|newAndPartiallyActive)
		"""
		return self._get_attribute('evcStatus')
	@EvcStatus.setter
	def EvcStatus(self, value):
		self._set_attribute('evcStatus', value)

	@property
	def EvcType(self):
		"""

		Returns:
			str(pointToPoint|multipointToMultipoint)
		"""
		return self._get_attribute('evcType')
	@EvcType.setter
	def EvcType(self, value):
		self._set_attribute('evcType', value)

	@property
	def ReferenceId(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('referenceId')
	@ReferenceId.setter
	def ReferenceId(self, value):
		self._set_attribute('referenceId', value)

	@property
	def UntaggedPriorityTagged(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('untaggedPriorityTagged')
	@UntaggedPriorityTagged.setter
	def UntaggedPriorityTagged(self, value):
		self._set_attribute('untaggedPriorityTagged', value)

	def add(self, DefaultEvc=None, Enabled=None, EvcIdentifier=None, EvcIdentifierLength=None, EvcStatus=None, EvcType=None, ReferenceId=None, UntaggedPriorityTagged=None):
		"""Adds a new evc node on the server and retrieves it in this instance.

		Args:
			DefaultEvc (bool): 
			Enabled (bool): 
			EvcIdentifier (str): 
			EvcIdentifierLength (number): 
			EvcStatus (str(notActive|newAndNotActive|active|newAndActive|partiallyActive|newAndPartiallyActive)): 
			EvcType (str(pointToPoint|multipointToMultipoint)): 
			ReferenceId (number): 
			UntaggedPriorityTagged (bool): 

		Returns:
			self: This instance with all currently retrieved evc data using find and the newly added evc data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the evc data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, DefaultEvc=None, Enabled=None, EvcIdentifier=None, EvcIdentifierLength=None, EvcStatus=None, EvcType=None, ReferenceId=None, UntaggedPriorityTagged=None):
		"""Finds and retrieves evc data from the server.

		All named parameters support regex and can be used to selectively retrieve evc data from the server.
		By default the find method takes no parameters and will retrieve all evc data from the server.

		Args:
			DefaultEvc (bool): 
			Enabled (bool): 
			EvcIdentifier (str): 
			EvcIdentifierLength (number): 
			EvcStatus (str(notActive|newAndNotActive|active|newAndActive|partiallyActive|newAndPartiallyActive)): 
			EvcType (str(pointToPoint|multipointToMultipoint)): 
			ReferenceId (number): 
			UntaggedPriorityTagged (bool): 

		Returns:
			self: This instance with matching evc data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of evc data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the evc data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
