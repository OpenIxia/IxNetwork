from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class DataMdt(Base):
	"""The DataMdt class encapsulates a user managed dataMdt node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the DataMdt property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'dataMdt'

	def __init__(self, parent):
		super(DataMdt, self).__init__(parent)

	@property
	def LearnedMdtState(self):
		"""An instance of the LearnedMdtState class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.pimsm.router.interface.datamdt.learnedmdtstate.learnedmdtstate.LearnedMdtState)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.pimsm.router.interface.datamdt.learnedmdtstate.learnedmdtstate import LearnedMdtState
		return LearnedMdtState(self)

	@property
	def ActivationInterval(self):
		"""The time period after which packets will be sent (to support the switchover from the default MDT to the data MDT). The default is 60 seconds.

		Returns:
			number
		"""
		return self._get_attribute('activationInterval')
	@ActivationInterval.setter
	def ActivationInterval(self, value):
		self._set_attribute('activationInterval', value)

	@property
	def CeGroupAddress(self):
		"""A multicast IPv4 address for the first CE destination group in the range.The default is 225.0.0.0.

		Returns:
			str
		"""
		return self._get_attribute('ceGroupAddress')
	@CeGroupAddress.setter
	def CeGroupAddress(self, value):
		self._set_attribute('ceGroupAddress', value)

	@property
	def CeGroupCount(self):
		"""The number of CE group addresses in the range.

		Returns:
			number
		"""
		return self._get_attribute('ceGroupCount')
	@CeGroupCount.setter
	def CeGroupCount(self, value):
		self._set_attribute('ceGroupCount', value)

	@property
	def CeSourceAddress(self):
		"""A unicast IPv4 address for the first CE source.

		Returns:
			str
		"""
		return self._get_attribute('ceSourceAddress')
	@CeSourceAddress.setter
	def CeSourceAddress(self, value):
		self._set_attribute('ceSourceAddress', value)

	@property
	def CeSourceCount(self):
		"""The number of CE Source Addresses in the range. Used with fully-meshed range type.

		Returns:
			number
		"""
		return self._get_attribute('ceSourceCount')
	@CeSourceCount.setter
	def CeSourceCount(self, value):
		self._set_attribute('ceSourceCount', value)

	@property
	def DataMdtGroupAddress(self):
		"""The first multicast group address in the data MDT range. The default is 230.0.0.0.

		Returns:
			str
		"""
		return self._get_attribute('dataMdtGroupAddress')
	@DataMdtGroupAddress.setter
	def DataMdtGroupAddress(self, value):
		self._set_attribute('dataMdtGroupAddress', value)

	@property
	def DataMdtGroupAddressCount(self):
		"""The number of group addresses in the data MDT range. The default is 1.

		Returns:
			number
		"""
		return self._get_attribute('dataMdtGroupAddressCount')
	@DataMdtGroupAddressCount.setter
	def DataMdtGroupAddressCount(self, value):
		self._set_attribute('dataMdtGroupAddressCount', value)

	@property
	def DiscardLearnedState(self):
		"""If enabled, learned states associated with this data MDT range will be discarded.The default is enabled.

		Returns:
			bool
		"""
		return self._get_attribute('discardLearnedState')
	@DiscardLearnedState.setter
	def DiscardLearnedState(self, value):
		self._set_attribute('discardLearnedState', value)

	@property
	def Enabled(self):
		"""If enabled, the switchover from the default MDT to the data MDT will triggered. The default is disabled.

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def PackTlv(self):
		"""Enables packing of the data MDT type-length-values (TLVs). Multiple TLVs can be transmitted in one message.The default is enabled.

		Returns:
			bool
		"""
		return self._get_attribute('packTlv')
	@PackTlv.setter
	def PackTlv(self, value):
		self._set_attribute('packTlv', value)

	@property
	def RangeType(self):
		"""The type of data MDT range.

		Returns:
			str(fullyMeshed|oneToOne)
		"""
		return self._get_attribute('rangeType')
	@RangeType.setter
	def RangeType(self, value):
		self._set_attribute('rangeType', value)

	def add(self, ActivationInterval=None, CeGroupAddress=None, CeGroupCount=None, CeSourceAddress=None, CeSourceCount=None, DataMdtGroupAddress=None, DataMdtGroupAddressCount=None, DiscardLearnedState=None, Enabled=None, PackTlv=None, RangeType=None):
		"""Adds a new dataMdt node on the server and retrieves it in this instance.

		Args:
			ActivationInterval (number): The time period after which packets will be sent (to support the switchover from the default MDT to the data MDT). The default is 60 seconds.
			CeGroupAddress (str): A multicast IPv4 address for the first CE destination group in the range.The default is 225.0.0.0.
			CeGroupCount (number): The number of CE group addresses in the range.
			CeSourceAddress (str): A unicast IPv4 address for the first CE source.
			CeSourceCount (number): The number of CE Source Addresses in the range. Used with fully-meshed range type.
			DataMdtGroupAddress (str): The first multicast group address in the data MDT range. The default is 230.0.0.0.
			DataMdtGroupAddressCount (number): The number of group addresses in the data MDT range. The default is 1.
			DiscardLearnedState (bool): If enabled, learned states associated with this data MDT range will be discarded.The default is enabled.
			Enabled (bool): If enabled, the switchover from the default MDT to the data MDT will triggered. The default is disabled.
			PackTlv (bool): Enables packing of the data MDT type-length-values (TLVs). Multiple TLVs can be transmitted in one message.The default is enabled.
			RangeType (str(fullyMeshed|oneToOne)): The type of data MDT range.

		Returns:
			self: This instance with all currently retrieved dataMdt data using find and the newly added dataMdt data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the dataMdt data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, ActivationInterval=None, CeGroupAddress=None, CeGroupCount=None, CeSourceAddress=None, CeSourceCount=None, DataMdtGroupAddress=None, DataMdtGroupAddressCount=None, DiscardLearnedState=None, Enabled=None, PackTlv=None, RangeType=None):
		"""Finds and retrieves dataMdt data from the server.

		All named parameters support regex and can be used to selectively retrieve dataMdt data from the server.
		By default the find method takes no parameters and will retrieve all dataMdt data from the server.

		Args:
			ActivationInterval (number): The time period after which packets will be sent (to support the switchover from the default MDT to the data MDT). The default is 60 seconds.
			CeGroupAddress (str): A multicast IPv4 address for the first CE destination group in the range.The default is 225.0.0.0.
			CeGroupCount (number): The number of CE group addresses in the range.
			CeSourceAddress (str): A unicast IPv4 address for the first CE source.
			CeSourceCount (number): The number of CE Source Addresses in the range. Used with fully-meshed range type.
			DataMdtGroupAddress (str): The first multicast group address in the data MDT range. The default is 230.0.0.0.
			DataMdtGroupAddressCount (number): The number of group addresses in the data MDT range. The default is 1.
			DiscardLearnedState (bool): If enabled, learned states associated with this data MDT range will be discarded.The default is enabled.
			Enabled (bool): If enabled, the switchover from the default MDT to the data MDT will triggered. The default is disabled.
			PackTlv (bool): Enables packing of the data MDT type-length-values (TLVs). Multiple TLVs can be transmitted in one message.The default is enabled.
			RangeType (str(fullyMeshed|oneToOne)): The type of data MDT range.

		Returns:
			self: This instance with matching dataMdt data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of dataMdt data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the dataMdt data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
