'''
Created on May 21, 2021
Translated May 23, 2021

@author: bleem
'''
from src.common import Constants
from src.common import Converter
from src.common.BehaviorsInfo import BehaviorsInfo
from src.common.RescorlaWagnerParameters import RescorlaWagnerParameters
from src.etbd.MutationInfo import MutationInfo
from src.etbd.RecombinationInfo import RecombinationInfo
from src.etbd.SelectionInfo import SelectionInfo


# This class is an abstract container for the specific organisms
class AnOrganism:
	''' 
	classdocs
	'''

	def __init__(self, json_data):
		self.m_currentSDColor = Constants.SD_COLOR_NULL
		self.stuBehaviorsInfo = self.load_behaviors_info(json_data)

	def get_behaviors_info(self):
		return self.stuBehaviorsInfo

	def load_behaviors_info(self, json_data):
		stuBehaviorsInfo = BehaviorsInfo()
		# Dim objPopulation As Behaviors
		# Dim objStringBuilder As New System.Text.StringBuilder
		#Read form--------------------------------------------------
		# Get discriminative stimulus
		stuBehaviorsInfo.set_sdid(json_data.get_sdid())
		if stuBehaviorsInfo.get_sdid() == -1:
			return  #  This SD as already been used.

		# Gray codes
		if json_data.use_gray_codes():
			stuBehaviorsInfo.set_use_gray_codes(True)
		else:
			stuBehaviorsInfo.set_use_gray_codes(False)

		# Properties
		stuBehaviorsInfo.set_decay_of_transfer(json_data.get_decay_of_transfer())
		stuBehaviorsInfo.set_fomo_a(json_data.get_fomo_a())

		#-----Viscosity
		if json_data.add_viscosity():
			stuBehaviorsInfo.set_viscosity_ticks(json_data.get_viscosity_ticks())
			if json_data.get_viscosity_selected_index() == 0:
				# "original"
				stuBehaviorsInfo.set_create_from_synthetic(False)
			else:
				# "amalgamated"
				stuBehaviorsInfo.set_create_from_synthetic(True)

		else:
			# if populations are to have no viscosity, then ViscosityTicks = 0
			# Note that when ViscosityTicks = 1 there is also no viscosity.
			# When ViscosityTicks = 0, the standard method of emitting a behavior
			# (random selection among phenotypes) is used; when ViscosityTicks = 1
			# the method based on relative frequencies is used.
			# Both methods should give the same results.
			stuBehaviorsInfo.set_viscosity_ticks(0)

		stuBehaviorsInfo.set_num_behaviors(json_data.get_num_behaviors())
		stuBehaviorsInfo.set_low_phenotype(json_data.get_low_phenotype())
		stuBehaviorsInfo.set_high_phenotype(json_data.get_high_phenotype())
		stuBehaviorsInfo.set_percent_to_replace(json_data.get_percent_to_replace())
		stuBehaviorsInfo.set_percent_to_replace_2(json_data.get_percent_to_replace_2())
		stuBehaviorsInfo.set_fitness_method(json_data.get_fitness_method())
		stuBehaviorsInfo.set_fitness_landscape(json_data.get_fitness_landscape())
		stuBehaviorsInfo.set_punishment_method(json_data.get_punishment_method())
		# Data structures
		stuBehaviorsInfo.set_RW_info(self.load_RW_info(json_data))
		stuBehaviorsInfo.set_selection_info(self.load_selection_info(json_data))
		stuBehaviorsInfo.set_recombination_info(self.load_recombination_info(json_data))
		stuBehaviorsInfo.set_mutation_info(self.load_mutation_info(json_data))
		# Non-ETBD parameters
		stuBehaviorsInfo.set_num_hidden_nodes(json_data.get_num_hidden_nodes())
		stuBehaviorsInfo.set_num_output_nodes(json_data.get_num_output_nodes())
		stuBehaviorsInfo.set_net_one_num_firing_hidden_nodes(json_data.get_net_one_num_firing_hidden_nodes())
		stuBehaviorsInfo.set_net_one_magnitude_slope(json_data.get_net_one_magnitude_slope())
		stuBehaviorsInfo.set_net_one_magnitude_intercept(json_data.get_net_one_magnitude_intercept())

		return stuBehaviorsInfo

	def reset_state(self):
		raise NotImplementedError
		# TODO - implement this for the other organism types

	def is_ready_to_emit(self):
		raise NotImplementedError
		# TODO - implement this for the other organism types

	def emit_behavior(self):
		raise NotImplementedError
		# TODO - implement this for the other organism types

	def set_selection(self, selectionParameter, value):
		raise NotImplementedError
		# TODO - implement this for the other organism types

	def load_selection_info(self, json_data):

		stuSelectionInfo = SelectionInfo()
		stuSelectionInfo.set_selection_method(json_data.get_selection_method())
		stuSelectionInfo.set_continuous_function_form(json_data.get_continuous_function_form())

		# High Phenotype------------------------------------------------------(added to implement punishment)
		stuSelectionInfo.set_high_phenotype(json_data.get_high_phenotype())

		# Fitness Landscare---------------------------------------------------(added to implement punishment)
		stuSelectionInfo.set_fitness_landscape(json_data.get_fitness_landscape())
		stuSelectionInfo.set_matchmaking_method(json_data.get_matchmaking_method())

		return stuSelectionInfo

	def load_recombination_info(self, json_data):

		stuRecombinationInfo = RecombinationInfo()
		stuRecombinationInfo.set_method(json_data.get_recombination_method())

		if json_data.get_recombination_method() == Constants.RECOMBINATION_METHOD_CROSSOVER:
			stuRecombinationInfo.set_points(json_data.get_crossover_points())

		return stuRecombinationInfo

	def load_mutation_info(self, json_data):

		stuMutationInfo = MutationInfo()
		stuMutationInfo.set_method(json_data.get_mutation_method())

		if stuMutationInfo.get_method() == Constants.MUTATION_METHOD_GAUSSIAN:
			stuMutationInfo.set_sd(json_data.get_gaussian_mutation_sd())
			stuMutationInfo.set_boundary(json_data.get_mutation_boundary())

		stuMutationInfo.set_rate(json_data.get_mutation_rate())

		# Redundant info needed by the Mutator object
		if json_data.use_gray_codes():
			stuMutationInfo.set_use_gray_codes(True)
		else:
			stuMutationInfo.set_use_gray_codes(False)
		stuMutationInfo.set_high_phenotype(json_data.get_high_phenotype())
		stuMutationInfo.set_low_phenotype(json_data.get_low_phenotype())

		return stuMutationInfo

	def get_sdcolor(self):
		return self.m_currentSDColor

	def get_sdcolor_str(self):
		return Converter.convert_sd_color_to_string(self.m_currentSDColor)

	def set_sdcolor(self, value):
		raise NotImplementedError

	def load_RW_info(self, json_data):

		stuRWInfo = RescorlaWagnerParameters()

		stuRWInfo.set_alpha(json_data.get_alpha())
		stuRWInfo.set_beta_0(json_data.get_beta_0())
		stuRWInfo.set_beta_1(json_data.get_beta_1())
		stuRWInfo.set_berg_a(1)  # Hard coded to 1 for now.
		stuRWInfo.set_lambda(1)  # Hard coded to 1 for now.

		return stuRWInfo
