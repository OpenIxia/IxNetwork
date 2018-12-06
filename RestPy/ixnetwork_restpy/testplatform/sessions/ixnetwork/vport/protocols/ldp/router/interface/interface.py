
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


class Interface(Base):
	"""The Interface class encapsulates a user managed interface node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Interface property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'interface'

	def __init__(self, parent):
		super(Interface, self).__init__(parent)

	@property
	def AtmLabelRange(self):
		"""An instance of the AtmLabelRange class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.ldp.router.interface.atmlabelrange.atmlabelrange.AtmLabelRange)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.ldp.router.interface.atmlabelrange.atmlabelrange import AtmLabelRange
		return AtmLabelRange(self)

	@property
	def LearnedFilter(self):
		"""An instance of the LearnedFilter class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.ldp.router.interface.learnedfilter.learnedfilter.LearnedFilter)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.ldp.router.interface.learnedfilter.learnedfilter import LearnedFilter
		return LearnedFilter(self)._select()

	@property
	def LearnedIpv4Label(self):
		"""An instance of the LearnedIpv4Label class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.ldp.router.interface.learnedipv4label.learnedipv4label.LearnedIpv4Label)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.ldp.router.interface.learnedipv4label.learnedipv4label import LearnedIpv4Label
		return LearnedIpv4Label(self)

	@property
	def LearnedIpv4P2mpLables(self):
		"""An instance of the LearnedIpv4P2mpLables class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.ldp.router.interface.learnedipv4p2mplables.learnedipv4p2mplables.LearnedIpv4P2mpLables)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.ldp.router.interface.learnedipv4p2mplables.learnedipv4p2mplables import LearnedIpv4P2mpLables
		return LearnedIpv4P2mpLables(self)

	@property
	def LearnedMartiniLabel(self):
		"""An instance of the LearnedMartiniLabel class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.ldp.router.interface.learnedmartinilabel.learnedmartinilabel.LearnedMartiniLabel)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.ldp.router.interface.learnedmartinilabel.learnedmartinilabel import LearnedMartiniLabel
		return LearnedMartiniLabel(self)

	@property
	def TargetPeer(self):
		"""An instance of the TargetPeer class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.ldp.router.interface.targetpeer.targetpeer.TargetPeer)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.ldp.router.interface.targetpeer.targetpeer import TargetPeer
		return TargetPeer(self)

	@property
	def AdvertisingMode(self):
		"""

		Returns:
			str(unsolicited|onDemand)
		"""
		return self._get_attribute('advertisingMode')
	@AdvertisingMode.setter
	def AdvertisingMode(self, value):
		self._set_attribute('advertisingMode', value)

	@property
	def AtmVcDirection(self):
		"""

		Returns:
			str(unidirectional|bidirectional)
		"""
		return self._get_attribute('atmVcDirection')
	@AtmVcDirection.setter
	def AtmVcDirection(self, value):
		self._set_attribute('atmVcDirection', value)

	@property
	def Authentication(self):
		"""

		Returns:
			str(null|md5)
		"""
		return self._get_attribute('authentication')
	@Authentication.setter
	def Authentication(self, value):
		self._set_attribute('authentication', value)

	@property
	def BfdOperationMode(self):
		"""

		Returns:
			str(singleHop|multiHop)
		"""
		return self._get_attribute('bfdOperationMode')
	@BfdOperationMode.setter
	def BfdOperationMode(self, value):
		self._set_attribute('bfdOperationMode', value)

	@property
	def DiscoveryMode(self):
		"""

		Returns:
			str(basic|extended|extendedMartini)
		"""
		return self._get_attribute('discoveryMode')
	@DiscoveryMode.setter
	def DiscoveryMode(self, value):
		self._set_attribute('discoveryMode', value)

	@property
	def EnableAtmSession(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableAtmSession')
	@EnableAtmSession.setter
	def EnableAtmSession(self, value):
		self._set_attribute('enableAtmSession', value)

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
	def IsLdpLearnedInfoRefreshed(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('isLdpLearnedInfoRefreshed')

	@property
	def LabelSpaceId(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('labelSpaceId')
	@LabelSpaceId.setter
	def LabelSpaceId(self, value):
		self._set_attribute('labelSpaceId', value)

	@property
	def Md5Key(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('md5Key')
	@Md5Key.setter
	def Md5Key(self, value):
		self._set_attribute('md5Key', value)

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

	def add(self, AdvertisingMode=None, AtmVcDirection=None, Authentication=None, BfdOperationMode=None, DiscoveryMode=None, EnableAtmSession=None, EnableBfdRegistration=None, Enabled=None, LabelSpaceId=None, Md5Key=None, ProtocolInterface=None):
		"""Adds a new interface node on the server and retrieves it in this instance.

		Args:
			AdvertisingMode (str(unsolicited|onDemand)): 
			AtmVcDirection (str(unidirectional|bidirectional)): 
			Authentication (str(null|md5)): 
			BfdOperationMode (str(singleHop|multiHop)): 
			DiscoveryMode (str(basic|extended|extendedMartini)): 
			EnableAtmSession (bool): 
			EnableBfdRegistration (bool): 
			Enabled (bool): 
			LabelSpaceId (number): 
			Md5Key (str): 
			ProtocolInterface (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface)): 

		Returns:
			self: This instance with all currently retrieved interface data using find and the newly added interface data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the interface data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, AdvertisingMode=None, AtmVcDirection=None, Authentication=None, BfdOperationMode=None, DiscoveryMode=None, EnableAtmSession=None, EnableBfdRegistration=None, Enabled=None, IsLdpLearnedInfoRefreshed=None, LabelSpaceId=None, Md5Key=None, ProtocolInterface=None):
		"""Finds and retrieves interface data from the server.

		All named parameters support regex and can be used to selectively retrieve interface data from the server.
		By default the find method takes no parameters and will retrieve all interface data from the server.

		Args:
			AdvertisingMode (str(unsolicited|onDemand)): 
			AtmVcDirection (str(unidirectional|bidirectional)): 
			Authentication (str(null|md5)): 
			BfdOperationMode (str(singleHop|multiHop)): 
			DiscoveryMode (str(basic|extended|extendedMartini)): 
			EnableAtmSession (bool): 
			EnableBfdRegistration (bool): 
			Enabled (bool): 
			IsLdpLearnedInfoRefreshed (bool): 
			LabelSpaceId (number): 
			Md5Key (str): 
			ProtocolInterface (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface)): 

		Returns:
			self: This instance with matching interface data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of interface data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the interface data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)

	def RefreshLearnedInfo(self):
		"""Executes the refreshLearnedInfo operation on the server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface)): The method internally sets Arg1 to the current href for this instance

		Returns:
			bool: 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('RefreshLearnedInfo', payload=locals(), response_object=None)
