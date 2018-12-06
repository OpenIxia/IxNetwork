
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


class DceMulticastIpv6GroupRange(Base):
	"""The DceMulticastIpv6GroupRange class encapsulates a user managed dceMulticastIpv6GroupRange node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the DceMulticastIpv6GroupRange property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'dceMulticastIpv6GroupRange'

	def __init__(self, parent):
		super(DceMulticastIpv6GroupRange, self).__init__(parent)

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
	def Topology(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('topology')
	@Topology.setter
	def Topology(self, value):
		self._set_attribute('topology', value)

	@property
	def UnicastSourcesPerMulticastIpv6(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('unicastSourcesPerMulticastIpv6')
	@UnicastSourcesPerMulticastIpv6.setter
	def UnicastSourcesPerMulticastIpv6(self, value):
		self._set_attribute('unicastSourcesPerMulticastIpv6', value)

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

	def add(self, Enabled=None, InterGroupUnicastIpv6Increment=None, IntraGroupUnicastIpv6Increment=None, MulticastIpv6Count=None, MulticastIpv6Step=None, SourceGroupMapping=None, StartMulticastIpv6=None, StartUnicastSourceIpv6=None, Topology=None, UnicastSourcesPerMulticastIpv6=None, VlanId=None):
		"""Adds a new dceMulticastIpv6GroupRange node on the server and retrieves it in this instance.

		Args:
			Enabled (bool): 
			InterGroupUnicastIpv6Increment (str): 
			IntraGroupUnicastIpv6Increment (str): 
			MulticastIpv6Count (number): 
			MulticastIpv6Step (str): 
			SourceGroupMapping (str(fullyMeshed|oneToOne|manualMapping)): 
			StartMulticastIpv6 (str): 
			StartUnicastSourceIpv6 (str): 
			Topology (number): 
			UnicastSourcesPerMulticastIpv6 (number): 
			VlanId (number): 

		Returns:
			self: This instance with all currently retrieved dceMulticastIpv6GroupRange data using find and the newly added dceMulticastIpv6GroupRange data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the dceMulticastIpv6GroupRange data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, Enabled=None, InterGroupUnicastIpv6Increment=None, IntraGroupUnicastIpv6Increment=None, MulticastIpv6Count=None, MulticastIpv6Step=None, SourceGroupMapping=None, StartMulticastIpv6=None, StartUnicastSourceIpv6=None, Topology=None, UnicastSourcesPerMulticastIpv6=None, VlanId=None):
		"""Finds and retrieves dceMulticastIpv6GroupRange data from the server.

		All named parameters support regex and can be used to selectively retrieve dceMulticastIpv6GroupRange data from the server.
		By default the find method takes no parameters and will retrieve all dceMulticastIpv6GroupRange data from the server.

		Args:
			Enabled (bool): 
			InterGroupUnicastIpv6Increment (str): 
			IntraGroupUnicastIpv6Increment (str): 
			MulticastIpv6Count (number): 
			MulticastIpv6Step (str): 
			SourceGroupMapping (str(fullyMeshed|oneToOne|manualMapping)): 
			StartMulticastIpv6 (str): 
			StartUnicastSourceIpv6 (str): 
			Topology (number): 
			UnicastSourcesPerMulticastIpv6 (number): 
			VlanId (number): 

		Returns:
			self: This instance with matching dceMulticastIpv6GroupRange data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of dceMulticastIpv6GroupRange data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the dceMulticastIpv6GroupRange data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
