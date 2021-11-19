'''
Created on May 24, 2021
Translated May 24, 2021

@author: bleem
'''

import Converter


class SelectionInfo(object):
	'''
	classdocs
	'''

	def __init__(self):
		self.m_SelectionMethod = None
		self.m_ContinuousFunctionForm = None
		self.m_HighPhenotype = None
		self.m_LowPhenotype = None
		self.m_FitnessLandscape = None
		self.m_MatchmakingMethod = None

	def get_selection_method(self):
		return self.m_SelectionMethod

	def get_selection_method_str(self):
		return Converter.convert_selection_method_to_string(self.m_SelectionMethod)

	def get_continuous_function_form(self):
		return self.m_ContinuousFunctionForm

	def get_continuous_function_form_str(self):
		return Converter.convert_continuous_function_form_to_string(self.m_ContinuousFunctionForm)

	def get_high_phenotype(self):
		return self.m_HighPhenotype

	def get_low_phenotype(self):
		return self.m_LowPhenotype

	def get_fitness_landscape(self):
		return self.m_FitnessLandscape

	def get_matchmaking_method(self):
		return self.m_MatchmakingMethod

	def set_selection_method(self, value):
		self.m_SelectionMethod = value

	def set_continuous_function_form(self, value):
		self.m_ContinuousFunctionForm = value

	def set_high_phenotype(self, value):
		self.m_HighPhenotype = value

	def set_low_phenotype(self, value):
		self.m_LowPhenotype = value

	def set_fitness_landscape(self, value):
		self.m_FitnessLandscape = value

	def set_matchmaking_method(self, value):
		self.m_MatchmakingMethod = value
