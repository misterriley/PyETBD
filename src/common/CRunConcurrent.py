# ##
# Created on May 24, 2021

# @author: bleem
# ##
import numpy

from src.common import Constants
from src.common import Tallies
from src.common.CProbEmitter import CProbEmitter
from src.common.CWriteData import CWriteData
from src.common.Logger import log
from src.common.RISchedule import RISchedule
from src.common.RRSchedule import RRSchedule
from src.common.SPSchedule import SPSchedule

PRINT_EVERY_N_GENS = 1000
GENS_FOR_SP_SCHEDULES = 1000000  # must be big enough to go to stop counts


class CRunConcurrent(object):
	# ##
	# classdocs
	# ##

	def __init__(self, myOrganism, experiment_index, experiment_parameters):
		# ##
		# Constructor
		# ##

		#This runs a concurrent RI RI schedule only for now****************************************************************************************************
		self.m_myOrganism = None
		self.m_structExpInfo = experiment_parameters
		self.m_intRepetitions = None
		self.m_intGenerations = None
		self.m_intSchedules = None
		self.m_experiment_index = experiment_index

		# ExperimentParameters structure is defined in CRunParameters.vb.  Does it have to be declared with the "New" keyword?  Doesn#t seem to make a difference either way.
		self.m_strOutpath = None
		self.m_strFileStub = None

		# intEmittedPheno(,,) As Integer # This holds the emitted phenotypes.
		# self.m_blnPhenoReinforced(,,) = False # This indicates whether the phenotype was reinforced.
		self.m_objRI1 = RISchedule()
		self.m_objRI2 = RISchedule()
		self.m_objRR1 = RRSchedule()
		self.m_objRR2 = RRSchedule()
		self.m_objRIPunish1 = RISchedule()
		self.m_objRIPunish2 = RISchedule()
		self.m_objPROB1 = CProbEmitter()
		self.m_objPROB2 = CProbEmitter()
		self.m_objBRR = RRSchedule()
		self.m_objBRI = RISchedule()

		self.m_spSched = SPSchedule()

		# Set properties
		self.set_organism(myOrganism)
		self.set_repetitions(experiment_parameters.get_num_repetitions())
		self.set_generations(experiment_parameters.get_num_generations())
		self.set_num_schedules(experiment_parameters.get_num_schedules())

		# in SP schedules the number of actual generations varies - this keeps track
		self.m_num_actual_gens = numpy.zeros((self.m_intRepetitions, self.get_num_schedules()))

		data_shape = (self.m_intRepetitions, self.get_num_schedules(), self.m_intGenerations)
		self.m_intEmittedPheno = numpy.zeros(data_shape)  # Holds the emitted --->These are global; will have to be cleared for a new experiment.
		self.m_blnPhenoReinforced = numpy.zeros(data_shape)  # Whether the pheno was reinforced --->These are global; will have to be cleared for a new experiment.
		# if e_info.get_equal_punishment_RI() != 0 or e_info.get_proportion_punishment() != 0:
		# Equal or proportional punishment is being run.
		# Will always ReDim this for now, because punishment T/F is always written to the files
		self.m_blnPhenoPunished = numpy.zeros(data_shape)  # Whether the pheno was punished --->These are global; will have to be cleared for a new experiment.
		#
		self.m_strOutpath = experiment_parameters.get_output_path()
		self.m_strFileStub = experiment_parameters.get_file_stub()
		#***************************************Test to make sure all this information has been transmitted correctly.
		# e_info stucture is defined in CRunParameters
		# Examine the schedule values--These are correctly transmitted
		# for i As Integer = 1 To UBound(e_info.get_sched_values_1())
		# 	raise AssertionError(CStr(e_info.get_sched_values_1()(i) & CStr(e_info.get_sched_values_2()(i))))
		# Next i
		# Examine the target ranges--these are correct.
		# raise AssertionError(e_info.get_t_1_lo() & "  " & e_info.get_t_1_hi() & "  " & e_info.get_t_2_lo() & "  " & e_info.get_t_2_hi())
		# Stop
		self.m_objLstAltPhenos = [[None]]
		self.m_lstAltTarget = [None]

	def getTallies(self, intRep, intSched):
		return Tallies.tally_schedule(intRep, intSched, self.m_intEmittedPheno, self.m_blnPhenoReinforced, self.m_blnPhenoPunished, False, None, self.m_structExpInfo)

	def getBlnPhenoPunished(self):
		return self.m_blnPhenoPunished

	def getBlnPhenoReinforced(self):
		return self.m_blnPhenoReinforced

	def get_organism(self):
		return self.m_myOrganism

	def set_organism(self, value):
		self.m_myOrganism = value

	def get_experiment_info(self):
		return self.m_structExpInfo

	# Number of schedules (conditions)
	def get_num_schedules(self):
		return self.m_intSchedules

	def set_num_schedules(self, value):
		self.m_intSchedules = value

	# Number of repetitions of each schedule
	def get_num_repetitions(self):
		return self.m_intRepetitions

	def set_repetitions(self, value):
		self.m_intRepetitions = value

	# Number of generations for each repetition
	def get_num_generations(self):
		return self.m_intGenerations

	def set_generations(self, value):
		self.m_intGenerations = value

	def giddyup(self, print_status = True, write_outfile = True):

		# I believe I can control everything from here, including  writing to output files.

		# Runs, RI schedules, RI schedules with superimposed punishment, and probabilistic schedules

		b_info = self.get_organism().get_behaviors_info()
		e_info = self.get_experiment_info()

		if write_outfile:
			objFileWriter = CWriteData(b_info, e_info, self.m_strOutpath, self.m_strFileStub, self.get_num_repetitions(), self.get_num_generations())

		# Dim intRep, intSched As Integer

		# Turn on a discriminative stimulus
		# Organism.SDColor = SDColor.Red # I think this makes the "Item" segment unnecessary throughout.  The "Item" segment was not used in the test-lab code.
		# Will delete it here.

		# for intSched = 1 To Schedules
		# 	#Organism.reset_population() #Actually, don#t need this.  Could just do it all in the for...next loop.
		# 	#Should the population be initialized (i.e., randomized) for each schedule?  Probably.
		# 	myExperiment.txtSchedule.Text = CStr(intSched) #Write to the experiment form
		# 	#Application.DoEvents() #So that write to the text boxes continues unimpaired.
		# 	for intRep = 1 To self.get_num_repetitions()
		# 		self.m_objRI1.set_mean(e_info.get_sched_values_1() # Setting the mean initializes the schedules.  Should this be initialized for every repetition?
		# 		self.m_objRI2.set_mean(e_info.get_sched_values_2()
		# 		Organism.reset_population() #This solves the problem of missing reinforcers!
		# 		#if intRep > 1: Organism.reset_population()
		# 		myExperiment.txtRepetition.Text = CStr(intRep) #Write to the experiment form
		# 		#Application.DoEvents() #So that write to the text boxes continues unimpaired.
		# 		DoARep(intSched, intRep)
		# 	Next intRep
		# Next intSched

		# Repetitions are controlled from this loop
		for intRep in range(self.get_num_repetitions()):
			log("starting rep " + str(intRep), print_status)

			if self.get_experiment_info().get_t_2_lo() == 0 and self.get_experiment_info().get_t_2_hi() == 0 and self.get_experiment_info().get_sched_type_2() != Constants.SCHED_TYPE_NONE:
				raise Exception("Not tested")
				self.DefineBackgroundClass()  # Different background phenos for each repetition.
				self.m_objLstAltPhenos.Add(self.m_lstAltTarget)  # This peserves the background phenos for each repetition so they can be saved if desired.

			# Make sure we#re in a good state before we start if the runs will pile up
			if not e_info.get_reset_between_runs():
				self.get_organism().reset_state()

			for intSched in range(self.get_num_schedules()):

				# Initialize the equal punishment RIs if necessary
				if e_info.get_equal_punishment_ri(intSched) != 0:
					raise Exception("Not tested")
					self.m_objRIPunish1.set_mean(e_info.get_equal_punishment_ri(intSched))
					self.m_objRIPunish2.set_mean(e_info.get_equal_punishment_ri(intSched))

				# Initialize the single punishment RI if necessary
				if e_info.get_single_punishment_ri(intSched) != 0:
					raise Exception("Not tested")
					self.m_objRIPunish1.set_mean(e_info.get_single_punishment_ri(intSched))

				log("\tstarting sched " + str(intSched), print_status)
				#Set the schedules**********************************************************************************************************
				if e_info.get_use_sp_schedules():
					self.m_spSched.set_FDF(e_info.get_sp_FDF(intSched))
					self.m_spSched.set_ratio(e_info.get_sp_ratio(intSched))
					self.m_spSched.set_mean(e_info.get_sp_mean(intSched))
					self.m_spSched.set_stop_count(e_info.get_sp_stop_count(intSched))

				elif e_info.get_sched_type_1() == Constants.SCHED_TYPE_PROB and e_info.get_sched_type_2() == Constants.SCHED_TYPE_PROB:
					# Running probabilistic schedules
					raise Exception("Not tested")
					self.m_objPROB1.set_prob_of_emission(e_info.get_sched_value_1(intSched))
					self.m_objPROB2.set_prob_of_emission(e_info.get_sched_value_2(intSched))
				elif e_info.get_sched_type_1() == Constants.SCHED_TYPE_RI and e_info.get_sched_type_2() == Constants.SCHED_TYPE_RI:
					# Otherwise, running RI schedules or RI schedules with superimposed punishment
					# for RI schedules and RI schedules with superimposed punishment

					self.m_objRI1.set_mean(e_info.get_sched_value_1(intSched))  # Setting the mean initializes the schedules.
					self.m_objRI2.set_mean(e_info.get_sched_value_2(intSched))
					# Initialize proportional punishment RIs if necessary
					if e_info.get_proportion_punishment(intSched) != 0:
						raise Exception("Not tested")
						self.m_objRIPunish1.set_mean((e_info.get_proportion_punishment(intSched)) * e_info.get_sched_values_1(intSched))
						self.m_objRIPunish2.set_mean((e_info.get_proportion_punishment(intSched)) * e_info.get_sched_values_2(intSched))

					# self.m_objRI1.SaveIRIs = True  Don#t do this!
					# self.m_objRI2.SaveIRIs = True  No!
				elif e_info.get_t_2_lo() == 0 and e_info.get_t_2_hi() == 0 and e_info.get_sched_type_2(intSched) != Constants.SCHED_TYPE_NONE:
					# Running single RI schedule on the left, background reinforcement on the right, with or without superimposed punishment
					raise Exception("Not tested")
					self.m_objRI1.set_mean(e_info.get_sched_value_1(intSched))
					if e_info.get_sched_type_2() == Constants.SCHED_TYPE_RI:
						# Running an RI background
						raise Exception("Not tested")
						self.m_objRI2.set_mean(e_info.get_sched_value_2(intSched))  #  Using this schedule object (rather than the background object) for now.
					elif e_info.get_sched_type_2() == Constants.SCHED_TYPE_RR:
						# Running an RR background
						raise Exception("Not tested")
						self.m_objBRR.set_mean(e_info.get_sched_value_2(intSched))
					else:
						raise Exception("Not tested")
						log("Trouble in Giddyup!", print_status)

				elif e_info.get_sched_type_2() == Constants.SCHED_TYPE_NONE or e_info.get_sched_type_2() == Constants.SCHED_TYPE_EXT:
					# Running original implementation of single schedules.  I believe you can superimpose punishment with the code as currently written.
					# This looks like it applies to a Conc RI EXT schedule
					raise Exception("Not tested")
					self.m_objRI1.set_mean(e_info.get_sched_value_1(intSched))  # Setting the mean initializes the schedules.

				elif (e_info.get_sched_type_1() == Constants.SCHED_TYPE_RR and e_info.get_sched_type_2() == Constants.SCHED_TYPE_RR) or (e_info.get_sched_type_1() == Constants.SCHED_TYPE_NRR and e_info.get_sched_type_2() == Constants.SCHED_TYPE_NRR):
					# Running con RR or conc NRR schedules in the components.  It should also be possible to superimpose punishment on these.
					self.m_objRR1.set_mean(e_info.get_sched_value_1(intSched))  # Setting the mean initializes the schedules.
					self.m_objRR2.set_mean(e_info.get_sched_value_2(intSched))

				elif e_info.get_sched_type_1() == Constants.SCHED_TYPE_RILF and e_info.get_sched_type_2() == Constants.SCHED_TYPE_RILF:
					# Running RI schedules with linear feedback in the components.
					raise Exception("Not tested")
					self.m_objRILF1.RRValue = e_info.get_sched_value_1(intSched)
					self.m_objRILF2.RRValue = e_info.get_sched_value_2(intSched)
				else:
					raise Exception("Not tested")
					log("The code does not support running the type of schedule you specified.", print_status)

				if e_info.get_reset_between_runs():
					self.get_organism().reset_state()  # This solves the problem of missing reinforcers! I don#t think the "Item" segment is necessary.

				#Run the schedules*************************************************************************************************************
				if e_info.get_sched_type_1() == Constants.SCHED_TYPE_PROB and e_info.get_sched_type_2() == Constants.SCHED_TYPE_PROB:
					# Running probabilistic schedules
					raise Exception("Not tested")
					self.do_a_prob_sched(intRep, intSched)  #  <---Runs a schedule
				else:
					# Running RI schedules or RI schedules with superimposed punishment.
					self.do_a_sched(intRep, intSched, print_status)  #  <---Runs a schedule
				log("\tfinishing sched " + str(intSched), print_status)
			log("finishing rep " + str(intRep), print_status)
		# At this point the phenotye and reinforcement and, if applicable, punishment arrays for all repetitions and schedules are loaded.

		if write_outfile:
			if e_info.get_use_sp_schedules():
				objFileWriter.set_num_actual_generations(self.m_num_actual_gens)

			# Clear info from form prior to write
			# myExperiment.txtRepetition.Text = ""
			# myExperiment.txtSchedule.Text = ""

			# Write data to .csv file and summary to Excel
			log("Writing .csv file...", print_status)
			# Application.DoEvents()
			objFileWriter.write_csv(self.m_blnPhenoReinforced, self.m_blnPhenoPunished, self.m_intEmittedPheno)

			log("Writing Excel file...", print_status)
			objFileWriter.write_excel(self.m_blnPhenoReinforced, self.m_blnPhenoPunished, self.m_intEmittedPheno)

			# My.Computer.Audio.Play(My.Resources._22Fillywhinnygrunt2000, AudioPlayMode.Background)
			# print("Done giddyuped!")
			# print("Last phenotype = " & CStr(intEmittedPheno(Schedules, Repetitions, Generations)))
			# 22Fillywhinnygrunt2000  My.Computer.Audio.Play(My.Resources.alonebad, AudioPlayMode.Background)

	def do_a_sched(self, intRep, intSched, print_status = True):

		# Runs a schedule and saves the results of each generation.
		e_info = self.get_experiment_info()
		intGen = intEmittedPhenoClass = 0
		intLastEmittedPhenoClass = None
		intLastChangeover = None
		blnRR = False  # Set equal to True if random ratios are being run in the components
		blnNRR = False  # Set equal to True for nonindependent concurrent ratio schedule
		blnRILF = False  # Set equal to True for RI schedule with linear feedback
		blnPunishmentFirst = True  # Determines whether punishment or reinforcement is delivered first when both are delivered in a time tick.
		# 										  I believe True is now permanent.
		blnPunishmentDelivered = False
		blnNoRMOnPunishment = False  # No recombination/mutation when only punishment is delivered. I believe this is now defunct (10/2018).
		blnEqualPunishmentRI = blnSinglePunishmentRI = blnProportionalPunishment = blnDifferentialPunishment = False

		# Set booleans for the punishment method, if necessary.  if there is no punishment, all booleans will be false.
		if e_info.get_equal_punishment_ri(intSched) != 0:
			raise Exception("Not tested")
			blnEqualPunishmentRI = True
		elif e_info.get_proportion_punishment(intSched) > 0:
			raise Exception("Not tested")
			blnProportionalPunishment = True
		elif e_info.get_single_punishment_ri(intSched) != 0:
			raise Exception("Not tested")
			blnSinglePunishmentRI = True
		elif e_info.get_punishment_ri_1(intSched) != 0:
			raise Exception("Not tested")
			blnDifferentialPunishment = True  # I#m not sure what differential punishment is.

		# Value aggregators:
		# Don#t need these variables if no punishment is being delivered.
		intValAgg = [None, 0, 0]  # Note that this declaration also reinitializes the value aggregators for each new schedule (pair)
		dblPunishProb = 0  # Final common pathway for both alternatives.
		dblPunishProb1 = 0  # for alternative 1, calculated from intValAgg array.
		dblPunishProb2 = 0  # for alternative 2, calculated from intValAgg array.
		dblA = self.m_myOrganism.get_behaviors_info().get_fomo_a()  # for manipulating the reinforcement loss aversion.  0.76 should decrease it, for example.

		num_gens = e_info.get_num_generations() if not e_info.get_use_sp_schedules() else GENS_FOR_SP_SCHEDULES

		for intGen in range(num_gens):

			if e_info.get_use_sp_schedules() and self.m_spSched.is_past_stop_count():
				self.m_num_actual_gens[intRep, intSched] = intGen
				break

			if intGen % PRINT_EVERY_N_GENS == 0:
				log("\t\t" + str(intRep + 1) + "/" + str(intSched + 1) + "/" + str(intGen), print_status)

			# Get a behavior
			if self.get_organism().is_ready_to_emit():  # I don#t think the "Item" segment is necessary.
				self.m_intEmittedPheno[intRep, intSched, intGen] = self.get_organism().emit_behavior().get_integer_value()  # I don#t think the "Item" segment is necessary.
			else:
				raise Exception("Not tested")
				log("Not ready to emit!", print_status)

			# Advance the schedule timers and/or response counters
			if e_info.get_t_2_lo() == 0 and e_info.get_t_2_hi() == 0 and e_info.get_sched_type_2() != Constants.SCHED_TYPE_None:
				# Running a single schedule on the left with background reinforcement on the right
				raise Exception("Not tested")
				self.m_objRI1.tick_tock()
				if e_info.get_sched_type_2(intSched) == Constants.SCHED_TYPE_RI:
					# Running an RI background
					raise Exception("Not tested")
					self.m_objRI2.tick_tock()
				elif e_info.get_sched_type_2(intSched) == Constants.SCHED_TYPE_RR:
					raise Exception("Not tested")
					pass
					# Running an RR background
					# objBgrRR.response()# This advances only if T2 is emitted
				else:
					raise Exception("Not tested")
					log("Trouble in DoASched!", print_status)

			elif e_info.get_sched_type_2() == Constants.SCHED_TYPE_NONE:
				# Running the originial implementation of an RI schedule
				raise Exception("Not tested")
				self.m_objRI1.tick_tock()
			elif e_info.get_use_sp_schedules():
				self.m_spSched.tick_tock()
			elif e_info.get_sched_type_1() == Constants.SCHED_TYPE_RI and e_info.get_sched_type_2() == Constants.SCHED_TYPE_RI:
				# Running a regular conc RI RI

				self.m_objRI1.tick_tock()
				self.m_objRI2.tick_tock()
			elif e_info.get_sched_type_1() == Constants.SCHED_TYPE_RI and e_info.get_sched_type_2() == Constants.SCHED_TYPE_EXT:
				# Running Conc RI EXT
				raise Exception("Not tested")
				self.m_objRI1.tick_tock()
			elif e_info.get_sched_type_1() == Constants.SCHED_TYPE_RR and e_info.get_sched_type_2() == Constants.SCHED_TYPE_RR:
				# Running a regular conc RR RR
				# response counters get advanced in self.check_for_targets
				blnRR = True
			elif e_info.get_sched_type_1() == Constants.SCHED_TYPE_NRR and e_info.get_sched_type_2() == Constants.SCHED_TYPE_NRR:
				# Running a nonindependent conc RR RR
				# response counters get advanced in self.check_for_targets
				raise Exception("Not tested")
				blnNRR = True
			elif e_info.get_sched_type_1(intSched) == Constants.SCHED_TYPE_RILF and e_info.get_sched_type_2(intSched) == Constants.SCHED_TYPE_RILF:
				# Running RI schedules with linear feedback in the components
				# response counters get advanced in self.check_for_targets
				raise Exception("Not tested")
				blnRILF = True
				self.m_objRILF1.tick_tock()
				self.m_objRILF2.tick_tock()
			else:
				raise Exception("Not tested")
				log("Trouble in DoASched II!", print_status)

			# response counters for RR and NRR schedules are advanced in self.check_for_targets

			# Advance interval timers for punishment, if necessary
			if blnEqualPunishmentRI or blnProportionalPunishment or blnDifferentialPunishment:
				# Equal, proportional, or diferential punishment is being run.
				raise Exception("Not tested")
				self.m_objRIPunish1.tick_tock()
				self.m_objRIPunish2.tick_tock()
			elif blnSinglePunishmentRI:
				raise Exception("Not tested")
				self.m_objRIPunish1.tick_tock()

			blnPunishmentDelivered = False  # Initialize this for each generation just to be safe.
			# 								This is used (i.e., blnPUnishcmentDelivered = True?) when there is no extra
			# 								recombination and mutation(i.e., a non-selection Event) following punishment.

			# Check for targets.
			if e_info.get_t_2_lo() == 0 and e_info.get_t_2_hi() == 0 and e_info.get_sched_type_2() != Constants.SCHED_TYPE_None:
				#Running a single schedule with a background alternative  <<*******************************************************************************************
				raise Exception("Not tested")
				intEmittedPhenoClass = self.check_for_targets_single_sched(self.m_intEmittedPheno(intRep, intSched, intGen))  # (0 = no target; 1 = Instrumental Target; 2 = Alternative Target)
			elif e_info.get_sched_type_2() == Constants.SCHED_TYPE_NONE:
				# Running the original implementation of a single schedule.
				raise Exception("Not tested")
				intEmittedPhenoClass = self.check_for_targets_single_sched(self.m_intEmittedPheno(intRep, intSched, intGen))  # (0 = no target; 1 = Instrumental Target)
			else:
				# Running a (more or less) normal concurrent schedule of one sort or another
				intEmittedPhenoClass = self.check_for_targets(self.m_intEmittedPheno[intRep, intSched, intGen], blnRR, blnNRR, blnRILF)  # (0 = no target; 1 = Target 1; 2 = Target 2)

			if intEmittedPhenoClass != 0:
				if intLastEmittedPhenoClass is not None and intLastEmittedPhenoClass != intEmittedPhenoClass:
					intLastChangeover = intGen

				intLastEmittedPhenoClass = intEmittedPhenoClass

			# Check for punishment
			if blnPunishmentFirst:  # This is now set = True apparently permanently (12/2019)
				# Check for punishment first and inform the organism of the result.
				if blnEqualPunishmentRI or blnProportionalPunishment or blnSinglePunishmentRI or blnDifferentialPunishment:
					if intValAgg[1] == 0 and intValAgg[2] == 0:
						raise Exception("Not tested")
						dblPunishProb1 = 0.5
						dblPunishProb2 = 0.5
					else:
						# This is working fine.  The intValAgg#s appear to be accumulating reinforcers
						raise Exception("Not tested")
						dblPunishProb1 = 1 - (intValAgg[1] ** dblA / (intValAgg[1] ** dblA + intValAgg[2] ** dblA))
						dblPunishProb2 = 1 - (intValAgg[2] ** dblA / (intValAgg[1] ** dblA + intValAgg[2] ** dblA))

					# Set final common pathway for dblPunishProb
					if intEmittedPhenoClass == 0:
						raise Exception("Not tested")
						dblPunishProb = 0  # for safety#s sake I guess
					elif intEmittedPhenoClass == 1:
						raise Exception("Not tested")
						dblPunishProb = dblPunishProb1
					elif intEmittedPhenoClass == 2:
						raise Exception("Not tested")
						dblPunishProb = dblPunishProb2
					else:
						raise Exception("Not tested")
						log("Trouble in DoASched", print_status)

					if self.check_for_punishment(intEmittedPhenoClass, dblPunishProb):
						# Update the punishment array
						raise Exception("Not tested")
						self.m_blnPhenoPunished[intRep, intSched, intGen] = True
						blnPunishmentDelivered = True
					else:
						raise Exception("Not tested")
						blnPunishmentDelivered = False

				# : check for reinforcement and inform the organism of the result
				if e_info.get_sched_type_2() == Constants.SCHED_TYPE_EXT and intEmittedPhenoClass == 2:
					raise Exception("Not tested")
					intEmittedPhenoClass = 0  # Running Conc RI EXT:  no reinforcement for PhenoClass 2
				if self.check_for_reinforcement(intEmittedPhenoClass, blnNoRMOnPunishment, blnPunishmentDelivered, blnRR, blnNRR, blnRILF, intSched, intGen, intLastChangeover, print_status):
					# Update the value aggregator
					intValAgg[intEmittedPhenoClass] += 1
					# Update the reinforcement array
					self.m_blnPhenoReinforced[intRep, intSched, intGen] = True

			else:
				raise Exception("Not tested")
				log("There is a problem in DoASched", print_status)
				#I don#t think the new method of not recombining or mutating if only punishment is delivered will work here in this case******
				# I believe the code will have to be substantially rewritten to make this happen.  Before checking for reinforcement here I will have
				# to know whether punishment occured so that if no reinforcement is delivered, no recombination/mutation will occur.
				# I could just get a true/false on reinforcement and punishment and then inform the organism of the outcome here insted of in the
				# CheckFor... procedures.  Yes, I think this will work.
				# Check for reinforcement first and inform the organism of the result
				# This will not work for differnetial punishment!!!  Modification required*********************************  Plus I
				# have commented out some of the code due to changes in self.check_for_punishment
				if self.check_for_reinforcement(intEmittedPhenoClass, blnNoRMOnPunishment, blnPunishmentDelivered, blnRR, blnNRR, blnRILF, intSched, intGen, intLastChangeover):
					# Update the reinforcement array
					self.m_blnPhenoReinforced[intRep, intSched, intGen] = True

				# : check for punishment and inform the organism of the result.
				if e_info.get_equal_punishment_ri(intSched) != 0:
					raise Exception("Not tested")
					pass
					# if self.check_for_punishment(intEmittedPhenoClass, True):
					# 	#Can update the punishment array here if this method works out
					# 	blnPunishmentDelivered = True
					# else:
					# 	blnPunishmentDelivered = False
					#

	def check_for_reinforcement(self, intEmittedPhenoClass, blnNoRMOnPunishment, blnPunishmentDelivered, blnRR, blnNRR, blnRILF, intSched, intGen, intLastChangeover, print_status):

		# if blnRR is true, then running a conc RR RR.  if blnNRR is true, then running a nonindependent conc RR RR

		e_info = self.get_experiment_info()

		# Changeover delay in effect? No reinforcement
		if intLastChangeover is not None and intGen - intLastChangeover < e_info.get_COD():
			self.get_organism().set_selection(0, False)
			if intGen != intLastChangeover:
				print("CO not met", print_status)
			return False

		# print("CO met")

		#Indendent or nonindependent Conc RR RR ***************************************************************************
		if blnRR or blnNRR:
			if intEmittedPhenoClass == 1:
				# Target 1 was emitted
				if self.m_objRR1.is_reinforcement_set_up():
					# Reinforcement is delivered on alterantive 1
					self.get_organism().set_selection(e_info.get_FDF_mean_1(intSched), True)  # Informs organism that reinforcement occurred
					return True
				else:
					# No reinforcement
					self.get_organism().set_selection(e_info.get_FDF_mean_1(intSched), False)
					return False

			elif intEmittedPhenoClass == 2:
				# Target 2 was emitted
				if self.m_objRR2.is_reinforcement_set_up():
					self.get_organism().set_selection(e_info.get_FDF_mean_2(intSched), True)  # Informs organism that reinforcement occurred.
					return True
				else:
					# No reinforcement
					self.get_organism().set_selection(e_info.get_FDF_mean_2(intSched), False)
					return False

			elif intEmittedPhenoClass == 0:
				# Neither target was emitted; no reinforcement
				self.get_organism().set_selection(e_info.get_FDF_mean_1(intSched), False)  # I don#t think it matters what Mag is passed when this is false.  The parameter is ignored.
				return False
			else:
				raise Exception("Not tested")
				log("Trouble in CheckForReinforcement when blnRR is True.", print_status)

		#RI with linear feedback components in a concurrent schedule ******************************************************
		if blnRILF:
			raise Exception("Not tested")
			if intEmittedPhenoClass == 1:
				raise Exception("Not tested")
				# Target 1 was emitted
				# print("Target 1")
				if self.m_objRILF1.is_reinforcement_set_up():
					raise Exception("Not tested")
					# Reinforcement is delivered on alterantive 1
					self.get_organism().set_selection(e_info.get_FDF_mean_1(intSched), True)  # Informs organism that reinforcement occurred
					return True
				else:
					raise Exception("Not tested")
					# No reinforcement
					self.get_organism().set_selection(e_info.get_FDF_mean_1(intSched), False)
					return False

			elif intEmittedPhenoClass == 2:
				raise Exception("Not tested")
				# Target 2 was emitted
				# print("Target 2")
				if self.m_objRILF2.is_reinforcement_set_up():
					raise Exception("Not tested")
					self.get_organism().set_selection(e_info.get_FDF_mean_2(intSched), True)  # Informs organism that reinforcement occurred.
					return True
				else:
					raise Exception("Not tested")
					# No reinforcement
					self.get_organism().set_selection(e_info.get_FDF_mean_2(intSched), False)
					return False

			elif intEmittedPhenoClass == 0:
				raise Exception("Not tested")
				# Neither target was emitted; no reinforcement
				# print("Target 0")
				self.get_organism().set_selection(e_info.get_FDF_mean_1(intSched), False)  # I don#t think it matters what Mag is passed when this is false.  The parameter is ignored.
				return False
			else:
				raise Exception("Not tested")
				log("Trouble in CheckForReinforcement when blnRILF is True.", print_status)

		#Original implementation of an RI schedule **********************************************************************
		if e_info.get_sched_type_2() == Constants.SCHED_TYPE_NONE:
			raise Exception("Not tested")
			# Running the original implementation of an RI schedule
			if intEmittedPhenoClass == 1:
				raise Exception("Not tested")
				# Target 1 was emitted
				if self.m_objRI1.is_reinforcement_set_up():
					raise Exception("Not tested")
					# Reinforcement is delivered on alterantive 1
					self.get_organism().set_selection(e_info.get_FDF_mean_1(intSched), True)  # Informs organism that reinforcement occurred
					return True
				else:
					raise Exception("Not tested")
					# No reinforcement
					# But if punishment was delivered and blnNoRMOnPunishment = True, then don#t do the extra recombination and mutation.
					if blnNoRMOnPunishment and blnPunishmentDelivered:
						raise Exception("Not tested")
						pass
						# Don#t do nuthin#
						# print("Ain#t doin# nuthin# on target 1")
					else:
						raise Exception("Not tested")
						self.get_organism().set_selection(e_info.get_FDF_mean_1(intSched), False)

					# if Not blnPunishmentDelivered: self.get_organism().set_selection(e_info.get_FDF_mean_1(intSched), False)
					return False

			elif intEmittedPhenoClass == 0:
				raise Exception("Not tested")
				# Neither target was emitted; no reinforcement
				# But if punishment was delivered then don#t do the extra recombination and mutation.
				#Wait a sec...if there is no target, then no punishment could have been delivered!!!
				# print("No target.")
				if blnNoRMOnPunishment and blnPunishmentDelivered:
					raise Exception("Not tested")
					# Don#t do nuthin#
					pass
				else:
					raise Exception("Not tested")
					self.get_organism().set_selection(e_info.get_FDF_mean_1(intSched), False)  # I don#t think it matters what Mag is passed when this is false.  The parameter is ignored.

				return False
			else:
				raise Exception("Not tested")
				log("Trouble in CheckForReinforcement for original implementation of single schedules.", print_status)

		#Conc RI RI, Conc RI EXT, or single RI with background reinforcement ******************************************************************************************************
		# This is the default
		if intEmittedPhenoClass == 1:

			# Target 1 was emitted
			if e_info.get_use_sp_schedules() and self.m_spSched.is_reinforcement_set_up(1):
				self.get_organism().set_selection(e_info.get_sp_FDF(intSched), True)
				return True
			elif not e_info.get_use_sp_schedules() and self.m_objRI1.is_reinforcement_set_up():

				# Reinforcement is delivered on alterantive 1
				self.get_organism().set_selection(e_info.get_FDF_mean_1(intSched), True)  # Informs organism that reinforcement occurred
				return True
			else:

				# No reinforcement
				# But if punishment was delivered and blnNoRMOnPunishment = True, then don#t do the extra recombination and mutation.
				if blnNoRMOnPunishment and blnPunishmentDelivered:
					raise Exception("Not tested")
					pass
					# Don#t do nuthin#
				else:
					self.get_organism().set_selection(0, False)

				return False

		elif intEmittedPhenoClass == 2:

			#Target 2 was emitted or, if a single schedule is running, a background behavior was emitted <<<<<<<<<<<<<--------------------------*******************
			if e_info.get_t_2_lo() == 0 and e_info.get_t_2_hi() == 0 and e_info.get_sched_type_2() == Constants.SCHED_TYPE_RR:
				raise Exception("Not tested")
				# Running single schedule.  The background is a ratio schedule
				# First advance the response count
				self.m_objBgrRR.response()

				if self.m_objBgrRR.is_reinforcement_set_up():
					raise Exception("Not tested")
					# Reinforcement is delivered for the background
					self.get_organism().set_selection(e_info.get_FDF_mean_2(intSched), True)  # Informs organism that reinforcement occurred.
					return True

			else:

				if e_info.get_use_sp_schedules() and self.m_spSched.is_reinforcement_set_up(2):
					self.get_organism().set_selection(e_info.get_sp_FDF(intSched), True)
					return True
				# Running regular conc RI RI or single schedule with background RI
				elif not e_info.get_use_sp_schedules() and self.m_objRI2.is_reinforcement_set_up():
					# Reinforcement is delivered on alternative 2, which could be the background for a single schedule
					self.get_organism().set_selection(e_info.get_FDF_mean_2(intSched), True)  # Informs organism that reinforcement occurred.
					return True
				else:

					# No reinforcement
					# But if punishment was delivered and blnNoRMOnPunishment=True, then don#t do the extra recombination and mutation.
					if blnNoRMOnPunishment and blnPunishmentDelivered:
						raise Exception("Not tested")
						pass
						# Don#t do nuthin#
					else:

						self.get_organism().set_selection(0, False)

					return False

		elif intEmittedPhenoClass == 0:

			# Neither target was emitted; no reinforcement
			# But if punishment was delivered then don#t do the extra recombination and mutation.
			#Wait a sec...if there is no target, then no punishment could have been delivered!!!
			# print("No target.")
			if blnNoRMOnPunishment and blnPunishmentDelivered:
				raise Exception("Not tested")
				pass
				# Don#t do nuthin#
			else:

				self.get_organism().set_selection(e_info.get_FDF_mean_1(intSched), False)  # I don#t think it matters what Mag is passed when this is false.  The parameter is ignored.

			return False
		else:
			raise Exception("Not tested")
			log("Trouble in CheckForReinforcement.", print_status)

	def check_for_targets_single_sched(self, intEmittedPheno, intSched):

		raise Exception("Not tested")
		# Dim i As Integer
		e_info = self.get_experiment_info()

		if e_info.get_sched_type_2(intSched) == Constants.SCHED_TYPE_None:
			# Running the original implementatio of a single schedule.
			if intEmittedPheno >= e_info.get_t_1_lo() and intEmittedPheno <= e_info.T1Hi:
				# Instrumental target pheno emitted
				return 1
			else:
				# No target emitted
				return 0

		if intEmittedPheno >= e_info.get_t_1_lo() and intEmittedPheno <= e_info.T1Hi:
			# Instrumental target pheno emitted
			return 1
		elif self.m_lstAltTarget.Contains(intEmittedPheno):
			return 2
		else:
			# Neither target emitted
			return 0

	def do_a_prob_sched(self, intRep, intSched):
		raise Exception("Not tested")

		# Runs a PROB schedule and saves the results of each generation.

		# Dim intGen, intEmittedPhenoClass As Integer
		# #Dim blnPunishmentFirst = True # Determines whether punishment or reinforcement is delivered first when both are delivered in a time tick.
		# 										  This is a bit clumsy. When no punishment is arranged, checking for punishment still occurs.
		# 										  Should perhaps have a separate If...Then...End if block (below) for when there is no punishment.
		# 										  Actually, it is OK as is.  Does not execute the self.check_for_punishment method if no punishment is arranged.
		# Dim blnPunishmentDelivered = False
		# Dim blnNoRMOnPunishment = False # No recombination/mutation when only punishment is delivered.

		# for differential punishment
		# Dim dblPunishMag = e_info.get_sched_values_1() / (e_info.get_sched_values_1() + e_info.get_sched_values_2())
		# ^This is punishMag for alternative 1.  Subtract it from 1 to get the punishMag for alternative 2.
		# Value aggregators for differential punishment:
		# Dim intValAgg(2) As Integer # Note that this declaration also reinitializes the value aggregators for each new schedule (pair)
		# Dim dblPunishProb = 0 # for alternative 1, calculated from intValAgg array.

		for intGen in range(1, self.get_num_generations() + 1):
			# myExperiment.txtGeneration.Text = CStr(intGen) #Write to the experiment form.
			# Get a behavior
			if self.get_organism().is_ready_to_emit():  # I don#t think the "Item" segment is necessary.
				# if self.get_organism().is_ready_to_emit():  # I don#t think the "Item" segment is necessary.
				self.m_intEmittedPheno[intRep][intSched][intGen] = self.get_organism().emit_behavior().get_integer_value()  # I don#t think the "Item" segment is necessary.
			else:
				raise AssertionError("Not ready to emit!")

			# #Extinction appears to be working just fine.  Hence all of the problem has to be right here.*****************************************<<<<<<
			# #Advance interval timers
			# self.m_objRI1.tick_tock()
			# self.m_objRI2.tick_tock()
			# if e_info.get_equal_punishment_RI() != 0 or e_info.get_proportion_punishment() != 0:
			# 	#raise AssertionError("Punishment RI running...")
			# 	#Stop
			# 	#Equal or proportional punishment is being run.
			# 	self.m_objRIPunish1.tick_tock()
			# 	self.m_objRIPunish2.tick_tock()
			#

			# blnPunishmentDelivered = False # Initialize this for each generation just to be safe.
			# 								This is used when there is no extra recombination and mutation (i.e., a non-selection event) following punishment

			# Check for target
			intEmittedPhenoClass = self.check_for_targets(self.m_intEmittedPheno[intRep][intSched][intGen])  # (0 = no target; 1 = Target 1; 2 = Target 2)

			# if blnPunishmentFirst = True:
			# 	#Check for punishment first and inform the organism of the result.
			# 	if e_info.get_equal_punishment_RI() != 0 or e_info.get_proportion_punishment() != 0: #
			# 		#Calculate dblPunishMag (but rename it dblPunishProb) for alternative 1 from intValAgg array here...make provision for possible 0 intValAgg(1).
			# 		#Actually, I don#t think 0 intValAggs will be a problem unless they#re both zero, in which case perhaps dblPunishProb should be 0.5?  Yes,
			# 		#no reinforcers delivered on either side yet, so both are equal in value.
			# 		if intValAgg(1) = 0 and intValAgg(2) = 0:
			# 			dblPunishProb = 0.5
			# 		else:
			# 			#This is working fine.  The intValAgg#s appear to be accumulating reinforcers
			# 			#raise AssertionError("Am I in here?	 " & intValAgg(1).ToString & "	" & intValAgg(2).ToString)
			# 			#Bonehead!  You calculated this the wrong way around!
			# 			dblPunishProb = intValAgg(2) / (intValAgg(1) + intValAgg(2))
			#
			# 		#raise AssertionError(dblPunishProb.ToString)
			# 		#V for testing
			# 		#dblPunishProb = dblPunishMag # The value aggregator method is not working for some reason.  See bonehead comment above.
			# 		if self.check_for_punishment(intEmittedPhenoClass, dblPunishProb, True):
			# 			#raise AssertionError("Punishment delivered")
			# 			#Update the punishment array
			# 			self.m_blnPhenoPunished(intRep, intSched, intGen, True)
			# 			blnPunishmentDelivered = True
			# 		else:
			# 			blnPunishmentDelivered = False
			#
			#
			# 	#Then check for reinforcement and inform the organism of the result
			if self.check_for_reinforcement2(intEmittedPhenoClass) == True:  # Checks for probabilistic reinforcement
				# Update the value aggregator
				# intValAgg(intEmittedPhenoClass) += 1
				# Update the reinforcement array
				self.m_blnPhenoReinforced[intRep][intSched][intGen] = True

			# else:
			# 	raise AssertionError("There is a problem in self.do_a_sched")
			#	#I don#t think the new method of not recombining or mutating if only punishment is delivered will work here in this case******
			# 	#I believe the code will have to be substantially rewritten to make this happen.  Before checking for reinforcement here I will have
			# 	#to know whether punishment occured so that if no reinforcement is delivered, no recombination/mutation will occur.
			# 	#I could just get a true/false on reinforcement and punishment and then inform the organism of the outcome here insted of in the
			# 	#CheckFor... procedures.  Yes, I think this will work.
			# 	#Check for reinforcement first and inform the organism of the result
			# 	#This will not work for differnetial punishment!!!  Modification required*********************************  Plus I
			# 	#have commented out some of the code due to changes in self.check_for_punishment
			# 	#if self.check_for_reinforcement(intEmittedPhenoClass, blnNoRMOnPunishment, blnPunishmentDelivered, True):
			# 	#	#Update the reinforcement array
			# 	#	self.m_blnPhenoReinforced(intRep, intSched, intGen, True)
			# 	#
			# 	#Then check for punishment and inform the organism of the result.
			# 	if e_info.get_equal_punishment_RI() != 0:
			# 		#if self.check_for_punishment(intEmittedPhenoClass, True):
			# 		#	#Can update the punishment array here if this method works out
			# 		#	blnPunishmentDelivered = True
			# 		#else:
			# 		#	blnPunishmentDelivered = False
			# 		#
			#
			#

	def check_for_targets(self, intEmittedPheno, blnRR, blnNRR, blnRILF):

		e_info = self.get_experiment_info()

		# if blnRR is true, then running a conc RR RR.
		# if blnNRR is true, then running a nonindependent conc RR RR.  Must advance the response counters in the schedule objects as appropriate.
		# if blnRILF is true, then running an RI schedule with linear feedback

		if intEmittedPheno >= e_info.get_t_1_lo() and intEmittedPheno <= e_info.get_t_1_hi():

			if blnRR:
				# Regular conc RR RR
				self.m_objRR1.response()
			elif blnNRR:
				raise Exception("Not tested")
				# Nonindependent conc RR RR
				if self.m_objRR1.SetUpQueryOnly():
					self.m_objRR2.response()
				else:
					self.m_objRR1.response()
					self.m_objRR2.response()

			elif blnRILF:
				raise Exception("Not tested")
				# RI schedule with linear feedback
				self.m_objRILF1.response()

			return 1
		elif intEmittedPheno >= e_info.get_t_2_lo() and intEmittedPheno <= e_info.get_t_2_hi():

			if blnRR:
				# Regular conc RR RR
				self.m_objRR2.response()
			elif blnNRR:
				raise Exception("Not tested")
				# Nonindependent conc RR RR
				if self.m_objRR2.SetUpQueryOnly:
					self.m_objRR1.response()
				else:
					self.m_objRR1.response()
					self.m_objRR2.response()

			elif blnRILF:
				raise Exception("Not tested")
				# RI schedule with linear feedback
				self.m_objRILF2.response()

			return 2
		else:
			return 0

	def check_for_punishment(self, intEmittedPhenoClass, dblPunishProb):
		raise Exception("Not tested")
		# This is for forced mutation punishment.

		#Currently this function is hard coded for differential punishment*********************************************************
		# dblPunishMag if for differential punishment.  It is for alternative 1.  Subtract from 1 to get punishMag for alternative 2.

		# raise AssertionError("Validate from self.check_for_punishment:  " & dblPunishMag.ToString)
		# dblPunishMag is being passed correctly

		blnRepulsionPunishment = False  #  Ultimately this needs to go back onto the user interface (it is there, but not used)
		blnPunish1Only = False  # Punish alternative 1 only

		e_info = self.get_experiment_info()
		if e_info.get_single_punishment_RI() != 0:
			blnPunish1Only = True

		if blnPunish1Only:
			# Only punish alternative 1
			if intEmittedPhenoClass == 1:
				# Target 1 was emitted
				if self.m_objRIPunish1.is_reinforcement_set_up():
					#v Hard coded for differential punishment for now*******************************************************************
					self.get_organism().forced_mut_punish(dblPunishProb, e_info.get_mut_func_param(), e_info.get_t_1_lo(), e_info.get_t_2_lo(), e_info.get_t_1_hi(), e_info.get_t_2_hi())
					return True
				else:
					# No punishment
					return False

			else:
				# Target 2 or no target was emitted
				return False

		# Punishment is being delivered on both alternatives, whether equal or propportional.
		if intEmittedPhenoClass == 1:
			# Target 1 was emitted
			if self.m_objRIPunish1.is_reinforcement_set_up():
				# Punishment is delivered on alternative 1
				#v Hard coded for differential punishment for now*******************************************************************
				if blnRepulsionPunishment:
					# Repel wrap (circular) punishment
					self.get_organism().diff_repel_punish(e_info.get_punishment_mag(), dblPunishProb)
					return True
				else:
					# Forced mutation punishment
					self.get_organism().forced_mut_punish(dblPunishProb, e_info.get_mut_func_param(), e_info.get_t_1_lo(), e_info.get_t_2_lo(), e_info.get_t_1_hi(), e_info.get_t_2_hi())
					return True

			else:
				# No punishment
				return False

		elif intEmittedPhenoClass == 2:
			# Target 2 was emitted
			if self.m_objRIPunish2.is_reinforcement_set_up():
				# Punishment is delivered on alternative 2
				#v Hard coded for differential punishment for now*******************************************************************
				if blnRepulsionPunishment:
					# Repel wrap (circular) punishment
					self.get_organism().diff_repel_punish(e_info.get_punishment_mag(), 1 - dblPunishProb)
					return True
				else:
					# Forced mutation punishment
					self.get_organism().forced_mut_punish(1 - dblPunishProb, e_info.get_mut_func_param(), e_info.get_t_1_lo(), e_info.get_t_2_lo(), e_info.get_t_1_hi(), e_info.get_t_2_hi())
					return True

			else:
				# No punishment
				return False

		else:
			# Neither target was emitted
			return False

	def check_for_reinforcement2(self, intEmittedPhenoClass, intSched):
		raise Exception("Not tested")
		# Checks for probabilistic reinforcement
		e_info = self.get_experiment_info()
		if intEmittedPhenoClass == 1:
			# Target 1 was emitted
			if self.m_objPROB1.get_emission() == True:
				# Reinforcement is delivered on alterantive 1
				self.get_organism().set_selection(e_info.get_FDF_mean_1(intSched), True)  # Informs organism that reinforcement occurred
				return True
			else:
				return False

		elif intEmittedPhenoClass == 2:
			# Target 2 was emitted
			if self.m_objPROB2.get_emission() == True:
				# Reinforcement is delivered on alternative 2
				self.get_organism().set_selection(e_info.get_FDF_mean_2(), True)  # Informs organism that reinforcement occurred.
				return True
			else:
				return False

		elif intEmittedPhenoClass == 0:
			# Neither target was emitted; no reinforcement
			# But if punishment was delivered then don#t do the extra recombination and mutation.
			#Wait a sec...if there is no target, then no punishment could have been delivered!!!
			# raise AssertionError("No target.")
			# if blnNoRMOnPunishment and blnPunishmentDelivered:
			# 	#Don#t do nuthin#
			# 	#raise AssertionError("Ain#t doin# nuthin# on target 0")
			# else:
			self.get_organism().set_selection(e_info.get_FDF_mean_1(intSched), False)  # I don#t think it matters what Mag is passed when this is false.  The parameter is ignored.
			# Informs organism that no reinforcement was delivered
			# raise AssertionError(blnNoRMOnPunishment.ToString &" " & blnPunishmentDelivered.ToString & "  Uh oh on target 0")
			#
			return False
		else:
			raise AssertionError("Trounble in self.check_for_reinforcement2.")
