from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class OpenFlowChannel(Base):
	"""The OpenFlowChannel class encapsulates a required openFlowChannel node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the OpenFlowChannel property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'openFlowChannel'

	def __init__(self, parent):
		super(OpenFlowChannel, self).__init__(parent)

	@property
	def FlowAggrMatchTemplate(self):
		"""An instance of the FlowAggrMatchTemplate class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.openflowchannel.flowaggrmatchtemplate.FlowAggrMatchTemplate)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.openflowchannel.flowaggrmatchtemplate import FlowAggrMatchTemplate
		return FlowAggrMatchTemplate(self)._select()

	@property
	def FlowStatMatchTemplate(self):
		"""An instance of the FlowStatMatchTemplate class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.openflowchannel.flowstatmatchtemplate.FlowStatMatchTemplate)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.openflowchannel.flowstatmatchtemplate import FlowStatMatchTemplate
		return FlowStatMatchTemplate(self)._select()

	@property
	def PacketOutActionTemplate(self):
		"""An instance of the PacketOutActionTemplate class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.openflowchannel.packetoutactiontemplate.PacketOutActionTemplate)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.openflowchannel.packetoutactiontemplate import PacketOutActionTemplate
		return PacketOutActionTemplate(self)._select()

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
	def RowNames(self):
		"""Name of rows

		Returns:
			list(str)
		"""
		return self._get_attribute('rowNames')
