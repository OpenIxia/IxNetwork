from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Layer47AppLibraryTrafficFilter(Base):
	"""The Layer47AppLibraryTrafficFilter class encapsulates a user managed layer47AppLibraryTrafficFilter node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Layer47AppLibraryTrafficFilter property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'layer47AppLibraryTrafficFilter'

	def __init__(self, parent):
		super(Layer47AppLibraryTrafficFilter, self).__init__(parent)

	@property
	def AdvancedFilter(self):
		"""An instance of the AdvancedFilter class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.layer47applibrarytrafficfilter.advancedfilter.advancedfilter.AdvancedFilter)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.layer47applibrarytrafficfilter.advancedfilter.advancedfilter import AdvancedFilter
		return AdvancedFilter(self)

	@property
	def AdvancedFilterName(self):
		"""Specifies an advanced filter from the ones available in the selected drill down view.

		Returns:
			str
		"""
		return self._get_attribute('advancedFilterName')
	@AdvancedFilterName.setter
	def AdvancedFilterName(self, value):
		self._set_attribute('advancedFilterName', value)

	@property
	def AllAdvancedFilters(self):
		"""Returns a list with all the filters that are present in the selected drill down views. This includes filters that cannot be applied for the current drill down view.

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=availableAdvancedFilters)
		"""
		return self._get_attribute('allAdvancedFilters')

	@property
	def MatchingAdvancedFilters(self):
		"""Specifies a list that contains only the filters which can be applied on the current drill down view.

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=availableAdvancedFilters)
		"""
		return self._get_attribute('matchingAdvancedFilters')

	@property
	def TopxEnabled(self):
		"""The view only shows the number of rows specified by TopXValue. If the view is OnDemand, it will become RealTime.

		Returns:
			bool
		"""
		return self._get_attribute('topxEnabled')
	@TopxEnabled.setter
	def TopxEnabled(self, value):
		self._set_attribute('topxEnabled', value)

	@property
	def TopxValue(self):
		"""The number of rows to be shown when TopXEnabled is set to true.

		Returns:
			number
		"""
		return self._get_attribute('topxValue')
	@TopxValue.setter
	def TopxValue(self, value):
		self._set_attribute('topxValue', value)

	def add(self, AdvancedFilterName=None, TopxEnabled=None, TopxValue=None):
		"""Adds a new layer47AppLibraryTrafficFilter node on the server and retrieves it in this instance.

		Args:
			AdvancedFilterName (str): Specifies an advanced filter from the ones available in the selected drill down view.
			TopxEnabled (bool): The view only shows the number of rows specified by TopXValue. If the view is OnDemand, it will become RealTime.
			TopxValue (number): The number of rows to be shown when TopXEnabled is set to true.

		Returns:
			self: This instance with all currently retrieved layer47AppLibraryTrafficFilter data using find and the newly added layer47AppLibraryTrafficFilter data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the layer47AppLibraryTrafficFilter data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, AdvancedFilterName=None, AllAdvancedFilters=None, MatchingAdvancedFilters=None, TopxEnabled=None, TopxValue=None):
		"""Finds and retrieves layer47AppLibraryTrafficFilter data from the server.

		All named parameters support regex and can be used to selectively retrieve layer47AppLibraryTrafficFilter data from the server.
		By default the find method takes no parameters and will retrieve all layer47AppLibraryTrafficFilter data from the server.

		Args:
			AdvancedFilterName (str): Specifies an advanced filter from the ones available in the selected drill down view.
			AllAdvancedFilters (str(None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=availableAdvancedFilters)): Returns a list with all the filters that are present in the selected drill down views. This includes filters that cannot be applied for the current drill down view.
			MatchingAdvancedFilters (str(None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=availableAdvancedFilters)): Specifies a list that contains only the filters which can be applied on the current drill down view.
			TopxEnabled (bool): The view only shows the number of rows specified by TopXValue. If the view is OnDemand, it will become RealTime.
			TopxValue (number): The number of rows to be shown when TopXEnabled is set to true.

		Returns:
			self: This instance with matching layer47AppLibraryTrafficFilter data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of layer47AppLibraryTrafficFilter data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the layer47AppLibraryTrafficFilter data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)

	def AddAdvancedFilter(self, Arg2):
		"""Executes the addAdvancedFilter operation on the server.

		NOT DEFINED

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=layer47AppLibraryTrafficFilter)): The method internally set Arg1 to the current href for this instance
			Arg2 (str(None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=availableAdvancedFilters)): NOT DEFINED

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('AddAdvancedFilter', payload=locals(), response_object=None)

	def RemoveAdvancedFilter(self, Arg2):
		"""Executes the removeAdvancedFilter operation on the server.

		NOT DEFINED

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=layer47AppLibraryTrafficFilter)): The method internally set Arg1 to the current href for this instance
			Arg2 (str): NOT DEFINED

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('RemoveAdvancedFilter', payload=locals(), response_object=None)

	def RemoveAllAdvancedFilters(self):
		"""Executes the removeAllAdvancedFilters operation on the server.

		NOT DEFINED

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=layer47AppLibraryTrafficFilter)): The method internally set Arg1 to the current href for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('RemoveAllAdvancedFilters', payload=locals(), response_object=None)
