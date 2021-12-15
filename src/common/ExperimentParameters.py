'''
Created on May 25, 2021

@author: bleem
'''

from src.common import Converter


class ExperimentParameters(object):
	'''
	classdocs
	'''

	def __init__(self, num_schedules):
		'''
		Constructor 
		'''

		# This is for concurrent schedules
		self.m_SD = None
		self.m_SchedType1 = None
		self.m_SchedType2 = None
		self.m_T1Lo = None  # These are the lo and Hi phenotypes for the 2 target classes.
		self.m_T1Hi = None
		self.m_T2Lo = None
		self.m_T2Hi = None
		self.m_EqualPunishmentRI = [None] * num_schedules
		self.m_SinglePunishmentRI = [None] * num_schedules
		self.m_PunishmentMag = None  # 0 to 1
		self.m_MutFuncParam = None
		self.m_ProportionPunishment = [None] * num_schedules
		self.m_organismType = None

		self.num_schedules = num_schedules
		self.num_repetitions = None
		self.num_generations = None

		self.output_path = None
		self.file_stub = None

		self.m_SchedValues1 = [None] * num_schedules
		self.m_SchedValues2 = [None] * num_schedules
		self.m_Mags1 = [None] * num_schedules
		self.m_Mags2 = [None] * num_schedules

		self.reset_between_runs = None

	def set_reset_between_runs(self, value):
		self.reset_between_runs = value

	def get_reset_between_runs(self):
		return self.reset_between_runs

	def set_output_path(self, value):
		self.output_path = value

	def get_output_path(self):
		return self.output_path

	def set_file_stub(self, value):
		self.file_stub = value

	def get_file_stub(self):
		return self.file_stub

	def get_generations(self):
		return self.num_generations

	def set_generations(self, value):
		self.num_generations = value

	def set_repetitions(self, value):
		self.num_repetitions = value

	def get_repetitions(self):
		return self.num_repetitions

	def get_num_schedules(self):
		return self.num_schedules

	def get_all_sched_values_1(self):
		return self.m_SchedValues1

	def get_all_sched_values_2(self):
		return self.m_SchedValues2

	def get_sched_value_1(self, schedule_index):
		return self.m_SchedValues1[schedule_index]

	def get_sched_value_2(self, schedule_index):
		return self.m_SchedValues2[schedule_index]

	def set_sched_value_1(self, schedule_index, value):
		self.m_SchedValues1[schedule_index] = value

	def set_sched_value_2(self, schedule_index, value):
		self.m_SchedValues2[schedule_index] = value

	def get_sd(self):
		return self.m_SD

	def get_sd_str(self):
		return self.get_sd()

	def get_sdid(self):
		return Converter.convert_string_to_sd(self.m_SD)

	def get_sched_type_1(self):
		return self.m_SchedType1

	def get_sched_type_1_str(self):
		return Converter.convert_sched_type_to_string(self.m_SchedType1)

	def get_sched_type_2(self):
		return self.m_SchedType2

	def get_sched_type_2_str(self):
		return Converter.convert_sched_type_to_string(self.m_SchedType2)

	def get_FDF_mean_1(self, schedule_index):
		return self.m_Mags1[schedule_index]

	def get_FDF_mean_2(self, schedule_index):
		return self.m_Mags2[schedule_index]

	def get_t_1_lo(self):
		return self.m_T1Lo

	def get_t_1_hi(self):
		return self.m_T1Hi

	def get_t_2_lo(self):
		return self.m_T2Lo

	def get_t_2_hi(self):
		return self.m_T2Hi

	def get_equal_punishment_ri(self, schedule_index):
		return self.m_EqualPunishmentRI[schedule_index]

	def get_single_punishment_ri(self, schedule_index):
		return self.m_SinglePunishmentRI[schedule_index]

	def get_punishment_mag(self):
		return self.m_PunishmentMag

	def get_mut_func_param(self):
		return self.m_MutFuncParam

	def get_proportion_punishment(self, schedule_index):
		return self.m_ProportionPunishment[schedule_index]

	def set_sd(self, value):
		self.m_SD = value

	def set_sched_type_1(self, value):
		self.m_SchedType1 = value

	def set_sched_type_2(self, value):
		self.m_SchedType2 = value

	def set_sched_mag_1(self, schedule_index, value):
		self.m_Mags1[schedule_index] = value

	def set_sched_mag_2(self, schedule_index, value):
		self.m_Mags2[schedule_index] = value

	def set_t_1_lo(self, value):
		self.m_T1Lo = value

	def set_t_1_hi(self, value):
		self.m_T1Hi = value

	def set_t_2_lo(self, value):
		self.m_T2Lo = value

	def set_t_2_hi(self, value):
		self.m_T2Hi = value

	def set_equal_punishment_ri(self, schedule_index, value):
		self.m_EqualPunishmentRI[schedule_index] = value

	def set_single_punishment_ri(self, schedule_index, value):
		self.m_SinglePunishmentRI[schedule_index] = value

	def set_punishment_mag(self, value):
		self.m_PunishmentMag = value

	def set_mut_func_param(self, value):
		self.m_MutFuncParam = value

	def set_proportion_punishment(self, schedule_index, value):
		self.m_ProportionPunishment[schedule_index] = value

	def set_organism_type(self, value):
		self.m_organismType = value

	def get_organism_type(self):
		return self.m_organismType

