
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


class DceNodeIpv4Groups(Base):
	"""The DceNodeIpv4Groups class encapsulates a user managed dceNodeIpv4Groups node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the DceNodeIpv4Groups property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'dceNodeIpv4Groups'

	def __init__(self, parent):
		super(DceNodeIpv4Groups, self).__init__(parent)

	@property
	def IncludeIpv4Groups(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('includeIpv4Groups')
	@IncludeIpv4Groups.setter
	def IncludeIpv4Groups(self, value):
		self._set_attribute('includeIpv4Groups', value)

	@property
	def InterGroupUnicastIpv4Increment(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('interGroupUnicastIpv4Increment')
	@InterGroupUnicastIpv4Increment.setter
	def InterGroupUnicastIpv4Increment(self, value):
		self._set_attribute('interGroupUnicastIpv4Increment', value)

	@property
	def IntraGroupUnicastIpv4Increment(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('intraGroupUnicastIpv4Increment')
	@IntraGroupUnicastIpv4Increment.setter
	def IntraGroupUnicastIpv4Increment(self, value):
		self._set_attribute('intraGroupUnicastIpv4Increment', value)

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
	def MulticastIpv4Count(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('multicastIpv4Count')
	@MulticastIpv4Count.setter
	def MulticastIpv4Count(self, value):
		self._set_attribute('multicastIpv4Count', value)

	@property
	def MulticastIpv4Step(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('multicastIpv4Step')
	@MulticastIpv4Step.setter
	def MulticastIpv4Step(self, value):
		self._set_attribute('multicastIpv4Step', value)

	@property
	def NoOfUnicastScrIpv4sPerMulicastIpv4(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('noOfUnicastScrIpv4sPerMulicastIpv4')
	@NoOfUnicastScrIpv4sPerMulicastIpv4.setter
	def NoOfUnicastScrIpv4sPerMulicastIpv4(self, value):
		self._set_attribute('noOfUnicastScrIpv4sPerMulicastIpv4', value)

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
	def StartMulticastIpv4(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('startMulticastIpv4')
	@StartMulticastIpv4.setter
	def StartMulticastIpv4(self, value):
		self._set_attribute('startMulticastIpv4', value)

	@property
	def StartUnicastSourceIpv4(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('startUnicastSourceIpv4')
	@StartUnicastSourceIpv4.setter
	def StartUnicastSourceIpv4(self, value):
		self._set_attribute('startUnicastSourceIpv4', value)

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

	def add(self, IncludeIpv4Groups=None, InterGroupUnicastIpv4Increment=None, IntraGroupUnicastIpv4Increment=None, MulticastAddressNodeStep=None, MulticastIpv4Count=None, MulticastIpv4Step=None, NoOfUnicastScrIpv4sPerMulicastIpv4=None, SourceGroupMapping=None, StartMulticastIpv4=None, StartUnicastSourceIpv4=None, UnicastAddressNodeStep=None, VlanId=None):
		"""Adds a new dceNodeIpv4Groups node on the server and retrieves it in this instance.

		Args:
			IncludeIpv4Groups (bool): 
			InterGroupUnicastIpv4Increment (str): 
			IntraGroupUnicastIpv4Increment (str): 
			MulticastAddressNodeStep (str): 
			MulticastIpv4Count (number): 
			MulticastIpv4Step (str): 
			NoOfUnicastScrIpv4sPerMulicastIpv4 (number): 
			SourceGroupMapping (str(fullyMeshed|oneToOne|manualMapping)): 
			StartMulticastIpv4 (str): 
			StartUnicastSourceIpv4 (str): 
			UnicastAddressNodeStep (str): 
			VlanId (number): 

		Returns:
			self: This instance with all currently retrieved dceNodeIpv4Groups data using find and the newly added dceNodeIpv4Groups data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the dceNodeIpv4Groups data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, IncludeIpv4Groups=None, InterGroupUnicastIpv4Increment=None, IntraGroupUnicastIpv4Increment=None, MulticastAddressNodeStep=None, MulticastIpv4Count=None, MulticastIpv4Step=None, NoOfUnicastScrIpv4sPerMulicastIpv4=None, SourceGroupMapping=None, StartMulticastIpv4=None, StartUnicastSourceIpv4=None, UnicastAddressNodeStep=None, VlanId=None):
		"""Finds and retrieves dceNodeIpv4Groups data from the server.

		All named parameters support regex and can be used to selectively retrieve dceNodeIpv4Groups data from the server.
		By default the find method takes no parameters and will retrieve all dceNodeIpv4Groups data from the server.

		Args:
			IncludeIpv4Groups (bool): 
			InterGroupUnicastIpv4Increment (str): 
			IntraGroupUnicastIpv4Increment (str): 
			MulticastAddressNodeStep (str): 
			MulticastIpv4Count (number): 
			MulticastIpv4Step (str): 
			NoOfUnicastScrIpv4sPerMulicastIpv4 (number): 
			SourceGroupMapping (str(fullyMeshed|oneToOne|manualMapping)): 
			StartMulticastIpv4 (str): 
			StartUnicastSourceIpv4 (str): 
			UnicastAddressNodeStep (str): 
			VlanId (number): 

		Returns:
			self: This instance with matching dceNodeIpv4Groups data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of dceNodeIpv4Groups data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the dceNodeIpv4Groups data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
