
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


class EventNotificationLearnedInfo(Base):
	"""The EventNotificationLearnedInfo class encapsulates a system managed eventNotificationLearnedInfo node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the EventNotificationLearnedInfo property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'eventNotificationLearnedInfo'

	def __init__(self, parent):
		super(EventNotificationLearnedInfo, self).__init__(parent)

	@property
	def LocalFrameErrorRunningTotal(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('localFrameErrorRunningTotal')

	@property
	def LocalFrameEventRunningTotal(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('localFrameEventRunningTotal')

	@property
	def LocalFramePeriodErrorRunningTotal(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('localFramePeriodErrorRunningTotal')

	@property
	def LocalFramePeriodEventRunningTotal(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('localFramePeriodEventRunningTotal')

	@property
	def LocalFrameSecSumErrorRunningTotal(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('localFrameSecSumErrorRunningTotal')

	@property
	def LocalFrameSecSumEventRunningTotal(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('localFrameSecSumEventRunningTotal')

	@property
	def LocalSymbolPeriodErrorRunningTotal(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('localSymbolPeriodErrorRunningTotal')

	@property
	def LocalSymbolPeriodEventRunningTotal(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('localSymbolPeriodEventRunningTotal')

	@property
	def RemoteFrameError(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('remoteFrameError')

	@property
	def RemoteFrameErrorRunningTotal(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('remoteFrameErrorRunningTotal')

	@property
	def RemoteFrameEventRunningTotal(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('remoteFrameEventRunningTotal')

	@property
	def RemoteFramePeriodError(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('remoteFramePeriodError')

	@property
	def RemoteFramePeriodErrorRunningTotal(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('remoteFramePeriodErrorRunningTotal')

	@property
	def RemoteFramePeriodEventRunningTotal(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('remoteFramePeriodEventRunningTotal')

	@property
	def RemoteFramePeriodThreshold(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('remoteFramePeriodThreshold')

	@property
	def RemoteFramePeriodWindow(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('remoteFramePeriodWindow')

	@property
	def RemoteFrameSecSumError(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('remoteFrameSecSumError')

	@property
	def RemoteFrameSecSumErrorRunningTotal(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('remoteFrameSecSumErrorRunningTotal')

	@property
	def RemoteFrameSecSumEventRunningTotal(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('remoteFrameSecSumEventRunningTotal')

	@property
	def RemoteFrameSecSumThreshold(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('remoteFrameSecSumThreshold')

	@property
	def RemoteFrameSecSumWindow(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('remoteFrameSecSumWindow')

	@property
	def RemoteFrameThreshold(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('remoteFrameThreshold')

	@property
	def RemoteFrameWindow(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('remoteFrameWindow')

	@property
	def RemoteSymbolPeriodErrorRunningTotal(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('remoteSymbolPeriodErrorRunningTotal')

	@property
	def RemoteSymbolPeriodErrors(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('remoteSymbolPeriodErrors')

	@property
	def RemoteSymbolPeriodEventRunningTotal(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('remoteSymbolPeriodEventRunningTotal')

	@property
	def RemoteSymbolPeriodThreshold(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('remoteSymbolPeriodThreshold')

	@property
	def RemoteSymbolPeriodWindow(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('remoteSymbolPeriodWindow')

	def find(self, LocalFrameErrorRunningTotal=None, LocalFrameEventRunningTotal=None, LocalFramePeriodErrorRunningTotal=None, LocalFramePeriodEventRunningTotal=None, LocalFrameSecSumErrorRunningTotal=None, LocalFrameSecSumEventRunningTotal=None, LocalSymbolPeriodErrorRunningTotal=None, LocalSymbolPeriodEventRunningTotal=None, RemoteFrameError=None, RemoteFrameErrorRunningTotal=None, RemoteFrameEventRunningTotal=None, RemoteFramePeriodError=None, RemoteFramePeriodErrorRunningTotal=None, RemoteFramePeriodEventRunningTotal=None, RemoteFramePeriodThreshold=None, RemoteFramePeriodWindow=None, RemoteFrameSecSumError=None, RemoteFrameSecSumErrorRunningTotal=None, RemoteFrameSecSumEventRunningTotal=None, RemoteFrameSecSumThreshold=None, RemoteFrameSecSumWindow=None, RemoteFrameThreshold=None, RemoteFrameWindow=None, RemoteSymbolPeriodErrorRunningTotal=None, RemoteSymbolPeriodErrors=None, RemoteSymbolPeriodEventRunningTotal=None, RemoteSymbolPeriodThreshold=None, RemoteSymbolPeriodWindow=None):
		"""Finds and retrieves eventNotificationLearnedInfo data from the server.

		All named parameters support regex and can be used to selectively retrieve eventNotificationLearnedInfo data from the server.
		By default the find method takes no parameters and will retrieve all eventNotificationLearnedInfo data from the server.

		Args:
			LocalFrameErrorRunningTotal (number): 
			LocalFrameEventRunningTotal (number): 
			LocalFramePeriodErrorRunningTotal (number): 
			LocalFramePeriodEventRunningTotal (number): 
			LocalFrameSecSumErrorRunningTotal (number): 
			LocalFrameSecSumEventRunningTotal (number): 
			LocalSymbolPeriodErrorRunningTotal (number): 
			LocalSymbolPeriodEventRunningTotal (number): 
			RemoteFrameError (number): 
			RemoteFrameErrorRunningTotal (number): 
			RemoteFrameEventRunningTotal (number): 
			RemoteFramePeriodError (number): 
			RemoteFramePeriodErrorRunningTotal (number): 
			RemoteFramePeriodEventRunningTotal (number): 
			RemoteFramePeriodThreshold (number): 
			RemoteFramePeriodWindow (number): 
			RemoteFrameSecSumError (number): 
			RemoteFrameSecSumErrorRunningTotal (number): 
			RemoteFrameSecSumEventRunningTotal (number): 
			RemoteFrameSecSumThreshold (number): 
			RemoteFrameSecSumWindow (number): 
			RemoteFrameThreshold (number): 
			RemoteFrameWindow (number): 
			RemoteSymbolPeriodErrorRunningTotal (number): 
			RemoteSymbolPeriodErrors (number): 
			RemoteSymbolPeriodEventRunningTotal (number): 
			RemoteSymbolPeriodThreshold (number): 
			RemoteSymbolPeriodWindow (number): 

		Returns:
			self: This instance with matching eventNotificationLearnedInfo data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of eventNotificationLearnedInfo data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the eventNotificationLearnedInfo data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
