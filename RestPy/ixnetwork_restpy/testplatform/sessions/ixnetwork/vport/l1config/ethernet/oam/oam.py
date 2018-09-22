from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Oam(Base):
	"""The Oam class encapsulates a required oam node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Oam property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'oam'

	def __init__(self, parent):
		super(Oam, self).__init__(parent)

	@property
	def EnableTlvOption(self):
		"""If true, enables the tlv option.

		Returns:
			bool
		"""
		return self._get_attribute('enableTlvOption')
	@EnableTlvOption.setter
	def EnableTlvOption(self, value):
		self._set_attribute('enableTlvOption', value)

	@property
	def Enabled(self):
		"""If true, enables OAM for the Ten Gig Lan port.

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def IdleTimer(self):
		"""The timer used to ensure OAM sub layer adheres to maximum number of OAMPDUs per second and emits at least one OAMPDU per second. The default is 1, minimum value is 1 and maximum value is 10.

		Returns:
			number
		"""
		return self._get_attribute('idleTimer')
	@IdleTimer.setter
	def IdleTimer(self, value):
		self._set_attribute('idleTimer', value)

	@property
	def LinkEvents(self):
		"""If true, enables link event interpreting support in Ixia port.

		Returns:
			bool
		"""
		return self._get_attribute('linkEvents')
	@LinkEvents.setter
	def LinkEvents(self, value):
		self._set_attribute('linkEvents', value)

	@property
	def Loopback(self):
		"""If true, enables the loopback. when an ixia port goes to loopback mode, then all non oam packets coming to that port gets looped back.

		Returns:
			bool
		"""
		return self._get_attribute('loopback')
	@Loopback.setter
	def Loopback(self, value):
		self._set_attribute('loopback', value)

	@property
	def MacAddress(self):
		"""Mac address of the local DTE. By default, the mac address is automatically generated from card, port and other related information.

		Returns:
			str
		"""
		return self._get_attribute('macAddress')
	@MacAddress.setter
	def MacAddress(self, value):
		self._set_attribute('macAddress', value)

	@property
	def MaxOAMPDUSize(self):
		"""Indicates the maximum OAMPDU size supported by local DTE. The default is 1500, minimum is 64, and maximum is 1500 in octets.

		Returns:
			number
		"""
		return self._get_attribute('maxOAMPDUSize')
	@MaxOAMPDUSize.setter
	def MaxOAMPDUSize(self, value):
		self._set_attribute('maxOAMPDUSize', value)

	@property
	def OrganizationUniqueIdentifier(self):
		"""This three-octet field contains a 24-bit Organizationally Unique Identifier. The default value is 00-01-00. Any three octets hex value can be given.

		Returns:
			str
		"""
		return self._get_attribute('organizationUniqueIdentifier')
	@OrganizationUniqueIdentifier.setter
	def OrganizationUniqueIdentifier(self, value):
		self._set_attribute('organizationUniqueIdentifier', value)

	@property
	def TlvType(self):
		"""Indicates the tlv type.

		Returns:
			str
		"""
		return self._get_attribute('tlvType')
	@TlvType.setter
	def TlvType(self, value):
		self._set_attribute('tlvType', value)

	@property
	def TlvValue(self):
		"""Enters the tlv value.

		Returns:
			str
		"""
		return self._get_attribute('tlvValue')
	@TlvValue.setter
	def TlvValue(self, value):
		self._set_attribute('tlvValue', value)

	@property
	def VendorSpecificInformation(self):
		"""Contains the vendor specific information that is used to differentiate a vendor's product modes/version. Default is 00000000.

		Returns:
			str
		"""
		return self._get_attribute('vendorSpecificInformation')
	@VendorSpecificInformation.setter
	def VendorSpecificInformation(self, value):
		self._set_attribute('vendorSpecificInformation', value)
