from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class FlowProfile(Base):
	"""The FlowProfile class encapsulates a required flowProfile node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the FlowProfile property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'flowProfile'

	def __init__(self, parent):
		super(FlowProfile, self).__init__(parent)

	@property
	def MatchAction(self):
		"""An instance of the MatchAction class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.matchaction.MatchAction)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.matchaction import MatchAction
		return MatchAction(self)

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

	def AddFromTemplate(self, Arg2):
		"""Executes the addFromTemplate operation on the server.

		Creates a Match Action prototype supported by the template.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally set Arg1 to the current href for this instance
			Arg2 (str(None|/api/v1/sessions/1/ixnetwork/?deepchild=*)): 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('AddFromTemplate', payload=locals(), response_object=None)
