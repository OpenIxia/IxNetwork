from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Globals(Base):
	"""The Globals class encapsulates a required globals node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Globals property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'globals'

	def __init__(self, parent):
		super(Globals, self).__init__(parent)

	@property
	def AppErrors(self):
		"""An instance of the AppErrors class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.apperrors.apperrors.AppErrors)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.apperrors.apperrors import AppErrors
		return AppErrors(self)

	@property
	def Interfaces(self):
		"""An instance of the Interfaces class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.interfaces.interfaces.Interfaces)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.interfaces.interfaces import Interfaces
		return Interfaces(self)._select()

	@property
	def Ixnet(self):
		"""An instance of the Ixnet class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.ixnet.ixnet.Ixnet)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.ixnet.ixnet import Ixnet
		return Ixnet(self)._select()

	@property
	def Licensing(self):
		"""An instance of the Licensing class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.licensing.licensing.Licensing)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.licensing.licensing import Licensing
		return Licensing(self)._select()

	@property
	def Preferences(self):
		"""An instance of the Preferences class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.preferences.preferences.Preferences)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.preferences.preferences import Preferences
		return Preferences(self)._select()

	@property
	def Scriptgen(self):
		"""An instance of the Scriptgen class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.scriptgen.scriptgen.Scriptgen)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.scriptgen.scriptgen import Scriptgen
		return Scriptgen(self)._select()

	@property
	def TestInspector(self):
		"""An instance of the TestInspector class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.testinspector.testinspector.TestInspector)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.testinspector.testinspector import TestInspector
		return TestInspector(self)._select()

	@property
	def Topology(self):
		"""An instance of the Topology class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.topology.Topology)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.topology import Topology
		return Topology(self)._select()

	@property
	def BuildNumber(self):
		"""The IxNetwork software build number.

		Returns:
			str
		"""
		return self._get_attribute('buildNumber')

	@property
	def ConfigFileName(self):
		"""The name of the configuration file.

		Returns:
			str
		"""
		return self._get_attribute('configFileName')

	@property
	def ConfigSummary(self):
		"""A high level summary description of the currently loaded configuration

		Returns:
			list(dict(arg1:str,arg2:str,arg3:list[dict(arg1:str,arg2:str)]))
		"""
		return self._get_attribute('configSummary')

	@property
	def IsConfigDifferent(self):
		"""(Read only) If true, then the current IxNetwork configuration is different than the configuration that was previously loaded.

		Returns:
			bool
		"""
		return self._get_attribute('isConfigDifferent')

	@property
	def IxosBuildNumber(self):
		"""The IxOS software build number.

		Returns:
			str
		"""
		return self._get_attribute('ixosBuildNumber')

	@property
	def PersistencePath(self):
		"""This attribute returns a directory of the IxNetwork API server machine, where users can drop their files from the client scripts using IxNetwork APIs. To Put files in this directory, users do not require to run IxNetwork API server in administrative mode

		Returns:
			str
		"""
		return self._get_attribute('persistencePath')

	@property
	def ProtocolbuildNumber(self):
		"""The build number of the protocol.

		Returns:
			str
		"""
		return self._get_attribute('protocolbuildNumber')

	@property
	def Username(self):
		"""The name of the user.

		Returns:
			str
		"""
		return self._get_attribute('username')

	def StartAllProtocolsAndTraffic(self, Arg2):
		"""Executes the startAllProtocolsAndTraffic operation on the server.

		connect ports, start protocols and generate/apply/start traffic

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/globals)): The method internally set Arg1 to the current href for this instance
			Arg2 (bool): a boolean indicating if ownership should be taken forcefully

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('StartAllProtocolsAndTraffic', payload=locals(), response_object=None)
