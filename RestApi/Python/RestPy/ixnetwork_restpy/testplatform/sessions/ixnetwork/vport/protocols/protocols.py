from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Protocols(Base):
	"""The Protocols class encapsulates a required protocols node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Protocols property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'protocols'

	def __init__(self, parent):
		super(Protocols, self).__init__(parent)
