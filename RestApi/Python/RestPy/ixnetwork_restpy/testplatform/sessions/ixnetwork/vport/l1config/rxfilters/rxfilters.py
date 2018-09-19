from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class RxFilters(Base):
	"""The RxFilters class encapsulates a required rxFilters node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the RxFilters property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'rxFilters'

	def __init__(self, parent):
		super(RxFilters, self).__init__(parent)

	@property
	def FilterPalette(self):
		"""An instance of the FilterPalette class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.l1config.rxfilters.filterpalette.filterpalette.FilterPalette)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.l1config.rxfilters.filterpalette.filterpalette import FilterPalette
		return FilterPalette(self)._select()

	@property
	def Uds(self):
		"""An instance of the Uds class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.l1config.rxfilters.uds.uds.Uds)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.l1config.rxfilters.uds.uds import Uds
		return Uds(self)
