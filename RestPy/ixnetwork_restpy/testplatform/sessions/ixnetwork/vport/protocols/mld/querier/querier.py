
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


class Querier(Base):
	"""The Querier class encapsulates a user managed querier node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Querier property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'querier'

	def __init__(self, parent):
		super(Querier, self).__init__(parent)

	@property
	def LearnedGroupInfo(self):
		"""An instance of the LearnedGroupInfo class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.mld.querier.learnedgroupinfo.learnedgroupinfo.LearnedGroupInfo)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.mld.querier.learnedgroupinfo.learnedgroupinfo import LearnedGroupInfo
		return LearnedGroupInfo(self)

	@property
	def DiscardLearnedInfo(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('discardLearnedInfo')
	@DiscardLearnedInfo.setter
	def DiscardLearnedInfo(self, value):
		self._set_attribute('discardLearnedInfo', value)

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
	def GeneralQueryInterval(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('generalQueryInterval')
	@GeneralQueryInterval.setter
	def GeneralQueryInterval(self, value):
		self._set_attribute('generalQueryInterval', value)

	@property
	def GqResponseInterval(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('gqResponseInterval')
	@GqResponseInterval.setter
	def GqResponseInterval(self, value):
		self._set_attribute('gqResponseInterval', value)

	@property
	def InterfaceId(self):
		"""

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface)
		"""
		return self._get_attribute('interfaceId')
	@InterfaceId.setter
	def InterfaceId(self, value):
		self._set_attribute('interfaceId', value)

	@property
	def InterfaceIndex(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('interfaceIndex')
	@InterfaceIndex.setter
	def InterfaceIndex(self, value):
		self._set_attribute('interfaceIndex', value)

	@property
	def InterfaceType(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('interfaceType')
	@InterfaceType.setter
	def InterfaceType(self, value):
		self._set_attribute('interfaceType', value)

	@property
	def Interfaces(self):
		"""

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range)
		"""
		return self._get_attribute('interfaces')
	@Interfaces.setter
	def Interfaces(self, value):
		self._set_attribute('interfaces', value)

	@property
	def IsQuerier(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('isQuerier')

	@property
	def IsRefreshComplete(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('isRefreshComplete')

	@property
	def QuerierAddress(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('querierAddress')

	@property
	def QuerierWorkingVersion(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('querierWorkingVersion')

	@property
	def RobustnessVariable(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('robustnessVariable')
	@RobustnessVariable.setter
	def RobustnessVariable(self, value):
		self._set_attribute('robustnessVariable', value)

	@property
	def RouterAlert(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('routerAlert')
	@RouterAlert.setter
	def RouterAlert(self, value):
		self._set_attribute('routerAlert', value)

	@property
	def SqResponseInterval(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('sqResponseInterval')
	@SqResponseInterval.setter
	def SqResponseInterval(self, value):
		self._set_attribute('sqResponseInterval', value)

	@property
	def SqTransmissionCount(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('sqTransmissionCount')
	@SqTransmissionCount.setter
	def SqTransmissionCount(self, value):
		self._set_attribute('sqTransmissionCount', value)

	@property
	def StartupQueryCount(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('startupQueryCount')
	@StartupQueryCount.setter
	def StartupQueryCount(self, value):
		self._set_attribute('startupQueryCount', value)

	@property
	def SupportElection(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('supportElection')
	@SupportElection.setter
	def SupportElection(self, value):
		self._set_attribute('supportElection', value)

	@property
	def SupportOlderVersionHost(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('supportOlderVersionHost')
	@SupportOlderVersionHost.setter
	def SupportOlderVersionHost(self, value):
		self._set_attribute('supportOlderVersionHost', value)

	@property
	def SupportOlderVersionQuerier(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('supportOlderVersionQuerier')
	@SupportOlderVersionQuerier.setter
	def SupportOlderVersionQuerier(self, value):
		self._set_attribute('supportOlderVersionQuerier', value)

	@property
	def Version(self):
		"""

		Returns:
			str(version1|version2)
		"""
		return self._get_attribute('version')
	@Version.setter
	def Version(self, value):
		self._set_attribute('version', value)

	def add(self, DiscardLearnedInfo=None, Enabled=None, GeneralQueryInterval=None, GqResponseInterval=None, InterfaceId=None, InterfaceIndex=None, InterfaceType=None, Interfaces=None, RobustnessVariable=None, RouterAlert=None, SqResponseInterval=None, SqTransmissionCount=None, StartupQueryCount=None, SupportElection=None, SupportOlderVersionHost=None, SupportOlderVersionQuerier=None, Version=None):
		"""Adds a new querier node on the server and retrieves it in this instance.

		Args:
			DiscardLearnedInfo (bool): 
			Enabled (bool): 
			GeneralQueryInterval (number): 
			GqResponseInterval (number): 
			InterfaceId (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface)): 
			InterfaceIndex (number): 
			InterfaceType (str): 
			Interfaces (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range)): 
			RobustnessVariable (number): 
			RouterAlert (bool): 
			SqResponseInterval (number): 
			SqTransmissionCount (number): 
			StartupQueryCount (number): 
			SupportElection (bool): 
			SupportOlderVersionHost (bool): 
			SupportOlderVersionQuerier (bool): 
			Version (str(version1|version2)): 

		Returns:
			self: This instance with all currently retrieved querier data using find and the newly added querier data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the querier data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, DiscardLearnedInfo=None, Enabled=None, GeneralQueryInterval=None, GqResponseInterval=None, InterfaceId=None, InterfaceIndex=None, InterfaceType=None, Interfaces=None, IsQuerier=None, IsRefreshComplete=None, QuerierAddress=None, QuerierWorkingVersion=None, RobustnessVariable=None, RouterAlert=None, SqResponseInterval=None, SqTransmissionCount=None, StartupQueryCount=None, SupportElection=None, SupportOlderVersionHost=None, SupportOlderVersionQuerier=None, Version=None):
		"""Finds and retrieves querier data from the server.

		All named parameters support regex and can be used to selectively retrieve querier data from the server.
		By default the find method takes no parameters and will retrieve all querier data from the server.

		Args:
			DiscardLearnedInfo (bool): 
			Enabled (bool): 
			GeneralQueryInterval (number): 
			GqResponseInterval (number): 
			InterfaceId (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface)): 
			InterfaceIndex (number): 
			InterfaceType (str): 
			Interfaces (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range)): 
			IsQuerier (bool): 
			IsRefreshComplete (bool): 
			QuerierAddress (str): 
			QuerierWorkingVersion (number): 
			RobustnessVariable (number): 
			RouterAlert (bool): 
			SqResponseInterval (number): 
			SqTransmissionCount (number): 
			StartupQueryCount (number): 
			SupportElection (bool): 
			SupportOlderVersionHost (bool): 
			SupportOlderVersionQuerier (bool): 
			Version (str(version1|version2)): 

		Returns:
			self: This instance with matching querier data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of querier data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the querier data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)

	def GetInterfaceAccessorIfaceList(self):
		"""Executes the getInterfaceAccessorIfaceList operation on the server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=querier)): The method internally sets Arg1 to the current href for this instance

		Returns:
			str: 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('GetInterfaceAccessorIfaceList', payload=locals(), response_object=None)

	def RefreshLearnedInfo(self):
		"""Executes the refreshLearnedInfo operation on the server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=querier)): The method internally sets Arg1 to the current href for this instance

		Returns:
			bool: 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('RefreshLearnedInfo', payload=locals(), response_object=None)
