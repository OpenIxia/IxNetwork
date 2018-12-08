
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
	def GroupRange(self):
		"""An instance of the GroupRange class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.mld.host.grouprange.grouprange.GroupRange)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.mld.host.grouprange.grouprange import GroupRange
		return GroupRange(self)

	@property
	def EnableImmediateResp(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableImmediateResp')
	@EnableImmediateResp.setter
	def EnableImmediateResp(self, value):
		self._set_attribute('enableImmediateResp', value)

	@property
	def EnableQueryResMode(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableQueryResMode')
	@EnableQueryResMode.setter
	def EnableQueryResMode(self, value):
		self._set_attribute('enableQueryResMode', value)

	@property
	def EnableRouterAlert(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableRouterAlert')
	@EnableRouterAlert.setter
	def EnableRouterAlert(self, value):
		self._set_attribute('enableRouterAlert', value)

	@property
	def EnableSpecificResMode(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableSpecificResMode')
	@EnableSpecificResMode.setter
	def EnableSpecificResMode(self, value):
		self._set_attribute('enableSpecificResMode', value)

	@property
	def EnableSuppressReport(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableSuppressReport')
	@EnableSuppressReport.setter
	def EnableSuppressReport(self, value):
		self._set_attribute('enableSuppressReport', value)

	@property
	def EnableUnsolicitedResMode(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableUnsolicitedResMode')
	@EnableUnsolicitedResMode.setter
	def EnableUnsolicitedResMode(self, value):
		self._set_attribute('enableUnsolicitedResMode', value)

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
	def ProtocolInterface(self):
		"""

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface)
		"""
		return self._get_attribute('protocolInterface')
	@ProtocolInterface.setter
	def ProtocolInterface(self, value):
		self._set_attribute('protocolInterface', value)

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
	def Version(self):
		"""

		Returns:
			str(version1|version2)
		"""
		return self._get_attribute('version')
	@Version.setter
	def Version(self, value):
		self._set_attribute('version', value)

	def add(self, EnableImmediateResp=None, EnableQueryResMode=None, EnableRouterAlert=None, EnableSpecificResMode=None, EnableSuppressReport=None, EnableUnsolicitedResMode=None, Enabled=None, InterfaceIndex=None, InterfaceType=None, Interfaces=None, ProtocolInterface=None, ReportFreq=None, RobustnessVariable=None, TrafficGroupId=None, Version=None):
		"""Adds a new host node on the server and retrieves it in this instance.

		Args:
			EnableImmediateResp (bool): 
			EnableQueryResMode (bool): 
			EnableRouterAlert (bool): 
			EnableSpecificResMode (bool): 
			EnableSuppressReport (bool): 
			EnableUnsolicitedResMode (bool): 
			Enabled (bool): 
			InterfaceIndex (number): 
			InterfaceType (str): 
			Interfaces (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range)): 
			ProtocolInterface (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface)): 
			ReportFreq (number): 
			RobustnessVariable (number): 
			TrafficGroupId (str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficGroup)): 
			Version (str(version1|version2)): 

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

	def find(self, EnableImmediateResp=None, EnableQueryResMode=None, EnableRouterAlert=None, EnableSpecificResMode=None, EnableSuppressReport=None, EnableUnsolicitedResMode=None, Enabled=None, InterfaceIndex=None, InterfaceType=None, Interfaces=None, ProtocolInterface=None, ReportFreq=None, RobustnessVariable=None, TrafficGroupId=None, Version=None):
		"""Finds and retrieves host data from the server.

		All named parameters support regex and can be used to selectively retrieve host data from the server.
		By default the find method takes no parameters and will retrieve all host data from the server.

		Args:
			EnableImmediateResp (bool): 
			EnableQueryResMode (bool): 
			EnableRouterAlert (bool): 
			EnableSpecificResMode (bool): 
			EnableSuppressReport (bool): 
			EnableUnsolicitedResMode (bool): 
			Enabled (bool): 
			InterfaceIndex (number): 
			InterfaceType (str): 
			Interfaces (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range|/api/v1/sessions/1/ixnetwork/vport?deepchild=range)): 
			ProtocolInterface (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface)): 
			ReportFreq (number): 
			RobustnessVariable (number): 
			TrafficGroupId (str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficGroup)): 
			Version (str(version1|version2)): 

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
