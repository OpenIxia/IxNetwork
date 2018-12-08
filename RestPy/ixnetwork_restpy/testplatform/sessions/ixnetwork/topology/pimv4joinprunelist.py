
# Copyright 1997 - 2018 by IXIA Keysight
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
    
from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class PimV4JoinPruneList(Base):
	"""The PimV4JoinPruneList class encapsulates a required pimV4JoinPruneList node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the PimV4JoinPruneList property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'pimV4JoinPruneList'

	def __init__(self, parent):
		super(PimV4JoinPruneList, self).__init__(parent)

	@property
	def Tag(self):
		"""An instance of the Tag class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.tag.Tag)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.tag import Tag
		return Tag(self)

	@property
	def Active(self):
		"""Activate/Deactivate Configuration

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('active')

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
	def EnableFlapInfo(self):
		"""If selected, enables this Source entry for use in PIM-SM Register messages.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableFlapInfo')

	@property
	def EnablePack(self):
		"""If enabled, Multiple Groups can be included within a single packet.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enablePack')

	@property
	def FlapInterval(self):
		"""(in seconds) Specifies the amount of time between emulated flap events. The default is 60 seconds.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('flapInterval')

	@property
	def GroupAddressCount(self):
		"""The number of multicast group addresses to be included in the multicast group range. The maximum number of valid possible addresses depends on the values for the Group Address and the Group Mask Width. The default value is 1.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('groupAddressCount')

	@property
	def GroupV4Address(self):
		"""Group Address

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('groupV4Address')

	@property
	def GroupV4MaskWidth(self):
		"""Group Mask width

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('groupV4MaskWidth')

	@property
	def LocalRouterId(self):
		"""The PIM-SM Router ID value, in IPv4 format.

		Returns:
			list(str)
		"""
		return self._get_attribute('localRouterId')

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
	def PruneSourceAddressCount(self):
		"""The number of Prune Source addresses to be included. The maximum number of valid possible addresses depends on the values for the Source Address and the Source Mask Width. The default value is 0. ONLY used for (*,G) Type to send (S,G,rpt) Prune Messages.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('pruneSourceAddressCount')

	@property
	def PruneSourceV4Address(self):
		"""Prune Source Address

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('pruneSourceV4Address')

	@property
	def PruneSourceV4MaskWidth(self):
		"""Prune Source Mask width

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('pruneSourceV4MaskWidth')

	@property
	def RangeType(self):
		"""The Multicast Range Type. Choose one of: (*, *, RP)-Wildcard Group Set. For (*,*, RP) Join/Prune messages. Refers to all Groups associated with this specific RP. (*, G)-Group Specific type. For (*,G) Join/Prune messages. Refers to all sources associated with a specific Group G on the RP tree. (S, G)-Source specific type. For (S,G) Join/Prune messages. Refers only to specific combination of Source S and Group G. (*, G) -> (S, G)-Switchover type. (For switchover from non-source specific group state to source-specific group state.) Register Triggered (S,G)-These are the ranges of multicast group address and unicast source address to which a PIM-SM Router emulating an RP (for those source-group combinations) will send Triggered (S,G) joins and Register-Stop messages after receiving Register messages.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('rangeType')

	@property
	def RegisterStopTriggerCount(self):
		"""Available ONLY for use with Register Triggered (S,G) Range Type. (Default = 10)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('registerStopTriggerCount')

	@property
	def RpV4Address(self):
		"""RP Address

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('rpV4Address')

	@property
	def SourceAddressCount(self):
		"""The number of multicast source addresses to be included. The maximum number of valid possible addresses depends on the values for the Source Address and the Source Mask Width. The default value is 0.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('sourceAddressCount')

	@property
	def SourceGroupMappingType(self):
		"""Choose one of: Fully-meshed, One-to-One

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('sourceGroupMappingType')

	@property
	def SourceV4Address(self):
		"""Source Address

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('sourceV4Address')

	@property
	def SourceV4MaskWidth(self):
		"""Source Mask width

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('sourceV4MaskWidth')

	@property
	def Status(self):
		"""Status

		Returns:
			list(str[join|leave|none|notStarted])
		"""
		return self._get_attribute('status')

	@property
	def SwitchOverInterval(self):
		"""(in seconds) The time interval allowed for the switch from using the RP tree to using a Source-specific tree-from (*,G) to (S,G). The default value is 0.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('switchOverInterval')

	def get_device_ids(self, PortNames=None, Active=None, EnableFlapInfo=None, EnablePack=None, FlapInterval=None, GroupAddressCount=None, GroupV4Address=None, GroupV4MaskWidth=None, PruneSourceAddressCount=None, PruneSourceV4Address=None, PruneSourceV4MaskWidth=None, RangeType=None, RegisterStopTriggerCount=None, RpV4Address=None, SourceAddressCount=None, SourceGroupMappingType=None, SourceV4Address=None, SourceV4MaskWidth=None, SwitchOverInterval=None):
		"""Base class infrastructure that gets a list of pimV4JoinPruneList device ids encapsulated by this object.

		Use the optional regex parameters in the method to refine the list of device ids encapsulated by this object.

		Args:
			PortNames (str): optional regex of port names
			Active (str): optional regex of active
			EnableFlapInfo (str): optional regex of enableFlapInfo
			EnablePack (str): optional regex of enablePack
			FlapInterval (str): optional regex of flapInterval
			GroupAddressCount (str): optional regex of groupAddressCount
			GroupV4Address (str): optional regex of groupV4Address
			GroupV4MaskWidth (str): optional regex of groupV4MaskWidth
			PruneSourceAddressCount (str): optional regex of pruneSourceAddressCount
			PruneSourceV4Address (str): optional regex of pruneSourceV4Address
			PruneSourceV4MaskWidth (str): optional regex of pruneSourceV4MaskWidth
			RangeType (str): optional regex of rangeType
			RegisterStopTriggerCount (str): optional regex of registerStopTriggerCount
			RpV4Address (str): optional regex of rpV4Address
			SourceAddressCount (str): optional regex of sourceAddressCount
			SourceGroupMappingType (str): optional regex of sourceGroupMappingType
			SourceV4Address (str): optional regex of sourceV4Address
			SourceV4MaskWidth (str): optional regex of sourceV4MaskWidth
			SwitchOverInterval (str): optional regex of switchOverInterval

		Returns:
			list(int): A list of device ids that meets the regex criteria provided in the method parameters

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._get_ngpf_device_ids(locals())

	def Join(self):
		"""Executes the join operation on the server.

		Join

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('Join', payload=locals(), response_object=None)

	def Join(self, SessionIndices):
		"""Executes the join operation on the server.

		Join

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('Join', payload=locals(), response_object=None)

	def Join(self, SessionIndices):
		"""Executes the join operation on the server.

		Join

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('Join', payload=locals(), response_object=None)

	def Join(self, Arg2):
		"""Executes the join operation on the server.

		Stops the protocol state machine for the given protocol session instances.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally sets Arg1 to the current href for this instance
			Arg2 (list(number)): List of indices into the protocol plugin. An empty list indicates all instances in the plugin.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('Join', payload=locals(), response_object=None)

	def Leave(self):
		"""Executes the leave operation on the server.

		Leave

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('Leave', payload=locals(), response_object=None)

	def Leave(self, SessionIndices):
		"""Executes the leave operation on the server.

		Leave

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('Leave', payload=locals(), response_object=None)

	def Leave(self, SessionIndices):
		"""Executes the leave operation on the server.

		Leave

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('Leave', payload=locals(), response_object=None)

	def Leave(self, Arg2):
		"""Executes the leave operation on the server.

		Stops the protocol state machine for the given protocol session instances.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally sets Arg1 to the current href for this instance
			Arg2 (list(number)): List of indices into the protocol plugin. An empty list indicates all instances in the plugin.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('Leave', payload=locals(), response_object=None)

	def ResumePeriodicJoin(self):
		"""Executes the resumePeriodicJoin operation on the server.

		Resume Periodic Join

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('ResumePeriodicJoin', payload=locals(), response_object=None)

	def ResumePeriodicJoin(self, SessionIndices):
		"""Executes the resumePeriodicJoin operation on the server.

		Resume Periodic Join

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('ResumePeriodicJoin', payload=locals(), response_object=None)

	def ResumePeriodicJoin(self, SessionIndices):
		"""Executes the resumePeriodicJoin operation on the server.

		Resume Periodic Join

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('ResumePeriodicJoin', payload=locals(), response_object=None)

	def ResumePeriodicJoin(self, Arg2):
		"""Executes the resumePeriodicJoin operation on the server.

		Stops the protocol state machine for the given protocol session instances.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally sets Arg1 to the current href for this instance
			Arg2 (list(number)): List of indices into the protocol plugin. An empty list indicates all instances in the plugin.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('ResumePeriodicJoin', payload=locals(), response_object=None)

	def StopPeriodicJoin(self):
		"""Executes the stopPeriodicJoin operation on the server.

		Stop Periodic Join

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('StopPeriodicJoin', payload=locals(), response_object=None)

	def StopPeriodicJoin(self, SessionIndices):
		"""Executes the stopPeriodicJoin operation on the server.

		Stop Periodic Join

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('StopPeriodicJoin', payload=locals(), response_object=None)

	def StopPeriodicJoin(self, SessionIndices):
		"""Executes the stopPeriodicJoin operation on the server.

		Stop Periodic Join

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('StopPeriodicJoin', payload=locals(), response_object=None)

	def StopPeriodicJoin(self, Arg2):
		"""Executes the stopPeriodicJoin operation on the server.

		Stops the protocol state machine for the given protocol session instances.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally sets Arg1 to the current href for this instance
			Arg2 (list(number)): List of indices into the protocol plugin. An empty list indicates all instances in the plugin.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('StopPeriodicJoin', payload=locals(), response_object=None)
