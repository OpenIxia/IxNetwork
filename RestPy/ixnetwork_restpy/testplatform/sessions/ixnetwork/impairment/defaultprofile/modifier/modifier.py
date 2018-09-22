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
		"""Number of packets to modify on each occurrence. Default: 1.

		Returns:
			number
		"""
		return self._get_attribute('clusterSize')
	@ClusterSize.setter
	def ClusterSize(self, value):
		self._set_attribute('clusterSize', value)

	@property
	def Enabled(self):
		"""If true, modify incoming packets.

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def L3MatchEtherType(self):
		"""EtherType value to match.

		Returns:
			str
		"""
		return self._get_attribute('l3MatchEtherType')
	@L3MatchEtherType.setter
	def L3MatchEtherType(self, value):
		self._set_attribute('l3MatchEtherType', value)

	@property
	def L3MatchMode(self):
		"""For an L3 offset, specify whether to modify only packets with a specific EtherType or bottom MPLS label.

		Returns:
			str(matchAny|matchBottomMplsLabel|matchEtherType)
		"""
		return self._get_attribute('l3MatchMode')
	@L3MatchMode.setter
	def L3MatchMode(self, value):
		self._set_attribute('l3MatchMode', value)

	@property
	def L3MatchMplsLabel(self):
		"""MPLS label to match.

		Returns:
			number
		"""
		return self._get_attribute('l3MatchMplsLabel')
	@L3MatchMplsLabel.setter
	def L3MatchMplsLabel(self, value):
		self._set_attribute('l3MatchMplsLabel', value)

	@property
	def L4MatchEncapsulation(self):
		"""For an L4 offset, specify whether to modify IPv4 packets, IPv6 packets, or both.

		Returns:
			str(matchIpv4|matchIpv4OrIpv6|matchIpv6)
		"""
		return self._get_attribute('l4MatchEncapsulation')
	@L4MatchEncapsulation.setter
	def L4MatchEncapsulation(self, value):
		self._set_attribute('l4MatchEncapsulation', value)

	@property
	def L4MatchMode(self):
		"""For an L4 offset, specify whether to modify only packets with a specific protocol number.

		Returns:
			str(matchAny|matchProtocolNumber)
		"""
		return self._get_attribute('l4MatchMode')
	@L4MatchMode.setter
	def L4MatchMode(self, value):
		self._set_attribute('l4MatchMode', value)

	@property
	def L4MatchProtocolNumber(self):
		"""Protocol number to match.

		Returns:
			number
		"""
		return self._get_attribute('l4MatchProtocolNumber')
	@L4MatchProtocolNumber.setter
	def L4MatchProtocolNumber(self, value):
		self._set_attribute('l4MatchProtocolNumber', value)

	@property
	def L5MatchEncapsulation(self):
		"""For an L5 offset, specify whether to modify TCP packets only or UDP packets only.

		Returns:
			str(matchTcp|matchUdp)
		"""
		return self._get_attribute('l5MatchEncapsulation')
	@L5MatchEncapsulation.setter
	def L5MatchEncapsulation(self, value):
		self._set_attribute('l5MatchEncapsulation', value)

	@property
	def L5MatchMode(self):
		"""For an L5 offset, specify whether to modify only packets with a specific source or destination port number.

		Returns:
			str(matchAny|matchDestinationPort|matchSourceOrDestinationPort|matchSourcePort)
		"""
		return self._get_attribute('l5MatchMode')
	@L5MatchMode.setter
	def L5MatchMode(self, value):
		self._set_attribute('l5MatchMode', value)

	@property
	def L5MatchPortNumber(self):
		"""Port number to match.

		Returns:
			number
		"""
		return self._get_attribute('l5MatchPortNumber')
	@L5MatchPortNumber.setter
	def L5MatchPortNumber(self, value):
		self._set_attribute('l5MatchPortNumber', value)

	@property
	def Mask(self):
		"""Mask identifying the bits of the field to be modified, as a hex string with prefix 0x (e.g. 0xFF FF). The bits of the mask must be contiguous.

		Returns:
			str
		"""
		return self._get_attribute('mask')
	@Mask.setter
	def Mask(self, value):
		self._set_attribute('mask', value)

	@property
	def MatchValue(self):
		"""Value to be matched. Format: MAC address, IPv4 address, IPv6 address, decimal value, binary string with prefix 0b (e.g. 0b0100), or a hex string with prefix 0x (e.g. 0xFF FF).

		Returns:
			str
		"""
		return self._get_attribute('matchValue')
	@MatchValue.setter
	def MatchValue(self, value):
		self._set_attribute('matchValue', value)

	@property
	def MatchValueEnabled(self):
		"""Only modify packets if the existing field value matches a specified value.

		Returns:
			bool
		"""
		return self._get_attribute('matchValueEnabled')
	@MatchValueEnabled.setter
	def MatchValueEnabled(self, value):
		self._set_attribute('matchValueEnabled', value)

	@property
	def Name(self):
		"""Name of the modifier.

		Returns:
			str
		"""
		return self._get_attribute('name')
	@Name.setter
	def Name(self, value):
		self._set_attribute('name', value)

	@property
	def Offset(self):
		"""The position of the field to be modified, as an offset in bytes.

		Returns:
			number
		"""
		return self._get_attribute('offset')
	@Offset.setter
	def Offset(self, value):
		self._set_attribute('offset', value)

	@property
	def OffsetStart(self):
		"""Define the position of the field to be modified, as an offset from a specified position. Default is from the start of the L2 header.

		Returns:
			str(l2Offset|l3Offset|l4Offset|l5Offset)
		"""
		return self._get_attribute('offsetStart')
	@OffsetStart.setter
	def OffsetStart(self, value):
		self._set_attribute('offsetStart', value)

	@property
	def PercentRate(self):
		"""How often to modify matching packets. Default: 100%.

		Returns:
			number
		"""
		return self._get_attribute('percentRate')
	@PercentRate.setter
	def PercentRate(self, value):
		self._set_attribute('percentRate', value)

	@property
	def ReplaceFixedValue(self):
		"""Fixed replacement value. Format: MAC address, IPv4 address, IPv6 address, decimal value, binary string with prefix 0b (e.g. 0b0100), or a hex string with prefix 0x (e.g. 0xFF FF).

		Returns:
			str
		"""
		return self._get_attribute('replaceFixedValue')
	@ReplaceFixedValue.setter
	def ReplaceFixedValue(self, value):
		self._set_attribute('replaceFixedValue', value)

	@property
	def ReplaceMode(self):
		"""Replace field with a fixed value or a range of values.

		Returns:
			str(fixedValue|range)
		"""
		return self._get_attribute('replaceMode')
	@ReplaceMode.setter
	def ReplaceMode(self, value):
		self._set_attribute('replaceMode', value)

	@property
	def ReplaceRangeCount(self):
		"""Number of values in range. Can be any value up to ceiling(2^width / step), where width is the width of the field mask.

		Returns:
			str
		"""
		return self._get_attribute('replaceRangeCount')
	@ReplaceRangeCount.setter
	def ReplaceRangeCount(self, value):
		self._set_attribute('replaceRangeCount', value)

	@property
	def ReplaceRangeDecrement(self):
		"""Decrement instead of incrementing. Default: false.

		Returns:
			bool
		"""
		return self._get_attribute('replaceRangeDecrement')
	@ReplaceRangeDecrement.setter
	def ReplaceRangeDecrement(self, value):
		self._set_attribute('replaceRangeDecrement', value)

	@property
	def ReplaceRangeFirst(self):
		"""Start of range.

		Returns:
			str
		"""
		return self._get_attribute('replaceRangeFirst')
	@ReplaceRangeFirst.setter
	def ReplaceRangeFirst(self, value):
		self._set_attribute('replaceRangeFirst', value)

	@property
	def ReplaceRangeStep(self):
		"""Step to be added or subtracted for each modified packet.

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
			ClusterSize (number): Number of packets to modify on each occurrence. Default: 1.
			Enabled (bool): If true, modify incoming packets.
			L3MatchEtherType (str): EtherType value to match.
			L3MatchMode (str(matchAny|matchBottomMplsLabel|matchEtherType)): For an L3 offset, specify whether to modify only packets with a specific EtherType or bottom MPLS label.
			L3MatchMplsLabel (number): MPLS label to match.
			L4MatchEncapsulation (str(matchIpv4|matchIpv4OrIpv6|matchIpv6)): For an L4 offset, specify whether to modify IPv4 packets, IPv6 packets, or both.
			L4MatchMode (str(matchAny|matchProtocolNumber)): For an L4 offset, specify whether to modify only packets with a specific protocol number.
			L4MatchProtocolNumber (number): Protocol number to match.
			L5MatchEncapsulation (str(matchTcp|matchUdp)): For an L5 offset, specify whether to modify TCP packets only or UDP packets only.
			L5MatchMode (str(matchAny|matchDestinationPort|matchSourceOrDestinationPort|matchSourcePort)): For an L5 offset, specify whether to modify only packets with a specific source or destination port number.
			L5MatchPortNumber (number): Port number to match.
			Mask (str): Mask identifying the bits of the field to be modified, as a hex string with prefix 0x (e.g. 0xFF FF). The bits of the mask must be contiguous.
			MatchValue (str): Value to be matched. Format: MAC address, IPv4 address, IPv6 address, decimal value, binary string with prefix 0b (e.g. 0b0100), or a hex string with prefix 0x (e.g. 0xFF FF).
			MatchValueEnabled (bool): Only modify packets if the existing field value matches a specified value.
			Name (str): Name of the modifier.
			Offset (number): The position of the field to be modified, as an offset in bytes.
			OffsetStart (str(l2Offset|l3Offset|l4Offset|l5Offset)): Define the position of the field to be modified, as an offset from a specified position. Default is from the start of the L2 header.
			PercentRate (number): How often to modify matching packets. Default: 100%.
			ReplaceFixedValue (str): Fixed replacement value. Format: MAC address, IPv4 address, IPv6 address, decimal value, binary string with prefix 0b (e.g. 0b0100), or a hex string with prefix 0x (e.g. 0xFF FF).
			ReplaceMode (str(fixedValue|range)): Replace field with a fixed value or a range of values.
			ReplaceRangeCount (str): Number of values in range. Can be any value up to ceiling(2^width / step), where width is the width of the field mask.
			ReplaceRangeDecrement (bool): Decrement instead of incrementing. Default: false.
			ReplaceRangeFirst (str): Start of range.
			ReplaceRangeStep (str): Step to be added or subtracted for each modified packet.

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
			ClusterSize (number): Number of packets to modify on each occurrence. Default: 1.
			Enabled (bool): If true, modify incoming packets.
			L3MatchEtherType (str): EtherType value to match.
			L3MatchMode (str(matchAny|matchBottomMplsLabel|matchEtherType)): For an L3 offset, specify whether to modify only packets with a specific EtherType or bottom MPLS label.
			L3MatchMplsLabel (number): MPLS label to match.
			L4MatchEncapsulation (str(matchIpv4|matchIpv4OrIpv6|matchIpv6)): For an L4 offset, specify whether to modify IPv4 packets, IPv6 packets, or both.
			L4MatchMode (str(matchAny|matchProtocolNumber)): For an L4 offset, specify whether to modify only packets with a specific protocol number.
			L4MatchProtocolNumber (number): Protocol number to match.
			L5MatchEncapsulation (str(matchTcp|matchUdp)): For an L5 offset, specify whether to modify TCP packets only or UDP packets only.
			L5MatchMode (str(matchAny|matchDestinationPort|matchSourceOrDestinationPort|matchSourcePort)): For an L5 offset, specify whether to modify only packets with a specific source or destination port number.
			L5MatchPortNumber (number): Port number to match.
			Mask (str): Mask identifying the bits of the field to be modified, as a hex string with prefix 0x (e.g. 0xFF FF). The bits of the mask must be contiguous.
			MatchValue (str): Value to be matched. Format: MAC address, IPv4 address, IPv6 address, decimal value, binary string with prefix 0b (e.g. 0b0100), or a hex string with prefix 0x (e.g. 0xFF FF).
			MatchValueEnabled (bool): Only modify packets if the existing field value matches a specified value.
			Name (str): Name of the modifier.
			Offset (number): The position of the field to be modified, as an offset in bytes.
			OffsetStart (str(l2Offset|l3Offset|l4Offset|l5Offset)): Define the position of the field to be modified, as an offset from a specified position. Default is from the start of the L2 header.
			PercentRate (number): How often to modify matching packets. Default: 100%.
			ReplaceFixedValue (str): Fixed replacement value. Format: MAC address, IPv4 address, IPv6 address, decimal value, binary string with prefix 0b (e.g. 0b0100), or a hex string with prefix 0x (e.g. 0xFF FF).
			ReplaceMode (str(fixedValue|range)): Replace field with a fixed value or a range of values.
			ReplaceRangeCount (str): Number of values in range. Can be any value up to ceiling(2^width / step), where width is the width of the field mask.
			ReplaceRangeDecrement (bool): Decrement instead of incrementing. Default: false.
			ReplaceRangeFirst (str): Start of range.
			ReplaceRangeStep (str): Step to be added or subtracted for each modified packet.

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
