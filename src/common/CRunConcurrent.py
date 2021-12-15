'''
Created on May 24, 2021

@author: bleem
'''
import numpy

from src.common import Constants
from src.common.CProbEmitter import CProbEmitter
from src.common.CWriteData import CWriteData
from src.common.RISchedule import RISchedule

PRINT_EVERY_N_GENS = 1000


class CRunConcurrent(object):
	'''
	classdocs
	'''

	def __init__(self, myOrganism, experiment_index, experiment_parameters):
		'''
		Constructor
		'''

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
		# blnPhenoReinforced(,,) As Boolean # This indicates whether the phenotype was reinforced.
		self.m_objRI1 = RISchedule()
		self.m_objRI2 = RISchedule()
		self.m_objRIPunish1 = RISchedule()
		self.m_objRIPunish2 = RISchedule()
		self.m_objPROB1 = CProbEmitter()
		self.m_objPROB2 = CProbEmitter()

		# Set properties
		self.set_organism(myOrganism)
		self.set_repetitions(experiment_parameters.get_repetitions())
		self.set_generations(experiment_parameters.get_generations())
		self.set_num_schedules(experiment_parameters.get_num_schedules())
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
	def get_repetitions(self):
		return self.m_intRepetitions

	def set_repetitions(self, value):
		self.m_intRepetitions = value

	# Number of generations for each repetition
	def get_generations(self):
		return self.m_intGenerations

	def set_generations(self, value):
		self.m_intGenerations = value

	def giddyup(self):

		# I believe I can control everything from here, including  writing to output files.

		# Runs, RI schedules, RI schedules with superimposed punishment, and probabilistic schedules

		b_info = self.get_organism().get_behaviors_info()
		e_info = self.get_experiment_info()

		objFileWriter = CWriteData(b_info, e_info, self.m_strOutpath, self.m_strFileStub, self.get_repetitions(), self.get_generations())

		# Dim intRep, intSched As Integer

		# Turn on a discriminative stimulus
		# Organism.SDColor = SDColor.Red # I think this makes the "Item" segment unnecessary throughout.  The "Item" segment was not used in the test-lab code.
		# Will delete it here.

		# for intSched = 1 To Schedules
		# 	#Organism.reset_population() #Actually, don#t need this.  Could just do it all in the for...next loop.
		# 	#Should the population be initialized (i.e., randomized) for each schedule?  Probably.
		# 	myExperiment.txtSchedule.Text = CStr(intSched) #Write to the experiment form
		# 	#Application.DoEvents() #So that write to the text boxes continues unimpaired.
		# 	for intRep = 1 To self.get_repetitions()
		# 		self.m_objRI1.set_mean(e_info.get_sched_values_1() # Setting the mean initializes the schedules.  Should this be initialized for every repetition?
		# 		self.m_objRI2.set_mean(e_info.get_sched_values_2()
		# 		Organism.reset_population() #This solves the problem of missing reinforcers!
		# 		#if intRep > 1: Organism.reset_population()
		# 		myExperiment.txtRepetition.Text = CStr(intRep) #Write to the experiment form
		# 		#Application.DoEvents() #So that write to the text boxes continues unimpaired.
		# 		DoARep(intSched, intRep)
		# 	Next intRep
		# Next intSched

		# Make sure we're in a good state before we start if the runs will pile up
		if not e_info.get_reset_between_runs():
			self.get_organism().reset_state()

		# Repetitions are controlled from this loop
		for intRep in range(self.get_repetitions()):
			print("starting rep " + str(intRep))
			for intSched in range(self.get_num_schedules()):

				# Initialize the equal punishment RIs if necessary
				if e_info.get_equal_punishment_ri(intSched) != 0:
					self.m_objRIPunish1.set_mean(e_info.get_equal_punishment_ri(intSched))
					self.m_objRIPunish2.set_mean(e_info.get_equal_punishment_ri(intSched))

				# Initialize the single punishment RI if necessary
				if e_info.get_single_punishment_ri(intSched) != 0:
					self.m_objRIPunish1.set_mean(e_info.get_single_punishment_ri(intSched))

				print("\tstarting sched " + str(intSched))
				#Set the schedules**********************************************************************************************************
				if e_info.get_sched_type_1() == Constants.SCHED_TYPE_PROB and e_info.get_sched_type_2() == Constants.SCHED_TYPE_PROB:
					# Running probabilistic schedules
					self.m_objPROB1.set_prob_of_emission(e_info.get_sched_value_1(intSched))
					self.m_objPROB2.set_prob_of_emission(e_info.get_sched_value_2(intSched))
				else:
					# Otherwise, running RI schedules or RI schedules with superimposed punishment
					# for RI schedules and RI schedules with superimposed punishment
					self.m_objRI1.set_mean(e_info.get_sched_value_1(intSched))  # Setting the mean initializes the schedules.
					self.m_objRI2.set_mean(e_info.get_sched_value_2(intSched))
					# Initialize proportional punishment RIs if necessary
					if e_info.get_proportion_punishment(intSched) != 0:
						self.m_objRIPunish1.set_mean((e_info.get_proportion_punishment(intSched)) * e_info.get_sched_values_1(intSched))
						self.m_objRIPunish2.set_mean((e_info.get_proportion_punishment(intSched)) * e_info.get_sched_values_2(intSched))

					# self.m_objRI1.SaveIRIs = True  Don#t do this!
					# self.m_objRI2.SaveIRIs = True  No!

				if e_info.get_reset_between_runs():
					self.get_organism().reset_state()  # This solves the problem of missing reinforcers! I don#t think the "Item" segment is necessary.

				#Run the schedules*************************************************************************************************************
				if e_info.get_sched_type_1() == Constants.SCHED_TYPE_PROB and e_info.get_sched_type_2() == Constants.SCHED_TYPE_PROB:
					# Running probabilistic schedules
					self.do_a_prob_sched(intRep, intSched)  #  <---Runs a schedule
				else:
					# Running RI schedules or RI schedules with superimposed punishment.
					self.do_a_sched(intRep, intSched)  #  <---Runs a schedule
				print("\tfinishing sched " + str(intSched))
			print("finishing rep " + str(intRep))
		# At this point the phenotye and reinforcement and, if applicable, punishment arrays for all repetitions and schedules are loaded.

		# Clear info from form prior to write
		# myExperiment.txtRepetition.Text = ""
		# myExperiment.txtSchedule.Text = ""

		# Write data to .csv file and summary to Excel
		print("Writing .csv file...")
		# Application.DoEvents()
		objFileWriter.write_csv(self.m_blnPhenoReinforced, self.m_blnPhenoPunished, self.m_intEmittedPheno)

		print("Writing Excel file...")
		objFileWriter.write_excel(self.m_blnPhenoReinforced, self.m_blnPhenoPunished, self.m_intEmittedPheno)

		# My.Computer.Audio.Play(My.Resources._22Fillywhinnygrunt2000, AudioPlayMode.Background)
		# print("Done giddyuped!")
		# MsgBox("Last phenotype = " & CStr(intEmittedPheno(Schedules, Repetitions, Generations)))
		# 22Fillywhinnygrunt2000  My.Computer.Audio.Play(My.Resources.alonebad, AudioPlayMode.Background)

	def do_a_sched(self, intRep, intSched):

		# Runs a schedule and saves the results of each generation.

		# Dim intGen, intEmittedPhenoClass As Integer
		blnPunishmentFirst = True  # Determines whether punishment or reinforcement is delivered first when both are delivered in a time tick.
		# 										  This is a bit clumsy. When no punishment is arranged, checking for punishment still occurs.
		# 										  Should perhaps have a separate If...Then...End If block (below) for when there is no punishment.
		# 										  Actually, it is OK as is.  Does not execute the self.check_for_punishment method if no punishment is arranged.
		# Dim blnPunishmentDelivered As Boolean
		blnNoRMOnPunishment = False  # No recombination/mutation when only punishment is delivered
		blnEqualPunishmentRI = False
		blnSinglePunishmentRI = False
		blnProportionalPunishment = False

		e_info = self.get_experiment_info()

		# Set booleans for the punishment method, if necessary
		if e_info.get_equal_punishment_ri(intSched) != 0:
			blnEqualPunishmentRI = True
		elif e_info.get_proportion_punishment(intSched) > 0:
			blnProportionalPunishment = True
		elif e_info.get_single_punishment_ri(intSched) != 0:
			blnSinglePunishmentRI = True

		# raise AssertionError(blnEqualPunishmentRI & "	 " & blnProportionalPunishment & "	 " & blnSinglePunishmentRI)
		# raise AssertionError(e_info.get_mut_func_param().ToString)
		# raise AssertionError(e_info.get_proportion_punishment().ToString)
		# Stop

		# for differential punishment
		# I don#t think dblPunishMag is used ny more.  Value aggregators replaced it.
		# Dim dblPunishMag As Double = e_info.get_sched_values_1() / (e_info.get_sched_values_1() + e_info.get_sched_values_2())
		# ^This is punishMag for alternative 1.  Subtract it from 1 to get the punishMag for alternative 2.
		# Value aggregators for differential punishment:
		intValAgg = [0] * 3  # Note that this declaration also reinitializes the value aggregators for each new schedule (pair)
		# Dim dblPunishProb As Double # for alternative 1, calculated from intValAgg array.
		dblA = self.m_myOrganism.get_behaviors_info().get_fomo_a()  # for manipulating the reinforcement loss aversion.  0.76 should decrease it.

		for intGen in range(self.get_generations()):

			# self.get_organism().sanity_check()  # For debug purposes

			if intGen % PRINT_EVERY_N_GENS == 0:
				print("\t\tgen " + str(intGen))
			# Get a behavior
			if self.get_organism().is_ready_to_emit():  # I don#t think the "Item" segment is necessary.
				# if self.get_organism().is_ready_to_emit():  # I don#t think the "Item" segment is necessary.
				self.m_intEmittedPheno[intRep][intSched][intGen] = self.get_organism().emit_behavior().get_integer_value()  # I don#t think the "Item" segment is necessary.
			else:
				raise AssertionError("Not ready to emit!")

			# Extinction appears to be working just fine.  Hence all of the problem has to be right here.*****************************************<<<<<<

			# Advance interval timers for reinforcement
			self.m_objRI1.tick_tock()
			self.m_objRI2.tick_tock()
			# Advance interval timers for punishment, if necessary
			if blnEqualPunishmentRI or blnProportionalPunishment:
				# Equal or proportional punishment is being run.
				self.m_objRIPunish1.tick_tock()
				self.m_objRIPunish2.tick_tock()
			elif blnSinglePunishmentRI:
				self.m_objRIPunish1.tick_tock()

			blnPunishmentDelivered = False  # Initialize this for each generation just to be safe.
			# 								This is used when there is no extra recombination and mutation (i.e., a non-selection event) following punishment

			# Check for target
			intEmittedPhenoClass = self.check_for_targets(self.m_intEmittedPheno[intRep][intSched][intGen])  # (0 = no target; 1 = Target 1; 2 = Target 2)

			if blnPunishmentFirst == True:
				# Check for punishment first and inform the organism of the result.
				if blnEqualPunishmentRI or blnProportionalPunishment or blnSinglePunishmentRI:
					# Calculate dblPunishMag (but rename it dblPunishProb) for alternative 1 from intValAgg array here...make provision for possible 0 intValAgg(1).
					# Actually, I don#t think 0 intValAggs will be a problem unless they#re both zero, in which case perhaps dblPunishProb should be 0.5?  Yes,
					# no reinforcers delivered on either side yet, so both are equal in value.
					if intValAgg[1] == 0 and intValAgg[2] == 0:
						dblPunishProb = 0.5
					else:
						# This is working fine.  The intValAgg's appear to be accumulating reinforcers
						# Bonehead!  You calculated this the wrong way around!
						dblPunishProb = intValAgg[2] ** dblA / (intValAgg[1] ** dblA + intValAgg[2] ** dblA)

					if self.check_for_punishment(intEmittedPhenoClass, dblPunishProb) == True:
						# Update the punishment array
						self.m_blnPhenoPunished[intRep][intSched][intGen] = True
						blnPunishmentDelivered = True
					else:
						blnPunishmentDelivered = False

				# Then check for reinforcement and inform the organism of the result
				if self.check_for_reinforcement(intEmittedPhenoClass, blnNoRMOnPunishment, blnPunishmentDelivered, intSched) == True:
					# Update the value aggregator
					intValAgg[intEmittedPhenoClass] += 1
					# Update the reinforcement array
					self.m_blnPhenoReinforced[intRep][intSched][intGen] = True

			else:
				raise AssertionError("There is a problem in self.do_a_sched")
				#I don#t think the new method of not recombining or mutating if only punishment is delivered will work here in this case******
				# I believe the code will have to be substantially rewritten to make this happen.  Before checking for reinforcement here I will have
				# to know whether punishment occured so that if no reinforcement is delivered, no recombination/mutation will occur.
				# I could just get a true/false on reinforcement and punishment and then inform the organism of the outcome here insted of in the
				# CheckFor... procedures.  Yes, I think this will work.
				# Check for reinforcement first and inform the organism of the result
				# This will not work for differnetial punishment!!!  Modification required*********************************  Plus I
				# have commented out some of the code due to changes in self.check_for_punishment
				if self.check_for_reinforcement(intEmittedPhenoClass, blnNoRMOnPunishment, blnPunishmentDelivered) == True:
					# Update the reinforcement array
					self.m_blnPhenoReinforced[intRep][intSched][intGen] = True

				# Then check for punishment and inform the organism of the result.
				if e_info.get_equal_punishment_RI() != 0:
					pass
					# if self.check_for_punishment(intEmittedPhenoClass) = True:
					# 	#Can update the punishment array here if this method works out
					# 	blnPunishmentDelivered = True
					# else:
					# 	blnPunishmentDelivered = False
					#

		# raise AssertionError(intValAgg(1).ToString & "	" & intValAgg(2).ToString)

	def do_a_prob_sched(self, intRep, intSched):

		# Runs a PROB schedule and saves the results of each generation.

		# Dim intGen, intEmittedPhenoClass As Integer
		# #Dim blnPunishmentFirst As Boolean = True # Determines whether punishment or reinforcement is delivered first when both are delivered in a time tick.
		# 										  This is a bit clumsy. When no punishment is arranged, checking for punishment still occurs.
		# 										  Should perhaps have a separate If...Then...End If block (below) for when there is no punishment.
		# 										  Actually, it is OK as is.  Does not execute the self.check_for_punishment method if no punishment is arranged.
		# Dim blnPunishmentDelivered As Boolean
		# Dim blnNoRMOnPunishment As Boolean = False # No recombination/mutation when only punishment is delivered.

		# for differential punishment
		# Dim dblPunishMag As Double = e_info.get_sched_values_1() / (e_info.get_sched_values_1() + e_info.get_sched_values_2())
		# ^This is punishMag for alternative 1.  Subtract it from 1 to get the punishMag for alternative 2.
		# Value aggregators for differential punishment:
		# Dim intValAgg(2) As Integer # Note that this declaration also reinitializes the value aggregators for each new schedule (pair)
		# Dim dblPunishProb As Double # for alternative 1, calculated from intValAgg array.

		for intGen in range(1, self.get_generations() + 1):
			# myExperiment.txtGeneration.Text = CStr(intGen) #Write to the experiment form.
			# Get a behavior
			if self.get_organism().is_ready_to_emit():  # I don#t think the "Item" segment is necessary.
				# If self.get_organism().is_ready_to_emit():  # I don#t think the "Item" segment is necessary.
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
			# 		if self.check_for_punishment(intEmittedPhenoClass, dblPunishProb) = True:
			# 			#raise AssertionError("Punishment delivered")
			# 			#Update the punishment array
			# 			self.m_blnPhenoPunished(intRep, intSched, intGen) = True
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
			# 	#if self.check_for_reinforcement(intEmittedPhenoClass, blnNoRMOnPunishment, blnPunishmentDelivered) = True:
			# 	#	#Update the reinforcement array
			# 	#	self.m_blnPhenoReinforced(intRep, intSched, intGen) = True
			# 	#
			# 	#Then check for punishment and inform the organism of the result.
			# 	if e_info.get_equal_punishment_RI() != 0:
			# 		#if self.check_for_punishment(intEmittedPhenoClass) = True:
			# 		#	#Can update the punishment array here if this method works out
			# 		#	blnPunishmentDelivered = True
			# 		#else:
			# 		#	blnPunishmentDelivered = False
			# 		#
			#
			#

	def check_for_targets(self, intEmittedPheno):

		e_info = self.get_experiment_info()
		if intEmittedPheno >= e_info.get_t_1_lo() and intEmittedPheno <= e_info.get_t_1_hi():
			return 1
		elif intEmittedPheno >= e_info.get_t_2_lo() and intEmittedPheno <= e_info.get_t_2_hi():
			return 2
		else:
			return 0

	def check_for_punishment(self, intEmittedPhenoClass, dblPunishProb):

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

	def check_for_reinforcement(self, intEmittedPhenoClass, blnNoRMOnPunishment, blnPunishmentDelivered, intSched):

		e_info = self.get_experiment_info()
		if intEmittedPhenoClass == 1:
			# Target 1 was emitted
			if self.m_objRI1.is_reinforcement_set_up() == True:
				# Reinforcement is delivered on alterantive 1
				self.get_organism().set_selection(e_info.get_FDF_mean_1(intSched), True)  # Informs organism that reinforcement occurred
				return True
			else:
				# No reinforcement
				# But if punishment was delivered and blnNoRMOnPunishment = True, then don#t do the extra recombination and mutation.
				if blnNoRMOnPunishment and blnPunishmentDelivered:
					pass
					# Don#t do nuthin#
					# raise AssertionError("Ain#t doin# nuthin# on target 1")
				else:
					self.get_organism().set_selection(e_info.get_FDF_mean_1(intSched), False)

				# if Not blnPunishmentDelivered: self.get_organism().Selection(e_info.get_FDF_mean_1()) = False
				return False

		elif intEmittedPhenoClass == 2:
			# Target 2 was emitted
			if self.m_objRI2.is_reinforcement_set_up() == True:
				# Reinforcement is delivered on alternative 2
				self.get_organism().set_selection(e_info.get_FDF_mean_2(intSched), True)  # Informs organism that reinforcement occurred.
				return True
			else:
				# No reinforcement
				# But if punishment was delivered and blnNoRMOnPunishment=True, then don#t do the extra recombination and mutation.
				if blnNoRMOnPunishment and blnPunishmentDelivered:
					pass
					# Don#t do nuthin#
					# raise AssertionError("Ain#t doin# nuthin# on target 2")
				else:
					self.get_organism().set_selection(e_info.get_FDF_mean_2(intSched), False)

				return False

		elif intEmittedPhenoClass == 0:
			# Neither target was emitted; no reinforcement
			# But if punishment was delivered then don#t do the extra recombination and mutation.
			#Wait a sec...if there is no target, then no punishment could have been delivered!!!
			# raise AssertionError("No target.")
			if blnNoRMOnPunishment and blnPunishmentDelivered:
				pass
				# Don#t do nuthin#
				# raise AssertionError("Ain#t doin# nuthin# on target 0")
			else:
				self.get_organism().set_selection(None,  # e_info.get_FDF_mean_1(intSched),
												False)  # I don#t think it matters what Mag is passed when this is false.  The parameter is ignored.
				# raise AssertionError(blnNoRMOnPunishment.ToString &" " & blnPunishmentDelivered.ToString & "  Uh oh on target 0")

			return False
		else:
			raise AssertionError("Trouble in self.check_for_reinforcement.")

	def check_for_reinforcement2(self, intEmittedPhenoClass):

		# Checks for probabilistic reinforcement
		e_info = self.get_experiment_info()
		if intEmittedPhenoClass == 1:
			# Target 1 was emitted
			if self.m_objPROB1.get_emission() == True:
				# Reinforcement is delivered on alterantive 1
				self.get_organism().set_selection(e_info.get_FDF_mean_1(), True)  # Informs organism that reinforcement occurred
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
			self.get_organism().set_selection(e_info.get_FDF_mean_1(), False)  # I don#t think it matters what Mag is passed when this is false.  The parameter is ignored.
			# Informs organism that no reinforcement was delivered
			# raise AssertionError(blnNoRMOnPunishment.ToString &" " & blnPunishmentDelivered.ToString & "  Uh oh on target 0")
			#
			return False
		else:
			raise AssertionError("Trounble in self.check_for_reinforcement2.")
