
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


class GroupFeatureStatLearnedInformation(Base):
	"""The GroupFeatureStatLearnedInformation class encapsulates a system managed groupFeatureStatLearnedInformation node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the GroupFeatureStatLearnedInformation property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'groupFeatureStatLearnedInformation'

	def __init__(self, parent):
		super(GroupFeatureStatLearnedInformation, self).__init__(parent)

	@property
	def ActionsAll(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('actionsAll')

	@property
	def ActionsFastFailOver(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('actionsFastFailOver')

	@property
	def ActionsIndirect(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('actionsIndirect')

	@property
	def ActionsSelect(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('actionsSelect')

	@property
	def DataPathIdAsHex(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('dataPathIdAsHex')

	@property
	def DatapathId(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('datapathId')

	@property
	def ErrorCode(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('errorCode')

	@property
	def ErrorType(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('errorType')

	@property
	def GroupCapabilities(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('groupCapabilities')

	@property
	def GroupType(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('groupType')

	@property
	def Latency(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('latency')

	@property
	def LocalIp(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('localIp')

	@property
	def MaxGroupsAll(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('maxGroupsAll')

	@property
	def MaxGroupsFastFailOver(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('maxGroupsFastFailOver')

	@property
	def MaxGroupsIndirect(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('maxGroupsIndirect')

	@property
	def MaxGroupsSelect(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('maxGroupsSelect')

	@property
	def NegotiatedVersion(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('negotiatedVersion')

	@property
	def RemoteIp(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('remoteIp')

	@property
	def ReplyState(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('replyState')

	def find(self, ActionsAll=None, ActionsFastFailOver=None, ActionsIndirect=None, ActionsSelect=None, DataPathIdAsHex=None, DatapathId=None, ErrorCode=None, ErrorType=None, GroupCapabilities=None, GroupType=None, Latency=None, LocalIp=None, MaxGroupsAll=None, MaxGroupsFastFailOver=None, MaxGroupsIndirect=None, MaxGroupsSelect=None, NegotiatedVersion=None, RemoteIp=None, ReplyState=None):
		"""Finds and retrieves groupFeatureStatLearnedInformation data from the server.

		All named parameters support regex and can be used to selectively retrieve groupFeatureStatLearnedInformation data from the server.
		By default the find method takes no parameters and will retrieve all groupFeatureStatLearnedInformation data from the server.

		Args:
			ActionsAll (str): 
			ActionsFastFailOver (str): 
			ActionsIndirect (str): 
			ActionsSelect (str): 
			DataPathIdAsHex (str): 
			DatapathId (str): 
			ErrorCode (str): 
			ErrorType (str): 
			GroupCapabilities (str): 
			GroupType (str): 
			Latency (number): 
			LocalIp (str): 
			MaxGroupsAll (number): 
			MaxGroupsFastFailOver (number): 
			MaxGroupsIndirect (number): 
			MaxGroupsSelect (number): 
			NegotiatedVersion (str): 
			RemoteIp (str): 
			ReplyState (str): 

		Returns:
			self: This instance with matching groupFeatureStatLearnedInformation data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of groupFeatureStatLearnedInformation data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the groupFeatureStatLearnedInformation data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
