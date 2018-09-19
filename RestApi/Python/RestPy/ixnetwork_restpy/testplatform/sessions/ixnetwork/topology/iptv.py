from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Iptv(Base):
	"""The Iptv class encapsulates a required iptv node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Iptv property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'iptv'

	def __init__(self, parent):
		super(Iptv, self).__init__(parent)

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
	def EnableGeneralQueryResponse(self):
		"""If enabled, General Query Response is send.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableGeneralQueryResponse')

	@property
	def JoinLatencyThreshold(self):
		"""The maximum time that is allowed for a multicast stream to arrive for channel for which a Join has been sent.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('joinLatencyThreshold')

	@property
	def LeaveLatencyThreshold(self):
		"""The maximum time allowed for a multicast stream to stop for a channel for which a Leave has been sent.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('leaveLatencyThreshold')

	@property
	def LogAllTimestamps(self):
		"""If enabled, all the captured timestamps for Join and Leave are saved to a log file.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('logAllTimestamps')

	@property
	def LogFailureTimestamps(self):
		"""If enabled, the timestamps for Join and Leave failures are saved to a log file.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('logFailureTimestamps')

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
	def NumChannelChangesBeforeView(self):
		"""Number of channels to change before stopping on a channel and watching it for View Duration.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('numChannelChangesBeforeView')

	@property
	def State(self):
		"""Indicates the state IPTV

		Returns:
			list(str[notStarted|started])
		"""
		return self._get_attribute('state')

	@property
	def StbLeaveJoinDelay(self):
		"""Time in milliseconds between sending a Leave for the current channel and Join for the next channel.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('stbLeaveJoinDelay')

	@property
	def ViewDuration(self):
		"""Specifies the time in milliseconds to view the last channel.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('viewDuration')

	@property
	def ZapBehavior(self):
		"""Use Zap Only to change channels without viewing the channel or Zap and View to change traffic and receive traffic for the last channel.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('zapBehavior')

	@property
	def ZapDirection(self):
		"""Specifies the direction of changing channels.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('zapDirection')

	@property
	def ZapInterval(self):
		"""Interval in milliseconds between channel changes based on the selected type.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('zapInterval')

	@property
	def ZapIntervalType(self):
		"""Specifies the wait interval type before changing the channels.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('zapIntervalType')

	def StartIptv(self):
		"""Executes the startIptv operation on the server.

		Start IPTV

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('StartIptv', payload=locals(), response_object=None)

	def StartIptv(self, SessionIndices):
		"""Executes the startIptv operation on the server.

		Start IPTV

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('StartIptv', payload=locals(), response_object=None)

	def StartIptv(self, SessionIndices):
		"""Executes the startIptv operation on the server.

		Start IPTV

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('StartIptv', payload=locals(), response_object=None)

	def StartIptv(self, Arg2):
		"""Executes the startIptv operation on the server.

		Start IPTV on selected interfaces

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally set Arg1 to the current href for this instance
			Arg2 (list(number)): List of indices into the IPTV grid An empty list indicates all instances in the plugin.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('StartIptv', payload=locals(), response_object=None)

	def StopIptv(self):
		"""Executes the stopIptv operation on the server.

		Stop IPTV

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('StopIptv', payload=locals(), response_object=None)

	def StopIptv(self, SessionIndices):
		"""Executes the stopIptv operation on the server.

		Stop IPTV

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('StopIptv', payload=locals(), response_object=None)

	def StopIptv(self, SessionIndices):
		"""Executes the stopIptv operation on the server.

		Stop IPTV

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('StopIptv', payload=locals(), response_object=None)

	def StopIptv(self, Arg2):
		"""Executes the stopIptv operation on the server.

		Stop IPTV on selected interfaces

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally set Arg1 to the current href for this instance
			Arg2 (list(number)): List of indices into the IPTV grid An empty list indicates all instances in the plugin.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('StopIptv', payload=locals(), response_object=None)
