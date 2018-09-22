from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class IsisPseudoInterface(Base):
	"""The IsisPseudoInterface class encapsulates a system managed isisPseudoInterface node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the IsisPseudoInterface property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'isisPseudoInterface'

	def __init__(self, parent):
		super(IsisPseudoInterface, self).__init__(parent)

	@property
	def IsisDcePseudoIfaceAttPoint1Config(self):
		"""An instance of the IsisDcePseudoIfaceAttPoint1Config class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.isisdcepseudoifaceattpoint1config.IsisDcePseudoIfaceAttPoint1Config)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.isisdcepseudoifaceattpoint1config import IsisDcePseudoIfaceAttPoint1Config
		return IsisDcePseudoIfaceAttPoint1Config(self)

	@property
	def IsisDcePseudoIfaceAttPoint2Config(self):
		"""An instance of the IsisDcePseudoIfaceAttPoint2Config class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.isisdcepseudoifaceattpoint2config.IsisDcePseudoIfaceAttPoint2Config)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.isisdcepseudoifaceattpoint2config import IsisDcePseudoIfaceAttPoint2Config
		return IsisDcePseudoIfaceAttPoint2Config(self)

	@property
	def IsisL3PseudoIfaceAttPoint1Config(self):
		"""An instance of the IsisL3PseudoIfaceAttPoint1Config class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.isisl3pseudoifaceattpoint1config.IsisL3PseudoIfaceAttPoint1Config)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.isisl3pseudoifaceattpoint1config import IsisL3PseudoIfaceAttPoint1Config
		return IsisL3PseudoIfaceAttPoint1Config(self)

	@property
	def IsisL3PseudoIfaceAttPoint2Config(self):
		"""An instance of the IsisL3PseudoIfaceAttPoint2Config class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.isisl3pseudoifaceattpoint2config.IsisL3PseudoIfaceAttPoint2Config)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.isisl3pseudoifaceattpoint2config import IsisL3PseudoIfaceAttPoint2Config
		return IsisL3PseudoIfaceAttPoint2Config(self)

	@property
	def IsisSpbPseudoIfaceAttPoint1Config(self):
		"""An instance of the IsisSpbPseudoIfaceAttPoint1Config class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.isisspbpseudoifaceattpoint1config.IsisSpbPseudoIfaceAttPoint1Config)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.isisspbpseudoifaceattpoint1config import IsisSpbPseudoIfaceAttPoint1Config
		return IsisSpbPseudoIfaceAttPoint1Config(self)

	@property
	def IsisSpbPseudoIfaceAttPoint2Config(self):
		"""An instance of the IsisSpbPseudoIfaceAttPoint2Config class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.isisspbpseudoifaceattpoint2config.IsisSpbPseudoIfaceAttPoint2Config)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.isisspbpseudoifaceattpoint2config import IsisSpbPseudoIfaceAttPoint2Config
		return IsisSpbPseudoIfaceAttPoint2Config(self)

	@property
	def IsisTrillPseudoIfaceAttPoint1Config(self):
		"""An instance of the IsisTrillPseudoIfaceAttPoint1Config class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.isistrillpseudoifaceattpoint1config.IsisTrillPseudoIfaceAttPoint1Config)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.isistrillpseudoifaceattpoint1config import IsisTrillPseudoIfaceAttPoint1Config
		return IsisTrillPseudoIfaceAttPoint1Config(self)

	@property
	def IsisTrillPseudoIfaceAttPoint2Config(self):
		"""An instance of the IsisTrillPseudoIfaceAttPoint2Config class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.isistrillpseudoifaceattpoint2config.IsisTrillPseudoIfaceAttPoint2Config)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.isistrillpseudoifaceattpoint2config import IsisTrillPseudoIfaceAttPoint2Config
		return IsisTrillPseudoIfaceAttPoint2Config(self)

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
	def LinkType(self):
		"""Link Type

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('linkType')

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

	def find(self, Count=None, DescriptiveName=None, Name=None):
		"""Finds and retrieves isisPseudoInterface data from the server.

		All named parameters support regex and can be used to selectively retrieve isisPseudoInterface data from the server.
		By default the find method takes no parameters and will retrieve all isisPseudoInterface data from the server.

		Args:
			Count (number): Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			self: This instance with matching isisPseudoInterface data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of isisPseudoInterface data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the isisPseudoInterface data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)

	def Start(self):
		"""Executes the start operation on the server.

		Start CPF control plane (equals to promote to negotiated state).

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('Start', payload=locals(), response_object=None)

	def Stop(self):
		"""Executes the stop operation on the server.

		Stop CPF control plane (equals to demote to PreValidated-DoDDone state).

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('Stop', payload=locals(), response_object=None)
