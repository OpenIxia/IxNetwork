from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class DrillDown(Base):
	"""The DrillDown class encapsulates a user managed drillDown node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the DrillDown property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'drillDown'

	def __init__(self, parent):
		super(DrillDown, self).__init__(parent)

	@property
	def AvailableTargetRowFilters(self):
		"""An instance of the AvailableTargetRowFilters class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.drilldown.availabletargetrowfilters.availabletargetrowfilters.AvailableTargetRowFilters)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.drilldown.availabletargetrowfilters.availabletargetrowfilters import AvailableTargetRowFilters
		return AvailableTargetRowFilters(self)

	@property
	def AvailableDrillDownOptions(self):
		"""Gets the available drill down options for the selected row.

		Returns:
			list(str)
		"""
		return self._get_attribute('availableDrillDownOptions')

	@property
	def TargetDrillDownOption(self):
		"""Sets the drill down option attribute to the drilldown object. It is one of the items in the list returned at 2.

		Returns:
			str
		"""
		return self._get_attribute('targetDrillDownOption')
	@TargetDrillDownOption.setter
	def TargetDrillDownOption(self, value):
		self._set_attribute('targetDrillDownOption', value)

	@property
	def TargetRow(self):
		"""Gets the target row, set previously, at step 1.

		Returns:
			list(str)
		"""
		return self._get_attribute('targetRow')

	@property
	def TargetRowFilter(self):
		"""Sets the row (from the view) that will be used to perform the drill-down. This is done by using one of the filters provided by availableTargetRowFilters

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=availableTargetRowFilters)
		"""
		return self._get_attribute('targetRowFilter')
	@TargetRowFilter.setter
	def TargetRowFilter(self, value):
		self._set_attribute('targetRowFilter', value)

	@property
	def TargetRowIndex(self):
		"""Sets the attribute targetRowIndex to the drill down object. This is the row (from the view) that will be used to perform the drill-down.

		Returns:
			number
		"""
		return self._get_attribute('targetRowIndex')
	@TargetRowIndex.setter
	def TargetRowIndex(self, value):
		self._set_attribute('targetRowIndex', value)

	def add(self, TargetDrillDownOption=None, TargetRowFilter=None, TargetRowIndex=None):
		"""Adds a new drillDown node on the server and retrieves it in this instance.

		Args:
			TargetDrillDownOption (str): Sets the drill down option attribute to the drilldown object. It is one of the items in the list returned at 2.
			TargetRowFilter (str(None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=availableTargetRowFilters)): Sets the row (from the view) that will be used to perform the drill-down. This is done by using one of the filters provided by availableTargetRowFilters
			TargetRowIndex (number): Sets the attribute targetRowIndex to the drill down object. This is the row (from the view) that will be used to perform the drill-down.

		Returns:
			self: This instance with all currently retrieved drillDown data using find and the newly added drillDown data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the drillDown data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, AvailableDrillDownOptions=None, TargetDrillDownOption=None, TargetRow=None, TargetRowFilter=None, TargetRowIndex=None):
		"""Finds and retrieves drillDown data from the server.

		All named parameters support regex and can be used to selectively retrieve drillDown data from the server.
		By default the find method takes no parameters and will retrieve all drillDown data from the server.

		Args:
			AvailableDrillDownOptions (list(str)): Gets the available drill down options for the selected row.
			TargetDrillDownOption (str): Sets the drill down option attribute to the drilldown object. It is one of the items in the list returned at 2.
			TargetRow (list(str)): Gets the target row, set previously, at step 1.
			TargetRowFilter (str(None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=availableTargetRowFilters)): Sets the row (from the view) that will be used to perform the drill-down. This is done by using one of the filters provided by availableTargetRowFilters
			TargetRowIndex (number): Sets the attribute targetRowIndex to the drill down object. This is the row (from the view) that will be used to perform the drill-down.

		Returns:
			self: This instance with matching drillDown data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of drillDown data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the drillDown data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)

	def DoDrillDown(self):
		"""Executes the doDrillDown operation on the server.

		Perform a drill down.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=drillDown)): The method internally set Arg1 to the current href for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('DoDrillDown', payload=locals(), response_object=None)
