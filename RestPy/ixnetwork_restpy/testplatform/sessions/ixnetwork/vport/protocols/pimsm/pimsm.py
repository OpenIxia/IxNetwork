
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


class Pimsm(Base):
	"""The Pimsm class encapsulates a required pimsm node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Pimsm property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'pimsm'

	def __init__(self, parent):
		super(Pimsm, self).__init__(parent)

	@property
	def Router(self):
		"""An instance of the Router class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.pimsm.router.router.Router)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.pimsm.router.router import Router
		return Router(self)

	@property
	def BsmFramePerInterval(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('bsmFramePerInterval')
	@BsmFramePerInterval.setter
	def BsmFramePerInterval(self, value):
		self._set_attribute('bsmFramePerInterval', value)

	@property
	def CrpFramePerInterval(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('crpFramePerInterval')
	@CrpFramePerInterval.setter
	def CrpFramePerInterval(self, value):
		self._set_attribute('crpFramePerInterval', value)

	@property
	def DataMdtFramePerInterval(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('dataMdtFramePerInterval')
	@DataMdtFramePerInterval.setter
	def DataMdtFramePerInterval(self, value):
		self._set_attribute('dataMdtFramePerInterval', value)

	@property
	def DenyGrePimIpPrefix(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('denyGrePimIpPrefix')
	@DenyGrePimIpPrefix.setter
	def DenyGrePimIpPrefix(self, value):
		self._set_attribute('denyGrePimIpPrefix', value)

	@property
	def EnableDiscardJoinPruneProcessing(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableDiscardJoinPruneProcessing')
	@EnableDiscardJoinPruneProcessing.setter
	def EnableDiscardJoinPruneProcessing(self, value):
		self._set_attribute('enableDiscardJoinPruneProcessing', value)

	@property
	def EnableRateControl(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableRateControl')
	@EnableRateControl.setter
	def EnableRateControl(self, value):
		self._set_attribute('enableRateControl', value)

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
	def GreFilterType(self):
		"""

		Returns:
			str(noDataMdt|dataMdtIpv4)
		"""
		return self._get_attribute('greFilterType')
	@GreFilterType.setter
	def GreFilterType(self, value):
		self._set_attribute('greFilterType', value)

	@property
	def HelloMsgsPerInterval(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('helloMsgsPerInterval')
	@HelloMsgsPerInterval.setter
	def HelloMsgsPerInterval(self, value):
		self._set_attribute('helloMsgsPerInterval', value)

	@property
	def Interval(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('interval')
	@Interval.setter
	def Interval(self, value):
		self._set_attribute('interval', value)

	@property
	def JoinPruneMessagesPerInterval(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('joinPruneMessagesPerInterval')
	@JoinPruneMessagesPerInterval.setter
	def JoinPruneMessagesPerInterval(self, value):
		self._set_attribute('joinPruneMessagesPerInterval', value)

	@property
	def OverrideSourceIpForSmInterface(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('overrideSourceIpForSmInterface')
	@OverrideSourceIpForSmInterface.setter
	def OverrideSourceIpForSmInterface(self, value):
		self._set_attribute('overrideSourceIpForSmInterface', value)

	@property
	def RegisterMessagesPerInterval(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('registerMessagesPerInterval')
	@RegisterMessagesPerInterval.setter
	def RegisterMessagesPerInterval(self, value):
		self._set_attribute('registerMessagesPerInterval', value)

	@property
	def RegisterStopMessagesPerInterval(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('registerStopMessagesPerInterval')
	@RegisterStopMessagesPerInterval.setter
	def RegisterStopMessagesPerInterval(self, value):
		self._set_attribute('registerStopMessagesPerInterval', value)

	@property
	def RunningState(self):
		"""

		Returns:
			str(unknown|stopped|stopping|starting|started)
		"""
		return self._get_attribute('runningState')

	def Start(self):
		"""Executes the start operation on the server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=pimsm)): The method internally sets Arg1 to the current href for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('Start', payload=locals(), response_object=None)

	def Stop(self):
		"""Executes the stop operation on the server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=pimsm)): The method internally sets Arg1 to the current href for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('Stop', payload=locals(), response_object=None)
