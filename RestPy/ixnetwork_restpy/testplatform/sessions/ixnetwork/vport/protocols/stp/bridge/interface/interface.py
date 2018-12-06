
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
	def LearnedInfo(self):
		"""An instance of the LearnedInfo class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.stp.bridge.interface.learnedinfo.learnedinfo.LearnedInfo)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.stp.bridge.interface.learnedinfo.learnedinfo import LearnedInfo
		return LearnedInfo(self)._select()

	@property
	def AutoPick(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('autoPick')
	@AutoPick.setter
	def AutoPick(self, value):
		self._set_attribute('autoPick', value)

	@property
	def BdpuGap(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('bdpuGap')
	@BdpuGap.setter
	def BdpuGap(self, value):
		self._set_attribute('bdpuGap', value)

	@property
	def Cost(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('cost')
	@Cost.setter
	def Cost(self, value):
		self._set_attribute('cost', value)

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
	def JitterEnabled(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('jitterEnabled')
	@JitterEnabled.setter
	def JitterEnabled(self, value):
		self._set_attribute('jitterEnabled', value)

	@property
	def JitterPercentage(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('jitterPercentage')
	@JitterPercentage.setter
	def JitterPercentage(self, value):
		self._set_attribute('jitterPercentage', value)

	@property
	def LinkType(self):
		"""

		Returns:
			str(pointToPoint|shared)
		"""
		return self._get_attribute('linkType')
	@LinkType.setter
	def LinkType(self, value):
		self._set_attribute('linkType', value)

	@property
	def MstiOrVlanId(self):
		"""

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=all|/api/v1/sessions/1/ixnetwork/vport?deepchild=msti|/api/v1/sessions/1/ixnetwork/vport?deepchild=vlan)
		"""
		return self._get_attribute('mstiOrVlanId')
	@MstiOrVlanId.setter
	def MstiOrVlanId(self, value):
		self._set_attribute('mstiOrVlanId', value)

	@property
	def PortNo(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('portNo')
	@PortNo.setter
	def PortNo(self, value):
		self._set_attribute('portNo', value)

	@property
	def Pvid(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('pvid')
	@Pvid.setter
	def Pvid(self, value):
		self._set_attribute('pvid', value)

	def add(self, AutoPick=None, BdpuGap=None, Cost=None, Enabled=None, InterfaceId=None, JitterEnabled=None, JitterPercentage=None, LinkType=None, MstiOrVlanId=None, PortNo=None, Pvid=None):
		"""Adds a new interface node on the server and retrieves it in this instance.

		Args:
			AutoPick (bool): 
			BdpuGap (number): 
			Cost (number): 
			Enabled (bool): 
			InterfaceId (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface)): 
			JitterEnabled (bool): 
			JitterPercentage (number): 
			LinkType (str(pointToPoint|shared)): 
			MstiOrVlanId (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=all|/api/v1/sessions/1/ixnetwork/vport?deepchild=msti|/api/v1/sessions/1/ixnetwork/vport?deepchild=vlan)): 
			PortNo (number): 
			Pvid (number): 

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

	def find(self, AutoPick=None, BdpuGap=None, Cost=None, Enabled=None, InterfaceId=None, JitterEnabled=None, JitterPercentage=None, LinkType=None, MstiOrVlanId=None, PortNo=None, Pvid=None):
		"""Finds and retrieves interface data from the server.

		All named parameters support regex and can be used to selectively retrieve interface data from the server.
		By default the find method takes no parameters and will retrieve all interface data from the server.

		Args:
			AutoPick (bool): 
			BdpuGap (number): 
			Cost (number): 
			Enabled (bool): 
			InterfaceId (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface)): 
			JitterEnabled (bool): 
			JitterPercentage (number): 
			LinkType (str(pointToPoint|shared)): 
			MstiOrVlanId (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=all|/api/v1/sessions/1/ixnetwork/vport?deepchild=msti|/api/v1/sessions/1/ixnetwork/vport?deepchild=vlan)): 
			PortNo (number): 
			Pvid (number): 

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

	def UpdateParameters(self):
		"""Executes the updateParameters operation on the server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=interface)): The method internally sets Arg1 to the current href for this instance

		Returns:
			bool: 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('UpdateParameters', payload=locals(), response_object=None)
