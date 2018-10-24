
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


class Col(Base):
	"""The Col class encapsulates a system managed col node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Col property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'col'

	def __init__(self, parent):
		super(Col, self).__init__(parent)

	@property
	def CellTable(self):
		"""An instance of the CellTable class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.learnedinfo.celltable.CellTable)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.learnedinfo.celltable import CellTable
		return CellTable(self)

	@property
	def Row(self):
		"""An instance of the Row class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.learnedinfo.row.Row)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.learnedinfo.row import Row
		return Row(self)

	@property
	def Value(self):
		"""A learned information value

		Returns:
			str
		"""
		return self._get_attribute('value')

	def find(self, Value=None):
		"""Finds and retrieves col data from the server.

		All named parameters support regex and can be used to selectively retrieve col data from the server.
		By default the find method takes no parameters and will retrieve all col data from the server.

		Args:
			Value (str): A learned information value

		Returns:
			self: This instance with matching col data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of col data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the col data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
