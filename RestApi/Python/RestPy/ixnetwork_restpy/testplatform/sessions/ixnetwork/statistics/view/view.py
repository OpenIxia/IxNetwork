from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class View(Base):
	"""The View class encapsulates a user managed view node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the View property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'view'

	def __init__(self, parent):
		super(View, self).__init__(parent)

	@property
	def AdvancedCVFilters(self):
		"""An instance of the AdvancedCVFilters class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.advancedcvfilters.advancedcvfilters.AdvancedCVFilters)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.advancedcvfilters.advancedcvfilters import AdvancedCVFilters
		return AdvancedCVFilters(self)

	@property
	def AvailableAdvancedFilters(self):
		"""An instance of the AvailableAdvancedFilters class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.availableadvancedfilters.availableadvancedfilters.AvailableAdvancedFilters)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.availableadvancedfilters.availableadvancedfilters import AvailableAdvancedFilters
		return AvailableAdvancedFilters(self)

	@property
	def AvailablePortFilter(self):
		"""An instance of the AvailablePortFilter class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.availableportfilter.availableportfilter.AvailablePortFilter)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.availableportfilter.availableportfilter import AvailablePortFilter
		return AvailablePortFilter(self)

	@property
	def AvailableProtocolFilter(self):
		"""An instance of the AvailableProtocolFilter class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.availableprotocolfilter.availableprotocolfilter.AvailableProtocolFilter)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.availableprotocolfilter.availableprotocolfilter import AvailableProtocolFilter
		return AvailableProtocolFilter(self)

	@property
	def AvailableProtocolStackFilter(self):
		"""An instance of the AvailableProtocolStackFilter class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.availableprotocolstackfilter.availableprotocolstackfilter.AvailableProtocolStackFilter)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.availableprotocolstackfilter.availableprotocolstackfilter import AvailableProtocolStackFilter
		return AvailableProtocolStackFilter(self)

	@property
	def AvailableStatisticFilter(self):
		"""An instance of the AvailableStatisticFilter class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.availablestatisticfilter.availablestatisticfilter.AvailableStatisticFilter)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.availablestatisticfilter.availablestatisticfilter import AvailableStatisticFilter
		return AvailableStatisticFilter(self)

	@property
	def AvailableTrackingFilter(self):
		"""An instance of the AvailableTrackingFilter class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.availabletrackingfilter.availabletrackingfilter.AvailableTrackingFilter)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.availabletrackingfilter.availabletrackingfilter import AvailableTrackingFilter
		return AvailableTrackingFilter(self)

	@property
	def AvailableTrafficItemFilter(self):
		"""An instance of the AvailableTrafficItemFilter class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.availabletrafficitemfilter.availabletrafficitemfilter.AvailableTrafficItemFilter)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.availabletrafficitemfilter.availabletrafficitemfilter import AvailableTrafficItemFilter
		return AvailableTrafficItemFilter(self)

	@property
	def Data(self):
		"""An instance of the Data class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.data.data.Data)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.data.data import Data
		return Data(self)._select()

	@property
	def DrillDown(self):
		"""An instance of the DrillDown class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.drilldown.drilldown.DrillDown)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.drilldown.drilldown import DrillDown
		return DrillDown(self)

	@property
	def FormulaCatalog(self):
		"""An instance of the FormulaCatalog class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.formulacatalog.formulacatalog.FormulaCatalog)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.formulacatalog.formulacatalog import FormulaCatalog
		return FormulaCatalog(self)._select()

	@property
	def InnerGlobalStats(self):
		"""An instance of the InnerGlobalStats class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.innerglobalstats.innerglobalstats.InnerGlobalStats)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.innerglobalstats.innerglobalstats import InnerGlobalStats
		return InnerGlobalStats(self)._select()

	@property
	def Layer23NextGenProtocolFilter(self):
		"""An instance of the Layer23NextGenProtocolFilter class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.layer23nextgenprotocolfilter.layer23nextgenprotocolfilter.Layer23NextGenProtocolFilter)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.layer23nextgenprotocolfilter.layer23nextgenprotocolfilter import Layer23NextGenProtocolFilter
		return Layer23NextGenProtocolFilter(self)

	@property
	def Layer23ProtocolAuthAccessFilter(self):
		"""An instance of the Layer23ProtocolAuthAccessFilter class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.layer23protocolauthaccessfilter.layer23protocolauthaccessfilter.Layer23ProtocolAuthAccessFilter)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.layer23protocolauthaccessfilter.layer23protocolauthaccessfilter import Layer23ProtocolAuthAccessFilter
		return Layer23ProtocolAuthAccessFilter(self)

	@property
	def Layer23ProtocolPortFilter(self):
		"""An instance of the Layer23ProtocolPortFilter class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.layer23protocolportfilter.layer23protocolportfilter.Layer23ProtocolPortFilter)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.layer23protocolportfilter.layer23protocolportfilter import Layer23ProtocolPortFilter
		return Layer23ProtocolPortFilter(self)

	@property
	def Layer23ProtocolRoutingFilter(self):
		"""An instance of the Layer23ProtocolRoutingFilter class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.layer23protocolroutingfilter.layer23protocolroutingfilter.Layer23ProtocolRoutingFilter)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.layer23protocolroutingfilter.layer23protocolroutingfilter import Layer23ProtocolRoutingFilter
		return Layer23ProtocolRoutingFilter(self)

	@property
	def Layer23ProtocolStackFilter(self):
		"""An instance of the Layer23ProtocolStackFilter class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.layer23protocolstackfilter.layer23protocolstackfilter.Layer23ProtocolStackFilter)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.layer23protocolstackfilter.layer23protocolstackfilter import Layer23ProtocolStackFilter
		return Layer23ProtocolStackFilter(self)

	@property
	def Layer23TrafficFlowDetectiveFilter(self):
		"""An instance of the Layer23TrafficFlowDetectiveFilter class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.layer23trafficflowdetectivefilter.layer23trafficflowdetectivefilter.Layer23TrafficFlowDetectiveFilter)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.layer23trafficflowdetectivefilter.layer23trafficflowdetectivefilter import Layer23TrafficFlowDetectiveFilter
		return Layer23TrafficFlowDetectiveFilter(self)

	@property
	def Layer23TrafficFlowFilter(self):
		"""An instance of the Layer23TrafficFlowFilter class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.layer23trafficflowfilter.layer23trafficflowfilter.Layer23TrafficFlowFilter)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.layer23trafficflowfilter.layer23trafficflowfilter import Layer23TrafficFlowFilter
		return Layer23TrafficFlowFilter(self)

	@property
	def Layer23TrafficItemFilter(self):
		"""An instance of the Layer23TrafficItemFilter class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.layer23trafficitemfilter.layer23trafficitemfilter.Layer23TrafficItemFilter)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.layer23trafficitemfilter.layer23trafficitemfilter import Layer23TrafficItemFilter
		return Layer23TrafficItemFilter(self)

	@property
	def Layer23TrafficPortFilter(self):
		"""An instance of the Layer23TrafficPortFilter class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.layer23trafficportfilter.layer23trafficportfilter.Layer23TrafficPortFilter)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.layer23trafficportfilter.layer23trafficportfilter import Layer23TrafficPortFilter
		return Layer23TrafficPortFilter(self)

	@property
	def Layer47AppLibraryTrafficFilter(self):
		"""An instance of the Layer47AppLibraryTrafficFilter class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.layer47applibrarytrafficfilter.layer47applibrarytrafficfilter.Layer47AppLibraryTrafficFilter)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.layer47applibrarytrafficfilter.layer47applibrarytrafficfilter import Layer47AppLibraryTrafficFilter
		return Layer47AppLibraryTrafficFilter(self)

	@property
	def Page(self):
		"""An instance of the Page class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.page.page.Page)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.page.page import Page
		return Page(self)._select()

	@property
	def Statistic(self):
		"""An instance of the Statistic class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.statistic.statistic.Statistic)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.statistic.statistic import Statistic
		return Statistic(self)

	@property
	def AutoRefresh(self):
		"""If true, automatically refreshes the statistics values. Default = true

		Returns:
			bool
		"""
		return self._get_attribute('autoRefresh')
	@AutoRefresh.setter
	def AutoRefresh(self, value):
		self._set_attribute('autoRefresh', value)

	@property
	def AutoUpdate(self):
		"""If true, automatically refreshes the statistics values. Default = true

		Returns:
			bool
		"""
		return self._get_attribute('autoUpdate')
	@AutoUpdate.setter
	def AutoUpdate(self, value):
		self._set_attribute('autoUpdate', value)

	@property
	def AvailableStatsSelectorColumns(self):
		"""NOT DEFINED

		Returns:
			list(str)
		"""
		return self._get_attribute('availableStatsSelectorColumns')

	@property
	def Caption(self):
		"""This is the name that will appear in the GUI stats view window header or in the added view tree from tcl. The caption must be unique.

		Returns:
			str
		"""
		return self._get_attribute('caption')
	@Caption.setter
	def Caption(self, value):
		self._set_attribute('caption', value)

	@property
	def CsvFileName(self):
		"""Specifies the file name which is used by the CSV Logging feature. The default value is the caption of the view.

		Returns:
			str
		"""
		return self._get_attribute('csvFileName')
	@CsvFileName.setter
	def CsvFileName(self, value):
		self._set_attribute('csvFileName', value)

	@property
	def EnableCsvLogging(self):
		"""If the CSV Logging feature is enabled the statistics values from a view will be written in a comma separated value format.

		Returns:
			bool
		"""
		return self._get_attribute('enableCsvLogging')
	@EnableCsvLogging.setter
	def EnableCsvLogging(self, value):
		self._set_attribute('enableCsvLogging', value)

	@property
	def Enabled(self):
		"""If true, enables the view that is created from the tcl script.

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def EnabledStatsSelectorColumns(self):
		"""NOT DEFINED

		Returns:
			list(str)
		"""
		return self._get_attribute('enabledStatsSelectorColumns')
	@EnabledStatsSelectorColumns.setter
	def EnabledStatsSelectorColumns(self, value):
		self._set_attribute('enabledStatsSelectorColumns', value)

	@property
	def PageTimeout(self):
		"""The statistics view page is timed out based on the time specified. default = 25,000 ms

		Returns:
			number
		"""
		return self._get_attribute('pageTimeout')
	@PageTimeout.setter
	def PageTimeout(self, value):
		self._set_attribute('pageTimeout', value)

	@property
	def ReadOnly(self):
		"""The default views created by the application will have this attribute set to false. Tcl SV created by user has this value set to true. Based on this attribute value, the user is allowed to modify the SV attributes.

		Returns:
			bool
		"""
		return self._get_attribute('readOnly')

	@property
	def TimeSeries(self):
		"""If false, then it displays non-timeseries grid views. If true, displays, timeseries line chart view. default = false (non-timeseries)

		Returns:
			bool
		"""
		return self._get_attribute('timeSeries')
	@TimeSeries.setter
	def TimeSeries(self, value):
		self._set_attribute('timeSeries', value)

	@property
	def TreeViewNodeName(self):
		"""Displays the name of the tree view node.

		Returns:
			str
		"""
		return self._get_attribute('treeViewNodeName')
	@TreeViewNodeName.setter
	def TreeViewNodeName(self, value):
		self._set_attribute('treeViewNodeName', value)

	@property
	def Type(self):
		"""The type of view the user wants to create from tcl.

		Returns:
			str(layer23NextGenProtocol|layer23ProtocolAuthAccess|layer23ProtocolPort|layer23ProtocolRouting|layer23ProtocolStack|layer23TrafficFlow|layer23TrafficFlowDetective|layer23TrafficItem|layer23TrafficPort|layer47AppLibraryTraffic|sVReadOnly)
		"""
		return self._get_attribute('type')
	@Type.setter
	def Type(self, value):
		self._set_attribute('type', value)

	@property
	def TypeDescription(self):
		"""If true, desribes the type

		Returns:
			str
		"""
		return self._get_attribute('typeDescription')

	@property
	def ViewCategory(self):
		"""Returns the category of the view based on the type of statistics displayed by the view.

		Returns:
			str(ClassicProtocol|L23Traffic|L47Traffic|Mixed|NextGenProtocol|PerSession|Unknown)
		"""
		return self._get_attribute('viewCategory')

	@property
	def Visible(self):
		"""If true, displays the custom created tcl SVs in the SV tree under TCL Views node.

		Returns:
			bool
		"""
		return self._get_attribute('visible')
	@Visible.setter
	def Visible(self, value):
		self._set_attribute('visible', value)

	def add(self, AutoRefresh=None, AutoUpdate=None, Caption=None, CsvFileName=None, EnableCsvLogging=None, Enabled=None, EnabledStatsSelectorColumns=None, PageTimeout=None, TimeSeries=None, TreeViewNodeName=None, Type=None, Visible=None):
		"""Adds a new view node on the server and retrieves it in this instance.

		Args:
			AutoRefresh (bool): If true, automatically refreshes the statistics values. Default = true
			AutoUpdate (bool): If true, automatically refreshes the statistics values. Default = true
			Caption (str): This is the name that will appear in the GUI stats view window header or in the added view tree from tcl. The caption must be unique.
			CsvFileName (str): Specifies the file name which is used by the CSV Logging feature. The default value is the caption of the view.
			EnableCsvLogging (bool): If the CSV Logging feature is enabled the statistics values from a view will be written in a comma separated value format.
			Enabled (bool): If true, enables the view that is created from the tcl script.
			EnabledStatsSelectorColumns (list(str)): NOT DEFINED
			PageTimeout (number): The statistics view page is timed out based on the time specified. default = 25,000 ms
			TimeSeries (bool): If false, then it displays non-timeseries grid views. If true, displays, timeseries line chart view. default = false (non-timeseries)
			TreeViewNodeName (str): Displays the name of the tree view node.
			Type (str(layer23NextGenProtocol|layer23ProtocolAuthAccess|layer23ProtocolPort|layer23ProtocolRouting|layer23ProtocolStack|layer23TrafficFlow|layer23TrafficFlowDetective|layer23TrafficItem|layer23TrafficPort|layer47AppLibraryTraffic|sVReadOnly)): The type of view the user wants to create from tcl.
			Visible (bool): If true, displays the custom created tcl SVs in the SV tree under TCL Views node.

		Returns:
			self: This instance with all currently retrieved view data using find and the newly added view data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the view data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, AutoRefresh=None, AutoUpdate=None, AvailableStatsSelectorColumns=None, Caption=None, CsvFileName=None, EnableCsvLogging=None, Enabled=None, EnabledStatsSelectorColumns=None, PageTimeout=None, ReadOnly=None, TimeSeries=None, TreeViewNodeName=None, Type=None, TypeDescription=None, ViewCategory=None, Visible=None):
		"""Finds and retrieves view data from the server.

		All named parameters support regex and can be used to selectively retrieve view data from the server.
		By default the find method takes no parameters and will retrieve all view data from the server.

		Args:
			AutoRefresh (bool): If true, automatically refreshes the statistics values. Default = true
			AutoUpdate (bool): If true, automatically refreshes the statistics values. Default = true
			AvailableStatsSelectorColumns (list(str)): NOT DEFINED
			Caption (str): This is the name that will appear in the GUI stats view window header or in the added view tree from tcl. The caption must be unique.
			CsvFileName (str): Specifies the file name which is used by the CSV Logging feature. The default value is the caption of the view.
			EnableCsvLogging (bool): If the CSV Logging feature is enabled the statistics values from a view will be written in a comma separated value format.
			Enabled (bool): If true, enables the view that is created from the tcl script.
			EnabledStatsSelectorColumns (list(str)): NOT DEFINED
			PageTimeout (number): The statistics view page is timed out based on the time specified. default = 25,000 ms
			ReadOnly (bool): The default views created by the application will have this attribute set to false. Tcl SV created by user has this value set to true. Based on this attribute value, the user is allowed to modify the SV attributes.
			TimeSeries (bool): If false, then it displays non-timeseries grid views. If true, displays, timeseries line chart view. default = false (non-timeseries)
			TreeViewNodeName (str): Displays the name of the tree view node.
			Type (str(layer23NextGenProtocol|layer23ProtocolAuthAccess|layer23ProtocolPort|layer23ProtocolRouting|layer23ProtocolStack|layer23TrafficFlow|layer23TrafficFlowDetective|layer23TrafficItem|layer23TrafficPort|layer47AppLibraryTraffic|sVReadOnly)): The type of view the user wants to create from tcl.
			TypeDescription (str): If true, desribes the type
			ViewCategory (str(ClassicProtocol|L23Traffic|L47Traffic|Mixed|NextGenProtocol|PerSession|Unknown)): Returns the category of the view based on the type of statistics displayed by the view.
			Visible (bool): If true, displays the custom created tcl SVs in the SV tree under TCL Views node.

		Returns:
			self: This instance with matching view data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of view data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the view data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)

	def ExportData(self, FilePathName):
		"""Executes the exportData operation on the server.

		Exports the data seen in a view to a file. Supported formats are .html, .xml, .xls and .txt.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=view)): The method internally set Arg1 to the current href for this instance
			FilePathName (str): The path where the exported file should be written.

		Returns:
			str: This can be either a success message or a description of the problem if any error occurred.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('ExportData', payload=locals(), response_object=None)

	def GetColumnValues(self, Arg2):
		"""Executes the getColumnValues operation on the server.

		Retrieves the requested column values.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=view)): The method internally set Arg1 to the current href for this instance
			Arg2 (str): The name of the column for which to retrieve statistics.

		Returns:
			dict(arg1:list[str],arg2:str): An array with the values retrieved.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('GetColumnValues', payload=locals(), response_object=None)

	def GetResultsPath(self):
		"""Executes the getResultsPath operation on the server.

		Gets the path where the results for the current tests are stored.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=view)): The method internally set Arg1 to the current href for this instance

		Returns:
			str: The results path.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('GetResultsPath', payload=locals(), response_object=None)

	def GetRowValues(self, Arg2):
		"""Executes the getRowValues operation on the server.

		Retrieves the requested row values.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=view)): The method internally set Arg1 to the current href for this instance
			Arg2 (str): The label identifying the row for which to retrieve statistics. It is formed from the values of the row label columns concatenated using | delimiter. Row label columns appear with orange or yellow names in the view.

		Returns:
			dict(arg1:list[str],arg2:str): An array with the values retrieved.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('GetRowValues', payload=locals(), response_object=None)

	def GetValue(self, Arg2, Arg3):
		"""Executes the getValue operation on the server.

		Retrieves the requested statistical data.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=view)): The method internally set Arg1 to the current href for this instance
			Arg2 (str): The label identifying the row for which to retrieve statistics. It is formed from the values of the row label columns concatenated using | delimiter. Row label columns appear with orange or yellow names in the view.
			Arg3 (str): The name of the column for which to retrieve statistics.

		Returns:
			str: The retrieved value.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('GetValue', payload=locals(), response_object=None)

	def Refresh(self):
		"""Executes the refresh operation on the server.

		Refreshes the existing values in the view with the new values. If the view is NGPF on demand, the refresh will get new values for all NGPF on demand views.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=view)): The method internally set Arg1 to the current href for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('Refresh', payload=locals(), response_object=None)

	def RestoreToDefaults(self):
		"""Executes the restoreToDefaults operation on the server.

		NOT DEFINED

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=view)): The method internally set Arg1 to the current href for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('RestoreToDefaults', payload=locals(), response_object=None)
