from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class NtpServers(Base):
	"""The NtpServers class encapsulates a required ntpServers node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the NtpServers property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'ntpServers'

	def __init__(self, parent):
		super(NtpServers, self).__init__(parent)

	@property
	def Active(self):
		"""Activate/Deactivate Configuration

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('active')

	@property
	def AuthDelay(self):
		"""Authentication Delay (microsecs)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('authDelay')

	@property
	def Authentication(self):
		"""Authentication Type

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('authentication')

	@property
	def AuthenticationKey(self):
		"""Authentication Key

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('authenticationKey')

	@property
	def BurstMode(self):
		"""Burst Mode

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('burstMode')

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
	def InitialBurstMode(self):
		"""Initial Burst Mode

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('initialBurstMode')

	@property
	def IsParentV6(self):
		"""Parent v6

		Returns:
			bool
		"""
		return self._get_attribute('isParentV6')
	@IsParentV6.setter
	def IsParentV6(self, value):
		self._set_attribute('isParentV6', value)

	@property
	def KeyId(self):
		"""Key Identifier

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('keyId')

	@property
	def MaxPollInterval(self):
		"""Max Poll Interval (log2 seconds)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('maxPollInterval')

	@property
	def MinPollInterval(self):
		"""Min Poll Interval (log2 seconds)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('minPollInterval')

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
	def ParticipateInClockSelect(self):
		"""Participate in Clock Select

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('participateInClockSelect')

	@property
	def ServerIPAddress(self):
		"""Server IP Address

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('serverIPAddress')

	@property
	def ServerIPv6Address(self):
		"""Server IPv6 Address

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('serverIPv6Address')

	def Start(self):
		"""Executes the start operation on the server.

		Activate/Enable Ntp Servers

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('Start', payload=locals(), response_object=None)

	def Start(self, SessionIndices):
		"""Executes the start operation on the server.

		Activate/Enable Ntp Servers

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('Start', payload=locals(), response_object=None)

	def Start(self, SessionIndices):
		"""Executes the start operation on the server.

		Activate/Enable Ntp Servers

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('Start', payload=locals(), response_object=None)

	def Start(self, Arg2):
		"""Executes the start operation on the server.

		Start

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally set Arg1 to the current href for this instance
			Arg2 (list(number)): List of indices into the protocol plugin. An empty list indicates all instances in the plugin.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('Start', payload=locals(), response_object=None)

	def Stop(self):
		"""Executes the stop operation on the server.

		Deactivate/Disable selected Ntp Servers

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('Stop', payload=locals(), response_object=None)

	def Stop(self, SessionIndices):
		"""Executes the stop operation on the server.

		Deactivate/Disable selected Ntp Servers

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('Stop', payload=locals(), response_object=None)

	def Stop(self, SessionIndices):
		"""Executes the stop operation on the server.

		Deactivate/Disable selected Ntp Servers

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('Stop', payload=locals(), response_object=None)

	def Stop(self, Arg2):
		"""Executes the stop operation on the server.

		Stop

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally set Arg1 to the current href for this instance
			Arg2 (list(number)): List of indices into the protocol plugin. An empty list indicates all instances in the plugin.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('Stop', payload=locals(), response_object=None)
