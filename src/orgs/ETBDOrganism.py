'''
Created on Dec 7, 2021

@author: bleem
'''

from src.common import Constants
from src.etbd.Behaviors import Behaviors

from src.orgs.AnOrganism import AnOrganism


class ETBDOrganism(AnOrganism):

	def __init__(self, json_data):
		super().__init__(json_data)
		self.m_indexOfPreviousPopulation = -999
		self.m_indexOfCurrentPopulation = 0
		self.m_blnTransferBehaviors = False
		self.m_behaviors_list = list()

		# An organism object is instantiated when this form is loaded.

		# Verify punishment settings if necessary
		if json_data.check_is_punishment_ok():
			if not self.verify_settings_for_punishment():
				return
		else:
			pass
			# No problemo

		# Create and populate population of potential behaviors
		objPopulation = Behaviors(self.get_behaviors_info())

		# Add population to organism
		self.add(objPopulation)

	def verify_settings_for_punishment(self, json_data):
		# Must use continuous exponential selection, and cannot use midpoint fitness method.
		# if cboSelectionMethod.SelectedIndex = 2 And cboContinuousFunctionForm.SelectedIndex = 3 And not cboFitnessMethod.SelectedIndex = 0:
		if json_data.get_selection_method() == Constants.SELECTION_METHOD_TOURNAMENT and json_data.get_fitness_method() != Constants.FITNESS_METHOD_MIDPOINT :
			# All is copacetic.
			return True
		else:
			# All is not copacetic.
			raise AssertionError("For punishment:\n\n	 1.  The Continuous Selection Method must be used.\n	 2.  The Midpoint Fitness Method cannot be used.\n\nClose this window and make the appropriate selections.")
			return False

	def get_transfer_behaviors(self):
		return self.m_blnTransferBehaviors

	def set_transfer_behaviors(self, value):
		self.m_blnTransferBehaviors = value

	def get_index_of_current_population(self):
		return self.m_indexOfCurrentPopulation

	def get_current_population(self):
		return self.m_behaviors_list[self.m_indexOfCurrentPopulation]

	def get_behaviors(self, index):
		return self.m_behaviors_list[index]

	def set_behaviors(self, index, value):
		self.m_behaviors_list[index] = value

	def add(self, behaviors):
		self.m_behaviors_list.append(behaviors)

	def remove(self, behaviors):
		self.m_behaviors_list.remove(behaviors)

	def remove_population_at(self, index):
		del self.m_behaviors_list[index]

	def clear_organism(self):
		self.m_behaviors_list.clear()

	def count(self):
		return len(self.m_behaviors_list)

	def get_item(self, index):
		return self.m_behaviors_list[index]

	# used to be called reset_population()
	def reset_state(self):
		self.get_current_population().reset_population()

	def reset_populations(self):
		for behaviors in self.m_behaviors_list:
			behaviors.reset_population()

	def forced_mut_punish(self, punishMag, mutFuncParam, loBoundaryPheno, loTargetPheno, hiTargetPheno, hiBoundaryPheno):
		self.get_current_population().forced_mut_punish(punishMag, mutFuncParam, loBoundaryPheno, loTargetPheno, hiTargetPheno, hiBoundaryPheno)

	def diff_repel_punish(self, paramPunisher, dblValueAdjustment):
		self.get_current_population().diff_repel_punish(paramPunisher, dblValueAdjustment)

	def get_raillard_reinforcer_bailouts(self):
		return self.get_current_population().get_raillard_reinforcer_bailouts()

	def set_raillard_reinforcer_bailouts(self, value):
		self.get_current_population().set_raillard_reinforcer_bailouts(value)

	def get_raillard_punisher_bailouts(self):
		return self.get_current_population().get_raillard_punisher_bailouts()

	def set_raillard_punisher_bailouts(self, value):
		self.get_current_population().set_raillard_punisher_bailouts(value)

	def get_index_of_emitted_pheno(self):
		return self.get_current_population().get_index_of_emitted_pheno()

	def set_index_of_emitted_pheno(self, value):
		self.get_current_population().set_index_of_emitted_pheno(value)

	def get_sd_charge(self):
		return self.get_current_population().get_sd_charge()

	def get_sd_charges(self):
		return self.get_current_population().get_sd_charges()

	def set_preload_population(self, value):
		self.get_current_population().set_preload_population(value)

	def get_generations_run(self):
		return self.get_current_population().get_generations_run()

	def set_pref_rev_selection(self, selectionParameter, percentToReplaceOnSelection, value):
		self.get_current_population().set_pref_rev_selection(selectionParameter, percentToReplaceOnSelection, value)

	# double
	def set_selection(self, selectionParameter, value):
		self.get_current_population().set_selection(selectionParameter, value)

	# double, double
	def set_selection_overload(self, paramReinforcer, paramPunisher, value):
		self.get_current_population().set_selection_overload(paramReinforcer, paramPunisher, value)

	# double, int
	def set_selection_overload_2(self, selectionParameter, midpoint, value):
		self.get_current_population().set_selection_overload2(selectionParameter, midpoint, value)

	def is_ready_to_emit(self):
		return self.get_current_population().is_ready_to_emit()

	def emit_behavior(self):
		return self.get_current_population().emit_behavior()

	def set_sdcolor(self, value):
		self.m_currentSDColor = value
		blnPopulationPresent = False
		lstIntegerPhenotypes = list()

		for i in range(len(self.m_behaviors_list)):
			behaviors = self.m_behaviors_list.get(i)
			if behaviors.get_SDID() == self.m_currentSDColor:
					blnPopulationPresent = True
					self.m_indexOfCurrentPopulation = i
					break

		if not blnPopulationPresent:
			raise AssertionError("No population associated with discriminative stimulus " + self.m_currentSDColor)

		if self.get_transfer_behaviors():
			if self.m_indexOfPreviousPopulation == -999:
				# There is no previous population so there is no transfer of behaviors.
				pass
			else:
				prev_population = self.m_behaviors_list(self.m_indexOfPreviousPopulation)
				for i in range(1, prev_population.get_num_behaviors() + 1):
					lstIntegerPhenotypes.append(prev_population.get_behavior_at_index(i - 1).get_integer_value())

				# 'Transfer them to this population; the TransferBehaviors procedure knows how to do this correctly (knock on wood).
				self.get_current_population().transfer_behaviors(lstIntegerPhenotypes)
