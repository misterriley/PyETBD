from src.common.CRandomNumber import CRandomNumber

	# Arranges a Random Ratio Schedule.

	# The mean of the schedule can be passed to the constructor or it can be set via the Mean property.
	# A schedule object can also save and return obtained IRIs if desired.  To do so, set the SaveIRIs property to true
	# from the calling program before the schedule is run, and then retrieve the IRIs from the IRIArray property after
	# the run is complete.

	# Usage:
	# Call the Response procedure after every target response.  This advances the ratio counter.  if IRI distributions are desired, then
	# call the TickTock procedure every time tick, e.g., after each behavioral emission.  This advances the IRI timer.
	# if a target behavior is emitted, call the Response procedure as usual, and the TickTock procedure if desired, then query the ReinforcementSetUp function
	# to determine whether reinforcement is available.


class RRSchedule(object):

	def __init__(self, intMean = None):
		self.m_Mean = 0
		self.m_intCurrentRatio = 0
		self.m_intPecksIntoRatio = 0  # Pecks (responses) since the last reinforcement.
		self.m_intTicksIntoIRI = 0  # Time (ticks) since the last reinforcement.
		self.m_blnSaveIRIs = False
		self.m_IRIArray = []

		self.m_objRandom = CRandomNumber()
		if intMean is not None:
			self.set_mean(intMean)

	# Sets or returns the mean of the RR schedule. Note that this is an integer.
	def get_mean(self):
		return self.m_Mean

	def set_mean(self, value):
		self.m_Mean = value
		self.m_objRandom.set_mean(self.m_Mean)
		# Initialize
		self.get_new_ratio()  # Sets the first ratio
		self.m_intPecksIntoRatio = 0  # In case the object is reused
		self.m_IRIArray = []  # In case the object is reused

	def get_save_IRIs(self):
		return self.m_blnSaveIRIs

	def set_save_IRIs(self, value):
		self.m_blnSaveIRIs = value

	def get_IRI_array(self):
		return self.m_IRIArray

	def get_new_ratio(self):
		self.m_intCurrentRatio = self.m_objRandom.get_exponential_double()

	def response(self):
		# Advances response count.  Must be called _every_ time there is a response.
		self.m_intPecksIntoRatio += 1

	def tick_tock(self):
		# Advances time ticks.  Must be called _every_ time tick.
		self.m_intTicksIntoIRI += 1

	def is_reinforcement_set_up(self):
		# Query for reinforcement availability after each target response.  The Response procedure must be called first, and also,
		# if an IRI distibution is desired, the TickTock procedure must be called first.
		if self.m_intPecksIntoRatio >= self.m_intCurrentRatio:
			# Reinforcement is available.  Deliver it.
			if self.m_blnSaveIRIs:
				# Save IRI
				self.m_IRIArray.Add(self.m_intTicksIntoIRI)

			self.get_new_ratio()
			self.m_intPecksIntoRatio = 0
			self.m_intTicksIntoIRI = 0
			return True
		else:
			# No reinforcement available
			return False

	def set_up_query_only(self):
		# For nonindependent Conc RR RR schedules
		if self.m_intPecksIntoRatio >= self.m_intCurrentRatio:
			return True
		else:
			return False
