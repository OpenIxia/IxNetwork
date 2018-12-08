
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


class Link(Base):
	"""The Link class encapsulates a user managed link node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Link property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'link'

	def __init__(self, parent):
		super(Link, self).__init__(parent)

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
	def LinkType(self):
		"""

		Returns:
			str(broadcast|pointToPoint)
		"""
		return self._get_attribute('linkType')
	@LinkType.setter
	def LinkType(self, value):
		self._set_attribute('linkType', value)

	@property
	def MoreMps(self):
		"""

		Returns:
			list(str[None|/api/v1/sessions/1/ixnetwork/vport?deepchild=mp])
		"""
		return self._get_attribute('moreMps')
	@MoreMps.setter
	def MoreMps(self, value):
		self._set_attribute('moreMps', value)

	@property
	def MpOutwardsIxia(self):
		"""

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=mp)
		"""
		return self._get_attribute('mpOutwardsIxia')
	@MpOutwardsIxia.setter
	def MpOutwardsIxia(self, value):
		self._set_attribute('mpOutwardsIxia', value)

	@property
	def MpTowardsIxia(self):
		"""

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=mp)
		"""
		return self._get_attribute('mpTowardsIxia')
	@MpTowardsIxia.setter
	def MpTowardsIxia(self, value):
		self._set_attribute('mpTowardsIxia', value)

	def add(self, Enabled=None, LinkType=None, MoreMps=None, MpOutwardsIxia=None, MpTowardsIxia=None):
		"""Adds a new link node on the server and retrieves it in this instance.

		Args:
			Enabled (bool): 
			LinkType (str(broadcast|pointToPoint)): 
			MoreMps (list(str[None|/api/v1/sessions/1/ixnetwork/vport?deepchild=mp])): 
			MpOutwardsIxia (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=mp)): 
			MpTowardsIxia (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=mp)): 

		Returns:
			self: This instance with all currently retrieved link data using find and the newly added link data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the link data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, Enabled=None, LinkType=None, MoreMps=None, MpOutwardsIxia=None, MpTowardsIxia=None):
		"""Finds and retrieves link data from the server.

		All named parameters support regex and can be used to selectively retrieve link data from the server.
		By default the find method takes no parameters and will retrieve all link data from the server.

		Args:
			Enabled (bool): 
			LinkType (str(broadcast|pointToPoint)): 
			MoreMps (list(str[None|/api/v1/sessions/1/ixnetwork/vport?deepchild=mp])): 
			MpOutwardsIxia (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=mp)): 
			MpTowardsIxia (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=mp)): 

		Returns:
			self: This instance with matching link data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of link data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the link data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
