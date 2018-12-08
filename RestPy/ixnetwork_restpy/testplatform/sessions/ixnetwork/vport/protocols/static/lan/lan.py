
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


class Lan(Base):
	"""The Lan class encapsulates a user managed lan node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Lan property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'lan'

	def __init__(self, parent):
		super(Lan, self).__init__(parent)

	@property
	def AtmEncapsulation(self):
		"""

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=atm)
		"""
		return self._get_attribute('atmEncapsulation')
	@AtmEncapsulation.setter
	def AtmEncapsulation(self, value):
		self._set_attribute('atmEncapsulation', value)

	@property
	def Count(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('count')
	@Count.setter
	def Count(self, value):
		self._set_attribute('count', value)

	@property
	def CountPerVc(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('countPerVc')
	@CountPerVc.setter
	def CountPerVc(self, value):
		self._set_attribute('countPerVc', value)

	@property
	def EnableIncrementMac(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableIncrementMac')
	@EnableIncrementMac.setter
	def EnableIncrementMac(self, value):
		self._set_attribute('enableIncrementMac', value)

	@property
	def EnableIncrementVlan(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableIncrementVlan')
	@EnableIncrementVlan.setter
	def EnableIncrementVlan(self, value):
		self._set_attribute('enableIncrementVlan', value)

	@property
	def EnableSiteId(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableSiteId')
	@EnableSiteId.setter
	def EnableSiteId(self, value):
		self._set_attribute('enableSiteId', value)

	@property
	def EnableVlan(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableVlan')
	@EnableVlan.setter
	def EnableVlan(self, value):
		self._set_attribute('enableVlan', value)

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
	def FrEncapsulation(self):
		"""

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=fr)
		"""
		return self._get_attribute('frEncapsulation')
	@FrEncapsulation.setter
	def FrEncapsulation(self, value):
		self._set_attribute('frEncapsulation', value)

	@property
	def IncrementPerVcVlanMode(self):
		"""

		Returns:
			str(noIncrement|parallelIncrement|innerFirst|outerFirst)
		"""
		return self._get_attribute('incrementPerVcVlanMode')
	@IncrementPerVcVlanMode.setter
	def IncrementPerVcVlanMode(self, value):
		self._set_attribute('incrementPerVcVlanMode', value)

	@property
	def IncrementVlanMode(self):
		"""

		Returns:
			str(noIncrement|parallelIncrement|innerFirst|outerFirst)
		"""
		return self._get_attribute('incrementVlanMode')
	@IncrementVlanMode.setter
	def IncrementVlanMode(self, value):
		self._set_attribute('incrementVlanMode', value)

	@property
	def IncremetVlanMode(self):
		"""

		Returns:
			str(noIncrement|parallelIncrement|innerFirst|outerFirst)
		"""
		return self._get_attribute('incremetVlanMode')
	@IncremetVlanMode.setter
	def IncremetVlanMode(self, value):
		self._set_attribute('incremetVlanMode', value)

	@property
	def Mac(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('mac')
	@Mac.setter
	def Mac(self, value):
		self._set_attribute('mac', value)

	@property
	def MacRangeMode(self):
		"""

		Returns:
			str(normal|bundled)
		"""
		return self._get_attribute('macRangeMode')
	@MacRangeMode.setter
	def MacRangeMode(self, value):
		self._set_attribute('macRangeMode', value)

	@property
	def NumberOfVcs(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('numberOfVcs')
	@NumberOfVcs.setter
	def NumberOfVcs(self, value):
		self._set_attribute('numberOfVcs', value)

	@property
	def SiteId(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('siteId')
	@SiteId.setter
	def SiteId(self, value):
		self._set_attribute('siteId', value)

	@property
	def SkipVlanIdZero(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('skipVlanIdZero')
	@SkipVlanIdZero.setter
	def SkipVlanIdZero(self, value):
		self._set_attribute('skipVlanIdZero', value)

	@property
	def Tpid(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('tpid')
	@Tpid.setter
	def Tpid(self, value):
		self._set_attribute('tpid', value)

	@property
	def TrafficGroupId(self):
		"""

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficGroup)
		"""
		return self._get_attribute('trafficGroupId')
	@TrafficGroupId.setter
	def TrafficGroupId(self, value):
		self._set_attribute('trafficGroupId', value)

	@property
	def VlanCount(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('vlanCount')
	@VlanCount.setter
	def VlanCount(self, value):
		self._set_attribute('vlanCount', value)

	@property
	def VlanId(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('vlanId')
	@VlanId.setter
	def VlanId(self, value):
		self._set_attribute('vlanId', value)

	@property
	def VlanPriority(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('vlanPriority')
	@VlanPriority.setter
	def VlanPriority(self, value):
		self._set_attribute('vlanPriority', value)

	def add(self, AtmEncapsulation=None, Count=None, CountPerVc=None, EnableIncrementMac=None, EnableIncrementVlan=None, EnableSiteId=None, EnableVlan=None, Enabled=None, FrEncapsulation=None, IncrementPerVcVlanMode=None, IncrementVlanMode=None, IncremetVlanMode=None, Mac=None, MacRangeMode=None, NumberOfVcs=None, SiteId=None, SkipVlanIdZero=None, Tpid=None, TrafficGroupId=None, VlanCount=None, VlanId=None, VlanPriority=None):
		"""Adds a new lan node on the server and retrieves it in this instance.

		Args:
			AtmEncapsulation (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=atm)): 
			Count (number): 
			CountPerVc (number): 
			EnableIncrementMac (bool): 
			EnableIncrementVlan (bool): 
			EnableSiteId (bool): 
			EnableVlan (bool): 
			Enabled (bool): 
			FrEncapsulation (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=fr)): 
			IncrementPerVcVlanMode (str(noIncrement|parallelIncrement|innerFirst|outerFirst)): 
			IncrementVlanMode (str(noIncrement|parallelIncrement|innerFirst|outerFirst)): 
			IncremetVlanMode (str(noIncrement|parallelIncrement|innerFirst|outerFirst)): 
			Mac (str): 
			MacRangeMode (str(normal|bundled)): 
			NumberOfVcs (number): 
			SiteId (number): 
			SkipVlanIdZero (bool): 
			Tpid (str): 
			TrafficGroupId (str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficGroup)): 
			VlanCount (number): 
			VlanId (str): 
			VlanPriority (str): 

		Returns:
			self: This instance with all currently retrieved lan data using find and the newly added lan data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the lan data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, AtmEncapsulation=None, Count=None, CountPerVc=None, EnableIncrementMac=None, EnableIncrementVlan=None, EnableSiteId=None, EnableVlan=None, Enabled=None, FrEncapsulation=None, IncrementPerVcVlanMode=None, IncrementVlanMode=None, IncremetVlanMode=None, Mac=None, MacRangeMode=None, NumberOfVcs=None, SiteId=None, SkipVlanIdZero=None, Tpid=None, TrafficGroupId=None, VlanCount=None, VlanId=None, VlanPriority=None):
		"""Finds and retrieves lan data from the server.

		All named parameters support regex and can be used to selectively retrieve lan data from the server.
		By default the find method takes no parameters and will retrieve all lan data from the server.

		Args:
			AtmEncapsulation (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=atm)): 
			Count (number): 
			CountPerVc (number): 
			EnableIncrementMac (bool): 
			EnableIncrementVlan (bool): 
			EnableSiteId (bool): 
			EnableVlan (bool): 
			Enabled (bool): 
			FrEncapsulation (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=fr)): 
			IncrementPerVcVlanMode (str(noIncrement|parallelIncrement|innerFirst|outerFirst)): 
			IncrementVlanMode (str(noIncrement|parallelIncrement|innerFirst|outerFirst)): 
			IncremetVlanMode (str(noIncrement|parallelIncrement|innerFirst|outerFirst)): 
			Mac (str): 
			MacRangeMode (str(normal|bundled)): 
			NumberOfVcs (number): 
			SiteId (number): 
			SkipVlanIdZero (bool): 
			Tpid (str): 
			TrafficGroupId (str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=trafficGroup)): 
			VlanCount (number): 
			VlanId (str): 
			VlanPriority (str): 

		Returns:
			self: This instance with matching lan data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of lan data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the lan data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
