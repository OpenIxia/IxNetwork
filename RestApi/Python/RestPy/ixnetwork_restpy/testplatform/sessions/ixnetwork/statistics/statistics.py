from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Statistics(Base):
	"""The Statistics class encapsulates a required statistics node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Statistics property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'statistics'

	def __init__(self, parent):
		super(Statistics, self).__init__(parent)

	@property
	def AutoRefresh(self):
		"""An instance of the AutoRefresh class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.autorefresh.autorefresh.AutoRefresh)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.autorefresh.autorefresh import AutoRefresh
		return AutoRefresh(self)._select()

	@property
	def CsvSnapshot(self):
		"""An instance of the CsvSnapshot class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.csvsnapshot.csvsnapshot.CsvSnapshot)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.csvsnapshot.csvsnapshot import CsvSnapshot
		return CsvSnapshot(self)._select()

	@property
	def Ixreporter(self):
		"""An instance of the Ixreporter class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.ixreporter.ixreporter.Ixreporter)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.ixreporter.ixreporter import Ixreporter
		return Ixreporter(self)._select()

	@property
	def MeasurementMode(self):
		"""An instance of the MeasurementMode class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.measurementmode.measurementmode.MeasurementMode)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.measurementmode.measurementmode import MeasurementMode
		return MeasurementMode(self)._select()

	@property
	def RawData(self):
		"""An instance of the RawData class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.rawdata.rawdata.RawData)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.rawdata.rawdata import RawData
		return RawData(self)._select()

	@property
	def StatRequest(self):
		"""An instance of the StatRequest class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.statrequest.statrequest.StatRequest)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.statrequest.statrequest import StatRequest
		return StatRequest(self)

	@property
	def View(self):
		"""An instance of the View class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.view.View)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.view import View
		return View(self)

	@property
	def AdditionalFcoeStat1(self):
		"""Signifies additional FCOE stat 1

		Returns:
			str(fcoeInvalidDelimiter|fcoeInvalidFrames|fcoeInvalidSize|fcoeNormalSizeBadFcCRC|fcoeNormalSizeGoodFcCRC|fcoeUndersizeBadFcCRC|fcoeUndersizeGoodFcCRC|fcoeValidFrames)
		"""
		return self._get_attribute('additionalFcoeStat1')
	@AdditionalFcoeStat1.setter
	def AdditionalFcoeStat1(self, value):
		self._set_attribute('additionalFcoeStat1', value)

	@property
	def AdditionalFcoeStat2(self):
		"""Sets the additional FCoE shared stats.

		Returns:
			str(fcoeInvalidDelimiter|fcoeInvalidFrames|fcoeInvalidSize|fcoeNormalSizeBadFcCRC|fcoeNormalSizeGoodFcCRC|fcoeUndersizeBadFcCRC|fcoeUndersizeGoodFcCRC|fcoeValidFrames)
		"""
		return self._get_attribute('additionalFcoeStat2')
	@AdditionalFcoeStat2.setter
	def AdditionalFcoeStat2(self, value):
		self._set_attribute('additionalFcoeStat2', value)

	@property
	def CsvFilePath(self):
		"""Sets the CSV file path.

		Returns:
			str
		"""
		return self._get_attribute('csvFilePath')
	@CsvFilePath.setter
	def CsvFilePath(self, value):
		self._set_attribute('csvFilePath', value)

	@property
	def CsvLogPollIntervalMultiplier(self):
		"""Used to specify the time interval between log polling events.

		Returns:
			number
		"""
		return self._get_attribute('csvLogPollIntervalMultiplier')
	@CsvLogPollIntervalMultiplier.setter
	def CsvLogPollIntervalMultiplier(self, value):
		self._set_attribute('csvLogPollIntervalMultiplier', value)

	@property
	def DataStorePollingIntervalMultiplier(self):
		"""The data store polling interval value is the result of the data store polling interval multiplier value multiplied by the polling interval value set for the test.

		Returns:
			number
		"""
		return self._get_attribute('dataStorePollingIntervalMultiplier')
	@DataStorePollingIntervalMultiplier.setter
	def DataStorePollingIntervalMultiplier(self, value):
		self._set_attribute('dataStorePollingIntervalMultiplier', value)

	@property
	def EnableAutoDataStore(self):
		"""If this option is enabled, StatViewer writes the statistical values in binary format for all test results in a view. The test results is converted into a binary array and written to a file.

		Returns:
			bool
		"""
		return self._get_attribute('enableAutoDataStore')
	@EnableAutoDataStore.setter
	def EnableAutoDataStore(self, value):
		self._set_attribute('enableAutoDataStore', value)

	@property
	def EnableCsvLogging(self):
		"""If this option is enabled, StatViewer writes the statistical values in comma separated value format for all test results in a view.

		Returns:
			bool
		"""
		return self._get_attribute('enableCsvLogging')
	@EnableCsvLogging.setter
	def EnableCsvLogging(self, value):
		self._set_attribute('enableCsvLogging', value)

	@property
	def EnableDataCenterSharedStats(self):
		"""If true, enables statistics for Data Center.

		Returns:
			bool
		"""
		return self._get_attribute('enableDataCenterSharedStats')
	@EnableDataCenterSharedStats.setter
	def EnableDataCenterSharedStats(self, value):
		self._set_attribute('enableDataCenterSharedStats', value)

	@property
	def GuardrailEnabled(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('guardrailEnabled')
	@GuardrailEnabled.setter
	def GuardrailEnabled(self, value):
		self._set_attribute('guardrailEnabled', value)

	@property
	def MaxNumberOfStatsPerCustomGraph(self):
		"""The data store polling interval value is the result of the data store polling interval multiplier value multiplied by the polling interval value set for the test.

		Returns:
			number
		"""
		return self._get_attribute('maxNumberOfStatsPerCustomGraph')
	@MaxNumberOfStatsPerCustomGraph.setter
	def MaxNumberOfStatsPerCustomGraph(self, value):
		self._set_attribute('maxNumberOfStatsPerCustomGraph', value)

	@property
	def PollInterval(self):
		"""The multiplier used with the frequency (2 seconds), to set the time interval between polling events. The default is 1 (1 times 2 seconds = 2 seconds).

		Returns:
			number
		"""
		return self._get_attribute('pollInterval')
	@PollInterval.setter
	def PollInterval(self, value):
		self._set_attribute('pollInterval', value)

	@property
	def TimeSynchronization(self):
		"""The statistics polling time can be configured to get synchronized with the system clock or reset it to 0 when the test starts. The time synchronization behavior can be changed only before the test starts and does not apply during test run.

		Returns:
			str(syncTimeToSystemClock|syncTimeToTestStart)
		"""
		return self._get_attribute('timeSynchronization')
	@TimeSynchronization.setter
	def TimeSynchronization(self, value):
		self._set_attribute('timeSynchronization', value)

	@property
	def TimestampPrecision(self):
		"""The timestamp precision allows you to change the timestamp precision from microseconds to nanoseconds for specific StatViewer statistics and features. The timestamp precision can be set to have the fstatistics display values with decimals ranging from 0 to 9.

		Returns:
			number
		"""
		return self._get_attribute('timestampPrecision')
	@TimestampPrecision.setter
	def TimestampPrecision(self, value):
		self._set_attribute('timestampPrecision', value)

	@property
	def UgsTcpPort(self):
		"""Used to specify the UGS TCP port.

		Returns:
			number
		"""
		return self._get_attribute('ugsTcpPort')

	def CheckViewTreeGroupExists(self, Arg2):
		"""Executes the checkViewTreeGroupExists operation on the server.

		This command verifies that the specified group name exists in the StatViewer tree.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/statistics)): The method internally set Arg1 to the current href for this instance
			Arg2 (str): NOT DEFINED

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('CheckViewTreeGroupExists', payload=locals(), response_object=None)

	def DockStatViewer(self):
		"""Executes the dockStatViewer operation on the server.

		NOT DEFINED

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/statistics)): The method internally set Arg1 to the current href for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('DockStatViewer', payload=locals(), response_object=None)

	def GetPGIDList(self, Arg2, Arg3):
		"""Executes the getPGIDList operation on the server.

		NOT DEFINED

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/statistics)): The method internally set Arg1 to the current href for this instance
			Arg2 (str): NOT DEFINED
			Arg3 (str): NOT DEFINED

		Returns:
			list(str): NOT DEFINED

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('GetPGIDList', payload=locals(), response_object=None)

	def GetStatsFooters(self, Arg2, Arg3, Arg4):
		"""Executes the getStatsFooters operation on the server.

		This command retrieves Stats Footers from traffic stats.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/statistics)): The method internally set Arg1 to the current href for this instance
			Arg2 (str): NOT DEFINED
			Arg3 (str): NOT DEFINED
			Arg4 (str): NOT DEFINED

		Returns:
			str: NOT DEFINED

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('GetStatsFooters', payload=locals(), response_object=None)
