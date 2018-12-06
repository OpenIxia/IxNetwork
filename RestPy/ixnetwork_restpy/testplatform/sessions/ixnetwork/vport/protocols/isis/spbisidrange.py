
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


class SpbIsIdRange(Base):
	"""The SpbIsIdRange class encapsulates a user managed spbIsIdRange node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the SpbIsIdRange property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'spbIsIdRange'

	def __init__(self, parent):
		super(SpbIsIdRange, self).__init__(parent)

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
	def CVlan(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('cVlan')
	@CVlan.setter
	def CVlan(self, value):
		self._set_attribute('cVlan', value)

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
	def ISid(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('iSid')
	@ISid.setter
	def ISid(self, value):
		self._set_attribute('iSid', value)

	@property
	def ITagEthernetType(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('iTagEthernetType')

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
	def SVlan(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('sVlan')
	@SVlan.setter
	def SVlan(self, value):
		self._set_attribute('sVlan', value)

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

	def add(self, CMacAddressCount=None, CMacAddressStep=None, CVlan=None, Enabled=None, ISid=None, RBit=None, SVlan=None, StartCmacAddress=None, TBit=None, TrafficDestMacAddress=None, TransmissionType=None, VlanType=None):
		"""Adds a new spbIsIdRange node on the server and retrieves it in this instance.

		Args:
			CMacAddressCount (number): 
			CMacAddressStep (str): 
			CVlan (number): 
			Enabled (bool): 
			ISid (number): 
			RBit (bool): 
			SVlan (number): 
			StartCmacAddress (str): 
			TBit (bool): 
			TrafficDestMacAddress (str): 
			TransmissionType (number): 
			VlanType (number): 

		Returns:
			self: This instance with all currently retrieved spbIsIdRange data using find and the newly added spbIsIdRange data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the spbIsIdRange data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, CMacAddressCount=None, CMacAddressStep=None, CVlan=None, Enabled=None, ISid=None, ITagEthernetType=None, RBit=None, SVlan=None, StartCmacAddress=None, TBit=None, TrafficDestMacAddress=None, TransmissionType=None, VlanType=None):
		"""Finds and retrieves spbIsIdRange data from the server.

		All named parameters support regex and can be used to selectively retrieve spbIsIdRange data from the server.
		By default the find method takes no parameters and will retrieve all spbIsIdRange data from the server.

		Args:
			CMacAddressCount (number): 
			CMacAddressStep (str): 
			CVlan (number): 
			Enabled (bool): 
			ISid (number): 
			ITagEthernetType (number): 
			RBit (bool): 
			SVlan (number): 
			StartCmacAddress (str): 
			TBit (bool): 
			TrafficDestMacAddress (str): 
			TransmissionType (number): 
			VlanType (number): 

		Returns:
			self: This instance with matching spbIsIdRange data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of spbIsIdRange data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the spbIsIdRange data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
