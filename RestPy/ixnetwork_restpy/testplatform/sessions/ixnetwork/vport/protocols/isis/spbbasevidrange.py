from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class SpbBaseVidRange(Base):
	"""The SpbBaseVidRange class encapsulates a user managed spbBaseVidRange node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the SpbBaseVidRange property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'spbBaseVidRange'

	def __init__(self, parent):
		super(SpbBaseVidRange, self).__init__(parent)

	@property
	def SpbIsIdRange(self):
		"""An instance of the SpbIsIdRange class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.spbisidrange.SpbIsIdRange)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.isis.spbisidrange import SpbIsIdRange
		return SpbIsIdRange(self)

	@property
	def BMacAddress(self):
		"""The B-MAC address. The default value is the System ID of the router.

		Returns:
			str
		"""
		return self._get_attribute('bMacAddress')
	@BMacAddress.setter
	def BMacAddress(self, value):
		self._set_attribute('bMacAddress', value)

	@property
	def BVlanPriority(self):
		"""The user priority of the Base VLAN tag.

		Returns:
			number
		"""
		return self._get_attribute('bVlanPriority')
	@BVlanPriority.setter
	def BVlanPriority(self, value):
		self._set_attribute('bVlanPriority', value)

	@property
	def BVlanTpId(self):
		"""The tag priority identifier for base VLAN.

		Returns:
			number
		"""
		return self._get_attribute('bVlanTpId')
	@BVlanTpId.setter
	def BVlanTpId(self, value):
		self._set_attribute('bVlanTpId', value)

	@property
	def BaseVid(self):
		"""The Base VLAN ID. The default value is 1. The maximum value is 4095. The minimum value is 0.

		Returns:
			number
		"""
		return self._get_attribute('baseVid')
	@BaseVid.setter
	def BaseVid(self, value):
		self._set_attribute('baseVid', value)

	@property
	def EctAlgorithmType(self):
		"""The type of SPB Equal Cost Tree (ECT) algorithm. The default value is 01-80-C2-01.

		Returns:
			number
		"""
		return self._get_attribute('ectAlgorithmType')
	@EctAlgorithmType.setter
	def EctAlgorithmType(self, value):
		self._set_attribute('ectAlgorithmType', value)

	@property
	def EnableAutoBmacEnabled(self):
		"""If true, enables auto base MAC address.

		Returns:
			bool
		"""
		return self._get_attribute('enableAutoBmacEnabled')
	@EnableAutoBmacEnabled.setter
	def EnableAutoBmacEnabled(self, value):
		self._set_attribute('enableAutoBmacEnabled', value)

	@property
	def EnableUseFlagBit(self):
		"""If set to true, allows to use flag bit.

		Returns:
			bool
		"""
		return self._get_attribute('enableUseFlagBit')
	@EnableUseFlagBit.setter
	def EnableUseFlagBit(self, value):
		self._set_attribute('enableUseFlagBit', value)

	def add(self, BMacAddress=None, BVlanPriority=None, BVlanTpId=None, BaseVid=None, EctAlgorithmType=None, EnableAutoBmacEnabled=None, EnableUseFlagBit=None):
		"""Adds a new spbBaseVidRange node on the server and retrieves it in this instance.

		Args:
			BMacAddress (str): The B-MAC address. The default value is the System ID of the router.
			BVlanPriority (number): The user priority of the Base VLAN tag.
			BVlanTpId (number): The tag priority identifier for base VLAN.
			BaseVid (number): The Base VLAN ID. The default value is 1. The maximum value is 4095. The minimum value is 0.
			EctAlgorithmType (number): The type of SPB Equal Cost Tree (ECT) algorithm. The default value is 01-80-C2-01.
			EnableAutoBmacEnabled (bool): If true, enables auto base MAC address.
			EnableUseFlagBit (bool): If set to true, allows to use flag bit.

		Returns:
			self: This instance with all currently retrieved spbBaseVidRange data using find and the newly added spbBaseVidRange data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the spbBaseVidRange data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, BMacAddress=None, BVlanPriority=None, BVlanTpId=None, BaseVid=None, EctAlgorithmType=None, EnableAutoBmacEnabled=None, EnableUseFlagBit=None):
		"""Finds and retrieves spbBaseVidRange data from the server.

		All named parameters support regex and can be used to selectively retrieve spbBaseVidRange data from the server.
		By default the find method takes no parameters and will retrieve all spbBaseVidRange data from the server.

		Args:
			BMacAddress (str): The B-MAC address. The default value is the System ID of the router.
			BVlanPriority (number): The user priority of the Base VLAN tag.
			BVlanTpId (number): The tag priority identifier for base VLAN.
			BaseVid (number): The Base VLAN ID. The default value is 1. The maximum value is 4095. The minimum value is 0.
			EctAlgorithmType (number): The type of SPB Equal Cost Tree (ECT) algorithm. The default value is 01-80-C2-01.
			EnableAutoBmacEnabled (bool): If true, enables auto base MAC address.
			EnableUseFlagBit (bool): If set to true, allows to use flag bit.

		Returns:
			self: This instance with matching spbBaseVidRange data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of spbBaseVidRange data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the spbBaseVidRange data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
