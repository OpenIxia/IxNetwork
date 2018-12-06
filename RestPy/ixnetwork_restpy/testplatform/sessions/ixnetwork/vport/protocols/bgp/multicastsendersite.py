
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


class MulticastSenderSite(Base):
	"""The MulticastSenderSite class encapsulates a user managed multicastSenderSite node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the MulticastSenderSite property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'multicastSenderSite'

	def __init__(self, parent):
		super(MulticastSenderSite, self).__init__(parent)

	@property
	def OpaqueValueElement(self):
		"""An instance of the OpaqueValueElement class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.opaquevalueelement.OpaqueValueElement)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bgp.opaquevalueelement import OpaqueValueElement
		return OpaqueValueElement(self)

	@property
	def AddressFamilyType(self):
		"""

		Returns:
			str(addressFamilyIpv4|addressFamilyIpv6)
		"""
		return self._get_attribute('addressFamilyType')
	@AddressFamilyType.setter
	def AddressFamilyType(self, value):
		self._set_attribute('addressFamilyType', value)

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
	def GroupAddressCount(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('groupAddressCount')
	@GroupAddressCount.setter
	def GroupAddressCount(self, value):
		self._set_attribute('groupAddressCount', value)

	@property
	def GroupMaskWidth(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('groupMaskWidth')
	@GroupMaskWidth.setter
	def GroupMaskWidth(self, value):
		self._set_attribute('groupMaskWidth', value)

	@property
	def IncludeIpv6ExplicitNullLabel(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('includeIpv6ExplicitNullLabel')
	@IncludeIpv6ExplicitNullLabel.setter
	def IncludeIpv6ExplicitNullLabel(self, value):
		self._set_attribute('includeIpv6ExplicitNullLabel', value)

	@property
	def MplsAssignedUpstreamLabel(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('mplsAssignedUpstreamLabel')
	@MplsAssignedUpstreamLabel.setter
	def MplsAssignedUpstreamLabel(self, value):
		self._set_attribute('mplsAssignedUpstreamLabel', value)

	@property
	def MplsAssignedUpstreamLabelStep(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('mplsAssignedUpstreamLabelStep')
	@MplsAssignedUpstreamLabelStep.setter
	def MplsAssignedUpstreamLabelStep(self, value):
		self._set_attribute('mplsAssignedUpstreamLabelStep', value)

	@property
	def SPmsiRsvpP2mpId(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('sPmsiRsvpP2mpId')
	@SPmsiRsvpP2mpId.setter
	def SPmsiRsvpP2mpId(self, value):
		self._set_attribute('sPmsiRsvpP2mpId', value)

	@property
	def SPmsiRsvpP2mpIdAsNumber(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('sPmsiRsvpP2mpIdAsNumber')
	@SPmsiRsvpP2mpIdAsNumber.setter
	def SPmsiRsvpP2mpIdAsNumber(self, value):
		self._set_attribute('sPmsiRsvpP2mpIdAsNumber', value)

	@property
	def SPmsiRsvpP2mpIdStep(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('sPmsiRsvpP2mpIdStep')
	@SPmsiRsvpP2mpIdStep.setter
	def SPmsiRsvpP2mpIdStep(self, value):
		self._set_attribute('sPmsiRsvpP2mpIdStep', value)

	@property
	def SPmsiRsvpTunnelCount(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('sPmsiRsvpTunnelCount')
	@SPmsiRsvpTunnelCount.setter
	def SPmsiRsvpTunnelCount(self, value):
		self._set_attribute('sPmsiRsvpTunnelCount', value)

	@property
	def SPmsiRsvpTunnelId(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('sPmsiRsvpTunnelId')
	@SPmsiRsvpTunnelId.setter
	def SPmsiRsvpTunnelId(self, value):
		self._set_attribute('sPmsiRsvpTunnelId', value)

	@property
	def SPmsiRsvpTunnelIdStep(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('sPmsiRsvpTunnelIdStep')
	@SPmsiRsvpTunnelIdStep.setter
	def SPmsiRsvpTunnelIdStep(self, value):
		self._set_attribute('sPmsiRsvpTunnelIdStep', value)

	@property
	def SPmsiTrafficGroupId(self):
		"""

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficGroup)
		"""
		return self._get_attribute('sPmsiTrafficGroupId')
	@SPmsiTrafficGroupId.setter
	def SPmsiTrafficGroupId(self, value):
		self._set_attribute('sPmsiTrafficGroupId', value)

	@property
	def SPmsiTunnelCount(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('sPmsiTunnelCount')
	@SPmsiTunnelCount.setter
	def SPmsiTunnelCount(self, value):
		self._set_attribute('sPmsiTunnelCount', value)

	@property
	def SendTriggeredSourceActiveAdRoute(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('sendTriggeredSourceActiveAdRoute')
	@SendTriggeredSourceActiveAdRoute.setter
	def SendTriggeredSourceActiveAdRoute(self, value):
		self._set_attribute('sendTriggeredSourceActiveAdRoute', value)

	@property
	def SetLeafInformationRequiredBit(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('setLeafInformationRequiredBit')
	@SetLeafInformationRequiredBit.setter
	def SetLeafInformationRequiredBit(self, value):
		self._set_attribute('setLeafInformationRequiredBit', value)

	@property
	def SourceAddressCount(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('sourceAddressCount')
	@SourceAddressCount.setter
	def SourceAddressCount(self, value):
		self._set_attribute('sourceAddressCount', value)

	@property
	def SourceGroupMapping(self):
		"""

		Returns:
			str(fullyMeshed|oneToOne)
		"""
		return self._get_attribute('sourceGroupMapping')
	@SourceGroupMapping.setter
	def SourceGroupMapping(self, value):
		self._set_attribute('sourceGroupMapping', value)

	@property
	def SourceMaskWidth(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('sourceMaskWidth')
	@SourceMaskWidth.setter
	def SourceMaskWidth(self, value):
		self._set_attribute('sourceMaskWidth', value)

	@property
	def StartGroupAddress(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('startGroupAddress')
	@StartGroupAddress.setter
	def StartGroupAddress(self, value):
		self._set_attribute('startGroupAddress', value)

	@property
	def StartSourceAddress(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('startSourceAddress')
	@StartSourceAddress.setter
	def StartSourceAddress(self, value):
		self._set_attribute('startSourceAddress', value)

	@property
	def TuunelType(self):
		"""

		Returns:
			str()
		"""
		return self._get_attribute('tuunelType')
	@TuunelType.setter
	def TuunelType(self, value):
		self._set_attribute('tuunelType', value)

	@property
	def UseUpstreamAssignedLabel(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('useUpstreamAssignedLabel')
	@UseUpstreamAssignedLabel.setter
	def UseUpstreamAssignedLabel(self, value):
		self._set_attribute('useUpstreamAssignedLabel', value)

	def add(self, AddressFamilyType=None, Enabled=None, GroupAddressCount=None, GroupMaskWidth=None, IncludeIpv6ExplicitNullLabel=None, MplsAssignedUpstreamLabel=None, MplsAssignedUpstreamLabelStep=None, SPmsiRsvpP2mpId=None, SPmsiRsvpP2mpIdAsNumber=None, SPmsiRsvpP2mpIdStep=None, SPmsiRsvpTunnelCount=None, SPmsiRsvpTunnelId=None, SPmsiRsvpTunnelIdStep=None, SPmsiTrafficGroupId=None, SPmsiTunnelCount=None, SendTriggeredSourceActiveAdRoute=None, SetLeafInformationRequiredBit=None, SourceAddressCount=None, SourceGroupMapping=None, SourceMaskWidth=None, StartGroupAddress=None, StartSourceAddress=None, TuunelType=None, UseUpstreamAssignedLabel=None):
		"""Adds a new multicastSenderSite node on the server and retrieves it in this instance.

		Args:
			AddressFamilyType (str(addressFamilyIpv4|addressFamilyIpv6)): 
			Enabled (bool): 
			GroupAddressCount (number): 
			GroupMaskWidth (number): 
			IncludeIpv6ExplicitNullLabel (bool): 
			MplsAssignedUpstreamLabel (number): 
			MplsAssignedUpstreamLabelStep (number): 
			SPmsiRsvpP2mpId (str): 
			SPmsiRsvpP2mpIdAsNumber (number): 
			SPmsiRsvpP2mpIdStep (number): 
			SPmsiRsvpTunnelCount (number): 
			SPmsiRsvpTunnelId (number): 
			SPmsiRsvpTunnelIdStep (number): 
			SPmsiTrafficGroupId (str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficGroup)): 
			SPmsiTunnelCount (number): 
			SendTriggeredSourceActiveAdRoute (bool): 
			SetLeafInformationRequiredBit (bool): 
			SourceAddressCount (number): 
			SourceGroupMapping (str(fullyMeshed|oneToOne)): 
			SourceMaskWidth (number): 
			StartGroupAddress (str): 
			StartSourceAddress (str): 
			TuunelType (str()): 
			UseUpstreamAssignedLabel (bool): 

		Returns:
			self: This instance with all currently retrieved multicastSenderSite data using find and the newly added multicastSenderSite data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the multicastSenderSite data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, AddressFamilyType=None, Enabled=None, GroupAddressCount=None, GroupMaskWidth=None, IncludeIpv6ExplicitNullLabel=None, MplsAssignedUpstreamLabel=None, MplsAssignedUpstreamLabelStep=None, SPmsiRsvpP2mpId=None, SPmsiRsvpP2mpIdAsNumber=None, SPmsiRsvpP2mpIdStep=None, SPmsiRsvpTunnelCount=None, SPmsiRsvpTunnelId=None, SPmsiRsvpTunnelIdStep=None, SPmsiTrafficGroupId=None, SPmsiTunnelCount=None, SendTriggeredSourceActiveAdRoute=None, SetLeafInformationRequiredBit=None, SourceAddressCount=None, SourceGroupMapping=None, SourceMaskWidth=None, StartGroupAddress=None, StartSourceAddress=None, TuunelType=None, UseUpstreamAssignedLabel=None):
		"""Finds and retrieves multicastSenderSite data from the server.

		All named parameters support regex and can be used to selectively retrieve multicastSenderSite data from the server.
		By default the find method takes no parameters and will retrieve all multicastSenderSite data from the server.

		Args:
			AddressFamilyType (str(addressFamilyIpv4|addressFamilyIpv6)): 
			Enabled (bool): 
			GroupAddressCount (number): 
			GroupMaskWidth (number): 
			IncludeIpv6ExplicitNullLabel (bool): 
			MplsAssignedUpstreamLabel (number): 
			MplsAssignedUpstreamLabelStep (number): 
			SPmsiRsvpP2mpId (str): 
			SPmsiRsvpP2mpIdAsNumber (number): 
			SPmsiRsvpP2mpIdStep (number): 
			SPmsiRsvpTunnelCount (number): 
			SPmsiRsvpTunnelId (number): 
			SPmsiRsvpTunnelIdStep (number): 
			SPmsiTrafficGroupId (str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficGroup)): 
			SPmsiTunnelCount (number): 
			SendTriggeredSourceActiveAdRoute (bool): 
			SetLeafInformationRequiredBit (bool): 
			SourceAddressCount (number): 
			SourceGroupMapping (str(fullyMeshed|oneToOne)): 
			SourceMaskWidth (number): 
			StartGroupAddress (str): 
			StartSourceAddress (str): 
			TuunelType (str()): 
			UseUpstreamAssignedLabel (bool): 

		Returns:
			self: This instance with matching multicastSenderSite data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of multicastSenderSite data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the multicastSenderSite data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)

	def SwitchToSpmsi(self):
		"""Executes the switchToSpmsi operation on the server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=multicastSenderSite)): The method internally sets Arg1 to the current href for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('SwitchToSpmsi', payload=locals(), response_object=None)
