
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


class DmLearnedInfo(Base):
	"""The DmLearnedInfo class encapsulates a system managed dmLearnedInfo node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the DmLearnedInfo property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'dmLearnedInfo'

	def __init__(self, parent):
		super(DmLearnedInfo, self).__init__(parent)

	@property
	def AverageLooseRtt(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('averageLooseRtt')

	@property
	def AverageLooseRttVariation(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('averageLooseRttVariation')

	@property
	def AverageStrictRtt(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('averageStrictRtt')

	@property
	def AverageStrictRttVariation(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('averageStrictRttVariation')

	@property
	def DmQueriesSent(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('dmQueriesSent')

	@property
	def DmResponsesReceived(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('dmResponsesReceived')

	@property
	def IncomingLabelOuterInner(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('incomingLabelOuterInner')

	@property
	def MaxLooseRtt(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('maxLooseRtt')

	@property
	def MaxStrictRtt(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('maxStrictRtt')

	@property
	def MinLooseRtt(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('minLooseRtt')

	@property
	def MinStrictRtt(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('minStrictRtt')

	@property
	def OutgoingLabelOuterInner(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('outgoingLabelOuterInner')

	@property
	def Type(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('type')

	def find(self, AverageLooseRtt=None, AverageLooseRttVariation=None, AverageStrictRtt=None, AverageStrictRttVariation=None, DmQueriesSent=None, DmResponsesReceived=None, IncomingLabelOuterInner=None, MaxLooseRtt=None, MaxStrictRtt=None, MinLooseRtt=None, MinStrictRtt=None, OutgoingLabelOuterInner=None, Type=None):
		"""Finds and retrieves dmLearnedInfo data from the server.

		All named parameters support regex and can be used to selectively retrieve dmLearnedInfo data from the server.
		By default the find method takes no parameters and will retrieve all dmLearnedInfo data from the server.

		Args:
			AverageLooseRtt (str): 
			AverageLooseRttVariation (str): 
			AverageStrictRtt (str): 
			AverageStrictRttVariation (str): 
			DmQueriesSent (number): 
			DmResponsesReceived (number): 
			IncomingLabelOuterInner (str): 
			MaxLooseRtt (str): 
			MaxStrictRtt (str): 
			MinLooseRtt (str): 
			MinStrictRtt (str): 
			OutgoingLabelOuterInner (str): 
			Type (str): 

		Returns:
			self: This instance with matching dmLearnedInfo data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of dmLearnedInfo data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the dmLearnedInfo data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
