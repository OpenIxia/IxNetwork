from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Meter(Base):
	"""The Meter class encapsulates a user managed meter node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Meter property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'meter'

	def __init__(self, parent):
		super(Meter, self).__init__(parent)

	@property
	def Band(self):
		"""An instance of the Band class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.band.Band)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.band import Band
		return Band(self)

	@property
	def Flags(self):
		"""An instance of the Flags class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.flags.Flags)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.openflow.flags import Flags
		return Flags(self)._select()

	@property
	def __id__(self):
		"""The value by which a meter is uniquely identified within a switch. The default value is 1.

		Returns:
			number
		"""
		return self._get_attribute('__id__')
	@__id__.setter
	def __id__(self, value):
		self._set_attribute('__id__', value)

	@property
	def Description(self):
		"""A description of the meter.

		Returns:
			str
		"""
		return self._get_attribute('description')
	@Description.setter
	def Description(self, value):
		self._set_attribute('description', value)

	@property
	def Enabled(self):
		"""If selected, this meter is used in this controller configuration.

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def MeterAdvertise(self):
		"""If this check box is selected, the following happens: Meter ADD message is sent automatically after OpenFlow channel comes up. Meter ADD or DEL message is sent out when the Enable is checked or cleared respectively.When this check box is not selected, no meter is advertised when the OpenFlow channel comes up or when the Enable check box is disabled/enabled. This field is useful to send meter ADD/MOD/DEL messages on demand, or doing negative testing. The on-demand ADD/MOD/DEL messages can be sent by choosing the appropriate option from the right-click menu or from the ribbon option of Update Meter Mod.

		Returns:
			bool
		"""
		return self._get_attribute('meterAdvertise')
	@MeterAdvertise.setter
	def MeterAdvertise(self, value):
		self._set_attribute('meterAdvertise', value)

	@property
	def UpdateMeterModStatus(self):
		"""It is a read-only field which indicates if any meter or associated band value is changed in the GUI. If any meter/band is changed then this status indicates to the user to send a Meter MOD request to the switch so that the changed value is updated in switch.

		Returns:
			str
		"""
		return self._get_attribute('updateMeterModStatus')

	def add(self, __id__=None, Description=None, Enabled=None, MeterAdvertise=None):
		"""Adds a new meter node on the server and retrieves it in this instance.

		Args:
			__id__ (number): The value by which a meter is uniquely identified within a switch. The default value is 1.
			Description (str): A description of the meter.
			Enabled (bool): If selected, this meter is used in this controller configuration.
			MeterAdvertise (bool): If this check box is selected, the following happens: Meter ADD message is sent automatically after OpenFlow channel comes up. Meter ADD or DEL message is sent out when the Enable is checked or cleared respectively.When this check box is not selected, no meter is advertised when the OpenFlow channel comes up or when the Enable check box is disabled/enabled. This field is useful to send meter ADD/MOD/DEL messages on demand, or doing negative testing. The on-demand ADD/MOD/DEL messages can be sent by choosing the appropriate option from the right-click menu or from the ribbon option of Update Meter Mod.

		Returns:
			self: This instance with all currently retrieved meter data using find and the newly added meter data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the meter data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, __id__=None, Description=None, Enabled=None, MeterAdvertise=None, UpdateMeterModStatus=None):
		"""Finds and retrieves meter data from the server.

		All named parameters support regex and can be used to selectively retrieve meter data from the server.
		By default the find method takes no parameters and will retrieve all meter data from the server.

		Args:
			__id__ (number): The value by which a meter is uniquely identified within a switch. The default value is 1.
			Description (str): A description of the meter.
			Enabled (bool): If selected, this meter is used in this controller configuration.
			MeterAdvertise (bool): If this check box is selected, the following happens: Meter ADD message is sent automatically after OpenFlow channel comes up. Meter ADD or DEL message is sent out when the Enable is checked or cleared respectively.When this check box is not selected, no meter is advertised when the OpenFlow channel comes up or when the Enable check box is disabled/enabled. This field is useful to send meter ADD/MOD/DEL messages on demand, or doing negative testing. The on-demand ADD/MOD/DEL messages can be sent by choosing the appropriate option from the right-click menu or from the ribbon option of Update Meter Mod.
			UpdateMeterModStatus (str): It is a read-only field which indicates if any meter or associated band value is changed in the GUI. If any meter/band is changed then this status indicates to the user to send a Meter MOD request to the switch so that the changed value is updated in switch.

		Returns:
			self: This instance with matching meter data retrieved from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def read(self, href):
		"""Retrieves a single instance of meter data from the server.

		Args:
			href (str): An href to the instance to be retrieved

		Returns:
			self: This instance with the meter data from the server available through an iterator or index

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._read(href)

	def UpdateMeterMod(self, Arg2):
		"""Executes the updateMeterMod operation on the server.

		NOT DEFINED

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=meter)): The method internally set Arg1 to the current href for this instance
			Arg2 (str(sendMeterAdd|sendMeterModify|sendMeterRemove)): NOT DEFINED

		Returns:
			bool: NOT DEFINED

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('UpdateMeterMod', payload=locals(), response_object=None)
