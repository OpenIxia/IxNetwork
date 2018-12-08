
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


class EthernetSegments(Base):
	"""The EthernetSegments class encapsulates a user managed ethernetSegments node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the EthernetSegments property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'ethernetSegments'

	def __init__(self, parent):
		super(EthernetSegments, self).__init__(parent)

	@property
	def AdBmacEsRouteAttributes(self):
		"""An instance of the AdBmacEsRouteAttributes class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.adbmacesrouteattributes.AdBmacEsRouteAttributes)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.adbmacesrouteattributes import AdBmacEsRouteAttributes
		return AdBmacEsRouteAttributes(self)._select()

	@property
	def BMacMappedIp(self):
		"""An instance of the BMacMappedIp class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.bmacmappedip.BMacMappedIp)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.bmacmappedip import BMacMappedIp
		return BMacMappedIp(self)

	@property
	def Evi(self):
		"""An instance of the Evi class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.evi.Evi)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.evi import Evi
		return Evi(self)

	@property
	def AutoConfigureEsImport(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('autoConfigureEsImport')
	@AutoConfigureEsImport.setter
	def AutoConfigureEsImport(self, value):
		self._set_attribute('autoConfigureEsImport', value)

	@property
	def BMacPrefix(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('bMacPrefix')
	@BMacPrefix.setter
	def BMacPrefix(self, value):
		self._set_attribute('bMacPrefix', value)

	@property
	def BMacPrefixLength(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('bMacPrefixLength')
	@BMacPrefixLength.setter
	def BMacPrefixLength(self, value):
		self._set_attribute('bMacPrefixLength', value)

	@property
	def DfElectionMethod(self):
		"""

		Returns:
			str(serviceCarving)
		"""
		return self._get_attribute('dfElectionMethod')
	@DfElectionMethod.setter
	def DfElectionMethod(self, value):
		self._set_attribute('dfElectionMethod', value)

	@property
	def DfElectionTimer(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('dfElectionTimer')
	@DfElectionTimer.setter
	def DfElectionTimer(self, value):
		self._set_attribute('dfElectionTimer', value)

	@property
	def EnableActiveStandby(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableActiveStandby')
	@EnableActiveStandby.setter
	def EnableActiveStandby(self, value):
		self._set_attribute('enableActiveStandby', value)

	@property
	def EnableRootLeaf(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableRootLeaf')
	@EnableRootLeaf.setter
	def EnableRootLeaf(self, value):
		self._set_attribute('enableRootLeaf', value)

	@property
	def EnableSecondLabel(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableSecondLabel')
	@EnableSecondLabel.setter
	def EnableSecondLabel(self, value):
		self._set_attribute('enableSecondLabel', value)

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
	def EsImport(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('esImport')
	@EsImport.setter
	def EsImport(self, value):
		self._set_attribute('esImport', value)

	@property
	def Esi(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('esi')
	@Esi.setter
	def Esi(self, value):
		self._set_attribute('esi', value)

	@property
	def EsiLabel(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('esiLabel')
	@EsiLabel.setter
	def EsiLabel(self, value):
		self._set_attribute('esiLabel', value)

	@property
	def FirstLabel(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('firstLabel')
	@FirstLabel.setter
	def FirstLabel(self, value):
		self._set_attribute('firstLabel', value)

	@property
	def IncludeMacMobilityExtendedCommunity(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('includeMacMobilityExtendedCommunity')
	@IncludeMacMobilityExtendedCommunity.setter
	def IncludeMacMobilityExtendedCommunity(self, value):
		self._set_attribute('includeMacMobilityExtendedCommunity', value)

	@property
	def SecondLabel(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('secondLabel')
	@SecondLabel.setter
	def SecondLabel(self, value):
		self._set_attribute('secondLabel', value)

	@property
	def SupportFastConvergence(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('supportFastConvergence')
	@SupportFastConvergence.setter
	def SupportFastConvergence(self, value):
		self._set_attribute('supportFastConvergence', value)

	@property
	def SupportMultiHomedEsAutoDiscovery(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('supportMultiHomedEsAutoDiscovery')
	@SupportMultiHomedEsAutoDiscovery.setter
	def SupportMultiHomedEsAutoDiscovery(self, value):
		self._set_attribute('supportMultiHomedEsAutoDiscovery', value)

	@property
	def TypeOfEthernetVpn(self):
		"""

		Returns:
			str(evpn|pbbEvpn)
		"""
		return self._get_attribute('typeOfEthernetVpn')
	@TypeOfEthernetVpn.setter
	def TypeOfEthernetVpn(self, value):
		self._set_attribute('typeOfEthernetVpn', value)

	@property
	def UseSameSequenceNumber(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('useSameSequenceNumber')
	@UseSameSequenceNumber.setter
	def UseSameSequenceNumber(self, value):
		self._set_attribute('useSameSequenceNumber', value)

	def add(self, AutoConfigureEsImport=None, BMacPrefix=None, BMacPrefixLength=None, DfElectionMethod=None, DfElectionTimer=None, EnableActiveStandby=None, EnableRootLeaf=None, EnableSecondLabel=None, Enabled=None, EsImport=None, Esi=None, EsiLabel=None, FirstLabel=None, IncludeMacMobilityExtendedCommunity=None, SecondLabel=None, SupportFastConvergence=None, SupportMultiHomedEsAutoDiscovery=None, TypeOfEthernetVpn=None, UseSameSequenceNumber=None):
		"""Adds a new ethernetSegments node on the server and retrieves it in this instance.

		Args:
			AutoConfigureEsImport (bool): 
			BMacPrefix (str): 
			BMacPrefixLength (number): 
			DfElectionMethod (str(serviceCarving)): 
			DfElectionTimer (number): 
			EnableActiveStandby (bool): 
			EnableRootLeaf (bool): 
			EnableSecondLabel (bool): 
			Enabled (bool): 
			EsImport (str): 
			Esi (str): 
			EsiLabel (number): 
			FirstLabel (number): 
			IncludeMacMobilityExtendedCommunity (bool): 
			SecondLabel (number): 
			SupportFastConvergence (bool): 
			SupportMultiHomedEsAutoDiscovery (bool): 
			TypeOfEthernetVpn (str(evpn|pbbEvpn)): 
			UseSameSequenceNumber (bool): 

		Returns:
			self: This instance with all currently retrieved ethernetSegments data using find and the newly added ethernetSegments data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the ethernetSegments data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, AutoConfigureEsImport=None, BMacPrefix=None, BMacPrefixLength=None, DfElectionMethod=None, DfElectionTimer=None, EnableActiveStandby=None, EnableRootLeaf=None, EnableSecondLabel=None, Enabled=None, EsImport=None, Esi=None, EsiLabel=None, FirstLabel=None, IncludeMacMobilityExtendedCommunity=None, SecondLabel=None, SupportFastConvergence=None, SupportMultiHomedEsAutoDiscovery=None, TypeOfEthernetVpn=None, UseSameSequenceNumber=None):
		"""Finds and retrieves ethernetSegments data from the server.

		All named parameters support regex and can be used to selectively retrieve ethernetSegments data from the server.
		By default the find method takes no parameters and will retrieve all ethernetSegments data from the server.

		Args:
			AutoConfigureEsImport (bool): 
			BMacPrefix (str): 
			BMacPrefixLength (number): 
			DfElectionMethod (str(serviceCarving)): 
			DfElectionTimer (number): 
			EnableActiveStandby (bool): 
			EnableRootLeaf (bool): 
			EnableSecondLabel (bool): 
			Enabled (bool): 
			EsImport (str): 
			Esi (str): 
			EsiLabel (number): 
			FirstLabel (number): 
			IncludeMacMobilityExtendedCommunity (bool): 
			SecondLabel (number): 
			SupportFastConvergence (bool): 
			SupportMultiHomedEsAutoDiscovery (bool): 
			TypeOfEthernetVpn (str(evpn|pbbEvpn)): 
			UseSameSequenceNumber (bool): 

		Returns:
			self: This instance with matching ethernetSegments data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of ethernetSegments data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the ethernetSegments data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)

	def FlushRemoteCmacForwardingTable(self):
		"""Executes the flushRemoteCmacForwardingTable operation on the server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=ethernetSegments)): The method internally sets Arg1 to the current href for this instance

		Returns:
			str: 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('FlushRemoteCmacForwardingTable', payload=locals(), response_object=None)
