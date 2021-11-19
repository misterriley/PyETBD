'''
Created on May 25, 2021

@author: bleem
'''
import Converter


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
		self.m_EqualPunishmentRI = None
		self.m_SinglePunishmentRI = None
		self.m_PunishmentMag = None  # 0 to 1
		self.m_MutFuncParam = None
		self.m_ProportionPunishment = None

		self.num_schedules = num_schedules

		self.m_SchedValues1 = [None] * num_schedules
		self.m_SchedValues2 = [None] * num_schedules
		self.m_Mags1 = [None] * num_schedules
		self.m_Mags2 = [None] * num_schedules

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

	def get_mag_1(self, schedule_index):
		return self.m_Mags1[schedule_index]

	def get_mag_2(self, schedule_index):
		return self.m_Mags2[schedule_index]

	def get_t_1_lo(self):
		return self.m_T1Lo

	def get_t_1_hi(self):
		return self.m_T1Hi

	def get_t_2_lo(self):
		return self.m_T2Lo

	def get_t_2_hi(self):
		return self.m_T2Hi

	def get_equal_punishment_ri(self):
		return self.m_EqualPunishmentRI

	def get_single_punishment_ri(self):
		return self.m_SinglePunishmentRI

	def get_punishment_mag(self):
		return self.m_PunishmentMag

	def get_mut_func_param(self):
		return self.m_MutFuncParam

	def get_proportion_punishment(self):
		return self.m_ProportionPunishment

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

	def set_equal_punishment_ri(self, value):
		self.m_EqualPunishmentRI = value

	def set_single_punishment_ri(self, value):
		self.m_SinglePunishmentRI = value

	def set_punishment_mag(self, value):
		self.m_PunishmentMag = value

	def set_mut_func_param(self, value):
		self.m_MutFuncParam = value

	def set_proportion_punishment(self, value):
		self.m_ProportionPunishment = value

