
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


class FlowRangeAction(Base):
	"""The FlowRangeAction class encapsulates a user managed flowRangeAction node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the FlowRangeAction property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'flowRangeAction'

	def __init__(self, parent):
		super(FlowRangeAction, self).__init__(parent)

	@property
	def EthDestination(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('ethDestination')
	@EthDestination.setter
	def EthDestination(self, value):
		self._set_attribute('ethDestination', value)

	@property
	def EthSource(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('ethSource')
	@EthSource.setter
	def EthSource(self, value):
		self._set_attribute('ethSource', value)

	@property
	def IpDscp(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('ipDscp')
	@IpDscp.setter
	def IpDscp(self, value):
		self._set_attribute('ipDscp', value)

	@property
	def Ipv4Destination(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('ipv4Destination')
	@Ipv4Destination.setter
	def Ipv4Destination(self, value):
		self._set_attribute('ipv4Destination', value)

	@property
	def Ipv4Source(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('ipv4Source')
	@Ipv4Source.setter
	def Ipv4Source(self, value):
		self._set_attribute('ipv4Source', value)

	@property
	def MaxByteLength(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('maxByteLength')
	@MaxByteLength.setter
	def MaxByteLength(self, value):
		self._set_attribute('maxByteLength', value)

	@property
	def OutputPort(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('outputPort')
	@OutputPort.setter
	def OutputPort(self, value):
		self._set_attribute('outputPort', value)

	@property
	def QueueId(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('queueId')
	@QueueId.setter
	def QueueId(self, value):
		self._set_attribute('queueId', value)

	@property
	def TransportDestination(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('transportDestination')
	@TransportDestination.setter
	def TransportDestination(self, value):
		self._set_attribute('transportDestination', value)

	@property
	def TransportSource(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('transportSource')
	@TransportSource.setter
	def TransportSource(self, value):
		self._set_attribute('transportSource', value)

	@property
	def TypeOfAction(self):
		"""

		Returns:
			str(none|output|enqueue|setVlanId|setVlanPriority|stripVlanHeader|setEthernetSrc|setEthernetDst|setIpv4TosBits|setIpv4SrcAddress|setIpv4DstAddress|setTransportSource|setTransportDestination|setVendorAction)
		"""
		return self._get_attribute('typeOfAction')
	@TypeOfAction.setter
	def TypeOfAction(self, value):
		self._set_attribute('typeOfAction', value)

	@property
	def TypeOfOutPort(self):
		"""

		Returns:
			str(ofppManual|ofppAll|ofppController|ofppInPort|ofppLocal|ofppNormal|ofppFlood)
		"""
		return self._get_attribute('typeOfOutPort')
	@TypeOfOutPort.setter
	def TypeOfOutPort(self, value):
		self._set_attribute('typeOfOutPort', value)

	@property
	def VendorData(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('vendorData')
	@VendorData.setter
	def VendorData(self, value):
		self._set_attribute('vendorData', value)

	@property
	def VendorDataLength(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('vendorDataLength')
	@VendorDataLength.setter
	def VendorDataLength(self, value):
		self._set_attribute('vendorDataLength', value)

	@property
	def VendorId(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('vendorId')
	@VendorId.setter
	def VendorId(self, value):
		self._set_attribute('vendorId', value)

	@property
	def VlanId(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('vlanId')
	@VlanId.setter
	def VlanId(self, value):
		self._set_attribute('vlanId', value)

	@property
	def VlanPriority(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('vlanPriority')
	@VlanPriority.setter
	def VlanPriority(self, value):
		self._set_attribute('vlanPriority', value)

	def add(self, EthDestination=None, EthSource=None, IpDscp=None, Ipv4Destination=None, Ipv4Source=None, MaxByteLength=None, OutputPort=None, QueueId=None, TransportDestination=None, TransportSource=None, TypeOfAction=None, TypeOfOutPort=None, VendorData=None, VendorDataLength=None, VendorId=None, VlanId=None, VlanPriority=None):
		"""Adds a new flowRangeAction node on the server and retrieves it in this instance.

		Args:
			EthDestination (str): 
			EthSource (str): 
			IpDscp (number): 
			Ipv4Destination (str): 
			Ipv4Source (str): 
			MaxByteLength (number): 
			OutputPort (number): 
			QueueId (number): 
			TransportDestination (number): 
			TransportSource (number): 
			TypeOfAction (str(none|output|enqueue|setVlanId|setVlanPriority|stripVlanHeader|setEthernetSrc|setEthernetDst|setIpv4TosBits|setIpv4SrcAddress|setIpv4DstAddress|setTransportSource|setTransportDestination|setVendorAction)): 
			TypeOfOutPort (str(ofppManual|ofppAll|ofppController|ofppInPort|ofppLocal|ofppNormal|ofppFlood)): 
			VendorData (str): 
			VendorDataLength (number): 
			VendorId (number): 
			VlanId (number): 
			VlanPriority (number): 

		Returns:
			self: This instance with all currently retrieved flowRangeAction data using find and the newly added flowRangeAction data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the flowRangeAction data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, EthDestination=None, EthSource=None, IpDscp=None, Ipv4Destination=None, Ipv4Source=None, MaxByteLength=None, OutputPort=None, QueueId=None, TransportDestination=None, TransportSource=None, TypeOfAction=None, TypeOfOutPort=None, VendorData=None, VendorDataLength=None, VendorId=None, VlanId=None, VlanPriority=None):
		"""Finds and retrieves flowRangeAction data from the server.

		All named parameters support regex and can be used to selectively retrieve flowRangeAction data from the server.
		By default the find method takes no parameters and will retrieve all flowRangeAction data from the server.

		Args:
			EthDestination (str): 
			EthSource (str): 
			IpDscp (number): 
			Ipv4Destination (str): 
			Ipv4Source (str): 
			MaxByteLength (number): 
			OutputPort (number): 
			QueueId (number): 
			TransportDestination (number): 
			TransportSource (number): 
			TypeOfAction (str(none|output|enqueue|setVlanId|setVlanPriority|stripVlanHeader|setEthernetSrc|setEthernetDst|setIpv4TosBits|setIpv4SrcAddress|setIpv4DstAddress|setTransportSource|setTransportDestination|setVendorAction)): 
			TypeOfOutPort (str(ofppManual|ofppAll|ofppController|ofppInPort|ofppLocal|ofppNormal|ofppFlood)): 
			VendorData (str): 
			VendorDataLength (number): 
			VendorId (number): 
			VlanId (number): 
			VlanPriority (number): 

		Returns:
			self: This instance with matching flowRangeAction data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of flowRangeAction data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the flowRangeAction data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
