from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Bands(Base):
	"""The Bands class encapsulates a system managed bands node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Bands property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'bands'

	def __init__(self, parent):
		super(Bands, self).__init__(parent)

	@property
	def BandDescription(self):
		"""The description of the Meter. It is a read-only field.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('bandDescription')

	@property
	def BandType(self):
		"""Select the band type from the list. Options are as follows: 1) Drop 2) DSCP Remark 3) Experimenter

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('bandType')

	@property
	def BurstSize(self):
		"""This indicates the length of the packet or byte burst to consider for applying the meter. The default value is 1.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('burstSize')

	@property
	def Count(self):
		"""Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group

		Returns:
			number
		"""
		return self._get_attribute('count')

	@property
	def DescriptiveName(self):
		"""Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context

		Returns:
			str
		"""
		return self._get_attribute('descriptiveName')

	@property
	def Experimenter(self):
		"""Indicats the experimenter ID. The default value is 1.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('experimenter')

	@property
	def MeterIndex(self):
		"""Indicats the Parent Meter Index

		Returns:
			list(str)
		"""
		return self._get_attribute('meterIndex')

	@property
	def Multiplier(self):
		"""Number of instances per parent instance (multiplier)

		Returns:
			number
		"""
		return self._get_attribute('multiplier')
	@Multiplier.setter
	def Multiplier(self, value):
		self._set_attribute('multiplier', value)

	@property
	def Name(self):
		"""Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			str
		"""
		return self._get_attribute('name')
	@Name.setter
	def Name(self, value):
		self._set_attribute('name', value)

	@property
	def PrecedenceLevel(self):
		"""This indicates the amount by which the drop precedence of the packet should be increased if the band is exceeded. The default value is 0.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('precedenceLevel')

	@property
	def Rate(self):
		"""This indicates the rate value above which the corresponding band may apply to packets. The default value is 1.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('rate')

	def find(self, Count=None, DescriptiveName=None, MeterIndex=None, Multiplier=None, Name=None):
		"""Finds and retrieves bands data from the server.

		All named parameters support regex and can be used to selectively retrieve bands data from the server.
		By default the find method takes no parameters and will retrieve all bands data from the server.

		Args:
			Count (number): Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			MeterIndex (list(str)): Indicats the Parent Meter Index
			Multiplier (number): Number of instances per parent instance (multiplier)
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			self: This instance with matching bands data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of bands data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the bands data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
