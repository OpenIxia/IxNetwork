from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class TunnelHeadToLeaf(Base):
	"""The TunnelHeadToLeaf class encapsulates a user managed tunnelHeadToLeaf node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the TunnelHeadToLeaf property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'tunnelHeadToLeaf'

	def __init__(self, parent):
		super(TunnelHeadToLeaf, self).__init__(parent)

	@property
	def DutHopType(self):
		"""Based on the input, the corresponding L bit in the packet is set.

		Returns:
			str(strict|loose)
		"""
		return self._get_attribute('dutHopType')
	@DutHopType.setter
	def DutHopType(self, value):
		self._set_attribute('dutHopType', value)

	@property
	def DutPrefixLength(self):
		"""Prefix length of DUT.

		Returns:
			number
		"""
		return self._get_attribute('dutPrefixLength')
	@DutPrefixLength.setter
	def DutPrefixLength(self, value):
		self._set_attribute('dutPrefixLength', value)

	@property
	def Enabled(self):
		"""It enables or disables the ERO/SERO specific configuration.

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def HeadIpStart(self):
		"""It is the tunnel head IP address for which the ERO/SERO is being configured.

		Returns:
			str
		"""
		return self._get_attribute('headIpStart')

	@property
	def IsAppendTunnelLeaf(self):
		"""If enabled, this appends the tunnel leaf at the end of the ERO/SERO list in the packet.

		Returns:
			bool
		"""
		return self._get_attribute('isAppendTunnelLeaf')
	@IsAppendTunnelLeaf.setter
	def IsAppendTunnelLeaf(self, value):
		self._set_attribute('isAppendTunnelLeaf', value)

	@property
	def IsPrependDut(self):
		"""Enables prepend DUT to the ERO/SERO list.

		Returns:
			bool
		"""
		return self._get_attribute('isPrependDut')
	@IsPrependDut.setter
	def IsPrependDut(self, value):
		self._set_attribute('isPrependDut', value)

	@property
	def IsSendingAsEro(self):
		"""If enabled, the entire configuration would go as ERO.

		Returns:
			bool
		"""
		return self._get_attribute('isSendingAsEro')
	@IsSendingAsEro.setter
	def IsSendingAsEro(self, value):
		self._set_attribute('isSendingAsEro', value)

	@property
	def IsSendingAsSero(self):
		"""If enabled, the entire configuration would go as SERO.

		Returns:
			bool
		"""
		return self._get_attribute('isSendingAsSero')
	@IsSendingAsSero.setter
	def IsSendingAsSero(self, value):
		self._set_attribute('isSendingAsSero', value)

	@property
	def SubObjectList(self):
		"""The sub-object list for this ERO/SERO can be configured by typing it as a string. Input String: = NULL| [<Subobject> ;< Subobject list>] Subobject: = <AS :< 1-65535> :< S|L>| <IP :< IP Addr>/<1-32> :< S|L> IP Addr: = <0-255>.<0-255>.<0-255>.<0-255> NULL: =Example. IP:2.2.2.2/24:S;AS:100:L;IP:33.33.33.33/32:S

		Returns:
			str
		"""
		return self._get_attribute('subObjectList')
	@SubObjectList.setter
	def SubObjectList(self, value):
		self._set_attribute('subObjectList', value)

	@property
	def TunnelLeafCount(self):
		"""The count of tunnel leaf.

		Returns:
			number
		"""
		return self._get_attribute('tunnelLeafCount')
	@TunnelLeafCount.setter
	def TunnelLeafCount(self, value):
		self._set_attribute('tunnelLeafCount', value)

	@property
	def TunnelLeafHopType(self):
		"""It is enabled if Append Leaf is enabled. Based on the input, corresponding L bit in the packet is set.

		Returns:
			str(strict|loose)
		"""
		return self._get_attribute('tunnelLeafHopType')
	@TunnelLeafHopType.setter
	def TunnelLeafHopType(self, value):
		self._set_attribute('tunnelLeafHopType', value)

	@property
	def TunnelLeafIpStart(self):
		"""It contains the start IP address of leaf for which the ERO/SERO will be configured.

		Returns:
			str
		"""
		return self._get_attribute('tunnelLeafIpStart')
	@TunnelLeafIpStart.setter
	def TunnelLeafIpStart(self, value):
		self._set_attribute('tunnelLeafIpStart', value)

	@property
	def TunnelLeafPrefixLength(self):
		"""Prefix length of tunnel leaf.

		Returns:
			number
		"""
		return self._get_attribute('tunnelLeafPrefixLength')
	@TunnelLeafPrefixLength.setter
	def TunnelLeafPrefixLength(self, value):
		self._set_attribute('tunnelLeafPrefixLength', value)

	def add(self, DutHopType=None, DutPrefixLength=None, Enabled=None, IsAppendTunnelLeaf=None, IsPrependDut=None, IsSendingAsEro=None, IsSendingAsSero=None, SubObjectList=None, TunnelLeafCount=None, TunnelLeafHopType=None, TunnelLeafIpStart=None, TunnelLeafPrefixLength=None):
		"""Adds a new tunnelHeadToLeaf node on the server and retrieves it in this instance.

		Args:
			DutHopType (str(strict|loose)): Based on the input, the corresponding L bit in the packet is set.
			DutPrefixLength (number): Prefix length of DUT.
			Enabled (bool): It enables or disables the ERO/SERO specific configuration.
			IsAppendTunnelLeaf (bool): If enabled, this appends the tunnel leaf at the end of the ERO/SERO list in the packet.
			IsPrependDut (bool): Enables prepend DUT to the ERO/SERO list.
			IsSendingAsEro (bool): If enabled, the entire configuration would go as ERO.
			IsSendingAsSero (bool): If enabled, the entire configuration would go as SERO.
			SubObjectList (str): The sub-object list for this ERO/SERO can be configured by typing it as a string. Input String: = NULL| [<Subobject> ;< Subobject list>] Subobject: = <AS :< 1-65535> :< S|L>| <IP :< IP Addr>/<1-32> :< S|L> IP Addr: = <0-255>.<0-255>.<0-255>.<0-255> NULL: =Example. IP:2.2.2.2/24:S;AS:100:L;IP:33.33.33.33/32:S
			TunnelLeafCount (number): The count of tunnel leaf.
			TunnelLeafHopType (str(strict|loose)): It is enabled if Append Leaf is enabled. Based on the input, corresponding L bit in the packet is set.
			TunnelLeafIpStart (str): It contains the start IP address of leaf for which the ERO/SERO will be configured.
			TunnelLeafPrefixLength (number): Prefix length of tunnel leaf.

		Returns:
			self: This instance with all currently retrieved tunnelHeadToLeaf data using find and the newly added tunnelHeadToLeaf data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the tunnelHeadToLeaf data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, DutHopType=None, DutPrefixLength=None, Enabled=None, HeadIpStart=None, IsAppendTunnelLeaf=None, IsPrependDut=None, IsSendingAsEro=None, IsSendingAsSero=None, SubObjectList=None, TunnelLeafCount=None, TunnelLeafHopType=None, TunnelLeafIpStart=None, TunnelLeafPrefixLength=None):
		"""Finds and retrieves tunnelHeadToLeaf data from the server.

		All named parameters support regex and can be used to selectively retrieve tunnelHeadToLeaf data from the server.
		By default the find method takes no parameters and will retrieve all tunnelHeadToLeaf data from the server.

		Args:
			DutHopType (str(strict|loose)): Based on the input, the corresponding L bit in the packet is set.
			DutPrefixLength (number): Prefix length of DUT.
			Enabled (bool): It enables or disables the ERO/SERO specific configuration.
			HeadIpStart (str): It is the tunnel head IP address for which the ERO/SERO is being configured.
			IsAppendTunnelLeaf (bool): If enabled, this appends the tunnel leaf at the end of the ERO/SERO list in the packet.
			IsPrependDut (bool): Enables prepend DUT to the ERO/SERO list.
			IsSendingAsEro (bool): If enabled, the entire configuration would go as ERO.
			IsSendingAsSero (bool): If enabled, the entire configuration would go as SERO.
			SubObjectList (str): The sub-object list for this ERO/SERO can be configured by typing it as a string. Input String: = NULL| [<Subobject> ;< Subobject list>] Subobject: = <AS :< 1-65535> :< S|L>| <IP :< IP Addr>/<1-32> :< S|L> IP Addr: = <0-255>.<0-255>.<0-255>.<0-255> NULL: =Example. IP:2.2.2.2/24:S;AS:100:L;IP:33.33.33.33/32:S
			TunnelLeafCount (number): The count of tunnel leaf.
			TunnelLeafHopType (str(strict|loose)): It is enabled if Append Leaf is enabled. Based on the input, corresponding L bit in the packet is set.
			TunnelLeafIpStart (str): It contains the start IP address of leaf for which the ERO/SERO will be configured.
			TunnelLeafPrefixLength (number): Prefix length of tunnel leaf.

		Returns:
			self: This instance with matching tunnelHeadToLeaf data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of tunnelHeadToLeaf data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the tunnelHeadToLeaf data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
