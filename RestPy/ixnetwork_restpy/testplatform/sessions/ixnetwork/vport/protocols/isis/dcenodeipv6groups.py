
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


class DceNodeIpv6Groups(Base):
	"""The DceNodeIpv6Groups class encapsulates a user managed dceNodeIpv6Groups node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the DceNodeIpv6Groups property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'dceNodeIpv6Groups'

	def __init__(self, parent):
		super(DceNodeIpv6Groups, self).__init__(parent)

	@property
	def IncludeIpv6Groups(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('includeIpv6Groups')
	@IncludeIpv6Groups.setter
	def IncludeIpv6Groups(self, value):
		self._set_attribute('includeIpv6Groups', value)

	@property
	def InterGroupUnicastIpv6Increment(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('interGroupUnicastIpv6Increment')
	@InterGroupUnicastIpv6Increment.setter
	def InterGroupUnicastIpv6Increment(self, value):
		self._set_attribute('interGroupUnicastIpv6Increment', value)

	@property
	def IntraGroupUnicastIpv6Increment(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('intraGroupUnicastIpv6Increment')
	@IntraGroupUnicastIpv6Increment.setter
	def IntraGroupUnicastIpv6Increment(self, value):
		self._set_attribute('intraGroupUnicastIpv6Increment', value)

	@property
	def MulticastAddressNodeStep(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('multicastAddressNodeStep')
	@MulticastAddressNodeStep.setter
	def MulticastAddressNodeStep(self, value):
		self._set_attribute('multicastAddressNodeStep', value)

	@property
	def MulticastIpv6Count(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('multicastIpv6Count')
	@MulticastIpv6Count.setter
	def MulticastIpv6Count(self, value):
		self._set_attribute('multicastIpv6Count', value)

	@property
	def MulticastIpv6Step(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('multicastIpv6Step')
	@MulticastIpv6Step.setter
	def MulticastIpv6Step(self, value):
		self._set_attribute('multicastIpv6Step', value)

	@property
	def NoOfUnicastScrIpv6sPerMulicastIpv6(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('noOfUnicastScrIpv6sPerMulicastIpv6')
	@NoOfUnicastScrIpv6sPerMulicastIpv6.setter
	def NoOfUnicastScrIpv6sPerMulicastIpv6(self, value):
		self._set_attribute('noOfUnicastScrIpv6sPerMulicastIpv6', value)

	@property
	def SourceGroupMapping(self):
		"""

		Returns:
			str(fullyMeshed|oneToOne|manualMapping)
		"""
		return self._get_attribute('sourceGroupMapping')
	@SourceGroupMapping.setter
	def SourceGroupMapping(self, value):
		self._set_attribute('sourceGroupMapping', value)

	@property
	def StartMulticastIpv6(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('startMulticastIpv6')
	@StartMulticastIpv6.setter
	def StartMulticastIpv6(self, value):
		self._set_attribute('startMulticastIpv6', value)

	@property
	def StartUnicastSourceIpv6(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('startUnicastSourceIpv6')
	@StartUnicastSourceIpv6.setter
	def StartUnicastSourceIpv6(self, value):
		self._set_attribute('startUnicastSourceIpv6', value)

	@property
	def UnicastAddressNodeStep(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('unicastAddressNodeStep')
	@UnicastAddressNodeStep.setter
	def UnicastAddressNodeStep(self, value):
		self._set_attribute('unicastAddressNodeStep', value)

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

	def add(self, IncludeIpv6Groups=None, InterGroupUnicastIpv6Increment=None, IntraGroupUnicastIpv6Increment=None, MulticastAddressNodeStep=None, MulticastIpv6Count=None, MulticastIpv6Step=None, NoOfUnicastScrIpv6sPerMulicastIpv6=None, SourceGroupMapping=None, StartMulticastIpv6=None, StartUnicastSourceIpv6=None, UnicastAddressNodeStep=None, VlanId=None):
		"""Adds a new dceNodeIpv6Groups node on the server and retrieves it in this instance.

		Args:
			IncludeIpv6Groups (bool): 
			InterGroupUnicastIpv6Increment (str): 
			IntraGroupUnicastIpv6Increment (str): 
			MulticastAddressNodeStep (str): 
			MulticastIpv6Count (number): 
			MulticastIpv6Step (str): 
			NoOfUnicastScrIpv6sPerMulicastIpv6 (number): 
			SourceGroupMapping (str(fullyMeshed|oneToOne|manualMapping)): 
			StartMulticastIpv6 (str): 
			StartUnicastSourceIpv6 (str): 
			UnicastAddressNodeStep (str): 
			VlanId (number): 

		Returns:
			self: This instance with all currently retrieved dceNodeIpv6Groups data using find and the newly added dceNodeIpv6Groups data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the dceNodeIpv6Groups data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, IncludeIpv6Groups=None, InterGroupUnicastIpv6Increment=None, IntraGroupUnicastIpv6Increment=None, MulticastAddressNodeStep=None, MulticastIpv6Count=None, MulticastIpv6Step=None, NoOfUnicastScrIpv6sPerMulicastIpv6=None, SourceGroupMapping=None, StartMulticastIpv6=None, StartUnicastSourceIpv6=None, UnicastAddressNodeStep=None, VlanId=None):
		"""Finds and retrieves dceNodeIpv6Groups data from the server.

		All named parameters support regex and can be used to selectively retrieve dceNodeIpv6Groups data from the server.
		By default the find method takes no parameters and will retrieve all dceNodeIpv6Groups data from the server.

		Args:
			IncludeIpv6Groups (bool): 
			InterGroupUnicastIpv6Increment (str): 
			IntraGroupUnicastIpv6Increment (str): 
			MulticastAddressNodeStep (str): 
			MulticastIpv6Count (number): 
			MulticastIpv6Step (str): 
			NoOfUnicastScrIpv6sPerMulicastIpv6 (number): 
			SourceGroupMapping (str(fullyMeshed|oneToOne|manualMapping)): 
			StartMulticastIpv6 (str): 
			StartUnicastSourceIpv6 (str): 
			UnicastAddressNodeStep (str): 
			VlanId (number): 

		Returns:
			self: This instance with matching dceNodeIpv6Groups data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of dceNodeIpv6Groups data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the dceNodeIpv6Groups data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
