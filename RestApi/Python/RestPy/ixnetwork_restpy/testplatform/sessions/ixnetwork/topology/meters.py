from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Meters(Base):
	"""The Meters class encapsulates a system managed meters node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Meters property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'meters'

	def __init__(self, parent):
		super(Meters, self).__init__(parent)

	@property
	def Bands(self):
		"""An instance of the Bands class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bands.Bands)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.bands import Bands
		return Bands(self)

	@property
	def Active(self):
		"""Activate/Deactivate Configuration

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('active')

	@property
	def Advertise(self):
		"""When this check box is cleared, no meter is advertised when the OpenFlow channel comes up or when the Enable check box is selected or cleared.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('advertise')

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
	def Flags(self):
		"""Select the meter configuration flags from the list.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('flags')

	@property
	def MeterDesc(self):
		"""A description of the meter

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('meterDesc')

	@property
	def MeterId(self):
		"""The value by which a meter is uniquely identified .

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('meterId')

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
	def NumberOfBands(self):
		"""Specify the number of Bands.

		Returns:
			number
		"""
		return self._get_attribute('numberOfBands')
	@NumberOfBands.setter
	def NumberOfBands(self, value):
		self._set_attribute('numberOfBands', value)

	def find(self, Count=None, DescriptiveName=None, Multiplier=None, Name=None, NumberOfBands=None):
		"""Finds and retrieves meters data from the server.

		All named parameters support regex and can be used to selectively retrieve meters data from the server.
		By default the find method takes no parameters and will retrieve all meters data from the server.

		Args:
			Count (number): Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Multiplier (number): Number of instances per parent instance (multiplier)
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario
			NumberOfBands (number): Specify the number of Bands.

		Returns:
			self: This instance with matching meters data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of meters data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the meters data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)

	def SendAllMeterAdd(self):
		"""Executes the sendAllMeterAdd operation on the server.

		Sends a Meter Add on all meters.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally set Arg1 to the current href for this instance

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('SendAllMeterAdd', payload=locals(), response_object=None)

	def SendAllMeterRemove(self):
		"""Executes the sendAllMeterRemove operation on the server.

		Sends a Meter Remove on all meters.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally set Arg1 to the current href for this instance

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('SendAllMeterRemove', payload=locals(), response_object=None)

	def SendMeterAdd(self, Arg2):
		"""Executes the sendMeterAdd operation on the server.

		Sends a Meter Add on selected Meter.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally set Arg1 to the current href for this instance
			Arg2 (list(number)): List of indices into the meter range grid

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('SendMeterAdd', payload=locals(), response_object=None)

	def SendMeterRemove(self, Arg2):
		"""Executes the sendMeterRemove operation on the server.

		Sends a Meter Remove on selected Meter.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally set Arg1 to the current href for this instance
			Arg2 (list(number)): List of indices into the meter range grid

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('SendMeterRemove', payload=locals(), response_object=None)
