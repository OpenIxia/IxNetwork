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
		"""If true, statistics will be displayed in multiple pages.

		Returns:
			bool
		"""
		return self._get_attribute('allowPaging')

	@property
	def ColumnCaptions(self):
		"""The statistics column caption.

		Returns:
			list(str)
		"""
		return self._get_attribute('columnCaptions')

	@property
	def ColumnCount(self):
		"""Displays the particular column number in the view.

		Returns:
			number
		"""
		return self._get_attribute('columnCount')

	@property
	def CurrentPage(self):
		"""The current page number being displayed.

		Returns:
			number
		"""
		return self._get_attribute('currentPage')
	@CurrentPage.setter
	def CurrentPage(self, value):
		self._set_attribute('currentPage', value)

	@property
	def EgressMode(self):
		"""Emulates conditional or paged egress tracking view based on selected mode.

		Returns:
			str(conditional|paged)
		"""
		return self._get_attribute('egressMode')
	@EgressMode.setter
	def EgressMode(self, value):
		self._set_attribute('egressMode', value)

	@property
	def EgressPageSize(self):
		"""The current egress page size across all ingress rows. Default = 3

		Returns:
			number
		"""
		return self._get_attribute('egressPageSize')
	@EgressPageSize.setter
	def EgressPageSize(self, value):
		self._set_attribute('egressPageSize', value)

	@property
	def IsBlocked(self):
		"""Is a flag used to fetch the status of view (returns true if the views was blocked by Guard Rail, false otherwise)

		Returns:
			bool
		"""
		return self._get_attribute('isBlocked')

	@property
	def IsReady(self):
		"""If true, the counter is ready to record the statistics.

		Returns:
			bool
		"""
		return self._get_attribute('isReady')

	@property
	def IsReadyTimeout(self):
		"""The maximum time (in seconds) for the -isReady attribute to wait before it returns false in case the page has no data.

		Returns:
			number
		"""
		return self._get_attribute('isReadyTimeout')
	@IsReadyTimeout.setter
	def IsReadyTimeout(self, value):
		self._set_attribute('isReadyTimeout', value)

	@property
	def PageSize(self):
		"""The number of statistics per page.

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
		"""Displays the particular row number in the view.

		Returns:
			number
		"""
		return self._get_attribute('rowCount')

	@property
	def RowValues(self):
		"""All statistics values in a row.

		Returns:
			dict(arg1:list[list[list[str]]])
		"""
		return self._get_attribute('rowValues')

	@property
	def Timestamp(self):
		"""Describes the date and time of the event.

		Returns:
			number
		"""
		return self._get_attribute('timestamp')

	@property
	def TotalPages(self):
		"""The total number of statistics pages.

		Returns:
			number
		"""
		return self._get_attribute('totalPages')

	@property
	def TotalRows(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('totalRows')
