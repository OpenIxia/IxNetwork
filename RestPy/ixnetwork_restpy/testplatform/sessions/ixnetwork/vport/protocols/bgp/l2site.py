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
		"""Distinguishes increment of the assigned value

		Returns:
			number
		"""
		return self._get_attribute('distinguishAssignedIncrement')
	@DistinguishAssignedIncrement.setter
	def DistinguishAssignedIncrement(self, value):
		self._set_attribute('distinguishAssignedIncrement', value)

	@property
	def DistinguishIpIncrement(self):
		"""Distinguishes the increment of the IP address

		Returns:
			str
		"""
		return self._get_attribute('distinguishIpIncrement')
	@DistinguishIpIncrement.setter
	def DistinguishIpIncrement(self, value):
		self._set_attribute('distinguishIpIncrement', value)

	@property
	def DistinguishNumberIncrementAs(self):
		"""Signifies the distinguished increment as number

		Returns:
			number
		"""
		return self._get_attribute('distinguishNumberIncrementAs')
	@DistinguishNumberIncrementAs.setter
	def DistinguishNumberIncrementAs(self, value):
		self._set_attribute('distinguishNumberIncrementAs', value)

	@property
	def EnableBfdVccv(self):
		"""If true, enables BFD VCCV

		Returns:
			bool
		"""
		return self._get_attribute('enableBfdVccv')
	@EnableBfdVccv.setter
	def EnableBfdVccv(self, value):
		self._set_attribute('enableBfdVccv', value)

	@property
	def EnableCluster(self):
		"""Enables and controls the use of L2 VPN VPLS.

		Returns:
			bool
		"""
		return self._get_attribute('enableCluster')
	@EnableCluster.setter
	def EnableCluster(self, value):
		self._set_attribute('enableCluster', value)

	@property
	def EnableControlWord(self):
		"""Enables the use of a control word, as part of the extended community information.

		Returns:
			bool
		"""
		return self._get_attribute('enableControlWord')
	@EnableControlWord.setter
	def EnableControlWord(self, value):
		self._set_attribute('enableControlWord', value)

	@property
	def EnableL2SiteAsTrafficEndpoint(self):
		"""If true, enables L2 site as traffic endpoint

		Returns:
			bool
		"""
		return self._get_attribute('enableL2SiteAsTrafficEndpoint')
	@EnableL2SiteAsTrafficEndpoint.setter
	def EnableL2SiteAsTrafficEndpoint(self, value):
		self._set_attribute('enableL2SiteAsTrafficEndpoint', value)

	@property
	def EnableSequenceDelivery(self):
		"""Enables the use of sequenced delivery of frames, as part of the extended community information.

		Returns:
			bool
		"""
		return self._get_attribute('enableSequenceDelivery')
	@EnableSequenceDelivery.setter
	def EnableSequenceDelivery(self, value):
		self._set_attribute('enableSequenceDelivery', value)

	@property
	def EnableVccvPing(self):
		"""If true, enables the VCCV ping

		Returns:
			bool
		"""
		return self._get_attribute('enableVccvPing')
	@EnableVccvPing.setter
	def EnableVccvPing(self, value):
		self._set_attribute('enableVccvPing', value)

	@property
	def Enabled(self):
		"""Enables or disables use of the L2 VPN site.

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def IsLearnedInfoRefreshed(self):
		"""If true, learned information is refreshed.

		Returns:
			bool
		"""
		return self._get_attribute('isLearnedInfoRefreshed')

	@property
	def Mtu(self):
		"""The Maximum Transmission Unit (MTU) allowed on this link, in bytes. The valid range is 0 to 16777215. (default = 1,500 bytes)

		Returns:
			number
		"""
		return self._get_attribute('mtu')
	@Mtu.setter
	def Mtu(self, value):
		self._set_attribute('mtu', value)

	@property
	def NoOfL2Site(self):
		"""Signifies the number of L2 sites

		Returns:
			number
		"""
		return self._get_attribute('noOfL2Site')
	@NoOfL2Site.setter
	def NoOfL2Site(self, value):
		self._set_attribute('noOfL2Site', value)

	@property
	def RouteDistinguisherAs(self):
		"""Available for use only if the route distinguish type is set to AS. The route distinguisher autonomous system (AS) number.

		Returns:
			number
		"""
		return self._get_attribute('routeDistinguisherAs')
	@RouteDistinguisherAs.setter
	def RouteDistinguisherAs(self, value):
		self._set_attribute('routeDistinguisherAs', value)

	@property
	def RouteDistinguisherAssignedNum(self):
		"""The assigned number for use with the distinguisher IP address or AS number, to create the route distinguisher.The default is 0.

		Returns:
			number
		"""
		return self._get_attribute('routeDistinguisherAssignedNum')
	@RouteDistinguisherAssignedNum.setter
	def RouteDistinguisherAssignedNum(self, value):
		self._set_attribute('routeDistinguisherAssignedNum', value)

	@property
	def RouteDistinguisherIp(self):
		"""Available for use only if the route Distinguish Type is set to IP. The route distinguisher IP address. A 4-byte IPv4 address.The default is 0.0.0.0.

		Returns:
			str
		"""
		return self._get_attribute('routeDistinguisherIp')
	@RouteDistinguisherIp.setter
	def RouteDistinguisherIp(self, value):
		self._set_attribute('routeDistinguisherIp', value)

	@property
	def RouteDistinguisherType(self):
		"""Indicates the type of administrator field used in route distinguisher that will be included in the route announcements.

		Returns:
			str(twoOctetAs|ip|fourOctetAs)
		"""
		return self._get_attribute('routeDistinguisherType')
	@RouteDistinguisherType.setter
	def RouteDistinguisherType(self, value):
		self._set_attribute('routeDistinguisherType', value)

	@property
	def RouteTargetAs(self):
		"""Autonomous system (AS) number. A 2-byte AS number, used to create the route target extended community attribute associated with this L2 site.

		Returns:
			number
		"""
		return self._get_attribute('routeTargetAs')
	@RouteTargetAs.setter
	def RouteTargetAs(self, value):
		self._set_attribute('routeTargetAs', value)

	@property
	def RouteTargetAssignedNum(self):
		"""Autonomous system (AS) and assigned number. A 2-byte AS number and a 4-byte assigned number, used to create the route target extended community attribute associated with this L2 site.

		Returns:
			number
		"""
		return self._get_attribute('routeTargetAssignedNum')
	@RouteTargetAssignedNum.setter
	def RouteTargetAssignedNum(self, value):
		self._set_attribute('routeTargetAssignedNum', value)

	@property
	def RouteTargetIp(self):
		"""IP address and assigned number. A 4-byte IPv4 address and a 2-byte assigned number, used to create the route target extended community attribute associated with this L2 site.

		Returns:
			str
		"""
		return self._get_attribute('routeTargetIp')
	@RouteTargetIp.setter
	def RouteTargetIp(self, value):
		self._set_attribute('routeTargetIp', value)

	@property
	def RouteTargetType(self):
		"""The Admin part type is to the type of route target attribute

		Returns:
			str(as|ip)
		"""
		return self._get_attribute('routeTargetType')
	@RouteTargetType.setter
	def RouteTargetType(self, value):
		self._set_attribute('routeTargetType', value)

	@property
	def SiteId(self):
		"""The identifier for the L2 (CE) site. The default is 0.

		Returns:
			number
		"""
		return self._get_attribute('siteId')
	@SiteId.setter
	def SiteId(self, value):
		self._set_attribute('siteId', value)

	@property
	def SiteIdIncrement(self):
		"""Increments the site identifier

		Returns:
			number
		"""
		return self._get_attribute('siteIdIncrement')
	@SiteIdIncrement.setter
	def SiteIdIncrement(self, value):
		self._set_attribute('siteIdIncrement', value)

	@property
	def TargetAssignedNumberIncrement(self):
		"""Signifies increment of the target assigned number

		Returns:
			number
		"""
		return self._get_attribute('targetAssignedNumberIncrement')
	@TargetAssignedNumberIncrement.setter
	def TargetAssignedNumberIncrement(self, value):
		self._set_attribute('targetAssignedNumberIncrement', value)

	@property
	def TargetIncrementAs(self):
		"""Signifies increment as target

		Returns:
			number
		"""
		return self._get_attribute('targetIncrementAs')
	@TargetIncrementAs.setter
	def TargetIncrementAs(self, value):
		self._set_attribute('targetIncrementAs', value)

	@property
	def TargetIpIncrement(self):
		"""Signifies the increment of IP as target

		Returns:
			str
		"""
		return self._get_attribute('targetIpIncrement')
	@TargetIpIncrement.setter
	def TargetIpIncrement(self, value):
		self._set_attribute('targetIpIncrement', value)

	@property
	def TrafficGroupId(self):
		"""Contains the object reference to a traffic group identifier as configured with the trafficGroup object.

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
			DistinguishAssignedIncrement (number): Distinguishes increment of the assigned value
			DistinguishIpIncrement (str): Distinguishes the increment of the IP address
			DistinguishNumberIncrementAs (number): Signifies the distinguished increment as number
			EnableBfdVccv (bool): If true, enables BFD VCCV
			EnableCluster (bool): Enables and controls the use of L2 VPN VPLS.
			EnableControlWord (bool): Enables the use of a control word, as part of the extended community information.
			EnableL2SiteAsTrafficEndpoint (bool): If true, enables L2 site as traffic endpoint
			EnableSequenceDelivery (bool): Enables the use of sequenced delivery of frames, as part of the extended community information.
			EnableVccvPing (bool): If true, enables the VCCV ping
			Enabled (bool): Enables or disables use of the L2 VPN site.
			Mtu (number): The Maximum Transmission Unit (MTU) allowed on this link, in bytes. The valid range is 0 to 16777215. (default = 1,500 bytes)
			NoOfL2Site (number): Signifies the number of L2 sites
			RouteDistinguisherAs (number): Available for use only if the route distinguish type is set to AS. The route distinguisher autonomous system (AS) number.
			RouteDistinguisherAssignedNum (number): The assigned number for use with the distinguisher IP address or AS number, to create the route distinguisher.The default is 0.
			RouteDistinguisherIp (str): Available for use only if the route Distinguish Type is set to IP. The route distinguisher IP address. A 4-byte IPv4 address.The default is 0.0.0.0.
			RouteDistinguisherType (str(twoOctetAs|ip|fourOctetAs)): Indicates the type of administrator field used in route distinguisher that will be included in the route announcements.
			RouteTargetAs (number): Autonomous system (AS) number. A 2-byte AS number, used to create the route target extended community attribute associated with this L2 site.
			RouteTargetAssignedNum (number): Autonomous system (AS) and assigned number. A 2-byte AS number and a 4-byte assigned number, used to create the route target extended community attribute associated with this L2 site.
			RouteTargetIp (str): IP address and assigned number. A 4-byte IPv4 address and a 2-byte assigned number, used to create the route target extended community attribute associated with this L2 site.
			RouteTargetType (str(as|ip)): The Admin part type is to the type of route target attribute
			SiteId (number): The identifier for the L2 (CE) site. The default is 0.
			SiteIdIncrement (number): Increments the site identifier
			TargetAssignedNumberIncrement (number): Signifies increment of the target assigned number
			TargetIncrementAs (number): Signifies increment as target
			TargetIpIncrement (str): Signifies the increment of IP as target
			TrafficGroupId (str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficGroup)): Contains the object reference to a traffic group identifier as configured with the trafficGroup object.

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
			DistinguishAssignedIncrement (number): Distinguishes increment of the assigned value
			DistinguishIpIncrement (str): Distinguishes the increment of the IP address
			DistinguishNumberIncrementAs (number): Signifies the distinguished increment as number
			EnableBfdVccv (bool): If true, enables BFD VCCV
			EnableCluster (bool): Enables and controls the use of L2 VPN VPLS.
			EnableControlWord (bool): Enables the use of a control word, as part of the extended community information.
			EnableL2SiteAsTrafficEndpoint (bool): If true, enables L2 site as traffic endpoint
			EnableSequenceDelivery (bool): Enables the use of sequenced delivery of frames, as part of the extended community information.
			EnableVccvPing (bool): If true, enables the VCCV ping
			Enabled (bool): Enables or disables use of the L2 VPN site.
			IsLearnedInfoRefreshed (bool): If true, learned information is refreshed.
			Mtu (number): The Maximum Transmission Unit (MTU) allowed on this link, in bytes. The valid range is 0 to 16777215. (default = 1,500 bytes)
			NoOfL2Site (number): Signifies the number of L2 sites
			RouteDistinguisherAs (number): Available for use only if the route distinguish type is set to AS. The route distinguisher autonomous system (AS) number.
			RouteDistinguisherAssignedNum (number): The assigned number for use with the distinguisher IP address or AS number, to create the route distinguisher.The default is 0.
			RouteDistinguisherIp (str): Available for use only if the route Distinguish Type is set to IP. The route distinguisher IP address. A 4-byte IPv4 address.The default is 0.0.0.0.
			RouteDistinguisherType (str(twoOctetAs|ip|fourOctetAs)): Indicates the type of administrator field used in route distinguisher that will be included in the route announcements.
			RouteTargetAs (number): Autonomous system (AS) number. A 2-byte AS number, used to create the route target extended community attribute associated with this L2 site.
			RouteTargetAssignedNum (number): Autonomous system (AS) and assigned number. A 2-byte AS number and a 4-byte assigned number, used to create the route target extended community attribute associated with this L2 site.
			RouteTargetIp (str): IP address and assigned number. A 4-byte IPv4 address and a 2-byte assigned number, used to create the route target extended community attribute associated with this L2 site.
			RouteTargetType (str(as|ip)): The Admin part type is to the type of route target attribute
			SiteId (number): The identifier for the L2 (CE) site. The default is 0.
			SiteIdIncrement (number): Increments the site identifier
			TargetAssignedNumberIncrement (number): Signifies increment of the target assigned number
			TargetIncrementAs (number): Signifies increment as target
			TargetIpIncrement (str): Signifies the increment of IP as target
			TrafficGroupId (str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficGroup)): Contains the object reference to a traffic group identifier as configured with the trafficGroup object.

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

		This function argument allows to refreshe the BGP learned information from the DUT.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=l2Site)): The method internally set Arg1 to the current href for this instance

		Returns:
			bool: NOT DEFINED

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('RefreshLearnedInfo', payload=locals(), response_object=None)
