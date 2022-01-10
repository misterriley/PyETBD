'''
Created on Jan 6, 2022

@author: bleem
This class implements Stubbs and Pliskoff style schedules
'''
import numpy

from src.common.CRandomNumber import CRandomNumber


class SPSchedule(object):

	def __init__(self):
		self.mean = None
		self.m_ratio = None
		self.m_FDF = None
		self.m_stop_count = None
		self.m_baited_target_class = None
		self.m_target_1_prob = None

		self.m_objRandom = CRandomNumber()
		self.m_reinforcers_dispensed = 0
		self.m_dblCurrentInterval = 0
		self.m_intTicksIntoInterval = 0  # Time (ticks) since the last reinforcement.
		self.m_blnSaveIRIs = False
		self.m_IRIArray = list()

	def get_mean(self):
		return self.m_mean

	def set_mean(self, value):
		self.m_mean = value
		self.m_objRandom.set_mean(self.m_mean)
		self.get_new_interval()
		self.m_intTicksIntoInterval = 0
		self.m_IRIArray = list()
		self.m_reinforcers_dispensed = 0

	def get_ratio(self):
		return self.m_ratio

	def set_ratio(self, value):
		self.m_ratio = value
		self.m_target_1_prob = value / (1.0 + value)

	def get_FDF(self):
		return self.m_FDF

	def set_FDF(self, value):
		self.m_FDF = value

	def is_past_stop_count(self):
		return self.m_reinforcers_dispensed >= self.m_stop_count

	def set_stop_count(self, value):
		self.m_stop_count = value

	def get_save_IRIs(self):
		raise NotImplementedError

	def set_save_IRIs(self, value):
		raise NotImplementedError

	def get_IRI_array(self):
		raise NotImplementedError

	def get_new_interval(self):
		self.m_dblCurrentInterval = self.m_objRandom.get_exponential_double()
		self.m_baited_target_class = 1 if numpy.random.uniform() < self.m_target_1_prob else 2

	def tick_tock(self):
		self.m_intTicksIntoInterval += 1

	def is_reinforcement_set_up(self, target_class):
		if self.m_intTicksIntoInterval >= self.m_dblCurrentInterval and target_class == self.m_baited_target_class:
			if self.m_blnSaveIRIs:
				self.m_IRIArray.append(self.m_intTicksIntoInterval)
			self.get_new_interval()
			self.m_intTicksIntoInterval = 0
			self.m_reinforcers_dispensed += 1
			return True
		return False
