from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class TapSettings(Base):
	"""The TapSettings class encapsulates a system managed tapSettings node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the TapSettings property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'tapSettings'

	def __init__(self, parent):
		super(TapSettings, self).__init__(parent)

	@property
	def Parameter(self):
		"""An instance of the Parameter class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.availablehardware.chassis.card.port.tapsettings.parameter.parameter.Parameter)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.availablehardware.chassis.card.port.tapsettings.parameter.parameter import Parameter
		return Parameter(self)

	def find(self):
		"""Finds and retrieves tapSettings data from the server.

		All named parameters support regex and can be used to selectively retrieve tapSettings data from the server.
		By default the find method takes no parameters and will retrieve all tapSettings data from the server.

		Returns:
			self: This instance with matching tapSettings data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of tapSettings data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the tapSettings data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
