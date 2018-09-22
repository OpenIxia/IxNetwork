from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Chassis(Base):
	"""The Chassis class encapsulates a user managed chassis node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Chassis property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'chassis'

	def __init__(self, parent):
		super(Chassis, self).__init__(parent)

	@property
	def Card(self):
		"""An instance of the Card class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.availablehardware.chassis.card.card.Card)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.availablehardware.chassis.card.card import Card
		return Card(self)

	@property
	def CableLength(self):
		"""Specifies the length of the cable between two adjacent chassis. Must be set only after the chassis hostname has been set and committed on the current chassis.

		Returns:
			number
		"""
		return self._get_attribute('cableLength')
	@CableLength.setter
	def CableLength(self, value):
		self._set_attribute('cableLength', value)

	@property
	def ChainTopology(self):
		"""The chain topology type. This must be defined on the master chassis. It must be defined only after the chassis host name has been specified and applied on the current chassis. For legacy chassis chains, the daisy chainTopology should be indicated.

		Returns:
			str(daisy|none|star)
		"""
		return self._get_attribute('chainTopology')
	@ChainTopology.setter
	def ChainTopology(self, value):
		self._set_attribute('chainTopology', value)

	@property
	def ChassisType(self):
		"""The type of chassis.

		Returns:
			str
		"""
		return self._get_attribute('chassisType')

	@property
	def ChassisVersion(self):
		"""The version of the Chassis in use.

		Returns:
			str
		"""
		return self._get_attribute('chassisVersion')

	@property
	def ConnectRetries(self):
		"""The number of time the client attempted to re-connect with the chassis. (read only)

		Returns:
			number
		"""
		return self._get_attribute('connectRetries')

	@property
	def Hostname(self):
		"""The IP address associated with the chassis.

		Returns:
			str
		"""
		return self._get_attribute('hostname')
	@Hostname.setter
	def Hostname(self, value):
		self._set_attribute('hostname', value)

	@property
	def Ip(self):
		"""The IP address associated with the chassis.

		Returns:
			str
		"""
		return self._get_attribute('ip')

	@property
	def IsLicensesRetrieved(self):
		"""Retrieves the licenses in the chassis.

		Returns:
			bool
		"""
		return self._get_attribute('isLicensesRetrieved')

	@property
	def IsMaster(self):
		"""Specifies whether this chassis is a master of a slave in a chain. There can be only one master chassis in a chain. NOTE: The master is automatically assigned based on cable connections.

		Returns:
			bool
		"""
		return self._get_attribute('isMaster')

	@property
	def IxnBuildNumber(self):
		"""IxNetwork build number.

		Returns:
			str
		"""
		return self._get_attribute('ixnBuildNumber')

	@property
	def IxosBuildNumber(self):
		"""The IxOS version of the Chassis in use.

		Returns:
			str
		"""
		return self._get_attribute('ixosBuildNumber')

	@property
	def LicenseErrors(self):
		"""Shows the licening errors that occurred due to licensing problems.

		Returns:
			list(str)
		"""
		return self._get_attribute('licenseErrors')

	@property
	def MasterChassis(self):
		"""Specify the hostname of the master chassis on a slave chassis. Must be left blank on master. Must be set only after the chassis hostname has been set and committed on the current chassis.

		Returns:
			str
		"""
		return self._get_attribute('masterChassis')
	@MasterChassis.setter
	def MasterChassis(self, value):
		self._set_attribute('masterChassis', value)

	@property
	def ProtocolBuildNumber(self):
		"""The Protocols version of the Chassis in use.

		Returns:
			str
		"""
		return self._get_attribute('protocolBuildNumber')

	@property
	def SequenceId(self):
		"""Indicates the order at which the chassis in a chassis chain are pulsed by IxOS. Star topology chains are automatically setting this value. Must be set only after the chassis hostname has been set and committed on the current chassis.

		Returns:
			number
		"""
		return self._get_attribute('sequenceId')
	@SequenceId.setter
	def SequenceId(self, value):
		self._set_attribute('sequenceId', value)

	@property
	def State(self):
		"""The following states can be read from the port: polling, ready, and down.

		Returns:
			str(down|down|polling|polling|polling|ready)
		"""
		return self._get_attribute('state')

	def add(self, CableLength=None, ChainTopology=None, Hostname=None, MasterChassis=None, SequenceId=None):
		"""Adds a new chassis node on the server and retrieves it in this instance.

		Args:
			CableLength (number): Specifies the length of the cable between two adjacent chassis. Must be set only after the chassis hostname has been set and committed on the current chassis.
			ChainTopology (str(daisy|none|star)): The chain topology type. This must be defined on the master chassis. It must be defined only after the chassis host name has been specified and applied on the current chassis. For legacy chassis chains, the daisy chainTopology should be indicated.
			Hostname (str): The IP address associated with the chassis.
			MasterChassis (str): Specify the hostname of the master chassis on a slave chassis. Must be left blank on master. Must be set only after the chassis hostname has been set and committed on the current chassis.
			SequenceId (number): Indicates the order at which the chassis in a chassis chain are pulsed by IxOS. Star topology chains are automatically setting this value. Must be set only after the chassis hostname has been set and committed on the current chassis.

		Returns:
			self: This instance with all currently retrieved chassis data using find and the newly added chassis data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the chassis data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, CableLength=None, ChainTopology=None, ChassisType=None, ChassisVersion=None, ConnectRetries=None, Hostname=None, Ip=None, IsLicensesRetrieved=None, IsMaster=None, IxnBuildNumber=None, IxosBuildNumber=None, LicenseErrors=None, MasterChassis=None, ProtocolBuildNumber=None, SequenceId=None, State=None):
		"""Finds and retrieves chassis data from the server.

		All named parameters support regex and can be used to selectively retrieve chassis data from the server.
		By default the find method takes no parameters and will retrieve all chassis data from the server.

		Args:
			CableLength (number): Specifies the length of the cable between two adjacent chassis. Must be set only after the chassis hostname has been set and committed on the current chassis.
			ChainTopology (str(daisy|none|star)): The chain topology type. This must be defined on the master chassis. It must be defined only after the chassis host name has been specified and applied on the current chassis. For legacy chassis chains, the daisy chainTopology should be indicated.
			ChassisType (str): The type of chassis.
			ChassisVersion (str): The version of the Chassis in use.
			ConnectRetries (number): The number of time the client attempted to re-connect with the chassis. (read only)
			Hostname (str): The IP address associated with the chassis.
			Ip (str): The IP address associated with the chassis.
			IsLicensesRetrieved (bool): Retrieves the licenses in the chassis.
			IsMaster (bool): Specifies whether this chassis is a master of a slave in a chain. There can be only one master chassis in a chain. NOTE: The master is automatically assigned based on cable connections.
			IxnBuildNumber (str): IxNetwork build number.
			IxosBuildNumber (str): The IxOS version of the Chassis in use.
			LicenseErrors (list(str)): Shows the licening errors that occurred due to licensing problems.
			MasterChassis (str): Specify the hostname of the master chassis on a slave chassis. Must be left blank on master. Must be set only after the chassis hostname has been set and committed on the current chassis.
			ProtocolBuildNumber (str): The Protocols version of the Chassis in use.
			SequenceId (number): Indicates the order at which the chassis in a chassis chain are pulsed by IxOS. Star topology chains are automatically setting this value. Must be set only after the chassis hostname has been set and committed on the current chassis.
			State (str(down|down|polling|polling|polling|ready)): The following states can be read from the port: polling, ready, and down.

		Returns:
			self: This instance with matching chassis data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of chassis data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the chassis data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)

	def GetTapSettings(self):
		"""Executes the getTapSettings operation on the server.

		Get TAP Settings for the given chassis

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/availableHardware?deepchild=chassis])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('GetTapSettings', payload=locals(), response_object=None)

	def RefreshInfo(self):
		"""Executes the refreshInfo operation on the server.

		Refresh the hardware information.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/availableHardware?deepchild=chassis|/api/v1/sessions/1/ixnetwork/availableHardware?deepchild=card])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('RefreshInfo', payload=locals(), response_object=None)

	def SetTapSettings(self):
		"""Executes the setTapSettings operation on the server.

		Send TAP Settings to IxServer for the given chassis.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/availableHardware?deepchild=chassis])): The method internally sets Arg1 to the encapsulated list of hrefs for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self
		return self._execute('SetTapSettings', payload=locals(), response_object=None)
