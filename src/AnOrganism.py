'''
Created on May 21, 2021
Translated May 23, 2021

@author: bleem
'''
import Constants, Converter


class AnOrganism:
	''' 
	classdocs
	'''

	def __init__(self):
		self.m_indexOfPreviousPopulation = -999
		self.m_indexOfCurrentPopulation = 0
		self.m_blnTransferBehaviors = False
		self.m_currentSDColor = Constants.SD_COLOR_NULL
		self.m_behaviors_list = list()

	def sanity_check(self):
		count = 0
		for b in self.m_behaviors_list[0].m_behavior_list:
			bools = b.get_binary_bits()
			count += bools[1]  # something fishy is going on with the first bit of the binary strings

		print(count)

	def get_transfer_behaviors(self):
		return self.m_blnTransferBehaviors

	def set_transfer_behaviors(self, value):
		self.m_blnTransferBehaviors = value

	def get_sdcolor(self):
		return self.m_currentSDColor

	def get_sdcolor_str(self):
		return Converter.convert_sd_color_to_string(self.m_currentSDColor)

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

	def get_index_of_current_population(self):
		return self.m_indexOfCurrentPopulation

	def get_current_population(self):
		return self.m_behaviors_list[self.m_indexOfCurrentPopulation]

	def get_sd_charge(self):
		return self.get_current_population().get_sd_charge()

	def get_sd_charges(self):
		return self.get_current_population().get_sd_charges()

	def get_behaviors_info(self):
		return self.get_current_population().get_behaviors_info()

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

	def get_behaviors(self, index):
		return self.m_behaviors_list[index]

	def set_behaviors(self, index, value):
		self.m_behaviors_list[index] = value

	def emit_behavior(self):
		return self.get_current_population().emit_behavior()

	def reset_population(self):
		self.get_current_population().reset_population()

	def reset_populations(self):
		for behaviors in self.m_behaviors_list:
			behaviors.reset_population()

	def forced_mut_punish(self, punishMag, mutFuncParam, loBoundaryPheno, loTargetPheno, hiTargetPheno, hiBoundaryPheno):
		self.get_current_population().forced_mut_punish(punishMag, mutFuncParam, loBoundaryPheno, loTargetPheno, hiTargetPheno, hiBoundaryPheno)

	def diff_repel_punish(self, paramPunisher, dblValueAdjustment):
		self.get_current_population().diff_repel_punish(paramPunisher, dblValueAdjustment)

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
