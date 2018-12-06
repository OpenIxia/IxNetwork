
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


class Host(Base):
	"""The Host class encapsulates a user managed host node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Host property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'host'

	def __init__(self, parent):
		super(Host, self).__init__(parent)

	@property
	def Group(self):
		"""An instance of the Group class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.igmp.host.group.group.Group)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.igmp.host.group.group import Group
		return Group(self)

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
	def GqResponseMode(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('gqResponseMode')
	@GqResponseMode.setter
	def GqResponseMode(self, value):
		self._set_attribute('gqResponseMode', value)

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
	def ReportFreq(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('reportFreq')
	@ReportFreq.setter
	def ReportFreq(self, value):
		self._set_attribute('reportFreq', value)

	@property
	def RespToQueryImmediately(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('respToQueryImmediately')
	@RespToQueryImmediately.setter
	def RespToQueryImmediately(self, value):
		self._set_attribute('respToQueryImmediately', value)

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
	def SqResponseMode(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('sqResponseMode')
	@SqResponseMode.setter
	def SqResponseMode(self, value):
		self._set_attribute('sqResponseMode', value)

	@property
	def SuppressReports(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('suppressReports')
	@SuppressReports.setter
	def SuppressReports(self, value):
		self._set_attribute('suppressReports', value)

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

	@property
	def UpResponseMode(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('upResponseMode')
	@UpResponseMode.setter
	def UpResponseMode(self, value):
		self._set_attribute('upResponseMode', value)

	@property
	def Version(self):
		"""

		Returns:
			str(igmpv1|igmpv2|igmpv3)
		"""
		return self._get_attribute('version')
	@Version.setter
	def Version(self, value):
		self._set_attribute('version', value)

	def add(self, Enabled=None, GqResponseMode=None, InterfaceId=None, InterfaceIndex=None, InterfaceType=None, Interfaces=None, ReportFreq=None, RespToQueryImmediately=None, RobustnessVariable=None, RouterAlert=None, SqResponseMode=None, SuppressReports=None, TrafficGroupId=None, UpResponseMode=None, Version=None):
		"""Adds a new host node on the server and retrieves it in this instance.

		Args:
			Enabled (bool): 
			GqResponseMode (bool): 
			InterfaceId (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface)): 
			InterfaceIndex (number): 
			InterfaceType (str): 
			Interfaces (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range)): 
			ReportFreq (number): 
			RespToQueryImmediately (bool): 
			RobustnessVariable (number): 
			RouterAlert (bool): 
			SqResponseMode (bool): 
			SuppressReports (bool): 
			TrafficGroupId (str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficGroup)): 
			UpResponseMode (bool): 
			Version (str(igmpv1|igmpv2|igmpv3)): 

		Returns:
			self: This instance with all currently retrieved host data using find and the newly added host data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the host data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, Enabled=None, GqResponseMode=None, InterfaceId=None, InterfaceIndex=None, InterfaceType=None, Interfaces=None, ReportFreq=None, RespToQueryImmediately=None, RobustnessVariable=None, RouterAlert=None, SqResponseMode=None, SuppressReports=None, TrafficGroupId=None, UpResponseMode=None, Version=None):
		"""Finds and retrieves host data from the server.

		All named parameters support regex and can be used to selectively retrieve host data from the server.
		By default the find method takes no parameters and will retrieve all host data from the server.

		Args:
			Enabled (bool): 
			GqResponseMode (bool): 
			InterfaceId (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface)): 
			InterfaceIndex (number): 
			InterfaceType (str): 
			Interfaces (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range)): 
			ReportFreq (number): 
			RespToQueryImmediately (bool): 
			RobustnessVariable (number): 
			RouterAlert (bool): 
			SqResponseMode (bool): 
			SuppressReports (bool): 
			TrafficGroupId (str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficGroup)): 
			UpResponseMode (bool): 
			Version (str(igmpv1|igmpv2|igmpv3)): 

		Returns:
			self: This instance with matching host data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of host data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the host data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)

	def GetInterfaceAccessorIfaceList(self):
		"""Executes the getInterfaceAccessorIfaceList operation on the server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=host)): The method internally sets Arg1 to the current href for this instance

		Returns:
			str: 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('GetInterfaceAccessorIfaceList', payload=locals(), response_object=None)
