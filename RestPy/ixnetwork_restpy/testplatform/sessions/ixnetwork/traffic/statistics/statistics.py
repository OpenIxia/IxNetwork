
# Copyright 1997 - 2018 by IXIA Keysight
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
    
from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Statistics(Base):
	"""The Statistics class encapsulates a required statistics node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Statistics property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'statistics'

	def __init__(self, parent):
		super(Statistics, self).__init__(parent)

	@property
	def AdvancedSequenceChecking(self):
		"""An instance of the AdvancedSequenceChecking class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.statistics.advancedsequencechecking.advancedsequencechecking.AdvancedSequenceChecking)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.statistics.advancedsequencechecking.advancedsequencechecking import AdvancedSequenceChecking
		return AdvancedSequenceChecking(self)._select()

	@property
	def CpdpConvergence(self):
		"""An instance of the CpdpConvergence class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.statistics.cpdpconvergence.cpdpconvergence.CpdpConvergence)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.statistics.cpdpconvergence.cpdpconvergence import CpdpConvergence
		return CpdpConvergence(self)._select()

	@property
	def DataIntegrity(self):
		"""An instance of the DataIntegrity class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.statistics.dataintegrity.dataintegrity.DataIntegrity)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.statistics.dataintegrity.dataintegrity import DataIntegrity
		return DataIntegrity(self)._select()

	@property
	def DelayVariation(self):
		"""An instance of the DelayVariation class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.statistics.delayvariation.delayvariation.DelayVariation)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.statistics.delayvariation.delayvariation import DelayVariation
		return DelayVariation(self)._select()

	@property
	def ErrorStats(self):
		"""An instance of the ErrorStats class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.statistics.errorstats.errorstats.ErrorStats)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.statistics.errorstats.errorstats import ErrorStats
		return ErrorStats(self)._select()

	@property
	def InterArrivalTimeRate(self):
		"""An instance of the InterArrivalTimeRate class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.statistics.interarrivaltimerate.interarrivaltimerate.InterArrivalTimeRate)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.statistics.interarrivaltimerate.interarrivaltimerate import InterArrivalTimeRate
		return InterArrivalTimeRate(self)._select()

	@property
	def Iptv(self):
		"""An instance of the Iptv class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.statistics.iptv.iptv.Iptv)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.statistics.iptv.iptv import Iptv
		return Iptv(self)._select()

	@property
	def L1Rates(self):
		"""An instance of the L1Rates class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.statistics.l1rates.l1rates.L1Rates)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.statistics.l1rates.l1rates import L1Rates
		return L1Rates(self)._select()

	@property
	def Latency(self):
		"""An instance of the Latency class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.statistics.latency.latency.Latency)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.statistics.latency.latency import Latency
		return Latency(self)._select()

	@property
	def MisdirectedPerFlow(self):
		"""An instance of the MisdirectedPerFlow class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.statistics.misdirectedperflow.misdirectedperflow.MisdirectedPerFlow)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.statistics.misdirectedperflow.misdirectedperflow import MisdirectedPerFlow
		return MisdirectedPerFlow(self)._select()

	@property
	def MultipleJoinLeaveLatency(self):
		"""An instance of the MultipleJoinLeaveLatency class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.statistics.multiplejoinleavelatency.multiplejoinleavelatency.MultipleJoinLeaveLatency)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.statistics.multiplejoinleavelatency.multiplejoinleavelatency import MultipleJoinLeaveLatency
		return MultipleJoinLeaveLatency(self)._select()

	@property
	def OneTimeJoinLeaveLatency(self):
		"""An instance of the OneTimeJoinLeaveLatency class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.statistics.onetimejoinleavelatency.onetimejoinleavelatency.OneTimeJoinLeaveLatency)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.statistics.onetimejoinleavelatency.onetimejoinleavelatency import OneTimeJoinLeaveLatency
		return OneTimeJoinLeaveLatency(self)._select()

	@property
	def PacketLossDuration(self):
		"""An instance of the PacketLossDuration class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.statistics.packetlossduration.packetlossduration.PacketLossDuration)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.statistics.packetlossduration.packetlossduration import PacketLossDuration
		return PacketLossDuration(self)._select()

	@property
	def Prbs(self):
		"""An instance of the Prbs class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.statistics.prbs.prbs.Prbs)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.statistics.prbs.prbs import Prbs
		return Prbs(self)._select()

	@property
	def SequenceChecking(self):
		"""An instance of the SequenceChecking class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.statistics.sequencechecking.sequencechecking.SequenceChecking)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.statistics.sequencechecking.sequencechecking import SequenceChecking
		return SequenceChecking(self)._select()
