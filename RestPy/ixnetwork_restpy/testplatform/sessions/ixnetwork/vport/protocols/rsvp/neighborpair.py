
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


class NeighborPair(Base):
	"""The NeighborPair class encapsulates a user managed neighborPair node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the NeighborPair property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'neighborPair'

	def __init__(self, parent):
		super(NeighborPair, self).__init__(parent)

	@property
	def AssignedLabel(self):
		"""An instance of the AssignedLabel class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.rsvp.assignedlabel.AssignedLabel)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.rsvp.assignedlabel import AssignedLabel
		return AssignedLabel(self)

	@property
	def DestinationRange(self):
		"""An instance of the DestinationRange class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.rsvp.destinationrange.DestinationRange)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.rsvp.destinationrange import DestinationRange
		return DestinationRange(self)

	@property
	def ReceivedLabel(self):
		"""An instance of the ReceivedLabel class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.rsvp.receivedlabel.ReceivedLabel)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.rsvp.receivedlabel import ReceivedLabel
		return ReceivedLabel(self)

	@property
	def ActualRestartTime(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('actualRestartTime')
	@ActualRestartTime.setter
	def ActualRestartTime(self, value):
		self._set_attribute('actualRestartTime', value)

	@property
	def DutIp(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('dutIp')
	@DutIp.setter
	def DutIp(self, value):
		self._set_attribute('dutIp', value)

	@property
	def EnableBfdRegistration(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableBfdRegistration')
	@EnableBfdRegistration.setter
	def EnableBfdRegistration(self, value):
		self._set_attribute('enableBfdRegistration', value)

	@property
	def EnableBundleMessageSending(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableBundleMessageSending')
	@EnableBundleMessageSending.setter
	def EnableBundleMessageSending(self, value):
		self._set_attribute('enableBundleMessageSending', value)

	@property
	def EnableGracefulRestartHelperMode(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableGracefulRestartHelperMode')
	@EnableGracefulRestartHelperMode.setter
	def EnableGracefulRestartHelperMode(self, value):
		self._set_attribute('enableGracefulRestartHelperMode', value)

	@property
	def EnableGracefulRestartingMode(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableGracefulRestartingMode')
	@EnableGracefulRestartingMode.setter
	def EnableGracefulRestartingMode(self, value):
		self._set_attribute('enableGracefulRestartingMode', value)

	@property
	def EnableHello(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableHello')
	@EnableHello.setter
	def EnableHello(self, value):
		self._set_attribute('enableHello', value)

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
	def GracefulRestartStartTime(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('gracefulRestartStartTime')
	@GracefulRestartStartTime.setter
	def GracefulRestartStartTime(self, value):
		self._set_attribute('gracefulRestartStartTime', value)

	@property
	def GracefulRestartUpTime(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('gracefulRestartUpTime')
	@GracefulRestartUpTime.setter
	def GracefulRestartUpTime(self, value):
		self._set_attribute('gracefulRestartUpTime', value)

	@property
	def HelloInterval(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('helloInterval')
	@HelloInterval.setter
	def HelloInterval(self, value):
		self._set_attribute('helloInterval', value)

	@property
	def HelloTimeoutMultiplier(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('helloTimeoutMultiplier')
	@HelloTimeoutMultiplier.setter
	def HelloTimeoutMultiplier(self, value):
		self._set_attribute('helloTimeoutMultiplier', value)

	@property
	def HelloTlvs(self):
		"""

		Returns:
			list(dict(arg1:number,arg2:number,arg3:str))
		"""
		return self._get_attribute('helloTlvs')
	@HelloTlvs.setter
	def HelloTlvs(self, value):
		self._set_attribute('helloTlvs', value)

	@property
	def IsAssignedInfoRefreshed(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('isAssignedInfoRefreshed')

	@property
	def IsLearnedInfoRefreshed(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('isLearnedInfoRefreshed')

	@property
	def LabelSpaceEnd(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('labelSpaceEnd')
	@LabelSpaceEnd.setter
	def LabelSpaceEnd(self, value):
		self._set_attribute('labelSpaceEnd', value)

	@property
	def LabelSpaceStart(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('labelSpaceStart')
	@LabelSpaceStart.setter
	def LabelSpaceStart(self, value):
		self._set_attribute('labelSpaceStart', value)

	@property
	def NumberOfGracefulRestarts(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('numberOfGracefulRestarts')
	@NumberOfGracefulRestarts.setter
	def NumberOfGracefulRestarts(self, value):
		self._set_attribute('numberOfGracefulRestarts', value)

	@property
	def OurIp(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('ourIp')
	@OurIp.setter
	def OurIp(self, value):
		self._set_attribute('ourIp', value)

	@property
	def RecoveryTimeInterval(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('recoveryTimeInterval')
	@RecoveryTimeInterval.setter
	def RecoveryTimeInterval(self, value):
		self._set_attribute('recoveryTimeInterval', value)

	@property
	def RefreshReduction(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('refreshReduction')
	@RefreshReduction.setter
	def RefreshReduction(self, value):
		self._set_attribute('refreshReduction', value)

	@property
	def RestartTimeInterval(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('restartTimeInterval')
	@RestartTimeInterval.setter
	def RestartTimeInterval(self, value):
		self._set_attribute('restartTimeInterval', value)

	@property
	def SummaryRefreshInterval(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('summaryRefreshInterval')
	@SummaryRefreshInterval.setter
	def SummaryRefreshInterval(self, value):
		self._set_attribute('summaryRefreshInterval', value)

	@property
	def TrafficGroupId(self):
		"""

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficGroup)
		"""
		return self._get_attribute('trafficGroupId')
	@TrafficGroupId.setter
	def TrafficGroupId(self, value):
		self._set_attribute('trafficGroupId', value)

	def add(self, ActualRestartTime=None, DutIp=None, EnableBfdRegistration=None, EnableBundleMessageSending=None, EnableGracefulRestartHelperMode=None, EnableGracefulRestartingMode=None, EnableHello=None, Enabled=None, GracefulRestartStartTime=None, GracefulRestartUpTime=None, HelloInterval=None, HelloTimeoutMultiplier=None, HelloTlvs=None, LabelSpaceEnd=None, LabelSpaceStart=None, NumberOfGracefulRestarts=None, OurIp=None, RecoveryTimeInterval=None, RefreshReduction=None, RestartTimeInterval=None, SummaryRefreshInterval=None, TrafficGroupId=None):
		"""Adds a new neighborPair node on the server and retrieves it in this instance.

		Args:
			ActualRestartTime (number): 
			DutIp (str): 
			EnableBfdRegistration (bool): 
			EnableBundleMessageSending (bool): 
			EnableGracefulRestartHelperMode (bool): 
			EnableGracefulRestartingMode (bool): 
			EnableHello (bool): 
			Enabled (bool): 
			GracefulRestartStartTime (number): 
			GracefulRestartUpTime (number): 
			HelloInterval (number): 
			HelloTimeoutMultiplier (number): 
			HelloTlvs (list(dict(arg1:number,arg2:number,arg3:str))): 
			LabelSpaceEnd (number): 
			LabelSpaceStart (number): 
			NumberOfGracefulRestarts (number): 
			OurIp (str): 
			RecoveryTimeInterval (number): 
			RefreshReduction (bool): 
			RestartTimeInterval (number): 
			SummaryRefreshInterval (number): 
			TrafficGroupId (str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficGroup)): 

		Returns:
			self: This instance with all currently retrieved neighborPair data using find and the newly added neighborPair data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the neighborPair data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, ActualRestartTime=None, DutIp=None, EnableBfdRegistration=None, EnableBundleMessageSending=None, EnableGracefulRestartHelperMode=None, EnableGracefulRestartingMode=None, EnableHello=None, Enabled=None, GracefulRestartStartTime=None, GracefulRestartUpTime=None, HelloInterval=None, HelloTimeoutMultiplier=None, HelloTlvs=None, IsAssignedInfoRefreshed=None, IsLearnedInfoRefreshed=None, LabelSpaceEnd=None, LabelSpaceStart=None, NumberOfGracefulRestarts=None, OurIp=None, RecoveryTimeInterval=None, RefreshReduction=None, RestartTimeInterval=None, SummaryRefreshInterval=None, TrafficGroupId=None):
		"""Finds and retrieves neighborPair data from the server.

		All named parameters support regex and can be used to selectively retrieve neighborPair data from the server.
		By default the find method takes no parameters and will retrieve all neighborPair data from the server.

		Args:
			ActualRestartTime (number): 
			DutIp (str): 
			EnableBfdRegistration (bool): 
			EnableBundleMessageSending (bool): 
			EnableGracefulRestartHelperMode (bool): 
			EnableGracefulRestartingMode (bool): 
			EnableHello (bool): 
			Enabled (bool): 
			GracefulRestartStartTime (number): 
			GracefulRestartUpTime (number): 
			HelloInterval (number): 
			HelloTimeoutMultiplier (number): 
			HelloTlvs (list(dict(arg1:number,arg2:number,arg3:str))): 
			IsAssignedInfoRefreshed (bool): 
			IsLearnedInfoRefreshed (bool): 
			LabelSpaceEnd (number): 
			LabelSpaceStart (number): 
			NumberOfGracefulRestarts (number): 
			OurIp (str): 
			RecoveryTimeInterval (number): 
			RefreshReduction (bool): 
			RestartTimeInterval (number): 
			SummaryRefreshInterval (number): 
			TrafficGroupId (str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficGroup)): 

		Returns:
			self: This instance with matching neighborPair data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of neighborPair data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the neighborPair data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)

	def RefreshAssignedLabelInfo(self):
		"""Executes the refreshAssignedLabelInfo operation on the server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=neighborPair)): The method internally sets Arg1 to the current href for this instance

		Returns:
			bool: 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('RefreshAssignedLabelInfo', payload=locals(), response_object=None)

	def RefreshReceivedLabelInfo(self):
		"""Executes the refreshReceivedLabelInfo operation on the server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=neighborPair)): The method internally sets Arg1 to the current href for this instance

		Returns:
			bool: 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('RefreshReceivedLabelInfo', payload=locals(), response_object=None)

	def RestartNeighbor(self):
		"""Executes the restartNeighbor operation on the server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=neighborPair)): The method internally sets Arg1 to the current href for this instance

		Returns:
			bool: 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('RestartNeighbor', payload=locals(), response_object=None)
