from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class SpbIsIdRange(Base):
	"""The SpbIsIdRange class encapsulates a user managed spbIsIdRange node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the SpbIsIdRange property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'spbIsIdRange'

	def __init__(self, parent):
		super(SpbIsIdRange, self).__init__(parent)

	@property
	def CMacAddressCount(self):
		"""The number of C-MAC for each C-MAC range. The default is 1. Maximum value is 4095. The minimum value is 1.

		Returns:
			number
		"""
		return self._get_attribute('cMacAddressCount')
	@CMacAddressCount.setter
	def CMacAddressCount(self, value):
		self._set_attribute('cMacAddressCount', value)

	@property
	def CMacAddressStep(self):
		"""The amount to increment each successive C-MAC address from the starting CMAC address.

		Returns:
			str
		"""
		return self._get_attribute('cMacAddressStep')
	@CMacAddressStep.setter
	def CMacAddressStep(self, value):
		self._set_attribute('cMacAddressStep', value)

	@property
	def CVlan(self):
		"""The number of stacked VLAN. The minimum value is 1. The maximum value is 4095. The default is 1.

		Returns:
			number
		"""
		return self._get_attribute('cVlan')
	@CVlan.setter
	def CVlan(self, value):
		self._set_attribute('cVlan', value)

	@property
	def Enabled(self):
		"""If true, the topology range will be part of the simulated network.

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def ISid(self):
		"""The I-component Service Instance identifier. The maximum value is 16777215. The minimum value is 0.

		Returns:
			number
		"""
		return self._get_attribute('iSid')
	@ISid.setter
	def ISid(self, value):
		self._set_attribute('iSid', value)

	@property
	def ITagEthernetType(self):
		"""The I-Tag Ethernet type. An I-Tag is a multiplexing tag for service instance scaling in Provider Bridged Networks.

		Returns:
			number
		"""
		return self._get_attribute('iTagEthernetType')

	@property
	def RBit(self):
		"""The Restart State bit.

		Returns:
			bool
		"""
		return self._get_attribute('rBit')
	@RBit.setter
	def RBit(self, value):
		self._set_attribute('rBit', value)

	@property
	def SVlan(self):
		"""The number of single VLAN. The minimum value is 1. The maximum value is 4095. The default is 1.

		Returns:
			number
		"""
		return self._get_attribute('sVlan')
	@SVlan.setter
	def SVlan(self, value):
		self._set_attribute('sVlan', value)

	@property
	def StartCmacAddress(self):
		"""The starting C-MAC address for the C_MAC range.

		Returns:
			str
		"""
		return self._get_attribute('startCmacAddress')
	@StartCmacAddress.setter
	def StartCmacAddress(self, value):
		self._set_attribute('startCmacAddress', value)

	@property
	def TBit(self):
		"""The external route tag bit.

		Returns:
			bool
		"""
		return self._get_attribute('tBit')
	@TBit.setter
	def TBit(self, value):
		self._set_attribute('tBit', value)

	@property
	def TrafficDestMacAddress(self):
		"""The traffic-destination MAC address.

		Returns:
			str
		"""
		return self._get_attribute('trafficDestMacAddress')
	@TrafficDestMacAddress.setter
	def TrafficDestMacAddress(self, value):
		self._set_attribute('trafficDestMacAddress', value)

	@property
	def TransmissionType(self):
		"""Select the type of packet transmission. Options include Unicast and Multicast.

		Returns:
			number
		"""
		return self._get_attribute('transmissionType')
	@TransmissionType.setter
	def TransmissionType(self, value):
		self._set_attribute('transmissionType', value)

	@property
	def VlanType(self):
		"""Select the VLAN type. Options include Single VLAN and Stacked VLAN. Selecting Stacked VLAN activates the C-VLAN options. The Default option is Single VLAN.

		Returns:
			number
		"""
		return self._get_attribute('vlanType')
	@VlanType.setter
	def VlanType(self, value):
		self._set_attribute('vlanType', value)

	def add(self, CMacAddressCount=None, CMacAddressStep=None, CVlan=None, Enabled=None, ISid=None, RBit=None, SVlan=None, StartCmacAddress=None, TBit=None, TrafficDestMacAddress=None, TransmissionType=None, VlanType=None):
		"""Adds a new spbIsIdRange node on the server and retrieves it in this instance.

		Args:
			CMacAddressCount (number): The number of C-MAC for each C-MAC range. The default is 1. Maximum value is 4095. The minimum value is 1.
			CMacAddressStep (str): The amount to increment each successive C-MAC address from the starting CMAC address.
			CVlan (number): The number of stacked VLAN. The minimum value is 1. The maximum value is 4095. The default is 1.
			Enabled (bool): If true, the topology range will be part of the simulated network.
			ISid (number): The I-component Service Instance identifier. The maximum value is 16777215. The minimum value is 0.
			RBit (bool): The Restart State bit.
			SVlan (number): The number of single VLAN. The minimum value is 1. The maximum value is 4095. The default is 1.
			StartCmacAddress (str): The starting C-MAC address for the C_MAC range.
			TBit (bool): The external route tag bit.
			TrafficDestMacAddress (str): The traffic-destination MAC address.
			TransmissionType (number): Select the type of packet transmission. Options include Unicast and Multicast.
			VlanType (number): Select the VLAN type. Options include Single VLAN and Stacked VLAN. Selecting Stacked VLAN activates the C-VLAN options. The Default option is Single VLAN.

		Returns:
			self: This instance with all currently retrieved spbIsIdRange data using find and the newly added spbIsIdRange data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the spbIsIdRange data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, CMacAddressCount=None, CMacAddressStep=None, CVlan=None, Enabled=None, ISid=None, ITagEthernetType=None, RBit=None, SVlan=None, StartCmacAddress=None, TBit=None, TrafficDestMacAddress=None, TransmissionType=None, VlanType=None):
		"""Finds and retrieves spbIsIdRange data from the server.

		All named parameters support regex and can be used to selectively retrieve spbIsIdRange data from the server.
		By default the find method takes no parameters and will retrieve all spbIsIdRange data from the server.

		Args:
			CMacAddressCount (number): The number of C-MAC for each C-MAC range. The default is 1. Maximum value is 4095. The minimum value is 1.
			CMacAddressStep (str): The amount to increment each successive C-MAC address from the starting CMAC address.
			CVlan (number): The number of stacked VLAN. The minimum value is 1. The maximum value is 4095. The default is 1.
			Enabled (bool): If true, the topology range will be part of the simulated network.
			ISid (number): The I-component Service Instance identifier. The maximum value is 16777215. The minimum value is 0.
			ITagEthernetType (number): The I-Tag Ethernet type. An I-Tag is a multiplexing tag for service instance scaling in Provider Bridged Networks.
			RBit (bool): The Restart State bit.
			SVlan (number): The number of single VLAN. The minimum value is 1. The maximum value is 4095. The default is 1.
			StartCmacAddress (str): The starting C-MAC address for the C_MAC range.
			TBit (bool): The external route tag bit.
			TrafficDestMacAddress (str): The traffic-destination MAC address.
			TransmissionType (number): Select the type of packet transmission. Options include Unicast and Multicast.
			VlanType (number): Select the VLAN type. Options include Single VLAN and Stacked VLAN. Selecting Stacked VLAN activates the C-VLAN options. The Default option is Single VLAN.

		Returns:
			self: This instance with matching spbIsIdRange data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of spbIsIdRange data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the spbIsIdRange data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
