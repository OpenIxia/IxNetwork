
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


class OspfRouteProperty(Base):
	"""The OspfRouteProperty class encapsulates a system managed ospfRouteProperty node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the OspfRouteProperty property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'ospfRouteProperty'

	def __init__(self, parent):
		super(OspfRouteProperty, self).__init__(parent)

	@property
	def CMacProperties(self):
		"""An instance of the CMacProperties class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.cmacproperties.CMacProperties)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.cmacproperties import CMacProperties
		return CMacProperties(self)

	@property
	def EvpnIPv4PrefixRange(self):
		"""An instance of the EvpnIPv4PrefixRange class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.evpnipv4prefixrange.EvpnIPv4PrefixRange)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.evpnipv4prefixrange import EvpnIPv4PrefixRange
		return EvpnIPv4PrefixRange(self)

	@property
	def EvpnIPv6PrefixRange(self):
		"""An instance of the EvpnIPv6PrefixRange class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.evpnipv6prefixrange.EvpnIPv6PrefixRange)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.evpnipv6prefixrange import EvpnIPv6PrefixRange
		return EvpnIPv6PrefixRange(self)

	@property
	def BAR(self):
		"""BIER Algorithm

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('BAR')

	@property
	def BFRId(self):
		"""BFR Id

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('BFRId')

	@property
	def BFRIdStep(self):
		"""BFR Id Step

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('BFRIdStep')

	@property
	def BIERBitStringLength(self):
		"""Bit String Length

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('BIERBitStringLength')

	@property
	def Active(self):
		"""Activate/Deactivate Configuration

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('active')

	@property
	def Algorithm(self):
		"""Algorithm

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('algorithm')

	@property
	def AllowPropagate(self):
		"""Allow Propagate

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('allowPropagate')

	@property
	def BierAFlag(self):
		"""Attach Flag

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('bierAFlag')

	@property
	def BierNFlag(self):
		"""Node Flag

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('bierNFlag')

	@property
	def ConfigureSIDIndexLabel(self):
		"""Configure SID/Index/Label

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('configureSIDIndexLabel')

	@property
	def Count(self):
		"""Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group

		Returns:
			number
		"""
		return self._get_attribute('count')

	@property
	def DescriptiveName(self):
		"""Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context

		Returns:
			str
		"""
		return self._get_attribute('descriptiveName')

	@property
	def EFlag(self):
		"""Explicit-Null Flag

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('eFlag')

	@property
	def IncludeBSLObject(self):
		"""If set, MPLS encapsulation sub-sub-Tlv will be advertised under Bier Info Sub-Tlv

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('includeBSLObject')

	@property
	def Ipa(self):
		"""IPA

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('ipa')

	@property
	def LFlag(self):
		"""Local or Global Flag

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('lFlag')

	@property
	def LabelStart(self):
		"""Label Start

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('labelStart')

	@property
	def MFlag(self):
		"""Mapping Server Flag

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('mFlag')

	@property
	def MaxSI(self):
		"""Max SI

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('maxSI')

	@property
	def Metric(self):
		"""Route Metric

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('metric')

	@property
	def MtId(self):
		"""Multi-Topology ID

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('mtId')

	@property
	def Name(self):
		"""Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			str
		"""
		return self._get_attribute('name')
	@Name.setter
	def Name(self, value):
		self._set_attribute('name', value)

	@property
	def NpFlag(self):
		"""No-PHP Flag

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('npFlag')

	@property
	def RouteOrigin(self):
		"""Route Origin

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('routeOrigin')

	@property
	def SidIndexLabel(self):
		"""SID/Index/Label

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('sidIndexLabel')

	@property
	def SubDomainId(self):
		"""Sub Domain Id

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('subDomainId')

	@property
	def VFlag(self):
		"""Value or Index Flag

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('vFlag')

	def find(self, Count=None, DescriptiveName=None, Name=None):
		"""Finds and retrieves ospfRouteProperty data from the server.

		All named parameters support regex and can be used to selectively retrieve ospfRouteProperty data from the server.
		By default the find method takes no parameters and will retrieve all ospfRouteProperty data from the server.

		Args:
			Count (number): Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			self: This instance with matching ospfRouteProperty data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of ospfRouteProperty data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the ospfRouteProperty data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)

	def get_device_ids(self, PortNames=None, BAR=None, BFRId=None, BFRIdStep=None, BIERBitStringLength=None, Active=None, Algorithm=None, AllowPropagate=None, BierAFlag=None, BierNFlag=None, ConfigureSIDIndexLabel=None, EFlag=None, IncludeBSLObject=None, Ipa=None, LFlag=None, LabelStart=None, MFlag=None, MaxSI=None, Metric=None, MtId=None, NpFlag=None, RouteOrigin=None, SidIndexLabel=None, SubDomainId=None, VFlag=None):
		"""Base class infrastructure that gets a list of ospfRouteProperty device ids encapsulated by this object.

		Use the optional regex parameters in the method to refine the list of device ids encapsulated by this object.

		Args:
			PortNames (str): optional regex of port names
			BAR (str): optional regex of BAR
			BFRId (str): optional regex of BFRId
			BFRIdStep (str): optional regex of BFRIdStep
			BIERBitStringLength (str): optional regex of BIERBitStringLength
			Active (str): optional regex of active
			Algorithm (str): optional regex of algorithm
			AllowPropagate (str): optional regex of allowPropagate
			BierAFlag (str): optional regex of bierAFlag
			BierNFlag (str): optional regex of bierNFlag
			ConfigureSIDIndexLabel (str): optional regex of configureSIDIndexLabel
			EFlag (str): optional regex of eFlag
			IncludeBSLObject (str): optional regex of includeBSLObject
			Ipa (str): optional regex of ipa
			LFlag (str): optional regex of lFlag
			LabelStart (str): optional regex of labelStart
			MFlag (str): optional regex of mFlag
			MaxSI (str): optional regex of maxSI
			Metric (str): optional regex of metric
			MtId (str): optional regex of mtId
			NpFlag (str): optional regex of npFlag
			RouteOrigin (str): optional regex of routeOrigin
			SidIndexLabel (str): optional regex of sidIndexLabel
			SubDomainId (str): optional regex of subDomainId
			VFlag (str): optional regex of vFlag

		Returns:
			list(int): A list of device ids that meets the regex criteria provided in the method parameters

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._get_ngpf_device_ids(locals())

	def AgeOutRoutes(self, Percentage):
		"""Executes the ageOutRoutes operation on the server.

		Age out percentage of OSPF Routes in a Route Range

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			Percentage (number): This parameter requires a percentage of type kInteger

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('AgeOutRoutes', payload=locals(), response_object=None)

	def AgeOutRoutes(self, Percentage, SessionIndices):
		"""Executes the ageOutRoutes operation on the server.

		Age out percentage of OSPF Routes in a Route Range

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			Percentage (number): This parameter requires a percentage of type kInteger
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('AgeOutRoutes', payload=locals(), response_object=None)

	def AgeOutRoutes(self, SessionIndices, Percentage):
		"""Executes the ageOutRoutes operation on the server.

		Age out percentage of OSPF Routes in a Route Range

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (str): This parameter requires a percentage of type kInteger
			Percentage (number): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('AgeOutRoutes', payload=locals(), response_object=None)

	def Ageoutroutes(self, Arg2, Arg3):
		"""Executes the ageoutroutes operation on the server.

		Completely/Partially age out routes contained in this route range.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally sets Arg1 to the current href for this instance
			Arg2 (list(number)): List of indices into the group. An empty list indicates all instances in the group.
			Arg3 (number): What percentage of routes to age out. 100% means all routes.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('Ageoutroutes', payload=locals(), response_object=None)

	def ReadvertiseRoutes(self):
		"""Executes the readvertiseRoutes operation on the server.

		Re-advertise Aged out OSPF Routes in a Route Range

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('ReadvertiseRoutes', payload=locals(), response_object=None)

	def ReadvertiseRoutes(self, SessionIndices):
		"""Executes the readvertiseRoutes operation on the server.

		Re-advertise Aged out OSPF Routes in a Route Range

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('ReadvertiseRoutes', payload=locals(), response_object=None)

	def ReadvertiseRoutes(self, SessionIndices):
		"""Executes the readvertiseRoutes operation on the server.

		Re-advertise Aged out OSPF Routes in a Route Range

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('ReadvertiseRoutes', payload=locals(), response_object=None)

	def Readvertiseroutes(self, Arg2):
		"""Executes the readvertiseroutes operation on the server.

		Readvertise only the aged-out routes contained in this route range.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally sets Arg1 to the current href for this instance
			Arg2 (list(number)): List of indices into the group. An empty list indicates all instances in the group.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('Readvertiseroutes', payload=locals(), response_object=None)

	def Start(self):
		"""Executes the start operation on the server.

		Start OSPF Route Range

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('Start', payload=locals(), response_object=None)

	def Start(self, SessionIndices):
		"""Executes the start operation on the server.

		Start OSPF Route Range

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('Start', payload=locals(), response_object=None)

	def Start(self, SessionIndices):
		"""Executes the start operation on the server.

		Start OSPF Route Range

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('Start', payload=locals(), response_object=None)

	def Stop(self):
		"""Executes the stop operation on the server.

		Stop OSPF Route Range

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('Stop', payload=locals(), response_object=None)

	def Stop(self, SessionIndices):
		"""Executes the stop operation on the server.

		Stop OSPF Route Range

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('Stop', payload=locals(), response_object=None)

	def Stop(self, SessionIndices):
		"""Executes the stop operation on the server.

		Stop OSPF Route Range

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('Stop', payload=locals(), response_object=None)
