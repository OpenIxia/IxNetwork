
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


class ClusterData(Base):
	"""The ClusterData class encapsulates a required clusterData node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the ClusterData property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'clusterData'

	def __init__(self, parent):
		super(ClusterData, self).__init__(parent)

	@property
	def ActionTriggered(self):
		"""Displays what Action Triggered for each Binding. Possible values: No Action, Attach, Detach

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('actionTriggered')

	@property
	def AttachAtStart(self):
		"""Attach at Start

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('attachAtStart')

	@property
	def AutoSyncAtStart(self):
		"""Synchronize TOR Database at Start.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('autoSyncAtStart')

	@property
	def BindingStatus(self):
		"""Additional information about the Binding's state

		Returns:
			list(str[attached|attaching|detached|detaching|disconnected])
		"""
		return self._get_attribute('bindingStatus')

	@property
	def BindingsCount(self):
		"""Bindings Count

		Returns:
			number
		"""
		return self._get_attribute('bindingsCount')
	@BindingsCount.setter
	def BindingsCount(self, value):
		self._set_attribute('bindingsCount', value)

	@property
	def Count(self):
		"""Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group

		Returns:
			number
		"""
		return self._get_attribute('count')

	@property
	def CurrentRetryCount(self):
		"""This field will Show current retry count value Controller is doing to Synchronize TOR Database Automatically when TOR is reconnecting while doing the action.

		Returns:
			number
		"""
		return self._get_attribute('currentRetryCount')

	@property
	def DescriptiveName(self):
		"""Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context

		Returns:
			str
		"""
		return self._get_attribute('descriptiveName')

	@property
	def ErrorStatus(self):
		"""Error information about the Binding

		Returns:
			list(str[deleteBindingError|deleteBindingTimeout|deleteLsError|deleteLsTimeout|differentLsName|duplicateVlanLsPort|insertBindingError|insertBindingTimeout|insertLsError|insertLsTimeout|none|vlanMappedToDifferentLSs])
		"""
		return self._get_attribute('errorStatus')

	@property
	def LogicalSwitchName(self):
		"""Logical_Switch Name

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('logicalSwitchName')

	@property
	def MaxRetryCount(self):
		"""Maximum number of Retries Controller will do the TOR Database Synchronization Automatically, If TOR is reconnecting while doing the action

		Returns:
			number
		"""
		return self._get_attribute('maxRetryCount')
	@MaxRetryCount.setter
	def MaxRetryCount(self, value):
		self._set_attribute('maxRetryCount', value)

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
	def PhysicalPortName(self):
		"""Physical_Port name

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('physicalPortName')

	@property
	def PhysicalSwitchName(self):
		"""Physical_Switch name

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('physicalSwitchName')

	@property
	def ProgressStatus(self):
		"""Gives info Controller is busy doing some actions. There are 3 states: 1. None - Default State. 2. In Progress - Processing is in Progress. 3. Done - Controller is done processing all requests.

		Returns:
			str
		"""
		return self._get_attribute('progressStatus')

	@property
	def RetryStatus(self):
		"""This field will Show if Controller has failed to complete the entire action even after Max Retry Count attempts There are 2 states: 1. None - Default State. 2. Retry Failed - Controller has done Max Retry Count attempts to complete the action, but failed

		Returns:
			str
		"""
		return self._get_attribute('retryStatus')

	@property
	def Vlan(self):
		"""VLAN ID

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('vlan')

	@property
	def Vni(self):
		"""VNI

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('vni')

	def get_device_ids(self, PortNames=None, ActionTriggered=None, AttachAtStart=None, AutoSyncAtStart=None, LogicalSwitchName=None, PhysicalPortName=None, PhysicalSwitchName=None, Vlan=None, Vni=None):
		"""Base class infrastructure that gets a list of clusterData device ids encapsulated by this object.

		Use the optional regex parameters in the method to refine the list of device ids encapsulated by this object.

		Args:
			PortNames (str): optional regex of port names
			ActionTriggered (str): optional regex of actionTriggered
			AttachAtStart (str): optional regex of attachAtStart
			AutoSyncAtStart (str): optional regex of autoSyncAtStart
			LogicalSwitchName (str): optional regex of logicalSwitchName
			PhysicalPortName (str): optional regex of physicalPortName
			PhysicalSwitchName (str): optional regex of physicalSwitchName
			Vlan (str): optional regex of vlan
			Vni (str): optional regex of vni

		Returns:
			list(int): A list of device ids that meets the regex criteria provided in the method parameters

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._get_ngpf_device_ids(locals())

	def Attach(self, Arg2):
		"""Executes the attach operation on the server.

		Attach.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally sets Arg1 to the current href for this instance
			Arg2 (list(number)): List of indices for which to Attach.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('Attach', payload=locals(), response_object=None)

	def Detach(self, Arg2):
		"""Executes the detach operation on the server.

		Detach.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally sets Arg1 to the current href for this instance
			Arg2 (list(number)): List of indices for which to Detach.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('Detach', payload=locals(), response_object=None)

	def FetchAndUpdateConfigFromCloud(self, Mode):
		"""Executes the fetchAndUpdateConfigFromCloud operation on the server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/globals?deepchild=*|/api/v1/sessions/1/ixnetwork/topology?deepchild=*)): The method internally sets Arg1 to the current href for this instance
			Mode (str): 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('FetchAndUpdateConfigFromCloud', payload=locals(), response_object=None)

	def ResetRetryStatus(self, Arg2):
		"""Executes the resetRetryStatus operation on the server.

		This method will reset Current Retry Count to 0 and Retry Status to None.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally sets Arg1 to the current href for this instance
			Arg2 (list(number)): List of indices for which to Reset Retry Status fields.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('ResetRetryStatus', payload=locals(), response_object=None)

	def SyncUmrMmrTables(self, Arg2):
		"""Executes the syncUmrMmrTables operation on the server.

		This method will insert missing UMR and MMR table entries for specified Logical Switches.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally sets Arg1 to the current href for this instance
			Arg2 (list(number)): List of indices for which to Sync UMR and MMR tables.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('SyncUmrMmrTables', payload=locals(), response_object=None)
