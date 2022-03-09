'''
Created on May 24, 2021

@author: bleem
'''

# from playsound import playsound

from src.common.CRunConcurrent import CRunConcurrent
from src.common.ExperimentParameters import ExperimentParameters
from src.common.Logger import log


class frmExperiment(object):
	'''
	classdocs 
	'''

	def __init__(self, frmOrganism):
		'''
		Constructor
		'''
		self.m_intExpNum = 0
		self.m_structExpInfo = []
		self.m_frmOrganism = frmOrganism
		self.m_objConcs = []

	def getObjConcs(self):
		return self.m_objConcs

	def add_experiments(self, json_data):

		# Should probably do this load here

		# Dim test As Integer
		# test = frmConcSchedules.txtPheno1Hi.Text

		self.m_intExpNum = json_data.get_num_experiments()
		for exp_index in range(self.m_intExpNum):
			num_schedules = json_data.get_num_schedules(exp_index)
			ep = ExperimentParameters(num_schedules)

			self.m_structExpInfo.append(ep)

			# Reads experimental info from the form and loads it into a data structure.  Note that only one SD is allowed for now.
			# Note that the PunishmentMag is not checked to ensure that it is in the range, 0 to 1.

			# Dim structExperimentInfo As ExperimentParameters <--This is now declared as a Public structure.  ExperimentParameters is declared in CRunParameters

			# Dim intN As Integer #Number of rows (conditions) in the dataviewgrid
			# Dim dblSchedValues1(), dblSchedValues2() As Double
			# Dim exp_index As Integer
			# Dim strSchedValues1 As String = "" #For reading from structExperimentInfo
			# Dim strSchedValues2 As String = "" #For reading from structExperimentInfo

			ep.set_file_stub(json_data.get_file_stub(exp_index))
			ep.set_output_path(json_data.get_output_path(exp_index))
			ep.set_generations(json_data.get_generations(exp_index))
			ep.set_repetitions(json_data.get_repetitions(exp_index))
			ep.set_sd(json_data.get_sd(exp_index))
			ep.set_sched_type_1(json_data.get_sched_type_1(exp_index))
			ep.set_sched_type_2(json_data.get_sched_type_2(exp_index))
			ep.set_t_1_lo(json_data.get_t_1_lo(exp_index))
			ep.set_t_1_hi(json_data.get_t_1_hi(exp_index))
			ep.set_t_2_lo(json_data.get_t_2_lo(exp_index))
			ep.set_t_2_hi(json_data.get_t_2_hi(exp_index))
			ep.set_organism_type(json_data.get_organism_type())
			ep.set_reset_between_runs(json_data.get_reset_between_runs())
			ep.set_use_sp_schedules(json_data.get_use_sp_schedules(exp_index))

			# exp_index now equals intN
			# raise AssertionError(CStr(exp_index))

			# TODO - start here

			# Load the arrays into the data structure.
			for schedule_index in range(json_data.get_num_schedules(exp_index)):
				ep.set_FDF_mean_1(schedule_index, json_data.get_FDF_mean_1(exp_index, schedule_index))
				ep.set_FDF_mean_2(schedule_index, json_data.get_FDF_mean_2(exp_index, schedule_index))
				ep.set_sched_value_1(schedule_index, json_data.get_sched_value_1(exp_index, schedule_index))
				ep.set_sched_value_2(schedule_index, json_data.get_sched_value_2(exp_index, schedule_index))

				ep.set_COD(json_data.get_COD())

				ep.set_sp_mean(schedule_index, json_data.get_sp_mean(exp_index, schedule_index))
				ep.set_sp_FDF(schedule_index, json_data.get_sp_FDF(exp_index, schedule_index))
				ep.set_sp_ratio(schedule_index, json_data.get_sp_ratio(exp_index, schedule_index))
				ep.set_sp_stop_count(schedule_index, json_data.get_sp_stop_count(exp_index, schedule_index))

				# These If...Then blocks are for punishment
				if json_data.punish_RI_is_enabled():
					ep.set_equal_punishment_ri(schedule_index, json_data.get_equal_punishment_ri(exp_index))
					ep.set_mut_func_param(json_data.get_mut_func_param(exp_index))

				else:
					# This ensures that there will be no lingering punishment info after a "Clear" operation
					ep.set_equal_punishment_ri(schedule_index, 0)

				if json_data.prop_punish_is_enabled(exp_index):
					ep.set_proportion_punishment(schedule_index, json_data.get_proportion_punishment(exp_index))  # The reciprocal of this value (0 to 1) times the reinforcement RI value
					# 																							  				gives the punishment RI value.  Not any more (7/2018).
					# 																							  				Now it is the factor that when multiplied by the RI
					# 																							  				reinforcement value gives the RI punishment value.
					ep.set_mut_func_param(json_data.get_mut_func_param(exp_index))
				else:
					# I guess this ensures the same as in the previous If...Then block
					ep.set_proportion_punishment(schedule_index, 0)

				if json_data.punish_1_RI_is_enabled(exp_index):
					ep.set_single_punishment_ri(json_data.get_single_punishment_ri(exp_index))
					ep.set_mut_func_param(json_data.get_mut_func_param(exp_index))
				else:
					# I guess this ensures the same as in the previous If...Then blocks
					ep.set_single_punishment_ri(schedule_index, 0)

	def clear(self):

		self.m_frmOrganism.clear_organism()
		self.m_frmOrganism.set_exists(False)

	def load_organism(self):

		if self.m_frmOrganism.exists():
			pass
			# myOrganism = None
			# myOrganism = self.m_frmOrganism.get_creature()  # '<--frmOrganism is now a Global variable (in Global declarations class)
		else:
			raise RuntimeError("You didn't build an organism!")

		# 'MsgBox(CStr(myOrganism.Item(0).BehaviorsInfo.MutationInfo.Rate))
		# 'Stop

		# 'Try
		# '	myOrganism = frmOrganism.Creature '<--frmOrganism is now a Global variable (in Global declarations class)
		# 'Catch ex As Exception ' The exception occurs in the organism code and does not pass through here.
		# '	MsgBox("Make sure you built an organism correctly")
		# 'End Try

		# 'myOrganism.SDColor = Organism.SDColor.Yellow 'Looks like this might be working after all!
		# 'Try writing some stuff out from myOrganism.  See how the info box is written on the frmOrganism form

		# 'Test read...The organism is ready to run.  Don't have to read this off until writing the data.  It all appears to be working well.
		# 'Dim stuLocalBehaviorsInfo As BehaviorsInfo <---Module level structure
		# 'For testing, otherwise don't need stuLocalBehaviorsInfo
		# myOrganism.get_item(0).get_behaviors_info()

		#'MsgBox("Discriminative stimulus: " & stuLocalBehaviorsInfo.SDID.ToString) '  It's woikin'!!!
		#'MsgBox("Number of behavior in population: " & stuLocalBehaviorsInfo.NumBehaviors.ToString) '  It's woikin'!!!
		#'MsgBox("Low Phenotype = " & stuLocalBehaviorsInfo.LowPhenotype.ToString & "; High Phenotype = " & stuLocalBehaviorsInfo.HighPhenotype.ToString) '  It's woikin'!!!
		#'MsgBox("Fitness landscape: " & stuLocalBehaviorsInfo.SelectionInfo.FitnessLandscape.ToString) '  It's woikin'!!!
		#'----------------------------------------------------------------------------------------------------------------------

	def run(self, json_data, print_status = True, write_outfile = True):

		self.add_experiments(json_data)
		self.load_organism()
		self.m_objConcs = [None] * self.m_intExpNum

		for i in range(self.m_intExpNum):
			log("starting experiment " + str(i), print_status)
			# Run the experiment and write the data.
			self.m_objConcs[i] = CRunConcurrent(self.m_frmOrganism.get_creature(), i, self.m_structExpInfo[i])
			self.m_objConcs[i].giddyup(print_status, write_outfile)
			log("finishing experiment " + str(i), print_status)

		log("Done giddyuped!", print_status)

