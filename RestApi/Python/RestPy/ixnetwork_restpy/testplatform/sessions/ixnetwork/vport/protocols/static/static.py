from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Static(Base):
	"""The Static class encapsulates a required static node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Static property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'static'

	def __init__(self, parent):
		super(Static, self).__init__(parent)

	@property
	def Atm(self):
		"""An instance of the Atm class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.static.atm.atm.Atm)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.static.atm.atm import Atm
		return Atm(self)

	@property
	def Fr(self):
		"""An instance of the Fr class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.static.fr.fr.Fr)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.static.fr.fr import Fr
		return Fr(self)

	@property
	def InterfaceGroup(self):
		"""An instance of the InterfaceGroup class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.static.interfacegroup.interfacegroup.InterfaceGroup)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.static.interfacegroup.interfacegroup import InterfaceGroup
		return InterfaceGroup(self)

	@property
	def Ip(self):
		"""An instance of the Ip class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.static.ip.ip.Ip)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.static.ip.ip import Ip
		return Ip(self)

	@property
	def Lan(self):
		"""An instance of the Lan class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.static.lan.lan.Lan)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.static.lan.lan import Lan
		return Lan(self)
