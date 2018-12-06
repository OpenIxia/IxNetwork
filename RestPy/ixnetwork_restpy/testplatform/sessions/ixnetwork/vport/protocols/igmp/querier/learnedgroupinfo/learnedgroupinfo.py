
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


class LearnedGroupInfo(Base):
	"""The LearnedGroupInfo class encapsulates a system managed learnedGroupInfo node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the LearnedGroupInfo property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'learnedGroupInfo'

	def __init__(self, parent):
		super(LearnedGroupInfo, self).__init__(parent)

	@property
	def CompatibilityMode(self):
		"""

		Returns:
			str(igmpv1|igmpv2|igmpv3)
		"""
		return self._get_attribute('compatibilityMode')

	@property
	def CompatibilityTimer(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('compatibilityTimer')

	@property
	def FilterMode(self):
		"""

		Returns:
			str(include|exclude)
		"""
		return self._get_attribute('filterMode')

	@property
	def GroupAddress(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('groupAddress')

	@property
	def GroupTimer(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('groupTimer')

	@property
	def SourceAddress(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('sourceAddress')

	@property
	def SourceTimer(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('sourceTimer')

	def find(self, CompatibilityMode=None, CompatibilityTimer=None, FilterMode=None, GroupAddress=None, GroupTimer=None, SourceAddress=None, SourceTimer=None):
		"""Finds and retrieves learnedGroupInfo data from the server.

		All named parameters support regex and can be used to selectively retrieve learnedGroupInfo data from the server.
		By default the find method takes no parameters and will retrieve all learnedGroupInfo data from the server.

		Args:
			CompatibilityMode (str(igmpv1|igmpv2|igmpv3)): 
			CompatibilityTimer (number): 
			FilterMode (str(include|exclude)): 
			GroupAddress (str): 
			GroupTimer (number): 
			SourceAddress (str): 
			SourceTimer (number): 

		Returns:
			self: This instance with matching learnedGroupInfo data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of learnedGroupInfo data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the learnedGroupInfo data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
