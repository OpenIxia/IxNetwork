
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


class Mld(Base):
	"""The Mld class encapsulates a required mld node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Mld property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'mld'

	def __init__(self, parent):
		super(Mld, self).__init__(parent)

	@property
	def Host(self):
		"""An instance of the Host class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.mld.host.host.Host)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.mld.host.host import Host
		return Host(self)

	@property
	def Querier(self):
		"""An instance of the Querier class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.mld.querier.querier.Querier)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.mld.querier.querier import Querier
		return Querier(self)

	@property
	def EnableDoneOnStop(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableDoneOnStop')
	@EnableDoneOnStop.setter
	def EnableDoneOnStop(self, value):
		self._set_attribute('enableDoneOnStop', value)

	@property
	def Enabled(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def Mldv2Report(self):
		"""

		Returns:
			str(type143|type206)
		"""
		return self._get_attribute('mldv2Report')
	@Mldv2Report.setter
	def Mldv2Report(self, value):
		self._set_attribute('mldv2Report', value)

	@property
	def NumberOfGroups(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('numberOfGroups')
	@NumberOfGroups.setter
	def NumberOfGroups(self, value):
		self._set_attribute('numberOfGroups', value)

	@property
	def NumberOfQueries(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('numberOfQueries')
	@NumberOfQueries.setter
	def NumberOfQueries(self, value):
		self._set_attribute('numberOfQueries', value)

	@property
	def QueryTimePeriod(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('queryTimePeriod')
	@QueryTimePeriod.setter
	def QueryTimePeriod(self, value):
		self._set_attribute('queryTimePeriod', value)

	@property
	def RunningState(self):
		"""

		Returns:
			str(unknown|stopped|stopping|starting|started)
		"""
		return self._get_attribute('runningState')

	@property
	def TimePeriod(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('timePeriod')
	@TimePeriod.setter
	def TimePeriod(self, value):
		self._set_attribute('timePeriod', value)

	def Start(self):
		"""Executes the start operation on the server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=mld)): The method internally sets Arg1 to the current href for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('Start', payload=locals(), response_object=None)

	def Stop(self):
		"""Executes the stop operation on the server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=mld)): The method internally sets Arg1 to the current href for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('Stop', payload=locals(), response_object=None)
