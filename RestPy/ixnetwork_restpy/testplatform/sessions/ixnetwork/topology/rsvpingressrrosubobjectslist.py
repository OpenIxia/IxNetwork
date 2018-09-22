from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class RsvpIngressRROSubObjectsList(Base):
	"""The RsvpIngressRROSubObjectsList class encapsulates a system managed rsvpIngressRROSubObjectsList node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the RsvpIngressRROSubObjectsList property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'rsvpIngressRROSubObjectsList'

	def __init__(self, parent):
		super(RsvpIngressRROSubObjectsList, self).__init__(parent)

	@property
	def BandwidthProtection(self):
		"""Bandwidth Protection

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('bandwidthProtection')

	@property
	def CType(self):
		"""C-Type

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('cType')

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
	def GlobalLabel(self):
		"""Global Label

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('globalLabel')

	@property
	def Ip(self):
		"""IP

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('ip')

	@property
	def Label(self):
		"""Label

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('label')

	@property
	def LocalIp(self):
		"""Local IP

		Returns:
			list(str)
		"""
		return self._get_attribute('localIp')

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
	def NodeProtection(self):
		"""Node Protection

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('nodeProtection')

	@property
	def ProtectionAvailable(self):
		"""Protection Available

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('protectionAvailable')

	@property
	def ProtectionInUse(self):
		"""Protection In Use

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('protectionInUse')

	@property
	def Type(self):
		"""Reservation Style

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('type')

	def find(self, Count=None, DescriptiveName=None, LocalIp=None, Name=None):
		"""Finds and retrieves rsvpIngressRROSubObjectsList data from the server.

		All named parameters support regex and can be used to selectively retrieve rsvpIngressRROSubObjectsList data from the server.
		By default the find method takes no parameters and will retrieve all rsvpIngressRROSubObjectsList data from the server.

		Args:
			Count (number): Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			LocalIp (list(str)): Local IP
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			self: This instance with matching rsvpIngressRROSubObjectsList data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of rsvpIngressRROSubObjectsList data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the rsvpIngressRROSubObjectsList data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)


class RsvpIngressRroSubObjectsList(Base):
	"""The RsvpIngressRroSubObjectsList class encapsulates a system managed rsvpIngressRroSubObjectsList node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the RsvpIngressRroSubObjectsList property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'rsvpIngressRroSubObjectsList'

	def __init__(self, parent):
		super(RsvpIngressRroSubObjectsList, self).__init__(parent)

	@property
	def BandwidthProtection(self):
		"""Bandwidth Protection

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('bandwidthProtection')

	@property
	def CType(self):
		"""C-Type

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('cType')

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
	def GlobalLabel(self):
		"""Global Label

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('globalLabel')

	@property
	def Ip(self):
		"""IP

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('ip')

	@property
	def Label(self):
		"""Label

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('label')

	@property
	def LocalIp(self):
		"""Local IP

		Returns:
			list(str)
		"""
		return self._get_attribute('localIp')

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
	def NodeProtection(self):
		"""Node Protection

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('nodeProtection')

	@property
	def P2mpIdAsIp(self):
		"""P2MP ID As IP

		Returns:
			list(str)
		"""
		return self._get_attribute('p2mpIdAsIp')

	@property
	def P2mpIdAsNum(self):
		"""P2MP ID displayed in Integer format

		Returns:
			list(str)
		"""
		return self._get_attribute('p2mpIdAsNum')

	@property
	def ProtectionAvailable(self):
		"""Protection Available

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('protectionAvailable')

	@property
	def ProtectionInUse(self):
		"""Protection In Use

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('protectionInUse')

	@property
	def Type(self):
		"""Type: IP or Label

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('type')

	def find(self, Count=None, DescriptiveName=None, LocalIp=None, Name=None, P2mpIdAsIp=None, P2mpIdAsNum=None):
		"""Finds and retrieves rsvpIngressRroSubObjectsList data from the server.

		All named parameters support regex and can be used to selectively retrieve rsvpIngressRroSubObjectsList data from the server.
		By default the find method takes no parameters and will retrieve all rsvpIngressRroSubObjectsList data from the server.

		Args:
			Count (number): Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			LocalIp (list(str)): Local IP
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario
			P2mpIdAsIp (list(str)): P2MP ID As IP
			P2mpIdAsNum (list(str)): P2MP ID displayed in Integer format

		Returns:
			self: This instance with matching rsvpIngressRroSubObjectsList data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of rsvpIngressRroSubObjectsList data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the rsvpIngressRroSubObjectsList data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
