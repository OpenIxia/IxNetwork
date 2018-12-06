
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
		"""

		Returns:
			str(fcoeInvalidDelimiter|fcoeInvalidFrames|fcoeInvalidSize|fcoeNormalSizeBadFcCRC|fcoeNormalSizeGoodFcCRC|fcoeUndersizeBadFcCRC|fcoeUndersizeGoodFcCRC|fcoeValidFrames)
		"""
		return self._get_attribute('additionalFcoeStat1')
	@AdditionalFcoeStat1.setter
	def AdditionalFcoeStat1(self, value):
		self._set_attribute('additionalFcoeStat1', value)

	@property
	def AdditionalFcoeStat2(self):
		"""

		Returns:
			str(fcoeInvalidDelimiter|fcoeInvalidFrames|fcoeInvalidSize|fcoeNormalSizeBadFcCRC|fcoeNormalSizeGoodFcCRC|fcoeUndersizeBadFcCRC|fcoeUndersizeGoodFcCRC|fcoeValidFrames)
		"""
		return self._get_attribute('additionalFcoeStat2')
	@AdditionalFcoeStat2.setter
	def AdditionalFcoeStat2(self, value):
		self._set_attribute('additionalFcoeStat2', value)

	@property
	def CsvFilePath(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('csvFilePath')
	@CsvFilePath.setter
	def CsvFilePath(self, value):
		self._set_attribute('csvFilePath', value)

	@property
	def CsvLogPollIntervalMultiplier(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('csvLogPollIntervalMultiplier')
	@CsvLogPollIntervalMultiplier.setter
	def CsvLogPollIntervalMultiplier(self, value):
		self._set_attribute('csvLogPollIntervalMultiplier', value)

	@property
	def DataStorePollingIntervalMultiplier(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('dataStorePollingIntervalMultiplier')
	@DataStorePollingIntervalMultiplier.setter
	def DataStorePollingIntervalMultiplier(self, value):
		self._set_attribute('dataStorePollingIntervalMultiplier', value)

	@property
	def EnableAutoDataStore(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableAutoDataStore')
	@EnableAutoDataStore.setter
	def EnableAutoDataStore(self, value):
		self._set_attribute('enableAutoDataStore', value)

	@property
	def EnableCsvLogging(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableCsvLogging')
	@EnableCsvLogging.setter
	def EnableCsvLogging(self, value):
		self._set_attribute('enableCsvLogging', value)

	@property
	def EnableDataCenterSharedStats(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableDataCenterSharedStats')
	@EnableDataCenterSharedStats.setter
	def EnableDataCenterSharedStats(self, value):
		self._set_attribute('enableDataCenterSharedStats', value)

	@property
	def GuardrailEnabled(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('guardrailEnabled')
	@GuardrailEnabled.setter
	def GuardrailEnabled(self, value):
		self._set_attribute('guardrailEnabled', value)

	@property
	def MaxNumberOfStatsPerCustomGraph(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('maxNumberOfStatsPerCustomGraph')
	@MaxNumberOfStatsPerCustomGraph.setter
	def MaxNumberOfStatsPerCustomGraph(self, value):
		self._set_attribute('maxNumberOfStatsPerCustomGraph', value)

	@property
	def PollInterval(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('pollInterval')
	@PollInterval.setter
	def PollInterval(self, value):
		self._set_attribute('pollInterval', value)

	@property
	def TimeSynchronization(self):
		"""

		Returns:
			str(syncTimeToSystemClock|syncTimeToTestStart)
		"""
		return self._get_attribute('timeSynchronization')
	@TimeSynchronization.setter
	def TimeSynchronization(self, value):
		self._set_attribute('timeSynchronization', value)

	@property
	def TimestampPrecision(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('timestampPrecision')
	@TimestampPrecision.setter
	def TimestampPrecision(self, value):
		self._set_attribute('timestampPrecision', value)

	@property
	def UgsTcpPort(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('ugsTcpPort')

	def CheckViewTreeGroupExists(self, Arg2):
		"""Executes the checkViewTreeGroupExists operation on the server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/statistics)): The method internally sets Arg1 to the current href for this instance
			Arg2 (str): 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('CheckViewTreeGroupExists', payload=locals(), response_object=None)

	def DockStatViewer(self):
		"""Executes the dockStatViewer operation on the server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/statistics)): The method internally sets Arg1 to the current href for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('DockStatViewer', payload=locals(), response_object=None)

	def GetPGIDList(self, Arg2, Arg3):
		"""Executes the getPGIDList operation on the server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/statistics)): The method internally sets Arg1 to the current href for this instance
			Arg2 (str): 
			Arg3 (str): 

		Returns:
			list(str): 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('GetPGIDList', payload=locals(), response_object=None)

	def GetStatsFooters(self, Arg2, Arg3, Arg4):
		"""Executes the getStatsFooters operation on the server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/statistics)): The method internally sets Arg1 to the current href for this instance
			Arg2 (str): 
			Arg3 (str): 
			Arg4 (str): 

		Returns:
			str: 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('GetStatsFooters', payload=locals(), response_object=None)
