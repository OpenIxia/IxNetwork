
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


class Modifier(Base):
	"""The Modifier class encapsulates a user managed modifier node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Modifier property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'modifier'

	def __init__(self, parent):
		super(Modifier, self).__init__(parent)

	@property
	def ClusterSize(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('clusterSize')
	@ClusterSize.setter
	def ClusterSize(self, value):
		self._set_attribute('clusterSize', value)

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
	def L3MatchEtherType(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('l3MatchEtherType')
	@L3MatchEtherType.setter
	def L3MatchEtherType(self, value):
		self._set_attribute('l3MatchEtherType', value)

	@property
	def L3MatchMode(self):
		"""

		Returns:
			str(matchAny|matchBottomMplsLabel|matchEtherType)
		"""
		return self._get_attribute('l3MatchMode')
	@L3MatchMode.setter
	def L3MatchMode(self, value):
		self._set_attribute('l3MatchMode', value)

	@property
	def L3MatchMplsLabel(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('l3MatchMplsLabel')
	@L3MatchMplsLabel.setter
	def L3MatchMplsLabel(self, value):
		self._set_attribute('l3MatchMplsLabel', value)

	@property
	def L4MatchEncapsulation(self):
		"""

		Returns:
			str(matchIpv4|matchIpv4OrIpv6|matchIpv6)
		"""
		return self._get_attribute('l4MatchEncapsulation')
	@L4MatchEncapsulation.setter
	def L4MatchEncapsulation(self, value):
		self._set_attribute('l4MatchEncapsulation', value)

	@property
	def L4MatchMode(self):
		"""

		Returns:
			str(matchAny|matchProtocolNumber)
		"""
		return self._get_attribute('l4MatchMode')
	@L4MatchMode.setter
	def L4MatchMode(self, value):
		self._set_attribute('l4MatchMode', value)

	@property
	def L4MatchProtocolNumber(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('l4MatchProtocolNumber')
	@L4MatchProtocolNumber.setter
	def L4MatchProtocolNumber(self, value):
		self._set_attribute('l4MatchProtocolNumber', value)

	@property
	def L5MatchEncapsulation(self):
		"""

		Returns:
			str(matchTcp|matchUdp)
		"""
		return self._get_attribute('l5MatchEncapsulation')
	@L5MatchEncapsulation.setter
	def L5MatchEncapsulation(self, value):
		self._set_attribute('l5MatchEncapsulation', value)

	@property
	def L5MatchMode(self):
		"""

		Returns:
			str(matchAny|matchDestinationPort|matchSourceOrDestinationPort|matchSourcePort)
		"""
		return self._get_attribute('l5MatchMode')
	@L5MatchMode.setter
	def L5MatchMode(self, value):
		self._set_attribute('l5MatchMode', value)

	@property
	def L5MatchPortNumber(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('l5MatchPortNumber')
	@L5MatchPortNumber.setter
	def L5MatchPortNumber(self, value):
		self._set_attribute('l5MatchPortNumber', value)

	@property
	def Mask(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('mask')
	@Mask.setter
	def Mask(self, value):
		self._set_attribute('mask', value)

	@property
	def MatchValue(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('matchValue')
	@MatchValue.setter
	def MatchValue(self, value):
		self._set_attribute('matchValue', value)

	@property
	def MatchValueEnabled(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('matchValueEnabled')
	@MatchValueEnabled.setter
	def MatchValueEnabled(self, value):
		self._set_attribute('matchValueEnabled', value)

	@property
	def Name(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('name')
	@Name.setter
	def Name(self, value):
		self._set_attribute('name', value)

	@property
	def Offset(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('offset')
	@Offset.setter
	def Offset(self, value):
		self._set_attribute('offset', value)

	@property
	def OffsetStart(self):
		"""

		Returns:
			str(l2Offset|l3Offset|l4Offset|l5Offset)
		"""
		return self._get_attribute('offsetStart')
	@OffsetStart.setter
	def OffsetStart(self, value):
		self._set_attribute('offsetStart', value)

	@property
	def PercentRate(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('percentRate')
	@PercentRate.setter
	def PercentRate(self, value):
		self._set_attribute('percentRate', value)

	@property
	def ReplaceFixedValue(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('replaceFixedValue')
	@ReplaceFixedValue.setter
	def ReplaceFixedValue(self, value):
		self._set_attribute('replaceFixedValue', value)

	@property
	def ReplaceMode(self):
		"""

		Returns:
			str(fixedValue|range)
		"""
		return self._get_attribute('replaceMode')
	@ReplaceMode.setter
	def ReplaceMode(self, value):
		self._set_attribute('replaceMode', value)

	@property
	def ReplaceRangeCount(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('replaceRangeCount')
	@ReplaceRangeCount.setter
	def ReplaceRangeCount(self, value):
		self._set_attribute('replaceRangeCount', value)

	@property
	def ReplaceRangeDecrement(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('replaceRangeDecrement')
	@ReplaceRangeDecrement.setter
	def ReplaceRangeDecrement(self, value):
		self._set_attribute('replaceRangeDecrement', value)

	@property
	def ReplaceRangeFirst(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('replaceRangeFirst')
	@ReplaceRangeFirst.setter
	def ReplaceRangeFirst(self, value):
		self._set_attribute('replaceRangeFirst', value)

	@property
	def ReplaceRangeStep(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('replaceRangeStep')
	@ReplaceRangeStep.setter
	def ReplaceRangeStep(self, value):
		self._set_attribute('replaceRangeStep', value)

	def add(self, ClusterSize=None, Enabled=None, L3MatchEtherType=None, L3MatchMode=None, L3MatchMplsLabel=None, L4MatchEncapsulation=None, L4MatchMode=None, L4MatchProtocolNumber=None, L5MatchEncapsulation=None, L5MatchMode=None, L5MatchPortNumber=None, Mask=None, MatchValue=None, MatchValueEnabled=None, Name=None, Offset=None, OffsetStart=None, PercentRate=None, ReplaceFixedValue=None, ReplaceMode=None, ReplaceRangeCount=None, ReplaceRangeDecrement=None, ReplaceRangeFirst=None, ReplaceRangeStep=None):
		"""Adds a new modifier node on the server and retrieves it in this instance.

		Args:
			ClusterSize (number): 
			Enabled (bool): 
			L3MatchEtherType (str): 
			L3MatchMode (str(matchAny|matchBottomMplsLabel|matchEtherType)): 
			L3MatchMplsLabel (number): 
			L4MatchEncapsulation (str(matchIpv4|matchIpv4OrIpv6|matchIpv6)): 
			L4MatchMode (str(matchAny|matchProtocolNumber)): 
			L4MatchProtocolNumber (number): 
			L5MatchEncapsulation (str(matchTcp|matchUdp)): 
			L5MatchMode (str(matchAny|matchDestinationPort|matchSourceOrDestinationPort|matchSourcePort)): 
			L5MatchPortNumber (number): 
			Mask (str): 
			MatchValue (str): 
			MatchValueEnabled (bool): 
			Name (str): 
			Offset (number): 
			OffsetStart (str(l2Offset|l3Offset|l4Offset|l5Offset)): 
			PercentRate (number): 
			ReplaceFixedValue (str): 
			ReplaceMode (str(fixedValue|range)): 
			ReplaceRangeCount (str): 
			ReplaceRangeDecrement (bool): 
			ReplaceRangeFirst (str): 
			ReplaceRangeStep (str): 

		Returns:
			self: This instance with all currently retrieved modifier data using find and the newly added modifier data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the modifier data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, ClusterSize=None, Enabled=None, L3MatchEtherType=None, L3MatchMode=None, L3MatchMplsLabel=None, L4MatchEncapsulation=None, L4MatchMode=None, L4MatchProtocolNumber=None, L5MatchEncapsulation=None, L5MatchMode=None, L5MatchPortNumber=None, Mask=None, MatchValue=None, MatchValueEnabled=None, Name=None, Offset=None, OffsetStart=None, PercentRate=None, ReplaceFixedValue=None, ReplaceMode=None, ReplaceRangeCount=None, ReplaceRangeDecrement=None, ReplaceRangeFirst=None, ReplaceRangeStep=None):
		"""Finds and retrieves modifier data from the server.

		All named parameters support regex and can be used to selectively retrieve modifier data from the server.
		By default the find method takes no parameters and will retrieve all modifier data from the server.

		Args:
			ClusterSize (number): 
			Enabled (bool): 
			L3MatchEtherType (str): 
			L3MatchMode (str(matchAny|matchBottomMplsLabel|matchEtherType)): 
			L3MatchMplsLabel (number): 
			L4MatchEncapsulation (str(matchIpv4|matchIpv4OrIpv6|matchIpv6)): 
			L4MatchMode (str(matchAny|matchProtocolNumber)): 
			L4MatchProtocolNumber (number): 
			L5MatchEncapsulation (str(matchTcp|matchUdp)): 
			L5MatchMode (str(matchAny|matchDestinationPort|matchSourceOrDestinationPort|matchSourcePort)): 
			L5MatchPortNumber (number): 
			Mask (str): 
			MatchValue (str): 
			MatchValueEnabled (bool): 
			Name (str): 
			Offset (number): 
			OffsetStart (str(l2Offset|l3Offset|l4Offset|l5Offset)): 
			PercentRate (number): 
			ReplaceFixedValue (str): 
			ReplaceMode (str(fixedValue|range)): 
			ReplaceRangeCount (str): 
			ReplaceRangeDecrement (bool): 
			ReplaceRangeFirst (str): 
			ReplaceRangeStep (str): 

		Returns:
			self: This instance with matching modifier data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of modifier data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the modifier data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
