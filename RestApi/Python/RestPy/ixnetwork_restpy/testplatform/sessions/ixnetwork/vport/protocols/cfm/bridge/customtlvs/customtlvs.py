from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class CustomTlvs(Base):
	"""The CustomTlvs class encapsulates a user managed customTlvs node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the CustomTlvs property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'customTlvs'

	def __init__(self, parent):
		super(CustomTlvs, self).__init__(parent)

	@property
	def Enabled(self):
		"""If true, the custom TLV is enabled.

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def IncludeInCcm(self):
		"""If true, a custom TLV is included in the bridge CCM messages.

		Returns:
			bool
		"""
		return self._get_attribute('includeInCcm')
	@IncludeInCcm.setter
	def IncludeInCcm(self, value):
		self._set_attribute('includeInCcm', value)

	@property
	def IncludeInLbm(self):
		"""If true, a custom TLV is included in the bridge loopback messages.

		Returns:
			bool
		"""
		return self._get_attribute('includeInLbm')
	@IncludeInLbm.setter
	def IncludeInLbm(self, value):
		self._set_attribute('includeInLbm', value)

	@property
	def IncludeInLbr(self):
		"""If true, a custom TLV is included in the bridge loopback responses messages.

		Returns:
			bool
		"""
		return self._get_attribute('includeInLbr')
	@IncludeInLbr.setter
	def IncludeInLbr(self, value):
		self._set_attribute('includeInLbr', value)

	@property
	def IncludeInLmm(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('includeInLmm')
	@IncludeInLmm.setter
	def IncludeInLmm(self, value):
		self._set_attribute('includeInLmm', value)

	@property
	def IncludeInLmr(self):
		"""NOT DEFINED

		Returns:
			bool
		"""
		return self._get_attribute('includeInLmr')
	@IncludeInLmr.setter
	def IncludeInLmr(self, value):
		self._set_attribute('includeInLmr', value)

	@property
	def IncludeInLtm(self):
		"""If true, a custom TLV is included in the bridge link trace messages.

		Returns:
			bool
		"""
		return self._get_attribute('includeInLtm')
	@IncludeInLtm.setter
	def IncludeInLtm(self, value):
		self._set_attribute('includeInLtm', value)

	@property
	def IncludeInLtr(self):
		"""If true, a custom TLV is included in the bridge link trace response messages.

		Returns:
			bool
		"""
		return self._get_attribute('includeInLtr')
	@IncludeInLtr.setter
	def IncludeInLtr(self, value):
		self._set_attribute('includeInLtr', value)

	@property
	def Length(self):
		"""Enter the data for the TLV length field.

		Returns:
			number
		"""
		return self._get_attribute('length')
	@Length.setter
	def Length(self, value):
		self._set_attribute('length', value)

	@property
	def Type(self):
		"""Enter the data for the TLV type field.

		Returns:
			number
		"""
		return self._get_attribute('type')
	@Type.setter
	def Type(self, value):
		self._set_attribute('type', value)

	@property
	def Value(self):
		"""Enter the data for the TLV value field. This data is in hexadecimal format.

		Returns:
			str
		"""
		return self._get_attribute('value')
	@Value.setter
	def Value(self, value):
		self._set_attribute('value', value)

	def add(self, Enabled=None, IncludeInCcm=None, IncludeInLbm=None, IncludeInLbr=None, IncludeInLmm=None, IncludeInLmr=None, IncludeInLtm=None, IncludeInLtr=None, Length=None, Type=None, Value=None):
		"""Adds a new customTlvs node on the server and retrieves it in this instance.

		Args:
			Enabled (bool): If true, the custom TLV is enabled.
			IncludeInCcm (bool): If true, a custom TLV is included in the bridge CCM messages.
			IncludeInLbm (bool): If true, a custom TLV is included in the bridge loopback messages.
			IncludeInLbr (bool): If true, a custom TLV is included in the bridge loopback responses messages.
			IncludeInLmm (bool): NOT DEFINED
			IncludeInLmr (bool): NOT DEFINED
			IncludeInLtm (bool): If true, a custom TLV is included in the bridge link trace messages.
			IncludeInLtr (bool): If true, a custom TLV is included in the bridge link trace response messages.
			Length (number): Enter the data for the TLV length field.
			Type (number): Enter the data for the TLV type field.
			Value (str): Enter the data for the TLV value field. This data is in hexadecimal format.

		Returns:
			self: This instance with all currently retrieved customTlvs data using find and the newly added customTlvs data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the customTlvs data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, Enabled=None, IncludeInCcm=None, IncludeInLbm=None, IncludeInLbr=None, IncludeInLmm=None, IncludeInLmr=None, IncludeInLtm=None, IncludeInLtr=None, Length=None, Type=None, Value=None):
		"""Finds and retrieves customTlvs data from the server.

		All named parameters support regex and can be used to selectively retrieve customTlvs data from the server.
		By default the find method takes no parameters and will retrieve all customTlvs data from the server.

		Args:
			Enabled (bool): If true, the custom TLV is enabled.
			IncludeInCcm (bool): If true, a custom TLV is included in the bridge CCM messages.
			IncludeInLbm (bool): If true, a custom TLV is included in the bridge loopback messages.
			IncludeInLbr (bool): If true, a custom TLV is included in the bridge loopback responses messages.
			IncludeInLmm (bool): NOT DEFINED
			IncludeInLmr (bool): NOT DEFINED
			IncludeInLtm (bool): If true, a custom TLV is included in the bridge link trace messages.
			IncludeInLtr (bool): If true, a custom TLV is included in the bridge link trace response messages.
			Length (number): Enter the data for the TLV length field.
			Type (number): Enter the data for the TLV type field.
			Value (str): Enter the data for the TLV value field. This data is in hexadecimal format.

		Returns:
			self: This instance with matching customTlvs data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of customTlvs data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the customTlvs data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
