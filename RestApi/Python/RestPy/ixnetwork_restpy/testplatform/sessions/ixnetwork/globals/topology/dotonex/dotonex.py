from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class DotOneX(Base):
	"""The DotOneX class encapsulates a required dotOneX node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the DotOneX property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'dotOneX'

	def __init__(self, parent):
		super(DotOneX, self).__init__(parent)

	@property
	def AltName(self):
		"""Other Options - Alternative Subject Name

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('altName')

	@property
	def AuthOnNoResponse(self):
		"""If the DUT is not responding to EAPoL Start after configured number of retries, declare the session a success

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('authOnNoResponse')

	@property
	def AuthWaitPeriod(self):
		"""The maximum time interval, measured in seconds, that a Supplicant will wait for an Authenticator response.Maximum value is 3600

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('authWaitPeriod')

	@property
	def City(self):
		"""Identification Info - City

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('city')

	@property
	def Company(self):
		"""Identification Info - Company

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('company')

	@property
	def Count(self):
		"""Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group

		Returns:
			number
		"""
		return self._get_attribute('count')

	@property
	def Country(self):
		"""Identification Info - Country

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('country')

	@property
	def Department(self):
		"""Identification Info - Department

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('department')

	@property
	def DescriptiveName(self):
		"""Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context

		Returns:
			str
		"""
		return self._get_attribute('descriptiveName')

	@property
	def DisableLogoff(self):
		"""Do not send Logoff message when closing a session.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('disableLogoff')

	@property
	def DutTestMode(self):
		"""Specify what is the dut port mode

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('dutTestMode')

	@property
	def FragmentSize(self):
		"""The maximum size of a fragment that can be sent on the wire for TLS fragments that comprise the phase 1 conversation (tunnel establishment). Max value is 1400

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('fragmentSize')

	@property
	def GetCACertOnly(self):
		"""Use this option to get CA Certificate Only. Eg: For PEAPv0/v1 case there is no need to get User Certificate.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('getCACertOnly')

	@property
	def KeySize(self):
		"""Key Options - Key Size

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('keySize')

	@property
	def KeyUsage(self):
		"""Select key usage extensions

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('keyUsage')

	@property
	def MacAuthPrefix(self):
		"""When using machine authentication, a prefix is needed to differentiate between users and machines.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('macAuthPrefix')

	@property
	def MaxOutstandingRequests(self):
		"""The maximum number of sessions that can be negotiated at one moment. Max value is 1024

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('maxOutstandingRequests')

	@property
	def MaxSetupRate(self):
		"""The number of interfaces to setup per second. Max rate is 1024

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('maxSetupRate')

	@property
	def MaxStart(self):
		"""The number of times to send EAPOL Start frames for which no response is received before declaring that the sessions have timed out. Max value is 100

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('maxStart')

	@property
	def MaxTeardownRate(self):
		"""The number of interfaces to tear down per second. Max value is 1024

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('maxTeardownRate')

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
	def OnlyMulticast(self):
		"""Specify if destination MAC address can be multicast.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('onlyMulticast')

	@property
	def RowNames(self):
		"""Name of rows

		Returns:
			list(str)
		"""
		return self._get_attribute('rowNames')

	@property
	def ServerURL(self):
		"""Certificate Server URL

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('serverURL')

	@property
	def StartPeriod(self):
		"""The time interval between successive EAPOL Start messages sent by a Supplicant.Maxium value is 3600

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('startPeriod')

	@property
	def State(self):
		"""Identification Info - State

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('state')

	@property
	def SuccessiveStart(self):
		"""The number of EAPOL Start messages sent when the supplicant starts the process of authentication. Max value is 100

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('successiveStart')

	@property
	def UseVlanIdentify(self):
		"""Specify if VLAN is to be used to identify the supplicants

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('useVlanIdentify')

	@property
	def WaitBeforeRun(self):
		"""The number of secs to wait before running the protocol.Maximum wait is 500

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('waitBeforeRun')
