
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


class L2Site(Base):
	"""The L2Site class encapsulates a user managed l2Site node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the L2Site property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'l2Site'

	def __init__(self, parent):
		super(L2Site, self).__init__(parent)

	@property
	def Cluster(self):
		"""An instance of the Cluster class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.cluster.Cluster)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.cluster import Cluster
		return Cluster(self)._select()

	@property
	def LabelBlock(self):
		"""An instance of the LabelBlock class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.labelblock.LabelBlock)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.labelblock import LabelBlock
		return LabelBlock(self)

	@property
	def LearnedRoute(self):
		"""An instance of the LearnedRoute class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.learnedroute.LearnedRoute)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.learnedroute import LearnedRoute
		return LearnedRoute(self)

	@property
	def MacAddressRange(self):
		"""An instance of the MacAddressRange class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.macaddressrange.MacAddressRange)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.macaddressrange import MacAddressRange
		return MacAddressRange(self)

	@property
	def DistinguishAssignedIncrement(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('distinguishAssignedIncrement')
	@DistinguishAssignedIncrement.setter
	def DistinguishAssignedIncrement(self, value):
		self._set_attribute('distinguishAssignedIncrement', value)

	@property
	def DistinguishIpIncrement(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('distinguishIpIncrement')
	@DistinguishIpIncrement.setter
	def DistinguishIpIncrement(self, value):
		self._set_attribute('distinguishIpIncrement', value)

	@property
	def DistinguishNumberIncrementAs(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('distinguishNumberIncrementAs')
	@DistinguishNumberIncrementAs.setter
	def DistinguishNumberIncrementAs(self, value):
		self._set_attribute('distinguishNumberIncrementAs', value)

	@property
	def EnableBfdVccv(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableBfdVccv')
	@EnableBfdVccv.setter
	def EnableBfdVccv(self, value):
		self._set_attribute('enableBfdVccv', value)

	@property
	def EnableCluster(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableCluster')
	@EnableCluster.setter
	def EnableCluster(self, value):
		self._set_attribute('enableCluster', value)

	@property
	def EnableControlWord(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableControlWord')
	@EnableControlWord.setter
	def EnableControlWord(self, value):
		self._set_attribute('enableControlWord', value)

	@property
	def EnableL2SiteAsTrafficEndpoint(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableL2SiteAsTrafficEndpoint')
	@EnableL2SiteAsTrafficEndpoint.setter
	def EnableL2SiteAsTrafficEndpoint(self, value):
		self._set_attribute('enableL2SiteAsTrafficEndpoint', value)

	@property
	def EnableSequenceDelivery(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableSequenceDelivery')
	@EnableSequenceDelivery.setter
	def EnableSequenceDelivery(self, value):
		self._set_attribute('enableSequenceDelivery', value)

	@property
	def EnableVccvPing(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableVccvPing')
	@EnableVccvPing.setter
	def EnableVccvPing(self, value):
		self._set_attribute('enableVccvPing', value)

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
	def IsLearnedInfoRefreshed(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('isLearnedInfoRefreshed')

	@property
	def Mtu(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('mtu')
	@Mtu.setter
	def Mtu(self, value):
		self._set_attribute('mtu', value)

	@property
	def NoOfL2Site(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('noOfL2Site')
	@NoOfL2Site.setter
	def NoOfL2Site(self, value):
		self._set_attribute('noOfL2Site', value)

	@property
	def RouteDistinguisherAs(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('routeDistinguisherAs')
	@RouteDistinguisherAs.setter
	def RouteDistinguisherAs(self, value):
		self._set_attribute('routeDistinguisherAs', value)

	@property
	def RouteDistinguisherAssignedNum(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('routeDistinguisherAssignedNum')
	@RouteDistinguisherAssignedNum.setter
	def RouteDistinguisherAssignedNum(self, value):
		self._set_attribute('routeDistinguisherAssignedNum', value)

	@property
	def RouteDistinguisherIp(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('routeDistinguisherIp')
	@RouteDistinguisherIp.setter
	def RouteDistinguisherIp(self, value):
		self._set_attribute('routeDistinguisherIp', value)

	@property
	def RouteDistinguisherType(self):
		"""

		Returns:
			str(twoOctetAs|ip|fourOctetAs)
		"""
		return self._get_attribute('routeDistinguisherType')
	@RouteDistinguisherType.setter
	def RouteDistinguisherType(self, value):
		self._set_attribute('routeDistinguisherType', value)

	@property
	def RouteTargetAs(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('routeTargetAs')
	@RouteTargetAs.setter
	def RouteTargetAs(self, value):
		self._set_attribute('routeTargetAs', value)

	@property
	def RouteTargetAssignedNum(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('routeTargetAssignedNum')
	@RouteTargetAssignedNum.setter
	def RouteTargetAssignedNum(self, value):
		self._set_attribute('routeTargetAssignedNum', value)

	@property
	def RouteTargetIp(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('routeTargetIp')
	@RouteTargetIp.setter
	def RouteTargetIp(self, value):
		self._set_attribute('routeTargetIp', value)

	@property
	def RouteTargetType(self):
		"""

		Returns:
			str(as|ip)
		"""
		return self._get_attribute('routeTargetType')
	@RouteTargetType.setter
	def RouteTargetType(self, value):
		self._set_attribute('routeTargetType', value)

	@property
	def SiteId(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('siteId')
	@SiteId.setter
	def SiteId(self, value):
		self._set_attribute('siteId', value)

	@property
	def SiteIdIncrement(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('siteIdIncrement')
	@SiteIdIncrement.setter
	def SiteIdIncrement(self, value):
		self._set_attribute('siteIdIncrement', value)

	@property
	def TargetAssignedNumberIncrement(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('targetAssignedNumberIncrement')
	@TargetAssignedNumberIncrement.setter
	def TargetAssignedNumberIncrement(self, value):
		self._set_attribute('targetAssignedNumberIncrement', value)

	@property
	def TargetIncrementAs(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('targetIncrementAs')
	@TargetIncrementAs.setter
	def TargetIncrementAs(self, value):
		self._set_attribute('targetIncrementAs', value)

	@property
	def TargetIpIncrement(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('targetIpIncrement')
	@TargetIpIncrement.setter
	def TargetIpIncrement(self, value):
		self._set_attribute('targetIpIncrement', value)

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

	def add(self, DistinguishAssignedIncrement=None, DistinguishIpIncrement=None, DistinguishNumberIncrementAs=None, EnableBfdVccv=None, EnableCluster=None, EnableControlWord=None, EnableL2SiteAsTrafficEndpoint=None, EnableSequenceDelivery=None, EnableVccvPing=None, Enabled=None, Mtu=None, NoOfL2Site=None, RouteDistinguisherAs=None, RouteDistinguisherAssignedNum=None, RouteDistinguisherIp=None, RouteDistinguisherType=None, RouteTargetAs=None, RouteTargetAssignedNum=None, RouteTargetIp=None, RouteTargetType=None, SiteId=None, SiteIdIncrement=None, TargetAssignedNumberIncrement=None, TargetIncrementAs=None, TargetIpIncrement=None, TrafficGroupId=None):
		"""Adds a new l2Site node on the server and retrieves it in this instance.

		Args:
			DistinguishAssignedIncrement (number): 
			DistinguishIpIncrement (str): 
			DistinguishNumberIncrementAs (number): 
			EnableBfdVccv (bool): 
			EnableCluster (bool): 
			EnableControlWord (bool): 
			EnableL2SiteAsTrafficEndpoint (bool): 
			EnableSequenceDelivery (bool): 
			EnableVccvPing (bool): 
			Enabled (bool): 
			Mtu (number): 
			NoOfL2Site (number): 
			RouteDistinguisherAs (number): 
			RouteDistinguisherAssignedNum (number): 
			RouteDistinguisherIp (str): 
			RouteDistinguisherType (str(twoOctetAs|ip|fourOctetAs)): 
			RouteTargetAs (number): 
			RouteTargetAssignedNum (number): 
			RouteTargetIp (str): 
			RouteTargetType (str(as|ip)): 
			SiteId (number): 
			SiteIdIncrement (number): 
			TargetAssignedNumberIncrement (number): 
			TargetIncrementAs (number): 
			TargetIpIncrement (str): 
			TrafficGroupId (str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficGroup)): 

		Returns:
			self: This instance with all currently retrieved l2Site data using find and the newly added l2Site data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the l2Site data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, DistinguishAssignedIncrement=None, DistinguishIpIncrement=None, DistinguishNumberIncrementAs=None, EnableBfdVccv=None, EnableCluster=None, EnableControlWord=None, EnableL2SiteAsTrafficEndpoint=None, EnableSequenceDelivery=None, EnableVccvPing=None, Enabled=None, IsLearnedInfoRefreshed=None, Mtu=None, NoOfL2Site=None, RouteDistinguisherAs=None, RouteDistinguisherAssignedNum=None, RouteDistinguisherIp=None, RouteDistinguisherType=None, RouteTargetAs=None, RouteTargetAssignedNum=None, RouteTargetIp=None, RouteTargetType=None, SiteId=None, SiteIdIncrement=None, TargetAssignedNumberIncrement=None, TargetIncrementAs=None, TargetIpIncrement=None, TrafficGroupId=None):
		"""Finds and retrieves l2Site data from the server.

		All named parameters support regex and can be used to selectively retrieve l2Site data from the server.
		By default the find method takes no parameters and will retrieve all l2Site data from the server.

		Args:
			DistinguishAssignedIncrement (number): 
			DistinguishIpIncrement (str): 
			DistinguishNumberIncrementAs (number): 
			EnableBfdVccv (bool): 
			EnableCluster (bool): 
			EnableControlWord (bool): 
			EnableL2SiteAsTrafficEndpoint (bool): 
			EnableSequenceDelivery (bool): 
			EnableVccvPing (bool): 
			Enabled (bool): 
			IsLearnedInfoRefreshed (bool): 
			Mtu (number): 
			NoOfL2Site (number): 
			RouteDistinguisherAs (number): 
			RouteDistinguisherAssignedNum (number): 
			RouteDistinguisherIp (str): 
			RouteDistinguisherType (str(twoOctetAs|ip|fourOctetAs)): 
			RouteTargetAs (number): 
			RouteTargetAssignedNum (number): 
			RouteTargetIp (str): 
			RouteTargetType (str(as|ip)): 
			SiteId (number): 
			SiteIdIncrement (number): 
			TargetAssignedNumberIncrement (number): 
			TargetIncrementAs (number): 
			TargetIpIncrement (str): 
			TrafficGroupId (str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficGroup)): 

		Returns:
			self: This instance with matching l2Site data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of l2Site data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the l2Site data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)

	def RefreshLearnedInfo(self):
		"""Executes the refreshLearnedInfo operation on the server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=l2Site)): The method internally sets Arg1 to the current href for this instance

		Returns:
			bool: 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('RefreshLearnedInfo', payload=locals(), response_object=None)
