from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class CustomTopologySpbNodeIsidRange(Base):
	"""The CustomTopologySpbNodeIsidRange class encapsulates a user managed customTopologySpbNodeIsidRange node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the CustomTopologySpbNodeIsidRange property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'customTopologySpbNodeIsidRange'

	def __init__(self, parent):
		super(CustomTopologySpbNodeIsidRange, self).__init__(parent)

	@property
	def CMacAddressCount(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('cMacAddressCount')
	@CMacAddressCount.setter
	def CMacAddressCount(self, value):
		self._set_attribute('cMacAddressCount', value)

	@property
	def CMacAddressStep(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('cMacAddressStep')
	@CMacAddressStep.setter
	def CMacAddressStep(self, value):
		self._set_attribute('cMacAddressStep', value)

	@property
	def EnableIsid(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('enableIsid')
	@EnableIsid.setter
	def EnableIsid(self, value):
		self._set_attribute('enableIsid', value)

	@property
	def InterNodeCmacAddress(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('interNodeCmacAddress')
	@InterNodeCmacAddress.setter
	def InterNodeCmacAddress(self, value):
		self._set_attribute('interNodeCmacAddress', value)

	@property
	def InterNodeCvlan(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('interNodeCvlan')
	@InterNodeCvlan.setter
	def InterNodeCvlan(self, value):
		self._set_attribute('interNodeCvlan', value)

	@property
	def InterNodeIsIdIncrement(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('interNodeIsIdIncrement')
	@InterNodeIsIdIncrement.setter
	def InterNodeIsIdIncrement(self, value):
		self._set_attribute('interNodeIsIdIncrement', value)

	@property
	def InterNodeSvlan(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('interNodeSvlan')
	@InterNodeSvlan.setter
	def InterNodeSvlan(self, value):
		self._set_attribute('interNodeSvlan', value)

	@property
	def Isid(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('isid')
	@Isid.setter
	def Isid(self, value):
		self._set_attribute('isid', value)

	@property
	def RBit(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('rBit')
	@RBit.setter
	def RBit(self, value):
		self._set_attribute('rBit', value)

	@property
	def StartCmacAddress(self):
		"""NOT DEFINED

		Returns:
			str
		"""
		return self._get_attribute('startCmacAddress')
	@StartCmacAddress.setter
	def StartCmacAddress(self, value):
		self._set_attribute('startCmacAddress', value)

	@property
	def StartCvlan(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('startCvlan')
	@StartCvlan.setter
	def StartCvlan(self, value):
		self._set_attribute('startCvlan', value)

	@property
	def StartSvlan(self):
		"""NOT DEFINED

		Returns:
			number
		"""
		return self._get_attribute('startSvlan')
	@StartSvlan.setter
	def StartSvlan(self, value):
		self._set_attribute('startSvlan', value)

	@property
	def TBit(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('tBit')
	@TBit.setter
	def TBit(self, value):
		self._set_attribute('tBit', value)

	@property
	def TransmissionType(self):
		"""NOT DEFINED

		Returns:
			str(unicast|multicast)
		"""
		return self._get_attribute('transmissionType')
	@TransmissionType.setter
	def TransmissionType(self, value):
		self._set_attribute('transmissionType', value)

	@property
	def VlanType(self):
		"""NOT DEFINED

		Returns:
			str(singleVlan|stackedVlanQinQ)
		"""
		return self._get_attribute('vlanType')
	@VlanType.setter
	def VlanType(self, value):
		self._set_attribute('vlanType', value)

	def add(self, CMacAddressCount=None, CMacAddressStep=None, EnableIsid=None, InterNodeCmacAddress=None, InterNodeCvlan=None, InterNodeIsIdIncrement=None, InterNodeSvlan=None, Isid=None, RBit=None, StartCmacAddress=None, StartCvlan=None, StartSvlan=None, TBit=None, TransmissionType=None, VlanType=None):
		"""Adds a new customTopologySpbNodeIsidRange node on the server and retrieves it in this instance.

		Args:
			CMacAddressCount (number): NOT DEFINED
			CMacAddressStep (str): NOT DEFINED
			EnableIsid (bool): NOT DEFINED
			InterNodeCmacAddress (str): NOT DEFINED
			InterNodeCvlan (number): NOT DEFINED
			InterNodeIsIdIncrement (number): NOT DEFINED
			InterNodeSvlan (number): NOT DEFINED
			Isid (number): NOT DEFINED
			RBit (bool): NOT DEFINED
			StartCmacAddress (str): NOT DEFINED
			StartCvlan (number): NOT DEFINED
			StartSvlan (number): NOT DEFINED
			TBit (bool): NOT DEFINED
			TransmissionType (str(unicast|multicast)): NOT DEFINED
			VlanType (str(singleVlan|stackedVlanQinQ)): NOT DEFINED

		Returns:
			self: This instance with all currently retrieved customTopologySpbNodeIsidRange data using find and the newly added customTopologySpbNodeIsidRange data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the customTopologySpbNodeIsidRange data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, CMacAddressCount=None, CMacAddressStep=None, EnableIsid=None, InterNodeCmacAddress=None, InterNodeCvlan=None, InterNodeIsIdIncrement=None, InterNodeSvlan=None, Isid=None, RBit=None, StartCmacAddress=None, StartCvlan=None, StartSvlan=None, TBit=None, TransmissionType=None, VlanType=None):
		"""Finds and retrieves customTopologySpbNodeIsidRange data from the server.

		All named parameters support regex and can be used to selectively retrieve customTopologySpbNodeIsidRange data from the server.
		By default the find method takes no parameters and will retrieve all customTopologySpbNodeIsidRange data from the server.

		Args:
			CMacAddressCount (number): NOT DEFINED
			CMacAddressStep (str): NOT DEFINED
			EnableIsid (bool): NOT DEFINED
			InterNodeCmacAddress (str): NOT DEFINED
			InterNodeCvlan (number): NOT DEFINED
			InterNodeIsIdIncrement (number): NOT DEFINED
			InterNodeSvlan (number): NOT DEFINED
			Isid (number): NOT DEFINED
			RBit (bool): NOT DEFINED
			StartCmacAddress (str): NOT DEFINED
			StartCvlan (number): NOT DEFINED
			StartSvlan (number): NOT DEFINED
			TBit (bool): NOT DEFINED
			TransmissionType (str(unicast|multicast)): NOT DEFINED
			VlanType (str(singleVlan|stackedVlanQinQ)): NOT DEFINED

		Returns:
			self: This instance with matching customTopologySpbNodeIsidRange data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of customTopologySpbNodeIsidRange data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the customTopologySpbNodeIsidRange data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
