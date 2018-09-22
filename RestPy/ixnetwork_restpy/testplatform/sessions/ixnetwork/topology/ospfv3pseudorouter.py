from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Ospfv3PseudoRouter(Base):
	"""The Ospfv3PseudoRouter class encapsulates a system managed ospfv3PseudoRouter node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Ospfv3PseudoRouter property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'ospfv3PseudoRouter'

	def __init__(self, parent):
		super(Ospfv3PseudoRouter, self).__init__(parent)

	@property
	def ExternalRoutes(self):
		"""An instance of the ExternalRoutes class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.externalroutes.ExternalRoutes)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.externalroutes import ExternalRoutes
		return ExternalRoutes(self)

	@property
	def InterAreaPrefix(self):
		"""An instance of the InterAreaPrefix class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.interareaprefix.InterAreaPrefix)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.interareaprefix import InterAreaPrefix
		return InterAreaPrefix(self)

	@property
	def InterAreaRouter(self):
		"""An instance of the InterAreaRouter class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.interarearouter.InterAreaRouter)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.interarearouter import InterAreaRouter
		return InterAreaRouter(self)

	@property
	def IntraAreaPrefix(self):
		"""An instance of the IntraAreaPrefix class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.intraareaprefix.IntraAreaPrefix)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.intraareaprefix import IntraAreaPrefix
		return IntraAreaPrefix(self)

	@property
	def LinkLsaRoutes(self):
		"""An instance of the LinkLsaRoutes class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.linklsaroutes.LinkLsaRoutes)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.linklsaroutes import LinkLsaRoutes
		return LinkLsaRoutes(self)

	@property
	def NssaRoutes(self):
		"""An instance of the NssaRoutes class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.nssaroutes.NssaRoutes)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.nssaroutes import NssaRoutes
		return NssaRoutes(self)

	@property
	def Active(self):
		"""Activate/Deactivate Configuration

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('active')

	@property
	def BBit(self):
		"""Router-LSA B-Bit

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('bBit')

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
	def EBit(self):
		"""Router-LSA E-Bit

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('eBit')

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
		"""Finds and retrieves ospfv3PseudoRouter data from the server.

		All named parameters support regex and can be used to selectively retrieve ospfv3PseudoRouter data from the server.
		By default the find method takes no parameters and will retrieve all ospfv3PseudoRouter data from the server.

		Args:
			Count (number): Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			self: This instance with matching ospfv3PseudoRouter data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of ospfv3PseudoRouter data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the ospfv3PseudoRouter data from the server available through an iterator or index

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

	def StartSimulatedRouter(self):
		"""Executes the startSimulatedRouter operation on the server.

		Start Pseudo Router

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('StartSimulatedRouter', payload=locals(), response_object=None)

	def StartSimulatedRouter(self, SessionIndices):
		"""Executes the startSimulatedRouter operation on the server.

		Start Pseudo Router

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('StartSimulatedRouter', payload=locals(), response_object=None)

	def StartSimulatedRouter(self, SessionIndices):
		"""Executes the startSimulatedRouter operation on the server.

		Start Pseudo Router

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('StartSimulatedRouter', payload=locals(), response_object=None)

	def StartSimulatedRouter(self, Arg2):
		"""Executes the startSimulatedRouter operation on the server.

		Shutdown OSPFv3 state machine on this simulated router.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally set Arg1 to the current href for this instance
			Arg2 (list(number)): List of indices into the network info. An empty list indicates all instances in the node specific data.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('StartSimulatedRouter', payload=locals(), response_object=None)

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

	def StopSimulatedRouter(self):
		"""Executes the stopSimulatedRouter operation on the server.

		Stop Pseudo Router

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('StopSimulatedRouter', payload=locals(), response_object=None)

	def StopSimulatedRouter(self, SessionIndices):
		"""Executes the stopSimulatedRouter operation on the server.

		Stop Pseudo Router

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('StopSimulatedRouter', payload=locals(), response_object=None)

	def StopSimulatedRouter(self, SessionIndices):
		"""Executes the stopSimulatedRouter operation on the server.

		Stop Pseudo Router

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('StopSimulatedRouter', payload=locals(), response_object=None)

	def StopSimulatedRouter(self, Arg2):
		"""Executes the stopSimulatedRouter operation on the server.

		Withdraws all the routes mentioned in this route range.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally set Arg1 to the current href for this instance
			Arg2 (list(number)): List of indices into the network info. An empty list indicates all instances in the network info.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('StopSimulatedRouter', payload=locals(), response_object=None)
