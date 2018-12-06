
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


class Page(Base):
	"""The Page class encapsulates a required page node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Page property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'page'

	def __init__(self, parent):
		super(Page, self).__init__(parent)

	@property
	def Egress(self):
		"""An instance of the Egress class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.page.egress.egress.Egress)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.page.egress.egress import Egress
		return Egress(self)

	@property
	def EgressRxCondition(self):
		"""An instance of the EgressRxCondition class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.page.egressrxcondition.egressrxcondition.EgressRxCondition)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.page.egressrxcondition.egressrxcondition import EgressRxCondition
		return EgressRxCondition(self)._select()

	@property
	def AllowPaging(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('allowPaging')

	@property
	def ColumnCaptions(self):
		"""

		Returns:
			list(str)
		"""
		return self._get_attribute('columnCaptions')

	@property
	def ColumnCount(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('columnCount')

	@property
	def CurrentPage(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('currentPage')
	@CurrentPage.setter
	def CurrentPage(self, value):
		self._set_attribute('currentPage', value)

	@property
	def EgressMode(self):
		"""

		Returns:
			str(conditional|paged)
		"""
		return self._get_attribute('egressMode')
	@EgressMode.setter
	def EgressMode(self, value):
		self._set_attribute('egressMode', value)

	@property
	def EgressPageSize(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('egressPageSize')
	@EgressPageSize.setter
	def EgressPageSize(self, value):
		self._set_attribute('egressPageSize', value)

	@property
	def IsBlocked(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('isBlocked')

	@property
	def IsReady(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('isReady')

	@property
	def IsReadyTimeout(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('isReadyTimeout')
	@IsReadyTimeout.setter
	def IsReadyTimeout(self, value):
		self._set_attribute('isReadyTimeout', value)

	@property
	def PageSize(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('pageSize')
	@PageSize.setter
	def PageSize(self, value):
		self._set_attribute('pageSize', value)

	@property
	def PageValues(self):
		"""Returns the values in the current page. The ingress row is grouped with its corresponding egress rows

		Returns:
			list(list[list[str]])
		"""
		return self._get_attribute('pageValues')

	@property
	def RowCount(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('rowCount')

	@property
	def RowValues(self):
		"""

		Returns:
			dict(arg1:list[list[list[str]]])
		"""
		return self._get_attribute('rowValues')

	@property
	def Timestamp(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('timestamp')

	@property
	def TotalPages(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('totalPages')

	@property
	def TotalRows(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('totalRows')
