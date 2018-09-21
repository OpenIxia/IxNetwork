from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Parameter(Base):
	"""The Parameter class encapsulates a system managed parameter node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Parameter property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'parameter'

	def __init__(self, parent):
		super(Parameter, self).__init__(parent)

	@property
	def Bool(self):
		"""An instance of the Bool class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.applibprofile.applibflow.connection.parameter.bool.bool.Bool)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.applibprofile.applibflow.connection.parameter.bool.bool import Bool
		return Bool(self)

	@property
	def Choice(self):
		"""An instance of the Choice class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.applibprofile.applibflow.connection.parameter.choice.choice.Choice)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.applibprofile.applibflow.connection.parameter.choice.choice import Choice
		return Choice(self)

	@property
	def Hex(self):
		"""An instance of the Hex class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.applibprofile.applibflow.connection.parameter.hex.hex.Hex)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.applibprofile.applibflow.connection.parameter.hex.hex import Hex
		return Hex(self)

	@property
	def Number(self):
		"""An instance of the Number class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.applibprofile.applibflow.connection.parameter.number.number.Number)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.applibprofile.applibflow.connection.parameter.number.number import Number
		return Number(self)

	@property
	def Range(self):
		"""An instance of the Range class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.applibprofile.applibflow.connection.parameter.range.range.Range)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.applibprofile.applibflow.connection.parameter.range.range import Range
		return Range(self)

	@property
	def String(self):
		"""An instance of the String class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.applibprofile.applibflow.connection.parameter.string.string.String)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.applibprofile.applibflow.connection.parameter.string.string import String
		return String(self)

	@property
	def DisplayValue(self):
		"""Current parameter UI Display Value

		Returns:
			str
		"""
		return self._get_attribute('displayValue')

	@property
	def Option(self):
		"""Each parameter has one or multiple options. Runtime supported options for specific parameter can be retrieved from supportedOptions attribute

		Returns:
			str(choice|range|value)
		"""
		return self._get_attribute('option')
	@Option.setter
	def Option(self, value):
		self._set_attribute('option', value)

	@property
	def SupportedOptions(self):
		"""Runtime supported options for a specific parameter

		Returns:
			list(str[choice|range|value])
		"""
		return self._get_attribute('supportedOptions')

	def find(self, DisplayValue=None, Option=None, SupportedOptions=None):
		"""Finds and retrieves parameter data from the server.

		All named parameters support regex and can be used to selectively retrieve parameter data from the server.
		By default the find method takes no parameters and will retrieve all parameter data from the server.

		Args:
			DisplayValue (str): Current parameter UI Display Value
			Option (str(choice|range|value)): Each parameter has one or multiple options. Runtime supported options for specific parameter can be retrieved from supportedOptions attribute
			SupportedOptions (list(str[choice|range|value])): Runtime supported options for a specific parameter

		Returns:
			self: This instance with matching parameter data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of parameter data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the parameter data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
