'''
Created on May 21, 2021
Translated May 23, 2021

@author: bleem
'''
from src.common import Converter


class BehaviorsInfo(object):

	def __init__(self):
		self.m_SDID = None  # 'Identifies the discriminative stimulus associated with this population
		self.m_DecayOfTransfer = None  #  ' To calcuate transfer from the previous SD
		self.m_ViscosityTicks = None  #  ' To arrange viscous populations
		self.m_CreateFromSynthetic = None  #  ' Flag for viscosity options
		self.m_UseGrayCodes = None  #  ' Flag for Gray code (True) vs. binary code (False)
		self.m_LowPhenotype = None  #
		self.m_HighPhenotype = None  #
		self.m_NumBehaviors = None  #
		self.m_PercentToReplace = None  #  ' Percentage of behaviors in the old generation to replace each new generation when selection occurs (remarks modified 1/2018)
		self.m_PercentToReplace2 = None  #  ' Percentage of behaviors to replace when selection does not occur (added 1/2018)
		self.m_PunishmentMethod = None  #
		self.m_KelleyN = None  # ' Exponent for use with repulsion punishment
		self.m_FOMOa = None  #  ' Exponent for use with forced mutation punishment
		self.m_FitnessMethod = None  #
		self.m_FitnessLandscape = None  #
		self.m_RW_Info = None  #  ' Rescorla-Wagner parameters for charging the discriminative stimulus
		self.m_MutationInfo = None  #  ' For the Mutator
		self.m_RecombinationInfo = None  #  ' For the Recombinator
		self.m_SelectionInfo = None  #  'For the Selector

		# parameters for non-ETBD organisms

		self.m_num_output_nodes = None
		self.m_num_hidden_nodes = None
		self.m_num_firing_hidden_nodes = None

		self.m_net_one_magnitude_multiplier = None
		self.m_net_one_magnitude_numerator = None
		self.m_net_one_neutral_magnitude = None

		self.m_net_two_neutral_magnitude = None
		self.m_net_two_selection_strength_multiplier = None
		self.m_net_two_selection_strength_exponent = None
		self.m_net_two_num_hidden_nodes = None

		self.m_ml_learning_rate = None
		self.m_ml_discount_rate = None
		self.m_ml_num_slots = None
		# self.m_ml_reward_multiplier = None
		self.m_ml_reward_exponent = None
		self.m_ml_pessimism = None
		self.m_ml_extinction = None
		self.m_ml_epsilon = None

	def get_ml_discount_rate(self):
		return self.__m_ml_discount_rate

	def set_ml_discount_rate(self, value):
		self.__m_ml_discount_rate = value

	def get_ml_epsilon(self):
		return self.m_ml_epsilon

	def set_ml_epsilon(self, value):
		self.m_ml_epsilon = value

	def get_ml_extinction(self):
		return self.__m_ml_extinction

	def set_ml_extinction(self, value):
		self.__m_ml_extinction = value

	def get_ml_pessimism(self):
		return self.__m_ml_pessimism

	def set_ml_pessimism(self, value):
		self.__m_ml_pessimism = value

	def get_ml_reward_exponent(self):
		return self.m_ml_reward_exponent

	def get_ml_learning_rate(self):
		return self.__m_ml_learning_rate

	def get_ml_num_slots(self):
		return self.__m_ml_num_slots

	def get_ml_reward_multiplier(self):
		return self.__m_ml_reward_multiplier

	def set_ml_learning_rate(self, value):
		self.__m_ml_learning_rate = value

	def set_ml_num_slots(self, value):
		self.__m_ml_num_slots = value

	def set_ml_reward_multiplier(self, value):
		self.__m_ml_reward_multiplier = value

	def set_ml_reward_exponent(self, value):
		self.m_ml_reward_exponent = value

	def get_net_two_num_hidden_nodes(self):
		return self.m_net_two_num_hidden_nodes

	def set_net_two_num_hidden_nodes(self, value):
		self.m_net_two_num_hidden_nodes = value

	def get_net_two_neutral_magnitude(self):
		return self.m_net_two_neutral_magnitude

	def set_net_two_neutral_magnitude(self, value):
		self.m_net_two_neutral_magnitude = value

	def get_net_two_selection_strength_multiplier(self):
		return self.m_net_two_selection_strength_multiplier

	def set_net_two_selection_strength_multiplier(self, value):
		self.m_net_two_selection_strength_multiplier = value

	def get_net_two_selection_strength_exponent(self):
		return self.m_net_two_selection_strength_exponent

	def set_net_two_selection_strength_exponent(self, value):
		self.m_net_two_selection_strength_exponent = value

	def get_net_one_magnitude_slope(self):
		return self.m_net_one_magnitude_slope

	def set_net_one_magnitude_slope(self, value):
		self.m_net_one_magnitude_slope = value

	def get_net_one_magnitude_intercept(self):
		return self.m_net_one_magnitude_intercept

	def set_net_one_magnitude_intercept(self, value):
		self.m_net_one_magnitude_intercept = value

	def get_net_one_neutral_magnitude(self):
		return self.m_net_one_neutral_magnitude

	def set_net_one_neutral_magnitude(self, value):
		self.m_net_one_neutral_magnitude = value

	def get_num_firing_hidden_nodes(self):
		return self.m_net_one_num_firing_hidden_nodes

	def set_num_firing_hidden_nodes(self, value):
		self.m_net_one_num_firing_hidden_nodes = value

	def get_num_output_nodes(self):
		return self.m_num_output_nodes

	def set_num_output_nodes(self, value):
		self.m_num_output_nodes = value

	def get_num_hidden_nodes(self):
		return self.m_num_hidden_nodes

	def set_num_hidden_nodes(self, value):
		self.m_num_hidden_nodes = value

	def get_sdid(self):
		return self.m_SDID

	def get_sd_str(self):
		return Converter.convert_sd_id_to_color(self.m_SDID)

	def get_decay_of_transfer(self):
		return self.m_DecayOfTransfer

	def get_viscosity_ticks(self):
		return self.m_ViscosityTicks

	def get_create_from_synthetic(self):
		return self.m_CreateFromSynthetic

	def get_use_gray_codes(self):
		return self.m_UseGrayCodes

	def get_low_phenotype(self):
		return self.m_LowPhenotype

	def get_high_phenotype(self):
		return self.m_HighPhenotype

	def get_num_behaviors(self):
		return self.m_NumBehaviors

	def get_percent_to_replace(self):
		return self.m_PercentToReplace

	def get_percent_to_replace_2(self):
		return self.m_PercentToReplace2

	def get_punishment_method(self):
		return self.m_PunishmentMethod

	def get_punishment_method_str(self):
		return Converter.convert_punishment_method_to_string(self.m_PunishmentMethod)

	def get_kelley_n(self):
		return self.m_KelleyN

	def get_fomo_a(self):
		return self.m_FOMOa

	def get_fitness_method(self):
		return self.m_FitnessMethod

	def get_fitness_method_str(self):
		return Converter.convert_fitness_method_to_string(self.m_FitnessMethod)

	def get_fitness_landscape(self):
		return self.m_FitnessLandscape

	def get_fitness_landscape_str(self):
		return Converter.convert_fitness_landscape_to_string(self.m_FitnessLandscape)

	def get_RW_info(self):
		return self.m_RW_Info

	def get_mutation_info(self):
		return self.m_MutationInfo

	def get_recombination_info(self):
		return self.m_RecombinationInfo

	def get_selection_info(self):
		return self.m_SelectionInfo

	def set_sdid(self, value):
		assert isinstance(value, int)
		self.m_SDID = value

	def set_decay_of_transfer(self, value):
		self.m_DecayOfTransfer = value

	def set_viscosity_ticks(self, value):
		self.m_ViscosityTicks = value

	def set_create_from_synthetic(self, value):
		self.m_CreateFromSynthetic = value

	def set_use_gray_codes(self, value):
		self.m_UseGrayCodes = value

	def set_low_phenotype(self, value):
		self.m_LowPhenotype = value

	def set_high_phenotype(self, value):
		self.m_HighPhenotype = value

	def set_num_behaviors(self, value):
		self.m_NumBehaviors = value

	def set_percent_to_replace(self, value):
		self.m_PercentToReplace = value

	def set_percent_to_replace_2(self, value):
		self.m_PercentToReplace2 = value

	def set_punishment_method(self, value):
		self.m_PunishmentMethod = value

	def set_kelley_n(self, value):
		self.m_KelleyN = value

	def set_fomo_a(self, value):
		self.m_FOMOa = value

	def set_fitness_method(self, value):
		self.m_FitnessMethod = value

	def set_fitness_landscape(self, value):
		self.m_FitnessLandscape = value

	def set_RW_info(self, value):
		self.m_RW_Info = value

	def set_mutation_info(self, value):
		self.m_MutationInfo = value

	def set_recombination_info(self, value):
		self.m_RecombinationInfo = value

	def set_selection_info(self, value):
		self.m_SelectionInfo = value

