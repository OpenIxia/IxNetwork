
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


class SpbmNodeIsIdRange(Base):
	"""The SpbmNodeIsIdRange class encapsulates a user managed spbmNodeIsIdRange node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the SpbmNodeIsIdRange property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'spbmNodeIsIdRange'

	def __init__(self, parent):
		super(SpbmNodeIsIdRange, self).__init__(parent)

	@property
	def CMacAddressCount(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('cMacAddressCount')
	@CMacAddressCount.setter
	def CMacAddressCount(self, value):
		self._set_attribute('cMacAddressCount', value)

	@property
	def CMacAddressStep(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('cMacAddressStep')
	@CMacAddressStep.setter
	def CMacAddressStep(self, value):
		self._set_attribute('cMacAddressStep', value)

	@property
	def ITagEthernetType(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('iTagEthernetType')

	@property
	def InterNodeCmacAddress(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('interNodeCmacAddress')
	@InterNodeCmacAddress.setter
	def InterNodeCmacAddress(self, value):
		self._set_attribute('interNodeCmacAddress', value)

	@property
	def InterNodeCvlan(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('interNodeCvlan')
	@InterNodeCvlan.setter
	def InterNodeCvlan(self, value):
		self._set_attribute('interNodeCvlan', value)

	@property
	def InterNodeIsIdIncrement(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('interNodeIsIdIncrement')
	@InterNodeIsIdIncrement.setter
	def InterNodeIsIdIncrement(self, value):
		self._set_attribute('interNodeIsIdIncrement', value)

	@property
	def InterNodeSvlan(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('interNodeSvlan')
	@InterNodeSvlan.setter
	def InterNodeSvlan(self, value):
		self._set_attribute('interNodeSvlan', value)

	@property
	def IsId(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('isId')
	@IsId.setter
	def IsId(self, value):
		self._set_attribute('isId', value)

	@property
	def RBit(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('rBit')
	@RBit.setter
	def RBit(self, value):
		self._set_attribute('rBit', value)

	@property
	def StartCmacAddress(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('startCmacAddress')
	@StartCmacAddress.setter
	def StartCmacAddress(self, value):
		self._set_attribute('startCmacAddress', value)

	@property
	def StartCvlan(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('startCvlan')
	@StartCvlan.setter
	def StartCvlan(self, value):
		self._set_attribute('startCvlan', value)

	@property
	def StartSvlan(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('startSvlan')
	@StartSvlan.setter
	def StartSvlan(self, value):
		self._set_attribute('startSvlan', value)

	@property
	def TBit(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('tBit')
	@TBit.setter
	def TBit(self, value):
		self._set_attribute('tBit', value)

	@property
	def TrafficDestMacAddress(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('trafficDestMacAddress')
	@TrafficDestMacAddress.setter
	def TrafficDestMacAddress(self, value):
		self._set_attribute('trafficDestMacAddress', value)

	@property
	def TransmissionType(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('transmissionType')
	@TransmissionType.setter
	def TransmissionType(self, value):
		self._set_attribute('transmissionType', value)

	@property
	def VlanType(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('vlanType')
	@VlanType.setter
	def VlanType(self, value):
		self._set_attribute('vlanType', value)

	def add(self, CMacAddressCount=None, CMacAddressStep=None, InterNodeCmacAddress=None, InterNodeCvlan=None, InterNodeIsIdIncrement=None, InterNodeSvlan=None, IsId=None, RBit=None, StartCmacAddress=None, StartCvlan=None, StartSvlan=None, TBit=None, TrafficDestMacAddress=None, TransmissionType=None, VlanType=None):
		"""Adds a new spbmNodeIsIdRange node on the server and retrieves it in this instance.

		Args:
			CMacAddressCount (number): 
			CMacAddressStep (str): 
			InterNodeCmacAddress (str): 
			InterNodeCvlan (number): 
			InterNodeIsIdIncrement (number): 
			InterNodeSvlan (number): 
			IsId (number): 
			RBit (bool): 
			StartCmacAddress (str): 
			StartCvlan (number): 
			StartSvlan (number): 
			TBit (bool): 
			TrafficDestMacAddress (str): 
			TransmissionType (number): 
			VlanType (number): 

		Returns:
			self: This instance with all currently retrieved spbmNodeIsIdRange data using find and the newly added spbmNodeIsIdRange data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the spbmNodeIsIdRange data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, CMacAddressCount=None, CMacAddressStep=None, ITagEthernetType=None, InterNodeCmacAddress=None, InterNodeCvlan=None, InterNodeIsIdIncrement=None, InterNodeSvlan=None, IsId=None, RBit=None, StartCmacAddress=None, StartCvlan=None, StartSvlan=None, TBit=None, TrafficDestMacAddress=None, TransmissionType=None, VlanType=None):
		"""Finds and retrieves spbmNodeIsIdRange data from the server.

		All named parameters support regex and can be used to selectively retrieve spbmNodeIsIdRange data from the server.
		By default the find method takes no parameters and will retrieve all spbmNodeIsIdRange data from the server.

		Args:
			CMacAddressCount (number): 
			CMacAddressStep (str): 
			ITagEthernetType (number): 
			InterNodeCmacAddress (str): 
			InterNodeCvlan (number): 
			InterNodeIsIdIncrement (number): 
			InterNodeSvlan (number): 
			IsId (number): 
			RBit (bool): 
			StartCmacAddress (str): 
			StartCvlan (number): 
			StartSvlan (number): 
			TBit (bool): 
			TrafficDestMacAddress (str): 
			TransmissionType (number): 
			VlanType (number): 

		Returns:
			self: This instance with matching spbmNodeIsIdRange data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of spbmNodeIsIdRange data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the spbmNodeIsIdRange data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
