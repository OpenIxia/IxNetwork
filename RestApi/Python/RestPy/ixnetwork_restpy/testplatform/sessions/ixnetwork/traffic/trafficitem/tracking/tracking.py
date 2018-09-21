from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Tracking(Base):
	"""The Tracking class encapsulates a system managed tracking node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Tracking property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'tracking'

	def __init__(self, parent):
		super(Tracking, self).__init__(parent)

	@property
	def Egress(self):
		"""An instance of the Egress class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.tracking.egress.egress.Egress)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.tracking.egress.egress import Egress
		return Egress(self)._select()

	@property
	def LatencyBin(self):
		"""An instance of the LatencyBin class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.tracking.latencybin.latencybin.LatencyBin)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.tracking.latencybin.latencybin import LatencyBin
		return LatencyBin(self)._select()

	@property
	def AvailableProtocolOffsets(self):
		"""Specifies the available Protocol Offsets when the Flows of a Traffic Item are tracked by Custom Override.

		Returns:
			list(str)
		"""
		return self._get_attribute('availableProtocolOffsets')

	@property
	def AvailableTrackBy(self):
		"""Returns list of available tracking field ids

		Returns:
			list(str)
		"""
		return self._get_attribute('availableTrackBy')

	@property
	def AvailableTrackByInfos(self):
		"""Returns list of tracking fields with id/displayname

		Returns:
			list(dict(arg1:str,arg2:str))
		"""
		return self._get_attribute('availableTrackByInfos')

	@property
	def FieldWidth(self):
		"""Specifies the Field Width when the flows of a Traffic Item are tracked by Custom Override.

		Returns:
			str(eightBits|sixteenBits|thirtyTwoBits|twentyFourBits)
		"""
		return self._get_attribute('fieldWidth')
	@FieldWidth.setter
	def FieldWidth(self, value):
		self._set_attribute('fieldWidth', value)

	@property
	def Offset(self):
		"""Specifies the Offset when the Flows of a Traffic Item are tracked by Custom Override.

		Returns:
			number
		"""
		return self._get_attribute('offset')
	@Offset.setter
	def Offset(self, value):
		self._set_attribute('offset', value)

	@property
	def OneToOneMesh(self):
		"""If true, one-one mesh is enabled when flows of a traffic item are tracked by Custom Override.

		Returns:
			bool
		"""
		return self._get_attribute('oneToOneMesh')
	@OneToOneMesh.setter
	def OneToOneMesh(self, value):
		self._set_attribute('oneToOneMesh', value)

	@property
	def ProtocolOffset(self):
		"""Specifies the Protocol Offset when flows of a Traffic Item are tracked by Custom Override.

		Returns:
			str
		"""
		return self._get_attribute('protocolOffset')
	@ProtocolOffset.setter
	def ProtocolOffset(self, value):
		self._set_attribute('protocolOffset', value)

	@property
	def TrackBy(self):
		"""Specifies the tracking option by which the Flows of a Traffic Item are tracked.

		Returns:
			list(str)
		"""
		return self._get_attribute('trackBy')
	@TrackBy.setter
	def TrackBy(self, value):
		self._set_attribute('trackBy', value)

	@property
	def Values(self):
		"""Specifies the Values when the Flows of a Traffic Item are tracked by Custom Override.

		Returns:
			list(str)
		"""
		return self._get_attribute('values')
	@Values.setter
	def Values(self, value):
		self._set_attribute('values', value)

	def find(self, AvailableProtocolOffsets=None, AvailableTrackBy=None, AvailableTrackByInfos=None, FieldWidth=None, Offset=None, OneToOneMesh=None, ProtocolOffset=None, TrackBy=None, Values=None):
		"""Finds and retrieves tracking data from the server.

		All named parameters support regex and can be used to selectively retrieve tracking data from the server.
		By default the find method takes no parameters and will retrieve all tracking data from the server.

		Args:
			AvailableProtocolOffsets (list(str)): Specifies the available Protocol Offsets when the Flows of a Traffic Item are tracked by Custom Override.
			AvailableTrackBy (list(str)): Returns list of available tracking field ids
			AvailableTrackByInfos (list(dict(arg1:str,arg2:str))): Returns list of tracking fields with id/displayname
			FieldWidth (str(eightBits|sixteenBits|thirtyTwoBits|twentyFourBits)): Specifies the Field Width when the flows of a Traffic Item are tracked by Custom Override.
			Offset (number): Specifies the Offset when the Flows of a Traffic Item are tracked by Custom Override.
			OneToOneMesh (bool): If true, one-one mesh is enabled when flows of a traffic item are tracked by Custom Override.
			ProtocolOffset (str): Specifies the Protocol Offset when flows of a Traffic Item are tracked by Custom Override.
			TrackBy (list(str)): Specifies the tracking option by which the Flows of a Traffic Item are tracked.
			Values (list(str)): Specifies the Values when the Flows of a Traffic Item are tracked by Custom Override.

		Returns:
			self: This instance with matching tracking data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of tracking data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the tracking data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)
