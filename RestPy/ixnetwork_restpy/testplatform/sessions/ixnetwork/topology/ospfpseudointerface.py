
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


class OspfPseudoInterface(Base):
	"""The OspfPseudoInterface class encapsulates a system managed ospfPseudoInterface node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the OspfPseudoInterface property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'ospfPseudoInterface'

	def __init__(self, parent):
		super(OspfPseudoInterface, self).__init__(parent)

	@property
	def SrlgValueList(self):
		"""An instance of the SrlgValueList class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.srlgvaluelist.SrlgValueList)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.srlgvaluelist import SrlgValueList
		return SrlgValueList(self)

	@property
	def AdjSID(self):
		"""Adjacency SID

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('adjSID')

	@property
	def AdministratorGroup(self):
		"""Administrator Group

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('administratorGroup')

	@property
	def BFlag(self):
		"""Backup Flag

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('bFlag')

	@property
	def BandwidthPriority0(self):
		"""Bandwidth for Priority 0 (B/sec)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('bandwidthPriority0')

	@property
	def BandwidthPriority1(self):
		"""Bandwidth for Priority 1 (B/sec)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('bandwidthPriority1')

	@property
	def BandwidthPriority2(self):
		"""Bandwidth for Priority 2 (B/sec)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('bandwidthPriority2')

	@property
	def BandwidthPriority3(self):
		"""Bandwidth for Priority 3 (B/sec)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('bandwidthPriority3')

	@property
	def BandwidthPriority4(self):
		"""Bandwidth for Priority 4 (B/sec)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('bandwidthPriority4')

	@property
	def BandwidthPriority5(self):
		"""Bandwidth for Priority 5 (B/sec)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('bandwidthPriority5')

	@property
	def BandwidthPriority6(self):
		"""Bandwidth for Priority 6 (B/sec)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('bandwidthPriority6')

	@property
	def BandwidthPriority7(self):
		"""Bandwidth for Priority 7 (B/sec)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('bandwidthPriority7')

	@property
	def Count(self):
		"""Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group

		Returns:
			number
		"""
		return self._get_attribute('count')

	@property
	def Dedicated1Plus1(self):
		"""This is a Protection Scheme with value 0x10. It means that a dedicated disjoint link is protecting this link. However, the protecting link is not advertised in the link state database and is therefore not available for the routing of LSPs.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('dedicated1Plus1')

	@property
	def Dedicated1To1(self):
		"""This is a Protection Scheme with value 0x08. It means that there is one dedicated disjoint link of type Extra Traffic that is protecting this link.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('dedicated1To1')

	@property
	def DescriptiveName(self):
		"""Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context

		Returns:
			str
		"""
		return self._get_attribute('descriptiveName')

	@property
	def EnLinkProtection(self):
		"""This enables the link protection on the OSPF link between two mentioned interfaces.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enLinkProtection')

	@property
	def Enable(self):
		"""TEEnabled

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enable')

	@property
	def EnableAdjSID(self):
		"""Enable Adj SID

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableAdjSID')

	@property
	def EnableSRLG(self):
		"""This enables the SRLG on the OSPF link between two mentioned interfaces.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableSRLG')

	@property
	def Enhanced(self):
		"""This is a Protection Scheme with value 0x20. It means that a protection scheme that is more reliable than Dedicated 1+1, e.g., 4 fiber BLSR/MS-SPRING, is being used to protect this link.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enhanced')

	@property
	def ExtraTraffic(self):
		"""This is a Protection Scheme with value 0x01. It means that the link is protecting another link or links. The LSPs on a link of this type will be lost if any of the links it is protecting fail.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('extraTraffic')

	@property
	def LFlag(self):
		"""Local/Global Flag

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('lFlag')

	@property
	def MaxBandwidth(self):
		"""Maximum Bandwidth (B/sec)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('maxBandwidth')

	@property
	def MaxReservableBandwidth(self):
		"""Maximum Reservable Bandwidth (B/sec)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('maxReservableBandwidth')

	@property
	def Metric(self):
		"""Link Metric

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('metric')

	@property
	def MetricLevel(self):
		"""TE Metric Level

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('metricLevel')

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
	def Reserved40(self):
		"""This is a Protection Scheme with value 0x40.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('reserved40')

	@property
	def Reserved80(self):
		"""This is a Protection Scheme with value 0x80.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('reserved80')

	@property
	def SFlag(self):
		"""Set Flag

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('sFlag')

	@property
	def Shared(self):
		"""This is a Protection Scheme with value 0x04. It means that there are one or more disjoint links of type Extra Traffic that are protecting this link. These Extra Traffic links are shared between one or more links of type Shared.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('shared')

	@property
	def SrlgCount(self):
		"""This field value shows how many SRLG Value columns would be there in the GUI.

		Returns:
			number
		"""
		return self._get_attribute('srlgCount')
	@SrlgCount.setter
	def SrlgCount(self, value):
		self._set_attribute('srlgCount', value)

	@property
	def Unprotected(self):
		"""This is a Protection Scheme with value 0x02. It means that there is no other link protecting this link. The LSPs on a link of this type will be lost if the link fails.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('unprotected')

	@property
	def VFlag(self):
		"""Value/Index Flag

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('vFlag')

	@property
	def Weight(self):
		"""Weight

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('weight')

	def find(self, Count=None, DescriptiveName=None, Name=None, SrlgCount=None):
		"""Finds and retrieves ospfPseudoInterface data from the server.

		All named parameters support regex and can be used to selectively retrieve ospfPseudoInterface data from the server.
		By default the find method takes no parameters and will retrieve all ospfPseudoInterface data from the server.

		Args:
			Count (number): Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario
			SrlgCount (number): This field value shows how many SRLG Value columns would be there in the GUI.

		Returns:
			self: This instance with matching ospfPseudoInterface data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of ospfPseudoInterface data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the ospfPseudoInterface data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)

	def get_device_ids(self, PortNames=None, AdjSID=None, AdministratorGroup=None, BFlag=None, BandwidthPriority0=None, BandwidthPriority1=None, BandwidthPriority2=None, BandwidthPriority3=None, BandwidthPriority4=None, BandwidthPriority5=None, BandwidthPriority6=None, BandwidthPriority7=None, Dedicated1Plus1=None, Dedicated1To1=None, EnLinkProtection=None, Enable=None, EnableAdjSID=None, EnableSRLG=None, Enhanced=None, ExtraTraffic=None, LFlag=None, MaxBandwidth=None, MaxReservableBandwidth=None, Metric=None, MetricLevel=None, Reserved40=None, Reserved80=None, SFlag=None, Shared=None, Unprotected=None, VFlag=None, Weight=None):
		"""Base class infrastructure that gets a list of ospfPseudoInterface device ids encapsulated by this object.

		Use the optional regex parameters in the method to refine the list of device ids encapsulated by this object.

		Args:
			PortNames (str): optional regex of port names
			AdjSID (str): optional regex of adjSID
			AdministratorGroup (str): optional regex of administratorGroup
			BFlag (str): optional regex of bFlag
			BandwidthPriority0 (str): optional regex of bandwidthPriority0
			BandwidthPriority1 (str): optional regex of bandwidthPriority1
			BandwidthPriority2 (str): optional regex of bandwidthPriority2
			BandwidthPriority3 (str): optional regex of bandwidthPriority3
			BandwidthPriority4 (str): optional regex of bandwidthPriority4
			BandwidthPriority5 (str): optional regex of bandwidthPriority5
			BandwidthPriority6 (str): optional regex of bandwidthPriority6
			BandwidthPriority7 (str): optional regex of bandwidthPriority7
			Dedicated1Plus1 (str): optional regex of dedicated1Plus1
			Dedicated1To1 (str): optional regex of dedicated1To1
			EnLinkProtection (str): optional regex of enLinkProtection
			Enable (str): optional regex of enable
			EnableAdjSID (str): optional regex of enableAdjSID
			EnableSRLG (str): optional regex of enableSRLG
			Enhanced (str): optional regex of enhanced
			ExtraTraffic (str): optional regex of extraTraffic
			LFlag (str): optional regex of lFlag
			MaxBandwidth (str): optional regex of maxBandwidth
			MaxReservableBandwidth (str): optional regex of maxReservableBandwidth
			Metric (str): optional regex of metric
			MetricLevel (str): optional regex of metricLevel
			Reserved40 (str): optional regex of reserved40
			Reserved80 (str): optional regex of reserved80
			SFlag (str): optional regex of sFlag
			Shared (str): optional regex of shared
			Unprotected (str): optional regex of unprotected
			VFlag (str): optional regex of vFlag
			Weight (str): optional regex of weight

		Returns:
			list(int): A list of device ids that meets the regex criteria provided in the method parameters

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._get_ngpf_device_ids(locals())

	def Disconnect(self):
		"""Executes the disconnect operation on the server.

		Disconnect Simulated Interface

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('Disconnect', payload=locals(), response_object=None)

	def Disconnect(self, SessionIndices):
		"""Executes the disconnect operation on the server.

		Disconnect Simulated Interface

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('Disconnect', payload=locals(), response_object=None)

	def Disconnect(self, SessionIndices):
		"""Executes the disconnect operation on the server.

		Disconnect Simulated Interface

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('Disconnect', payload=locals(), response_object=None)

	def FetchAndUpdateConfigFromCloud(self, Mode):
		"""Executes the fetchAndUpdateConfigFromCloud operation on the server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/globals?deepchild=*|/api/v1/sessions/1/ixnetwork/topology?deepchild=*)): The method internally sets Arg1 to the current href for this instance
			Mode (str): 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('FetchAndUpdateConfigFromCloud', payload=locals(), response_object=None)

	def Reconnect(self):
		"""Executes the reconnect operation on the server.

		Reconnect Simulated Interface

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('Reconnect', payload=locals(), response_object=None)

	def Reconnect(self, SessionIndices):
		"""Executes the reconnect operation on the server.

		Reconnect Simulated Interface

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('Reconnect', payload=locals(), response_object=None)

	def Reconnect(self, SessionIndices):
		"""Executes the reconnect operation on the server.

		Reconnect Simulated Interface

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('Reconnect', payload=locals(), response_object=None)

	def Start(self):
		"""Executes the start operation on the server.

		Start CPF control plane (equals to promote to negotiated state).

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('Start', payload=locals(), response_object=None)

	def Stop(self):
		"""Executes the stop operation on the server.

		Stop CPF control plane (equals to demote to PreValidated-DoDDone state).

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('Stop', payload=locals(), response_object=None)
