'''
Created on May 21, 2021
Translated May 23, 2021

@author: bleem
'''

from Behavior import Behavior
from CFitnessLimits import CFitnessLimits
from CRandomNumber import CRandomNumber
from CRepulsionPunishment import CRepulsionPunishment
from CRescorlaWagner import CRescorlaWagner
from Mutator import Mutator
from PopulationSaver import PopulationSaver
from Recombinator import Recombinator
from SampleWoutReplace import SampleWoutReplace
from Selector import Selector
import Constants, Converter, BinaryConvertBoolean, CGrayCodes


class Behaviors(object):

	def __init__(self, stuBehaviorsInfo):

		# This is a population of potential behaviors

		self.m_stuBehaviorsInfo = None  # Contains all the information passed to this class

		self.m_SDID = None  # ID of the discriminative stimulus associated with this population
		self.m_DecayOfTransfer = None  # Used to calculate transfer from the previous SD
		self.m_ViscosityTicks = None  # Used to arrange viscous populations
		self.m_lowPhenotype = None
		self.m_highPhenotype = None
		self.m_numBehaviors = None  # Properties of the population
		self.m_classUpperBounds = None  # Upper bounds of the classes of behavior; the upper bound of a class is part of the class
		self.m_blnUseGrayCodes = None  # Property of the population
		self.m_intPercentToReplace = None  # Property of the population
		self.m_intPercentToReplace2 = None  # Property of the population
		self.m_fitnessMethod = None  # Fitness property
		self.m_fitnessLandscape = None  # Fitness property

		self.m_indexOfEmittedBehavior = None  # Index of the most recently emitted behavior
		self.m_phenotypeOfEmittedBehavior = None  # Phenotype of the most recently emitted behavior.
		# 												 Saved when the behavior is emitted in the EmitBehavior procedure.
		self.m_blnSelection = None  # Tells if the most recently emitted behavior was selected
		self.m_intMidpoint = None  # for use with midpoint fitness method:  Midpoint of target class.
		self.m_readyForNextEmission = None  # Ensures that after the Selection property is set, the next generation
		# 												  has been completed and subjected to mutation

		self.m_objMutator = None  # for the Mutator object
		self.m_objRecombinator = None  # for the Recombinator object
		self.m_objSelector = None  # for the Selector object
		self.m_objRW = None  # for the Rescorla-Wagner object

		self.m_bitsInHighPhenotype = None  # for dimensioning booleans.  Set when self.get_high_phenotype() property is set.
		self.m_objRandom = CRandomNumber()  # Defaults to the Mersenne Twister algorithm
		self.m_objCoinToss = CRandomNumber()  # Defaults to the Mersenne Twister algorithm.  Added for punishment coin tossing so as not to screw up
		# 										  the setting and resetting of self.m_objRandom.  Highest and Lowest integers set in the constructor.
		self.m_objSampler = SampleWoutReplace()  # To sample without replacement
		self.m_objFitnessLimits = None

		# To force cloning when punishment leaves 0 or 1 fit behaviors
		self.m_blnForceClone = False  # Flag to force cloning.  Set to true when the BehaviorToClone property is set.  Must be reset after the
		# 									instance of forced cloning is complete.
		self.m_objBehaviorToClone = None

		# for testing procedures to add viscosity, stickiness, persistence, "memory"
		self.m_integerValueOfEmittedBehavior = None
		self.m_objSavedPops = None
		self.m_blnCreateFromSynthetic = None  # New generations from orginal (False) or amalgamated (True) populations

		# for Raillard punishment
		self.m_intRBailOuts = None  # Reinforcer bailouts
		self.m_intPBailOuts = None  # Punisher bailouts
		# self.m__intSmallestFitnessValue, self.m_intLargestFitnessValue As Integer #To speed up handling the exponential FDF for both reinforcement and punishment (NOT!)

		# for repulsion punishment
		self.m_blnRepulsionPunishment = None
		self.m_punishmentMethod = None
		self.m_dblKelleyN = None
		self.m_objRepulsionPunishment = None

		# for forced mutation punishment
		# self.m_punishmentMag As Double  Don#t use this.
		self.m_blnForcedMutPunishment = None
		self.m_objProbEmitter = None
		self.m_objRandomBit = None

		self.m_behavior_list = list()

		self.load_behaviors_info(stuBehaviorsInfo)

	def load_behaviors_info(self, stuBehaviorsInfo):
		# stuBehaviorsInfo itself is preserved in self.m_stuBehaviorsInfo and can be accessed through the BehaviorsInfo property
		# of this class.
		# Members of stuBehaviorsInfo are also available as individual properties of this class.  The data structures for
		# Mutator, Recombinator, Selector, and Rescorla-Wagner objects are passed to these objects when they are instantiated.

		self.m_stuBehaviorsInfo = stuBehaviorsInfo

		# Set properties of this population of potential behaviors.
		self.set_sdid(stuBehaviorsInfo.get_sdid())
		self.set_decay_of_transfer(stuBehaviorsInfo.get_decay_of_transfer())
		self.set_viscosity_ticks(stuBehaviorsInfo.get_viscosity_ticks())
		self.m_blnCreateFromSynthetic = stuBehaviorsInfo.get_create_from_synthetic()  # Note there is no property for this (yet).
		self.set_use_gray_codes(stuBehaviorsInfo.get_use_gray_codes())
		self.set_low_phenotype(stuBehaviorsInfo.get_low_phenotype())
		self.set_high_phenotype(stuBehaviorsInfo.get_high_phenotype())
		self.set_num_behaviors(stuBehaviorsInfo.get_num_behaviors())
		self.set_percent_to_replace(stuBehaviorsInfo.get_percent_to_replace())
		self.set_percent_to_replace_2(stuBehaviorsInfo.get_percent_to_replace_2())
		self.set_fitness_method(stuBehaviorsInfo.get_fitness_method())
		self.set_fitness_landscape(stuBehaviorsInfo.get_fitness_landscape())
		self.set_punishment_method(stuBehaviorsInfo.get_punishment_method())

		# Instantiate the Mutator, Recombinator, and Selector objects
		self.m_objMutator = Mutator(stuBehaviorsInfo.get_mutation_info())
		self.m_objRecombinator = Recombinator(stuBehaviorsInfo.get_recombination_info())
		self.m_objSelector = Selector(stuBehaviorsInfo.get_selection_info())

		# Instantiate the Rescorla-Wagner object
		self.m_objRW = CRescorlaWagner(stuBehaviorsInfo.get_RW_info())

		# Instantiate FitnessLimits object (for use with uniform and linear FDFs when testing for at least two fit phenotypes)
		self.m_objFitnessLimits = CFitnessLimits(self.m_objSelector.get_continuous_function_form(), self.m_objSelector.get_fitness_landscape(), self.get_low_phenotype(), self.get_high_phenotype())

		# Instantiate RepulsionPunishment object if necessary
		self.m_blnRepulsionPunishment = True  # (5/2018)
		if self.m_blnRepulsionPunishment:
			self.m_dblKelleyN = stuBehaviorsInfo.get_kelley_n()  # Don#t really need this; could just use stuBehaviorsInfo.KelleyN in the line below.
			self.m_objRepulsionPunishment = CRepulsionPunishment(self.get_low_phenotype(), self.get_high_phenotype(), self.m_bitsInHighPhenotype, self.m_dblKelleyN)

		# Fill the population with random behaviors
		self.populate_with_random_behaviors()

		# Instantiate the PopulationSaver object
		if self.get_viscosity_ticks() > 0:
			# Note that if self.get_viscosity_ticks() = 1 there is no viscosity, but behavior emissions will be
			# determined using the relative frequency method rather than by the random phenotype method (when self.get_viscosity_ticks() = 0).
			# See EmitBehavior function.  Both methods should produce the same results.
			self.m_objSavedPops = PopulationSaver(self.get_low_phenotype(), self.get_high_phenotype(), self.get_num_behaviors(), self.get_viscosity_ticks(), self.m_blnCreateFromSynthetic)
			self.m_objSavedPops.set_save_population(self.m_behavior_list)

		# Prepare self.m_objRandom to emit behaviors at random
		self.m_objRandom.set_lowest_integer(0)
		self.m_objRandom.set_highest_integer(self.get_num_behaviors() - 1)

		# Prepare self.m_objCoinToss for punishment coin tossing
		self.m_objCoinToss.set_lowest_integer(0)
		self.m_objCoinToss.set_highest_integer(1)

	def get_behaviors_info(self):
		return self.m_stuBehaviorsInfo

	def get_sdid(self):
		return self.m_SDID

	def get_sd_str(self):
		return Converter.convert_to_sd_color(self.m_SDID)

	def set_sdid(self, value):
		self.m_SDID = value

	def get_sd_charge(self):
		return self.m_objRW.get_current_associative_strength()

	def get_sd_charges(self):
		return self.m_objRW.get_associative_strengths()

	def get_decay_of_transfer(self):
		return self.m_DecayOfTransfer

	def set_decay_of_transfer(self, value):
		self.m_DecayOfTransfer = value

	def get_viscosity_ticks(self):
		return self.m_ViscosityTicks

	def set_viscosity_ticks(self, value):
		self.m_ViscosityTicks = value

	def get_generations_run(self):
		return len(self.get_sd_charges()) - 1

	def get_use_gray_codes(self):
		return self.m_blnUseGrayCodes

	def set_use_gray_codes(self, value):
		self.m_blnUseGrayCodes = value

	def get_low_phenotype(self):
		return self.m_lowPhenotype

	def set_low_phenotype(self, value):
		self.m_lowPhenotype = value

	def get_high_phenotype(self):
		return self.m_highPhenotype

	def set_high_phenotype(self, value):
		self.m_highPhenotype = value
		self.m_bitsInHighPhenotype = len(BinaryConvertBoolean.convert_from_base_10(self.m_highPhenotype, 0)) - 1

	def get_num_behaviors(self):
		return self.m_numBehaviors

	def set_num_behaviors(self, value):
		self.m_numBehaviors = value

	def get_percent_to_replace(self):
		return self.m_intPercentToReplace

	def set_percent_to_replace(self, value):
		self.m_intPercentToReplace = value

	def get_percent_to_replace_2(self):
		return self.m_intPercentToReplace2

	def set_percent_to_replace_2(self, value):
		self.m_intPercentToReplace2 = value

	def get_raillard_reinforcer_bailouts(self):
		return self.m_intRBailOuts

	def set_raillard_reinforcer_bailouts(self, value):
		self.m_intRBailOuts = value

	def get_raillard_punisher_bailouts(self):
		return self.m_intPBailOuts

	def set_raillard_punisher_bailouts(self, value):
		self.m_intPBailOuts = value

	def get_fitness_method(self):
		return self.m_fitnessMethod

	def get_fitness_method_str(self):
		return Converter.convert_fitness_method_to_string(self.m_fitnessMethod)

	def set_fitness_method(self, value):
		self.m_fitnessMethod = value

	def get_fitness_landscape(self):
		return self.m_fitnessLandscape

	def get_fitness_landscape_str(self):
		return Converter.convert_fitness_landscape_to_string(self.m_fitnessLandscape)

	def set_fitness_landscape(self, value):
		self.m_fitnessLandscape = value

	def get_punishment_method(self):
		return self.m_punishmentMethod

	def get_punishment_method_str(self):
		return Converter.convert_punishment_method_to_string(self.m_punishmentMethod)

	def set_punishment_method(self, value):
		self.m_punishmentMethod = value

	def get_behavior_to_clone(self):
		return self.m_objBehaviorToClone

	def set_behavior_to_clone(self, value):
		self.m_objBehaviorToClone = value
		self.m_blnForceClone = True

	def get_behavior(self, index):
		return self.m_behavior_list[index]

	def set_behavior(self, index, value):
		self.m_behavior_list[index] = value

	def set_preload_population(self, lstPreloadBehaviors):
		if self.get_generations_run() > 0:
			raise AssertionError("You cannot preload behaviors into an existing population.")

		for tempPhenotype in lstPreloadBehaviors:
			if tempPhenotype < self.get_low_phenotype() or tempPhenotype > self.get_high_phenotype():
				raise AssertionError("Your preload contains at least one out-of-bounds phenotype.")

		if len(lstPreloadBehaviors) > self.get_num_behaviors():
			raise AssertionError("There are too many phenotypes in your preload.")

		self.m_behavior_list.clear()

		for tempPhenotype in lstPreloadBehaviors:
			objBehavior = Behavior(tempPhenotype)
			objBehavior.pad_to(self.m_bitsInHighPhenotype)
			self.add_behavior(objBehavior)

		if len(self.m_behavior_list) < self.get_num_behaviors():
			objRandom = CRandomNumber()
			objRandom.set_highest_integer(self.get_high_phenotype())
			objRandom.set_lowest_integer(self.get_low_phenotype())
			for _ in range(1, self.get_num_behaviors() - len(self.m_behavior_list)):
				objBehavior = Behavior(objRandom.get_rectangular_integer())
				objBehavior.pad_to(self.m_bitsInHighPhenotype)
				self.add_behavior(objBehavior)

	def is_ready_to_emit(self):
		return self.m_readyForNextEmission

	def set_ready_to_emit(self, value):
		self.m_readyForNextEmission = value

	def set_pref_rev_selection(self, selectionParameter, percentToReplaceOnSelection, value):
		self.set_percent_to_replace(percentToReplaceOnSelection)
		self.set_selection(selectionParameter, 0, value)

	def get_index_of_emitted_pheno(self):
		return self.m_indexOfEmittedBehavior

	def set_index_of_emitted_pheno(self, value):
		self.m_indexOfEmittedBehavior = value

	def set_selection(self, selectionParameter, value):
		self.set_selection_overload_2(selectionParameter, 0, value)

	def set_selection_overload(self, paramReinforcer, paramPunisher, value):

		if self.m_blnRepulsionPunishment and value == True:
			if paramPunisher == 0 and not paramReinforcer == 0:
				raise AssertionError("Reinforcer-only delivery unhandled in Selection(Double, Double)")
			self.administer_repulsion_punishment(paramReinforcer, paramPunisher)

		if value == True and self.m_blnRepulsionPunishment:
			raise AssertionError("You shouldn't be seeing this for repulsion punishment")

		if value == True:
			if paramReinforcer == 0 and not paramPunisher == 0:
				self.set_selection_overload_2(-paramPunisher, 0, True)
			elif not paramReinforcer == 0 and paramPunisher == 0:
				self.set_selection_overload_2(paramReinforcer, 0, True)
			elif not paramReinforcer == 0 and not paramPunisher == 0:
				function_form = self.m_objSelector.get_continuous_function_form()
				if function_form == Constants.CONTINUOUS_FUNCTION_FORM_UNIFORM or function_form == Constants.CONTINUOUS_FUNCTION_FORM_LINEAR:
					# Both Punisher and Reinforcer:  half the time deliver a punisher, half the time a reinforcer
					coinflip = self.m_objCoinToss.get_rectangular_integer()
					if coinflip == 0:
						# Deliver a punisher
						self.set_selection_overload_2(-paramPunisher, 0, True)
					elif coinflip == 1:
						# Deliver a reinforcer
						self.set_selection_overload_2(paramReinforcer, 0, True)
					else:
						raise AssertionError("The coin tosser in Behaviors.vb Selection(Double, Double) is not working correctly.")
				elif function_form == Constants.CONTINUOUS_FUNCTION_FORM_EXPONENTIAL:
					# Both Punisher and Reinforcer
					# for the exponential fitness density function, the sum of the reinforcer and punisher magnitudes,
					# 1/paramReinforcer - 1/paramPunisher, must be calculated and its reciprocal
					# must be passed to the Selection property immediately following.  If the sum is zero, then there
					# is no selection.  This corresponds to the case where a reinforcer and a punisher are both
					# delivered, but cancel each other out, and hence selection does not occur.
					consequenceMag = 1 / paramReinforcer - 1 / paramPunisher
					if consequenceMag == 0:
						# Neutral consequence:  reinforcer and punisher cancel each other out.
						self.set_selection_overload2(0, 0, False)  # Parameters are dummies, they are not used by the Selection property
						# 						 when there is no selection.
					else:
						self.set_selection_overload2(1 / consequenceMag, 0, True)
			else:
				self.set_selection_overload_2(0, 0, False)  # Parameters are dummies, they are not used by the Selection property
				# 						 when there is no selection.
				raise AssertionError("Neutral consequence:  This block of code should not be entered routinely because the Selection property should not be set equal to True if there is no selection.")
				# Neutral consequence:  both paramReinforcer and paramPunisher = 0
		else:
			self.set_selection_overload_2(0, 0, False)  # Parameters are dummies, they are not used by the Selection property
			# 						 when there is no selection.
			# No consequence was delivered, value = False

	def set_selection_overload_2(self, selectionParameter, intMidpoint, value):
		# This is the final common pathway for all selections.

		assert isinstance(value, bool)

		# Records whether the emitted behavior was selected (True) or not (False).
		# selectionParameter is the truncation percentage, number of competitors, or mean of the parental choosing function
		# for the Trunction, Tournament, or Continuous selection methods.

		# The creation of each new generation, including the addition of mutation, is completely controlled from this procedure.
		# The calling (laboratory or environment) program first calls EmitBehavior to obtain a behavior, determines
		# whether to select the emitted behavior, and then sets this property (in one of its overloaded forms [6/2013]).  This sequence MUST be followed by
		# the calling program:  namely, Call EmitBehavior, figure out whether to select, then set this property.  Might want to
		# put in some flags that prevent this property from being set unless a new emission has occurred.  Could probably combine
		# this somehow with the self.m_readyForNextEmission flag.
		# The index of the emitted behavior has been saved in self.m_indexOfEmittedBehavior (do I use this?  Yes, it is used to assign
		# fitness values when the Individual fitness method is used).

		self.m_blnSelection = value
		self.m_readyForNextEmission = False  #  Ensures that the next emission will not occur until the new generation is completed.

		if self.m_blnSelection:

			#Selection occurred---------------------
			# 1.  Assign fitness values
			# 2.  Create a new generation
			# 3.  Add mutation
			# 4.  Increment associative strength of SD
			#---------------------------------------

			#*************************************************************************************************************************************************
			# 6/2013:  Note while modifying the code for continuous uniform punishment:  At this point selectionParameter will be positive if a reinforcer was delivered,
			# and negative if a punisher was delivered.
			#*************************************************************************************************************************************************

			# 1.  Assign fitness values
			# Set the passed midpoint (relevant in the case of midpoint fitness only).
			self.m_intMidpoint = intMidpoint
			if self.get_fitness_landscape() == Constants.FITNESS_LANDSCAPE_FLAT:
				self.assign_flat_fitness_values()
			elif self.get_fitness_landscape() == Constants.FITNESS_LANDSCAPE_CIRCULAR:
				self.assign_circular_fitness_values()
			else:
				raise AssertionError("Trouble in Selection property of Behaviors class.")

			# 2.  Create a new generation
			# Set the GenericSelectionParameter property of the Selector.  The Selector will turn this into the
			# specific selection parameter required by the selection method in effect.
			# Also, pass the phenotype of the just emitted behavior to the selector so that the maximum fitness can be calculated when using
			# a flat fitness landscape.
			self.m_objSelector.set_generic_selection_parameter(selectionParameter)  # Will be positive for reinforcement, negative for punishment
			self.m_objSelector.set_just_emitted_phenotype(self.m_phenotypeOfEmittedBehavior)
			# for continuous linear or continuous uniform selection, check to make sure that there are at least
			# two unique fit phenotypes for mating.  If not, raise an exception (that must be trapped by the calling
			# program), and then exit this procedure.  See comments in the DoARun procedure (in "Defunct procedures no longer used" region)
			# of frmBuildOrganism for how to handle the exception.
			# The last AND clause was added by Nick Calvin:  it is not necessary to have two unique fit phenotypes when cloning.
			if self.m_objSelector.get_selection_method() == Constants.SELECTION_METHOD_CONTINUOUS and (self.m_objSelector.get_continuous_function_form() == Constants.CONTINUOUS_FUNCTION_FORM_LINEAR or self.m_objSelector.get_continuous_function_form() == Constants.CONTINUOUS_FUNCTION_FORM_UNIFORM) and (self.m_stuBehaviorsInfo.get_recombination_info().get_method() != Constants.RECOMBINATION_METHOD_CLONE):
				if not self.at_least_two_fit_phenotypes(selectionParameter):
					raise AssertionError("Only one fit phenotype.")
			elif self.m_objSelector.get_selection_method() == Constants.SELECTION_METHOD_CONTINUOUS and self.m_objSelector.get_continuous_function_form() == Constants.CONTINUOUS_FUNCTION_FORM_EXPONENTIAL:
				pass
				# #Test for too long dwell on two parent draws (equivalent to 2 fit behaviors)--This is a disaster.
				# #raise AssertionError("Testing for too long dwell.")
				# tempIndex = DwellTooLong(-1)
				# if tempIndex = -999 Then
				# 	self.m_blnSelection = False
				# else:
				# 	tempIndex = DwellTooLong(tempIndex)
				# 	#Trying for a distinct mother
				# 	#raise AssertionError("Trying a mother.")
				# 	if tempIndex = -999 Then
				# 		self.m_blnSelection = False
				#
				#
			self.create_new_generation(self.m_blnSelection)
			# 3.  Add mutation
			self.add_mutation()
			# 4.  Increment associative strength of SD
			if selectionParameter > 0:
				# A reinforcer was delivered.
				self.m_objRW.reinforcement_is_present()  # Increment only in the case of reinforcement (not punishment)
			else:
				# A punishmer was delivered.
				self.m_objRW.reinforcement_is_absent()  # Note that this equates punishment with non-reinforcement, which may not be reasonable.
		else:
			# Selection did not occur; no need to assign fitness values
			self.create_new_generation(self.m_blnSelection)
			self.add_mutation()
			self.m_objRW.reinforcement_is_absent()

		self.m_readyForNextEmission = True  # The new generation is complete; the next emission can occur.

	def emit_behavior(self):

		# Emit a random behavior from the population.

		# HighestInteger and LowestInteger properties of self.m_objRandom were set to 0 and self.get_num_behaviors()-1
		# in the constructor.

		if not self.m_readyForNextEmission:
			return
		# 												  Exiting the function here will probably generate an error in the calling
		# 												  program.  But this is a safeguard (don't know it if is really necessary)
		# 												  to ensure that a new generation is complete before a behavior is
		# 												  emitted from it.  The calling (laboratory or environment) program should
		# 												  test the ReadyToEmit property before calling this function.

		if self.get_viscosity_ticks() > 0:
			tempBehavior = Behavior(self.m_objSavedPops.emit_phenotype())
			tempBehavior.pad_to(self.m_bitsInHighPhenotype)
			self.m_integerValueOfEmittedBehavior = tempBehavior.get_integer_value()  # Must be saved because it is used to assign fitness values
			# 															for the Individual Fitness method

			#-----------------------------------------------------------------------------------------------------------------------

			# If want to use the other method of amalgamation, where the next generation is created from the amalgamated population,
			# then the amalgamated population must replace the existing population here.  (There are problems here.  It appears that
			# mutation may not be working correctly.  It does appear to be working correctly when the original populations are used.)

			if self.m_blnCreateFromSynthetic:
				self.m_behavior_list.clear()
				lstSyntheticPhenotypes = self.m_objSavedPops.get_synthetic_phenotypes()
				for tempInteger in lstSyntheticPhenotypes:
					syntheticBehavior = Behavior(tempInteger)
					syntheticBehavior.pad_to(self.m_bitsInHighPhenotype)
					self.add_behavior(syntheticBehavior)
			#-----------------------------------------------------------------------------------------------------------------------

			return tempBehavior
			# Exit Function

		# The following line is executed if the "Add Viscosity" check box is unchecked or if it
		# is checked and self.get_viscosity_ticks() = 0.  Could rewrite this so that the integer value is saved here
		# as well (instead of the index of the emitted behavior).  This would make the code more uniform.
		# Note that the Assign...FitnessValues procedures would have to be changed if the code were rewritten.
		# Leave it as is for now, though.  May want to rewrite it if the viscosity thing works out.
		self.m_indexOfEmittedBehavior = self.m_objRandom.get_rectangular_integer()
		# Now (Spring 2012) saving the integer phenotype of the emitted behavior so that the exponential FDF can
		# be normalized over a flat fitness landscape.
		self.m_phenotypeOfEmittedBehavior = self.m_behavior_list[self.m_indexOfEmittedBehavior].get_integer_value()
		return self.m_behavior_list[self.m_indexOfEmittedBehavior]

	# Region " Procedures for assigning and testing fitness."

	def assign_flat_fitness_values(self):

		# Called by the Selection property

		# lstOfFitnesses(self.m_behavior_list.Count - 1) As Integer
		# intCounter  = -1
		# intCounter2  = -1

		if self.get_fitness_method() == Constants.FITNESS_METHOD_INDIVIDUAL:
			for objBehavior in self.m_behavior_list:
				if self.get_viscosity_ticks() > 0:
					objBehavior.set_fitness(abs(objBehavior.get_integer_value() - self.m_integerValueOfEmittedBehavior))
				else:
					objBehavior.set_fitness(abs(objBehavior.get_integer_value()) - self.m_behavior_list(self.m_indexOfEmittedBehavior).get_integer_value())
		elif self.get_fitness_method() == Constants.FITNESS_METHOD_MIDPOINT:
			for objBehavior in self.m_behavior_list:
				objBehavior.set_fitness(abs(objBehavior.get_integer_value()) - self.m_intMidpoint)
		elif self.get_fitness_method() == Constants.FITNESS_METHOD_ENTIRE_CLASS:
			raise AssertionError("The class fitness method has not yet been implemented.")
		else:
			raise AssertionError("Trouble in AssignFlatFitnessValues procedure in Behaviors class.")

		# THIS DOES NOT PRODUCE A SUBSTANTIAL REDUCTION IN DWELL TIMES<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
		# #Sort fitnesses and assign smallest and largest values to module level variables. (Added 2/2014--to deal with the exponential dwell times).
		# #Note that, for now, this is only implemented for Flat fitness landscapes.
		# #Remember that both self.m_behavior_list and lstOfFitnesses are zero based.
		# #First thing to test:  see if this reduces the dwell times for Raillard punishment.  NOT DRAMATICALLY.<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
		# if self.m_objSelector.get_selection_method() = SelectionMethod.Continuous and self.m_objSelector.ContinuousFunctionForm = ContinuousFunctionForm.Exponential Then
		# 	for objBehavior in self.m_behavior_list
		# 		intCounter += 1 #Initialized to -1 when dimensioned
		# 		lstOfFitnesses(intCounter) = objBehavior.get_fitness()
		#
		# 	Array.Sort(lstOfFitnesses)
		# 	#I think the zeroth item in the list will always be zero because it is for the emitted behavior.  Also, subsequent items will be zero if there
		# 	#are more instances of the emitted behavior in the population.
		# 	#So...find the first non-zero item
		# 	Do
		# 		intCounter2 += 1 #Initialized to -1 when dimensioned
		# 	Loop While lstOfFitnesses(intCounter2) = 0
		# 	self.m_intSmallestFitnessValue = lstOfFitnesses(intCounter2)
		# 	self.m_intLargestFitnessValue = lstOfFitnesses(intCounter)
		# 	raise AssertionError("First = " & lstOfFitnesses(0).ToString & "; smallest (" & intCounter2.ToString & ") = " & self.m_intSmallestFitnessValue.ToString & "; largest = " & self.m_intLargestFitnessValue.ToString & "; total = " & (intCounter + 1).ToString)
		# 	#Pass the smallest nonzero and largest fitness values to the Selector
		# 	self.m_objSelector.SmallestNonZeroFitness = self.m_intSmallestFitnessValue
		# 	self.m_objSelector.LargestFitness = self.m_intLargestFitnessValue
		#

	def assign_circular_fitness_values(self):

		if self.get_fitness_method() == Constants.FITNESS_METHOD_INDIVIDUAL:
			for objBehavior in self.m_behavior_list:
				if self.get_viscosity_ticks() > 0:
					oneWay = abs(objBehavior.get_integer_value() - self.m_integerValueOfEmittedBehavior)
				else:
					oneWay = abs(objBehavior.get_integer_value() - self.m_behavior_list[self.m_indexOfEmittedBehavior].get_integer_value())
				otherWay = self.get_high_phenotype() - self.get_low_phenotype() + 1 - oneWay
				if oneWay <= otherWay:
					objBehavior.set_fitness(oneWay)
				else:
					objBehavior.set_fitness(otherWay)
		elif self.get_fitness_method() == Constants.FITNESS_METHOD_MIDPOINT:
			for objBehavior in self.m_behavior_list:
				oneWay = abs(objBehavior.get_integer_value() - self.m_intMidpoint)
				otherWay = self.get_high_phenotype() - self.get_low_phenotype() + 1 - oneWay
				if oneWay <= otherWay:
					objBehavior.set_fitness(oneWay)
				else:
					objBehavior.set_fitness(otherWay)
		elif self.get_fitness_method() == Constants.FITNESS_METHOD_ENTIRE_CLASS:
			raise AssertionError("The class fitness method has not yet been implemented.")
		else:
			raise AssertionError("Trouble in AssignCircularFitnessValues procedure in Behaviors class.")

	def dwell_too_long(self, intIndexFather):

		gotOne = False
		timesThroughPopulation = 0
		while not gotOne:
			itemCounter = 0
			targetFitness = self.m_objSelector.draw_random_fitness()
			for objBehavior in self.m_behavior_list:
				if objBehavior.get_fitness() == targetFitness and intIndexFather != itemCounter:
					gotOne = True
					indexToReturn = itemCounter
					break
				itemCounter += 1

			if not gotOne:
				timesThroughPopulation += 1
				if timesThroughPopulation == 1000:
					break

		if gotOne:
			return indexToReturn
		else:
			return -999

	def at_least_two_fit_phenotypes(self, selectionParameter):

		# Called by the Selection(Double, Integer) property when using a continuous linear or continuous uniform FDF
		# The passed selectionParameter will be positive for reinforcement and negative for punishment.
		# The .ContinuousMean property of the Selector was set to selectionParameter in the Selection(Double, Integer) property
		# above.  So I guess I don#t really need to pass it here.  Alternatively, I could use selectionParameter in this
		# procedure instead of .ContinuousMean.  I think I#ll do the latter.

		# Returns False if there are fewer than 2 fit behaviors, otherwise returns True.  Significant work is done in this
		# procedure if there are not at least two fit phenotypes.

		objSampler = SampleWoutReplace()
		intCounter = 0
		blnNoProblemo = False

		# Calculate fitness limits (this takes into account whether reinforcement or punishment occurred).
		self.m_objFitnessLimits.calculate_fitness_limits(selectionParameter, self.m_phenotypeOfEmittedBehavior)

		# See if there are at least 2 fit behaviors (works for both reinforcement and punishment).
		for objBehavior in self.m_behavior_list:
			if objBehavior.get_fitness() < self.m_objFitnessLimits.get_maximum_fitness() and objBehavior.get_fitness() >= self.m_objFitnessLimits.get_minimum_fitness():
				# Why this is not <= intMaxFitness is discused on p. 172 of my Single Selection notebook.
				# This fine point may be worth investigating because it seems like a glitch, although evidently
				# not a serious one.  I am not sure whether the second inequality should be > or >= (6/2013).
				if objSampler.OK(objBehavior.get_integer_value()):
					# N.B., There must be at least two fit behaviors with different integer values, i.e. two unique phenotypes.
					# This is consistent with the old code (which would kick out an abort message when the infinite loops
					# occurred), but may be worth investigating further.  What happens when there are several fit behaviors,
					# but they are all the same phenotype, and hence would produce clones?
					# With this If...Then block, should never get the infinite loop again (famous last words...I hope not).
					# Caveat:  if midpoint fitness is used, there MUST be an odd number of behaviors in the target class,
					# i.e. the midpoint of the target class must be an integer, otherwise I think the infinite loop can still happen.
					intCounter += 1
					objLastFitBehavior = objBehavior
			if intCounter == 2:
				blnNoProblemo = True
				break
		if blnNoProblemo:
			return True  # There are at least two fit phenotypes

		# if selectionParameter > 0 Then
		# 	#A reinforcer was delivered.
		# 	if intCounter = 0 Then
		# 		#**********I believe this is impossible.  The reinforcer had to have been produced by a fit behavior.
		# 		raise AssertionError("Reinforcement delivered:  0 fit parents.")
		# 		raise AssertionError(CStr(self.m_objFitnessLimits.MinimumFitness) & "-" & CStr(self.m_objFitnessLimits.MaximumFitness) & "	 " & CStr(self.m_phenotypeOfEmittedBehavior))
		# 		#for objBehavior in self.m_behavior_list
		# 		#	print(CStr(objBehavior.IntegerValue) & "	 " & CStr(objBehavior.get_fitness()))
		# 		#
		# 		#

		# 		#A behavior with a nonzero fitness must be selected and cloned.
		# 		intFitnessOfClone = self.m_objSelector..draw_random_fitness()
		# 		intPhenotypeOfClone = intFitnessOfClone + self.m_phenotypeOfEmittedBehavior # This works only for flat fitness landscapes for now.  Double check!
		# 		tempBehavior = New Behavior(intPhenotypeOfClone)
		# 		tempBehavior.pad_to(self.m_bitsInHighPhenotype) #Ensures the correct number of bits in the behavior to be cloned.
		# 		BehaviorToClone = tempBehavior
		# 		blnNoProblemo = True #No kickout
		# 	elif intCounter = 1 Then
		# 		#raise AssertionError("Reinforcement delivered:  1 fit parent.")
		# 		#raise AssertionError(CStr(self.m_objFitnessLimits.MinimumFitness) & "-" & CStr(self.m_objFitnessLimits.MaximumFitness) & "	 " & CStr(self.m_phenotypeOfEmittedBehavior))
		# 		#for objBehavior in self.m_behavior_list
		# 		#	print(CStr(objBehavior.IntegerValue) & "	 " & CStr(objBehavior.get_fitness()))
		# 		#
		# 		#

		# 		#This behavior must be cloned.
		# 		BehaviorToClone = objLastFitBehavior #This will force cloning using the 1 fit behavior
		# 		blnNoProblemo = True # No kickout
		#
		# elif selectionParameter < 0 Then
		# 	#A punisher was delivered.
		# EndIf

		if intCounter == 0:  # There are no fit phenotypes.  A behavior with a nonzero fitness must be selected and cloned.
			while True:
				intFitnessOfClone = self.m_objSelector.draw_random_fitness()  # DrawRandomFitness knows whether a reinforcer or a punisher was delivered.
				if intFitnessOfClone + self.m_phenotypeOfEmittedBehavior <= self.get_high_phenotype():
					# It is possible to get a phenotype that is beyond the specified range.
					# Fitness OK.  (Otherwise, draw another fitness value).
					break

			#for testing-------------------------------------------------------
			# if selectionParameter < 0 Then print(CStr(intFitnessOfClone))
			#------------------------------------------------------------------
			intPhenotypeOfClone = intFitnessOfClone + self.m_phenotypeOfEmittedBehavior
			# This works only for flat fitness landscapes for now.  Double check!
			# Why shouldn#t intPhenotypeOfClone = intFitnessOfClone?  Because the emitted behavior has zero fitness.  The phenotype of the clone
			# must be an integer distance away from the emitted behavior that is equal to its fitness.  Hence _that_ phenotype has the fitness
			# value that was drawn at random.  intPhenotypeOfClone = inFitnessOfClone only when the phenotype of the emitted behavior is zero.
			#Test----------------------------------------------
			if intPhenotypeOfClone > self.get_high_phenotype():
				raise AssertionError("> {self.get_high_phenotype()}")
				# This appears to be an extremely rare event (at least for the 0-40 target range) but just in case...
				# The Do...Loop above should take care of this problem, but I#m still not 100% clear what the effect is.
				intPhenotypeOfClone = self.get_high_phenotype()
			#--------------------------------------------------
			tempBehavior = Behavior(intPhenotypeOfClone)
			tempBehavior.pad_to(self.m_bitsInHighPhenotype)  # Ensures the correct number of bits in the behavior to be cloned.
			self.set_behavior_to_clone(tempBehavior)
			blnNoProblemo = True  # No kickout
		elif intCounter == 1:  # There is only one fit phenotype.  This behavior must be cloned.
			self.set_behavior_to_clone(objLastFitBehavior)  # This will force cloning using the 1 fit behavior
			blnNoProblemo = True  # No kickout

		if blnNoProblemo:
			return True
		else:
			return False

	def administer_repulsion_punishment(self, paramReinforcer, paramPunisher):

		lstRepelledBehaviors = list()
		reproduceAndMutate = True  # for use after punishment
		# for testing, change this property here.
		# m_punishmentMethod = PunishmentMethod.RepelFold

		if paramReinforcer != 0 and paramPunisher != 0:
			# Both reinforcer and punisher were delivered.
			# Flip a coin to determine whether to punish or reinforce first
			intCoinToss = self.m_objCoinToss.get_rectangular_integer()
			#To test always punishing first--------------------------------------------------------------------------------------------
			intCoinToss = 0
			#--------------------------------------------------------------------------------------------------------------------------
			#To test repell-only when punishing first----------------------------------------------------------------------------------
			# reproduceAndMutate = True
			#--------------------------------------------------------------------------------------------------------------------------
			if intCoinToss == 0:
				# Punish first
				# Repell the behaviors
				# m_objRepulsionPunishment.RepelBehaviors(self.m_behavior_list, self.m_phenotypeOfEmittedBehavior, paramPunisher, lstRepelledBehaviors)
				# m_objRepulsionPunishment.RepelBehaviors2(self.m_behavior_list, self.m_phenotypeOfEmittedBehavior, paramPunisher, lstRepelledBehaviors)
				if self.get_punishment_method() == Constants.PUNISHMENT_METHOD_REPEL_FOLD:
					# Fold-over repulsion puishment
					self.m_objRepulsionPunishment.kelley_repel_behaviors_2(self.m_behavior_list, self.m_phenotypeOfEmittedBehavior, paramPunisher, lstRepelledBehaviors)
				elif self.get_punishment_method() == Constants.PUNISHMENT_METHOD_REPEL_WRAP:
					# Circular repulsion punishment
					self.m_objRepulsionPunishment.circular_repel(self.m_behavior_list, self.m_phenotypeOfEmittedBehavior, paramPunisher, lstRepelledBehaviors, 0)
				else:
					raise AssertionError("Trouble in AdministerRepulsionPunishment.")

				# Transfer the repelled behaviors to self.m_behavior_list
				self.m_behavior_list.clear()
				for tempBehavior in lstRepelledBehaviors:
					self.add_behavior(tempBehavior)
				if reproduceAndMutate:
					self.set_selection_overload_2(0, 0, False)
				else:
					pass
					# Repell only

				# Now deliver the reinforcer
				self.set_selection_overload_2(paramReinforcer, 0, True)
			elif intCoinToss == 1:
				# Reinforce first
				self.set_selection_overload_2(paramReinforcer, 0, True)
				# Now punish
				# Repell the behaviors
				# m_objRepulsionPunishment.RepelBehaviors(self.m_behavior_list, self.m_phenotypeOfEmittedBehavior, paramPunisher, lstRepelledBehaviors)
				# m_objRepulsionPunishment.RepelBehaviors2(self.m_behavior_list, self.m_phenotypeOfEmittedBehavior, paramPunisher, lstRepelledBehaviors)
				if self.get_punishment_method() == Constants.PUNISHMENT_METHOD_REPEL_FOLD:
					# Fold-over repulsion puishment
					self.m_objRepulsionPunishment.kelley_repel_behaviors_2(self.m_behavior_list, self.m_phenotypeOfEmittedBehavior, paramPunisher, lstRepelledBehaviors)
				elif self.get_punishment_method() == Constants.PUNISHMENT_METHOD_REPEL_WRAP:
					# Circular repulsion punishment
					self.m_objRepulsionPunishment.circular_repel(self.m_behaviors_list, self.m_phenotypeOfEmittedBehavior, paramPunisher, lstRepelledBehaviors, 0)
				else:
					raise AssertionError("Trouble in AdministerRepulsionPunishment.")

				# Transfer the repelled behaviors to self.m_behavior_list
				self.m_behaviors_list.clear()
				for tempBehavior in lstRepelledBehaviors:
					self.add_behavior(tempBehavior)
				# Create a new generation by selecting parent behaviors at random from the list of repelled behaviors and add mutation
				# (i.e., pretend there was no selection).
				self.set_selection_overload_2(0, 0, False)
			else:
				raise AssertionError("Coin toss problem in Behaviors.Selection(Double, Double)")
			# Another option:  do each half the time (less complicated).
		elif paramReinforcer == 0 and paramPunisher != 0:
			# Punisher only was delivered
			# Repell the behaviors
			# m_objRepulsionPunishment.RepelBehaviors(self.m_behavior_list, self.m_phenotypeOfEmittedBehavior, paramPunisher, lstRepelledBehaviors)
			# m_objRepulsionPunishment.RepelBehaviors2(self.m_behavior_list, self.m_phenotypeOfEmittedBehavior, paramPunisher, lstRepelledBehaviors)
			if self.get_punishment_method() == Constants.PUNISHMENT_METHOD_REPEL_FOLD:
				# Fold-over repulsion puishment
				self.m_objRepulsionPunishment.kelley_repel_behaviors_2(self.m_behavior_list, self.m_phenotypeOfEmittedBehavior, paramPunisher, lstRepelledBehaviors)
			elif self.get_punishment_method() == Constants.PUNISHMENT_METHOD_REPEL_WRAP:
				# Circular repulsion punishment
				self.m_objRepulsionPunishment.circular_repel(self.m_behavior_list, self.m_phenotypeOfEmittedBehavior, paramPunisher, lstRepelledBehaviors, 0)
			else:
				raise AssertionError("Trouble in AdministerRepulsionPunishment.")

			self.m_behavior_list.clear()
			for tempBehavior in lstRepelledBehaviors:
				self.add_behavior(tempBehavior)
			# Transfer the repelled behaviors to self.m_behavior_list
			# Create a new generation by selecting parent behaviors at random from the list of repelled behaviors
			# (i.e., pretend there was no selection).
			self.set_selection_overload_2(0, 0, False)
		else:
			raise AssertionError("Trouble in Selection(Double, Double).  Reinforcer-only delivery unhandled.")

	def diff_repel_punish(self, paramPunisher, dblValueAdjustment):

		# Carries out differential circular repulsion punishment (5/2018).  This is a new procedure to bypass AdministerRepulsionPunishment

		lstRepelledBehaviors = list()
		blnReproduceAndMutate = True

		# Permit only circular punishment for now.  for some reason this is not getting loaded into the organism info structure.
		self.set_punishment_method(Constants.PUNISHMENT_METHOD_REPEL_WRAP)

		# Repell the behaviors
		# m_objRepulsionPunishment.RepelBehaviors(self.m_behavior_list, self.m_phenotypeOfEmittedBehavior, paramPunisher, lstRepelledBehaviors)
		# m_objRepulsionPunishment.RepelBehaviors2(self.m_behavior_list, self.m_phenotypeOfEmittedBehavior, paramPunisher, lstRepelledBehaviors)
		if self.get_punishment_method() == Constants.PUNISHMENT_METHOD_REPEL_FOLD:
			raise AssertionError("Shouldn't be in here in Behaviors.DiffRepelPunish")
			# Fold-over repulsion puishment
			self.m_objRepulsionPunishment.kelley_repel_behaviors_2(self.m_behavior_list, self.m_phenotypeOfEmittedBehavior, paramPunisher, lstRepelledBehaviors)
		elif self.get_punishment_method() == Constants.PUNISHMENT_METHOD_REPEL_WRAP:
			# Circular repulsion punishment
			self.m_objRepulsionPunishment.circular_repel(self.m_behavior_list, self.m_phenotypeOfEmittedBehavior, paramPunisher, lstRepelledBehaviors, dblValueAdjustment)
		else:
			raise AssertionError("Trouble in DiffRepelPunish.")

		# Transfer the repelled behaviors to self.m_behavior_list
		self.m_behavior_list.clear()
		for tempBehavior in lstRepelledBehaviors:
			self.add_behavior(tempBehavior)

		if blnReproduceAndMutate:
			# Create a new generation by selecting parent behaviors at random from the list of repelled behaviors and add mutation.
			# (i.e., pretend there was no selection).
			self.set_selection_overload_2(0, 0, False)
		else:
			pass
			# Repell only

	def forced_mut_punish(self, punishMag, mutFuncParam, loBoundaryPheno, loTargetPheno, hiTargetPheno, hiBoundaryPheno):

		# Booleans for mutation methods:
		# blnFlip2 = flip two bits, blnFlipAll = flip all bits, blnMutateOut = mutate out of target class, blnMutateOutOfBoth = mutate out of both target classes.
		# When all are set to False, the original single bit-flip method of mutation is used.
		blnFlip2 = False
		blnFlipAll = False
		blnMutateOut = False
		blnMutateOutOfBoth = False
		# Dim blnLinearMutationFunction As Boolean = False, blnRectMutationFunction As Boolean = False  Not going to use these anymore (5/31/2018)
		blnFixedNumberOut = False  # Fixed number of behaviors mutate out for every punisher
		blnDiffPunishMO = False  # Differential punishment, which depends on the reinforcement context.
		# 									   This is set to True for both "mutate out" and "mutate once" options.
		# 									   if blnMutateOnce = False then "mutate out" is in effect; if True then "mutate once" is in effect.
		blnDiffPunishRectPulse = True

		self.m_objProbEmitter.set_prob_of_emission(punishMag)
		self.m_objRandomBit.set_lowest_integer(1)
		self.m_objRandomBit.set_highest_integer(10)

		if blnDiffPunishRectPulse:  # This will probably end up being the default, The One
			# Assign "fitness" values.
			# These will already be assigned if reinforcement was delivered first.  They will be reassigned here.
			# If punishment is delivered first, then they will be freshly assigned here and reassigned when reinforcement is delivered.
			for objBehavior in self.m_behavior_list:
				oneWay = abs(objBehavior.get_integer_value() - self.get_behavior(self.m_indexOfEmittedBehavior).get_integer_value())
				otherWay = self.get_high_phenotype() - self.get_low_phenotype() + 1 - oneWay
				if oneWay <= otherWay:
					objBehavior.set_fitness(oneWay)
				else:
					objBehavior.set_fitness(otherWay)

			# Go through the list to identify behaviors with "fitness" values <= mutFuncParam (which is the rectangular extent of the uniform mutation function
			# --only these will undergo mutation.
			# (for now, use the standard method of mutation, viz., flip one bit at random.)
			for index in range(len(self.m_behavior_list)):
				thisFitness = self.get_behavior(index).get_fitness()
				if thisFitness <= mutFuncParam:  # mutFuncParam is (half?) the extent of the rectangular mutation function.
					# Phenotype is within the rectangular pulse
					if self.m_objProbEmitter.get_emission() == True:  # This implements the differential punishment
						# Mutate it
						if blnMutateOut == True:
							# Mutate out of the rectangular pulse
							thisPheno = self.get_behavior(index).get_integer_value()
							while True:
								thisGeno = self.m_objMutator.convert_integer_to_boolean(thisPheno)
								intBitToFlip = self.m_objRandomBit.get_rectangular_integer()
								thisGeno[intBitToFlip] = not thisGeno[intBitToFlip]
								mutantPheno = self.m_objMutator.get_integer_to_return(thisGeno)
								if mutantPheno > self.m_phenotypeOfEmittedBehavior + mutFuncParam or mutantPheno < self.m_phenotypeOfEmittedBehavior - mutFuncParam:
									# The phenotype has mutated out of the target class
									self.set_behavior(index, Behavior(mutantPheno))  # Evidently, this replaces the behavior at this index with the new (mutant) behavior
									self.get_behavior(index).pad_to(self.m_bitsInHighPhenotype)
									break

								thisPheno = mutantPheno
						else:
							# Mutate once
							thisGeno = self.m_objMutator.convert_integer_to_boolean(self.get_behavior(index).get_integer_value())
							intBitToFlip = self.m_objRandomBit.get_rectangular_integer()
							thisGeno[intBitToFlip] = not thisGeno[intBitToFlip]
							mutantPheno = self.m_objMutator.get_integer_to_return(thisGeno)
							self.set_behavior(index, Behavior(mutantPheno))  # Evidently, this replaces the behavior at this index with the new (mutant) behavior
							self.get_behavior(index).pad_to(self.m_bitsInHighPhenotype)

			return

		if blnDiffPunishMO == True:  # Also runs "mutate once" when blnMutateOnce = True
			# This is identical to blnMutateOut (not anymore).  N.B.: the correct value of punishMag must be passed!!
			blnMutateOnce = True  #<<<<<<<---------------*********************************************************************************
			for index in range(len(self.m_behavior_list)):
				# Sort through the list to identify behaviors in the appropriate target class.
				thisPheno = self.get_behavior(index).get_integer_value()
				if thisPheno >= loTargetPheno and thisPheno <= hiTargetPheno:
					# thisPheno is in the target class; check to see if it should mutate
					if self.m_objProbEmitter.get_emission() == True:
						# This behavior should mutate
						if blnMutateOnce:
							# Mutate once
							thisGeno = self.m_objMutator.convert_integer_to_boolean(thisPheno)
							intBitToFlip = self.m_objRandomBit.get_rectangular_integer()
							thisGeno[intBitToFlip] = not thisGeno[intBitToFlip]
							mutantPheno = self.m_objMutator.get_integer_to_return(thisGeno)
							self.set_behavior(index, Behavior(mutantPheno))  # Evidently, this replaces the behavior at this index with the new (mutant) behavior
							self.get_behavior(index).pad_to(self.m_bitsInHighPhenotype)
						else:
							# Mutate out of the target class
							while True:
								thisGeno = self.m_objMutator.conver_integer_to_boolean(thisPheno)
								intBitToFlip = self.m_objRandomBit.get_rectangular_integer()
								thisGeno[intBitToFlip] = not thisGeno[intBitToFlip]
								mutantPheno = self.m_objMutator.get_integer_to_return(thisGeno)
								if mutantPheno > hiTargetPheno or mutantPheno < loTargetPheno:
									# The phenotype has mutated out of the target class
									self.set_behavior(index, Behavior(mutantPheno))  # Evidently, this replaces the behavior at this index with the new (mutant) behavior
									self.get_behavior(index).pad_to(self.m_bitsInHighPhenotype)
									break

								thisPheno = mutantPheno

			return

		if blnFixedNumberOut == True:
			intNumTargetBehaviors = 0
			intNumberOut = 0
			# Count the number of behaviors in the target class
			for index in range(len(self.m_behavior_list)):
				thisPheno = self.get_behavior(index).get_integer_value()
				if thisPheno >= loTargetPheno and thisPheno <= hiTargetPheno:
					intNumTargetBehaviors += 1

			for index in range(len(self.m_behavior_list)):

				if intNumberOut < mutFuncParam and intNumberOut < intNumTargetBehaviors:
					# Sort through the list to identify behaviors in the appropriate target class.
					thisPheno = self.get_behavior(index).get_integer_value()

					if thisPheno >= loTargetPheno and thisPheno <= hiTargetPheno:
						# thisPheno is in the target class; mutate it out
						while True:
							thisGeno = self.m_objMutator.convert_integer_to_boolean(thisPheno)
							intBitToFlip = self.m_objRandomBit.get_rectangular_integer()
							thisGeno[intBitToFlip] = not thisGeno[intBitToFlip]
							mutantPheno = self.m_objMutator.get_integer_to_return(thisGeno)
							if mutantPheno > hiTargetPheno or mutantPheno < loTargetPheno:
								# The phenotype has mutated out of the target class
								self.set_behavior(index, mutantPheno)  # Evidently, this replaces the behavior at this index with the new (mutant) behavior
								self.get_behavior(index).pad_to(self.m_bitsInHighPhenotype)
								break

							thisPheno = mutantPheno

						intNumberOut += 1

				else:
					# mutFuncParm or intNumTargetBehaviors behaviors have been mutated out of the target class
					break

			return

		# Not going to use these any more

		# if blnRectMutationFunction = True Then
		# 	#Assign "fitness" values.
		# 	#These will already be assigned if reinforcement was delivered first.  They will be reassigned here.
		# 	#If punishment is delivered first, then they will be freshly assigned here and reassigned when reinforcement is delivered.
		# 	for objBehavior in self.m_behavior_list
		# 		oneWay = Math.Abs(objBehavior.IntegerValue - self.get_behavior(self.m_indexOfEmittedBehavior).IntegerValue)
		# 		otherWay = self.get_high_phenotype() - self.get_low_phenotype() + 1 - oneWay
		# 		if oneWay <= otherWay Then
		# 			objBehavior.Fitness = oneWay
		# 		else:
		# 			objBehavior.Fitness = otherWay
		#
		#
		# 	#Go through the list to identify behaviors with "fitness" values <= mutFuncParam (which is the rectangular extent of the uniform mutation function
		# 	#--only these will undergo mutation.
		# 	#(for now, use the standard method of mutation, viz., flip one bit at random.)
		# 	for index in range(len(self.m_behavior_list)):
		# 		thisFitness = self.get_behavior(index).get_fitness()
		# 		if thisFitness < mutFuncParam Then # mutFuncParam is the extent of the rectangular mutation function.
		# 			#Mutate it
		# 			thisGeno = self.m_objMutator.convert_integer_to_boolean(self.get_behavior(index).get_integer_value())
		# 			intBitToFlip = self.m_objRandomBit.get_rectangular_integer()
		# 			thisGeno[intBitToFlip] = Not thisGeno[intBitToFlip]
		# 			mutantPheno = self.m_objMutator.get_integer_to_return(thisGeno)
		# 			self.set_behavior(index,  New Behavior(mutantPheno) # Evidently, this replaces the behavior at this index with the new (mutant) behavior
		# 			self.get_behavior(index).pad_to(self.m_bitsInHighPhenotype)
		#
		#
		# 	return
		#

		# if blnLinearMutationFunction = True Then
		# 	#Assign "fitness" values.
		# 	#These will already be assigned if reinforcement was delivered first.  They will be reassigned here.
		# 	#If punishment is delivered first, then they will be freshly assigned here and reassigned when reinforcement is delivered.
		# 	for objBehavior in self.m_behavior_list
		# 		oneWay = Math.Abs(objBehavior.IntegerValue - self.get_behavior(self.m_indexOfEmittedBehavior).IntegerValue)
		# 		otherWay = self.get_high_phenotype() - self.get_low_phenotype() + 1 - oneWay
		# 		if oneWay <= otherWay Then
		# 			objBehavior.Fitness = oneWay
		# 		else:
		# 			objBehavior.Fitness = otherWay
		#
		#
		#	#**************This currently works only for a linear mutation density function.*****************
		# 	#Go through the list to identify behaviors with "fitness" values <= mutFuncParam (which is the reciprocal of the slope of the mutation function
		# 	#--only these will have non-negative probabilities of mutation.
		# 	#Then calculate the probability that the identified behavior will mutate using the mutation function; carry out the mutation if required.
		# 	#(for now, use the standard method of mutation, viz., flip one bit at random.)
		# 	for index in range(len(self.m_behavior_list)):
		# 		thisFitness = self.get_behavior(index).get_fitness()
		# 		if thisFitness < mutFuncParam Then # mutFuncParam is the x-intercept of the mutation function.
		# 			##-------------for testing
		# 			#dblTest = -(1 / mutFuncParam) * thisFitness + 1
		# 			#blnTest = self.m_objProbEmitter.get_emission()
		# 			#raise AssertionError(mutFuncParam.ToString & "	" & "Mutation might occur.   " & thisFitness.ToString & "	 " & dblTest.ToString & "   " & blnTest.ToString)
		# 			##This all appears to be working fine.  The mutation probabilities are pretty low, though, hence not many mutants?  This does not appear to be the case.
		#			##--------------------------
		# 			#This behavior may mutate
		# 			self.m_objProbEmitter.ProbOfEmission = -(1 / mutFuncParam) * thisFitness + 1 # Linear mutation function is used to determine probability of mutation.
		# 			#																		 Its y-intercept = 1 and its x-intercept = mutFuncParam
		# 			if self.m_objProbEmitter.get_emission() = True Then
		# 				#Carry out the mutation.
		# 				thisGeno = self.m_objMutator.convert_integer_to_boolean(self.get_behavior(index).get_integer_value())
		# 				intBitToFlip = self.m_objRandomBit.get_rectangular_integer()
		# 				thisGeno[intBitToFlip] = Not thisGeno[intBitToFlip]
		# 				mutantPheno = self.m_objMutator.get_integer_to_return(thisGeno)
		# 				self.set_behavior(index,  New Behavior(mutantPheno) # Evidently, this replaces the behavior at this index with the new (mutant) behavior
		# 				self.get_behavior(index).pad_to(self.m_bitsInHighPhenotype)
		#
		#
		#
		# 	return
		#

		if blnFlipAll == True:
			for index in range(len(self.m_behavior_list)):
				# Sort through the list to identify behaviors in the appropriate target class.
				thisPheno = self.get_behavior(index).get_integer_value()
				if thisPheno >= loTargetPheno and thisPheno <= hiTargetPheno:
					# thisPheno is in the target class; check to see if it should mutate
					if self.m_objProbEmitter.get_emission() == True:
						thisGeno = self.m_objMutator.convert_integer_to_boolean(thisPheno)
						# Flip all bits
						for i in range(1, 11):
							thisGeno[i] = not thisGeno[i]

						mutantPheno = self.m_objMutator.get_integer_to_return(thisGeno)
						self.set_behavior(index, Behavior(mutantPheno))  # Evidently, this replaces the behavior at this index with the new (mutant) behavior
						self.get_behavior(index).pad_to(self.m_bitsInHighPhenotype)

			return

		if blnMutateOut == True:
			for index in range(len(self.m_behavior_list)):
				# Sort through the list to identify behaviors in the appropriate target class.
				thisPheno = self.get_behavior(index).get_integer_value()
				if thisPheno >= loTargetPheno and thisPheno <= hiTargetPheno:
					# thisPheno is in the target class; check to see if it should mutate
					if self.m_objProbEmitter.get_emission() == True:
						# Mutate this pheno out of the target class
						while True:
							thisGeno = self.m_objMutator.convert_integer_to_boolean(thisPheno)
							intBitToFlip = self.m_objRandomBit.get_rectangular_integer()
							thisGeno[intBitToFlip] = not thisGeno[intBitToFlip]
							mutantPheno = self.m_objMutator.get_integer_to_return(thisGeno)
							if mutantPheno > hiTargetPheno or mutantPheno < loTargetPheno:
								# The phenotype has mutated out of the target class
								self.set_behavior(index, Behavior(mutantPheno))  # Evidently, this replaces the behavior at this index with the new (mutant) behavior
								self.get_behavior(index).pad_to(self.m_bitsInHighPhenotype)
								break

							thisPheno = mutantPheno

			return

		if blnMutateOutOfBoth == True:
			for index in range(len(self.m_behavior_list)):
				# Sort through the list to identify behaviors in the appropriate target class.
				thisPheno = self.get_behavior(index).get_integer_value()
				if thisPheno >= loTargetPheno and thisPheno <= hiTargetPheno:
					# thisPheno is in the target class; check to see if it should mutate
					if self.m_objProbEmitter.get_emission() == True:
						# Mutate this pheno out of the target class
						while True:
							thisGeno = self.m_objMutator.convert_integer_to_boolean(thisPheno)
							intBitToFlip = self.m_objRandomBit.get_rectangular_integer()
							thisGeno[intBitToFlip] = not thisGeno[intBitToFlip]
							mutantPheno = self.m_objMutator.get_integer_to_return(thisGeno)
							if mutantPheno > hiBoundaryPheno or mutantPheno < loBoundaryPheno:
								# The phenotype has mutated out of both target classes
								self.set_behavior(index, Behavior(mutantPheno))  # Evidently, this replaces the behavior at this index with the new (mutant) behavior
								self.get_behavior(index).pad_to(self.m_bitsInHighPhenotype)
								break

							thisPheno = mutantPheno

			return

		# It looks like this stub is never encountered because of the return statements in the If...Then structures
		for index in range(len(self.m_behavior_list)):
			# Sort through the list to identify behaviors in the appropriate target class.
			thisPheno = self.get_behavior(index).get_integer_value()
			if thisPheno >= loTargetPheno and thisPheno <= hiTargetPheno:
				# thisPheno is in the target class; check to see if it should mutate
				if self.m_objProbEmitter.get_emission() == True:
					# Mutate this pheno
					thisGeno = self.m_objMutator.convert_integer_to_boolean(thisPheno)
					intBitToFlip = self.m_objRandomBit.get_rectangular_integer()
					thisGeno[intBitToFlip] = not thisGeno[intBitToFlip]
					if blnFlip2 == True:
						# Mutate this pheno by flipping another, different, bit
						intBitFlipped = intBitToFlip
						while intBitFlipped == intBitToFlip:
							intBitToFlip = self.m_objRandomBit.get_rectangular_integer()

						thisGeno[intBitToFlip] = not thisGeno[intBitToFlip]

					# Replace thisPheno with mutantPheno in the List
					mutantPheno = self.m_objMutator.get_integer_to_return(thisGeno)
					self.set_behavior(index, Behavior(mutantPheno))  # Evidently, this replaces the behavior at this index with the new (mutant) behavior
					self.get_behavior(index).pad_to(self.m_bitsInHighPhenotype)

# Region " Procedures for creating new generations."

	def create_new_generation(self, blnSelection):
		# Called by the Selection(Double, Integer) property.

		# Receive information from the environment about whether EmitBehavior resulted in a
		# selection event (blnSelection = True) or not (blnSelection = False), and create a new population
		# accordingly.

		# Steps:
		# 1.  Get parents from Selector object.  (Don#t need this when getting random parents.)
		# 2.  Send parents to Recombinator to get child.
		# 3.  Add child to lstNewChldBehaivors
		# 4.  Transfer lstNewChildBehaviors to self.m_behavior_list

		intNumToReplace = int(self.get_percent_to_replace() / 100 * self.get_num_behaviors())  # When selection occurs
		intNumToReplace2 = int(self.get_percent_to_replace_2() / 100 * self.get_num_behaviors())  # When selection does not occur (added 1/2018)
		lstNewChildBehaviors = list()  # This will contain the new child behaviors

		if blnSelection and self.m_blnForceClone:
			# Force cloning when punishment leaves 0 or 1 fit parents
			for _ in range(intNumToReplace):
				blnChild = self.m_objBehaviorToClone.get_binary_bits()
				lstNewChildBehaviors.append(Behavior(blnChild))

			self.m_blnForceClone = False  # Reset self.m_blnForceClone flag
		elif blnSelection:
			#Choose parents on the basis of their fitness------------------------------------------
			for _ in range(intNumToReplace):  # intNumToReplace was assigned the correct value
				# 						 when it was dimensioned in this procedure.

				# Get indices of father and mother behaviors
				self.m_objSampler.clear()
				intIndexFather = self.m_objSelector.get_parent_index(self.m_behavior_list)
				# #------------------------------------------------------------888888888888888888888888888888888888888888888888888888888888888888 FATHER-BAILOUT
				# if intIndexFather = -999 Then #Dwell was too long
				# 	#raise AssertionError("Father-dwell too long.")
				# 	Select Case self.m_objSelector.ContinuousMean
				# 		Case Is > 0
				# 			self.m_intRBailOuts += 1
				# 		Case Is < 0
				# 			self.m_intPBailOuts += 1
				# 		Case Else
				# 			raise AssertionError("Bailout problem in CreateNewGeneration.")
				#
				# 	CreateNewGeneration(False) #Creates a new generation with random parents from the population
				# 	return
				# 	#CreateNGWithRandomFitParents(lstNewChildBehaviors, intNumToReplace)
				# 	#Exit For
				#
				# #------------------------------------------------------------88888888888888888888888888888888888888888888888888888888888888888888888888888888
				self.m_objSampler.OK(intIndexFather)  # Puts intIndexFather into the list of sampled indices.
				#----Make sure mother is different from father (i.e., has a different index = is a different
				#----behavior; this behavior could have the same phenotype as the father).
				# The following If...Then...Else structure is due to Nick:  you don#t need to find a mother behavior in the case of cloning
				if self.m_stuBehaviorsInfo.get_recombination_info().get_method() == Constants.RECOMBINATION_METHOD_CLONE:
					# Don't need to find a mother
					intIndexMother = intIndexFather  # Dummy statement; mother index is not needed.
				else:
					# Do need to find a mother.
					intMotherLoopCounter = 0
					while True:
						intIndexMother = self.m_objSelector.get_parent_index(self.m_behavior_list, intIndexFather)  # The second argument is part of
						# Nick#s solution to the mother loop problem.  See notes in the GetParentIndex procedure of the Selector
						# for details.
						# #--------------------------------------------------------------------------------------------8888888888888888888888888 MOTHER-BAILOUT
						# if intIndexMother = -999 Then #Dwell was too long
						# 	Select Case self.m_objSelector.ContinuousMean
						# 		Case Is > 0
						# 			self.m_intRBailOuts += 1
						# 		Case Is < 0
						# 			self.m_intPBailOuts += 1
						# 		Case Else
						# 			raise AssertionError("Bailout problem in CreateNewGeneration.")
						#
						# 	CreateNewGeneration(False) #Creates a new generation with random parents from the population
						# 	return
						# 	#CreateNGWithRandomFitParents(lstNewChildBehaviors, intNumToReplace)
						# 	#Exit For
						#
						# #for testing---------------------------------------------------------------------------------8888888888888888888888888888888888888888
						# This is to test the infinite loop problem which occurs
						# when there are at least two fit behaviors, but all have
						# the same fitness.  GetParentIndex will keep returning the
						# first fit behavior it finds, which will be the same as the father.
						intMotherLoopCounter += 1
						if intMotherLoopCounter > 100000:
							raise AssertionError("More than 100000 mother loops for True blnSelection.")
							for objBehavior in self.m_behavior_list:
								print(objBehavior.get_fitness())

						if self.m_objSampler.OK(intIndexMother):
							break
						#----------------------------------------------------
					intMotherLoopCounter = 0  # for testing

				# Make a baby
				blnChild = self.make_a_baby(intIndexFather, intIndexMother)

				# Add child to list
				lstNewChildBehaviors.append(Behavior(blnChild))  # This list contains the child behaviors

		else:
			# Selection did not occur.
			#Choose parents from population at random--------------------------------------------------------------

			# Could call CreateNGWithRandomParents here instead, but double check to make sure that it will work correctly with
			# the code in this procedure.  I#m pretty sure it will (2/2014).

			# Note:  it is not necessary to use the Selector object for random parents.
			# HighestInteger and LowestInteger properties of self.m_objRandom were set to 0 and self.get_num_behaviors()-1
			# in the constructor.
			# Get the list of child behaviors
			for _ in range(intNumToReplace2):  # intNumToReplace2 was assigned the correct value
				# 						  when it was dimensioned in this procedure.
				# 						  if intNumToReplace2 = 0 then this For...Next loop with not execute, right?

				# Get indices of father and mother behaviors
				self.m_objSampler.clear()
				intIndexFather = self.m_objRandom.get_rectangular_integer()
				self.m_objSampler.OK(intIndexFather)  # Puts intIndexFather into the list of sampled indices.
				#-----Make sure mother is different from father
				intMotherLoopCounter = 0
				while True:
					intIndexMother = self.m_objRandom.get_rectangular_integer()
					#for testing-----------------------------------------
					# This will definitely not happen here; but I put this test code in here
					# to be obsessively safe.
					intMotherLoopCounter += 1
					if intMotherLoopCounter > 1000:
						raise AssertionError("More than 1000 mother loops for False blnSelection.")
						for objBehavior in self.m_behavior_list:
							print(objBehavior.get_fitness())

					#----------------------------------------------------
					if self.m_objSampler.OK(intIndexMother):
						break
				intMotherLoopCounter = 0

				# Make a baby
				blnChild = self.make_a_baby(intIndexFather, intIndexMother)

				# Add child to list
				lstNewChildBehaviors.append(Behavior(blnChild))  # This list contains the child behaviors

		# Transfer the list of child behaviors to self.m_behavior_list
		if blnSelection:  # (This If...Then added 1/2018)
			if self.get_percent_to_replace() == 100:
				# Transfer all behaviors in lstNewChildBehaviors to self.m_behavior_list
				# This transfer has been tested thoroughly with cloning and works _perfectly_.
				self.m_behavior_list.clear()
				for tempBehavior in lstNewChildBehaviors:
					self.add_behavior(tempBehavior)

			elif self.get_percent_to_replace() > 0:
				# Replace < 100% of the behaviors.
				# Sample indices in self.m_behavior_list randomly without replacement and replace with child behaviors.
				self.m_objSampler.clear()
				for tempBehavior in lstNewChildBehaviors:
					# Find an unused spot to put this behavior
					while True:
						# Probably not necessary to replace random behaviors, but what the heck.
						intIndex = self.m_objRandom.get_rectangular_integer()  # Highest and Lowest integers were previously set to 0 and self.get_num_behaviors()-1
						if self.m_objSampler.OK(intIndex):
							break
					self.set_behavior(intIndex, tempBehavior)

			else:
				pass
				# self.get_percent_to_replace() == 0.  Do nothing.  self.m_behavior_list is not changed.

		else:
			# Selection did not occur, use self.get_percent_to_replace2() (added 1/2018)
			if self.get_percent_to_replace_2() == 100:
				# Transfer all behaviors in lstNewChildBehaviors to self.m_behavior_list
				# This transfer has been tested thoroughly with cloning and works _perfectly_.
				self.m_behavior_list.clear()
				for tempBehavior in lstNewChildBehaviors:
					self.add_behavior(tempBehavior)
			elif self.get_percent_to_replace2() > 0:
				# Replace < 100% of the behaviors.
				# Sample indices in self.m_behavior_list randomly without replacement and replace with child behaviors.
				self.m_objSampler.clear()
				for tempBehavior in lstNewChildBehaviors:
					# Find an unused spot to put this behavior
					while True:
						# Probably not necessary to replace random behaviors, but what the heck.
						intIndex = self.m_objRandom.get_rectangular_integer()  # Highest and Lowest integers were previously set to 0 and self.get_num_behaviors()-1
						if self.m_objSampler.OK(intIndex): break
					self.set_behavior(intIndex, tempBehavior)

			else:
				pass
				# self.get_percent_to_replace() = 0.  Do nothing.  self.m_behavior_list is not changed.

		# Save the population
		if self.get_viscosity_ticks() > 0: self.m_objSavedPops.set_save_population(self.m_behavior_list)

	def create_NG_with_random_parents(self, lstNewChildBehaviors, intNumToReplace):
		# Create a generation from parents chosen at random from the population.  This could be called from CreateNewGeneration. It is not currently used.

		lstNewChildBehaviors.clear()

		#Choose parents at random--------------------------------------------------------------
		# HighestInteger and LowestInteger properties of self.m_objRandom were set to 0 and self.get_num_behaviors()-1
		# in the constructor.
		# Get the list of child behaviors
		for _ in range(1, intNumToReplace + 1):

			# Get indices of father and mother behaviors
			self.m_objSampler.clear()
			intIndexFather = self.m_objRandom.get_rectangular_integer()
			self.m_objSampler.OK(intIndexFather)  # Puts intIndexFather into the list of sampled indices.
			#-----Make sure mother is different from father
			intMotherLoopCounter = 0
			while True:
				intIndexMother = self.m_objRandom.get_rectangular_integer()
				#for testing-----------------------------------------
				# This will definitely not happen here; but I put this test code in here
				# to be obsessively safe.
				intMotherLoopCounter += 1
				if intMotherLoopCounter > 1000:
					raise AssertionError("More than 1000 mother loops for False blnSelection.")
					for objBehavior in self.m_behavior_list:
						print(objBehavior.get_fitness())

				#----------------------------------------------------
				if self.m_objSampler.OK(intIndexMother): break
			intMotherLoopCounter = 0

			# Make a baby
			blnChild = self.make_a_baby(intIndexFather, intIndexMother)

			# Add child to list
			lstNewChildBehaviors.append(Behavior(blnChild))  # This list contains the child behaviors

	def create_ng_with_random_fit_parents(self, lstNewChildBehaviors, intNumToReplace):
		# Create a new generation from random fit parents.  Called by CreateNewGeneration.
		# Note that lstNewChildBehaviors is passed ByRef because it will be changed and used when execution returns to CreateNewGeneration.

		# Draw fitness values at random from the FDF and create the corresponding fit parents.  Recombine to create children
		# and return the list of new child behaviors to CreateNewGeneration to complete the build.

		# This is a bailout option for long dwell times when using Raillard exponential punishment.

		lstNewChildBehaviors.clear()

		for _ in range(1, intNumToReplace + 1):

			# Get father and mother phenotypes, which could be the same
			intFatherFitness = self.m_objSelector.draw_random_fitness()
			intFatherPhenotype = self.get_phenotype_from_fitness(intFatherFitness)
			fatherBehavior = Behavior(intFatherPhenotype)
			fatherBehavior.pad_to(self.m_bitsInHighPhenotype)
			intMotherFitness = self.m_objSelector.draw_random_fitness()
			intMotherPhenotype = self.get_phenotype_from_fitness(intMotherFitness)
			motherBehavior = Behavior(intMotherPhenotype)
			motherBehavior.pad_to(self.m_bitsInHighPhenotype)

			# Make a baby
			if self.use_gray_codes():
				# Gray code bits
				blnChild = self.m_objRecombinator.get_child(fatherBehavior.get_gray_bits(), motherBehavior.get_gray_bits())
				#-----Convert to binary bits
				blnChild = CGrayCodes.gray_to_binary_booleans(blnChild)
			else:
				# Binary bits
				blnChild = self.m_objRecombinator.get_child(fatherBehavior.get_binary_bits(), motherBehavior.get_binary_bits())

			# Add child to list
			lstNewChildBehaviors.append(Behavior(blnChild))  # This list contains the child behaviors

	def get_phenotype_from_fitness(self, intFitness):

		# for now, can be used for Flat fitness landscapes only.  Called by CreateNGWithRandomFitParents.

		coinToss = self.m_objCoinToss.get_rectangular_integer()

		if coinToss == 0:
			# Try below the emitted phenotype first
			intPhenotype = self.m_phenotypeOfEmittedBehavior - intFitness
			if intPhenotype >= self.get_low_phenotype():
				# All is copacetic
				pass
			else:
				# Go above
				intPhenotype = self.m_phenotypeOfEmittedBehavior + intFitness
				# Double check
				if intPhenotype > self.get_high_phenotype(): raise AssertionError("Range problem in CreateNGWithRandomFitParents")

		elif coinToss == 1:
			# Try above the emitted phenotype first
			intPhenotype = self.m_phenotypeOfEmittedBehavior + intFitness
			if intPhenotype <= self.get_high_phenotype():
				# All is copacetic
				pass
			else:
				# Go below
				intPhenotype = self.m_phenotypeOfEmittedBehavior - intFitness
				# Double check
				if intPhenotype < self.get_low_phenotype(): raise AssertionError("Range problem in CreateNGWithRandomFitParents")

		else:
			raise AssertionError("Problems with coin tosser in CreateNGWithRandomFitParents.")

		return intPhenotype

	def make_a_baby(self, intIndexFather, intIndexMother):

		# Called by CreateNewGenration.  Returns a child behavior in binary bits.

		if self.get_use_gray_codes():
			# Gray code bits
			blnChild = self.m_objRecombinator.get_child(self.get_behavior(intIndexFather).get_gray_bits(), self.get_behavior(intIndexMother).get_gray_bits())
			#-----Convert to binary bits
			blnChild = CGrayCodes.gray_to_binary_booleans(blnChild)
		else:
			# Binary bits
			blnChild = self.m_objRecombinator.get_child(self.get_behavior(intIndexFather).get_binary_bits(), self.get_behavior(intIndexMother).get_binary_bits())

		return blnChild

# End Region

	def add_mutation(self):

		# Called by the Selection property

		blnEnableDebug = False  # for testing
		numMutants = 0

		for index in range(len(self.m_behavior_list)):

			# Send each behavior to the Mutator.

			#-------------------------------------------------------------
			if blnEnableDebug: print(self.get_behavior(index).get_integer_value())
			#-------------------------------------------------------------

			integerValuePassed = self.get_behavior(index).get_integer_value()  # Save passed integer.  I think this is necessary only for testing.
			integerValueReturned = self.m_objMutator.get_mutant(integerValuePassed)  # The mutator knows whether to use Gray or binary
			# 																   bits when either of the bitflip mutation methods
			# 																   is used.

			#-----------------------------------------------------------------------
			if blnEnableDebug:
				print(f"{self.get_behavior(index).get_integer_value()} Is this as it was or as it will be?")
				print("+++++++++")
				strToPrint = ""
				for objBehavior in self.m_behavior_list:
					strToPrint += str(objBehavior.IntegerValue) + "   "

				print(strToPrint.ToString)
				print("+++++++++")

			#------------------------------------------------------------------------

			if integerValueReturned != integerValuePassed:
				# This is a mutant and must replace the behavior at this index
				self.set_behavior(index, Behavior(integerValueReturned, self.m_bitsInHighPhenotype))
				self.get_behavior(index).pad_to(self.m_bitsInHighPhenotype)

			#for testing-------------------------------------------------------------
			if integerValueReturned != integerValuePassed:
				# This is a mutant.
				numMutants += 1
				if blnEnableDebug: print("mutate")

			if blnEnableDebug: print(self.get_behavior(index).get_integer_value())  # This will print the mutant.
			#------------------------------------------------------------------------

		#for testing-----------------------------------------------------
		if blnEnableDebug: print(str(numMutants) + " mutants")
		#----------------------------------------------------------------

	def transfer_behaviors(self, lstIntegerPhenotypes):
		# This procedure implements interactions among populations, as might occur, e.g., in multiple schedules.
		# It transfers a proportion of the behaviors from the previous population (SD) to this population.
		# The list, lstIntegerPhenotypes, contains the integer phenotypes from the previous population.

		# The proportion of behaviors transferred decays hyperbolically as a function of the number of generations
		# this condition has been run.

		# As currently written, this procedure assumes that lstIntegerPhenotypes.Count = self.get_num_behaviors(), i.e., that both
		# populations have the same number of behaviors.

		# This procedure requires testing in a multiple schedule.

		objRandom = CRandomNumber()
		objSampler = SampleWoutReplace()

		if len(lstIntegerPhenotypes) != self.get_num_behaviors():
			raise AssertionError("There may be a problem in the population transfer (procedure TransferBehaviors in Behaviors class).")

		dblTransferProportion = 1 / (1 + self.get_decay_of_transfer() * self.get_generations_run())  # Hyperbolic decay
		intNumberToTransfer = int(dblTransferProportion * self.get_num_behaviors())

		if intNumberToTransfer == self.get_num_behaviors():
			# Transfer all phenotypes to this population
			self.m_behavior_list.clear()
			for tempPhenotype in lstIntegerPhenotypes:
				objBehavior = Behavior(tempPhenotype)
				# Pad with leading zeros if necessary
				objBehavior.pad_to(self.m_bitsInHighPhenotype)
				self.add_behavior(objBehavior)

		else:
			# Transfer intNumberToTransfer of the phenotypes to this population.
			# The random number generator will generate random indexes
			objRandom.set_lowest_integer(0)
			objRandom.set_highest_integer(self.get_num_behaviors() - 1)
			for _ in range(1, intNumberToTransfer + 1):
				while True:
					intRandomIndex = objRandom.get_rectangular_integer()
					if not objSampler.OK(intRandomIndex):
						break
				self.set_behavior(intRandomIndex, None)
				objBehavior = Behavior(lstIntegerPhenotypes[intRandomIndex])
				objBehavior.pad_to(self.m_bitsInHighPhenotype)
				self.set_behavior(intRandomIndex, objBehavior)

	def punishment_error_nag(self, paramPunisher):

		# This procedure nags the user if there are problems with the punishment settings.  The tests in the procedure should be incorporated into the
		# laboratory environment to be efficient (not fully implemented in my test laboratory yet).  for example, the procedure is entered every time a punisher
		# is delivered, which is highly inefficient.

		# First check the organism settings to see if they allow for punishment.  These are also checked when the Punishment check check box on the Organism form is checked.
		# To implement punishment, the selection method must be continuous, and the midpoint fitness method cannot be used, but now
		# any of the three continuous function forms can be used, viz., linear, uniform, or exponential.
		if self.m_stuBehaviorsInfo.get_selection_info().get_selection_method() == Constants.SELECTION_METHOD_CONTINUOUS and self.m_stuBehaviorsInfo.get_fitness_method() != Constants.FITNESS_METHOD_MIDPOINT:
			# OK for punishment
			pass
		else:
			raise AssertionError("Your organism settings do not permit the use of punishment:\n\n	 1.  Continuous Selection must be used.\n	 2.  The Midpoint Fitness Method cannot be used.\nIf #1 is violated your experiment will soon crash.  If #2 is violated you will get bogus results.")
			# Exit Property

		# Also check that the punishment mean meets the test condition.  The test conditions are calculated in "9.  Notebook on Punishment", pp. 13ff.

		intXSubM = 0
		if self.get_fitness_landscape() == Constants.FITNESS_LANDSCAPE_FLAT:
			intXSubM = self.get_high_phenotype()
		elif self.get_fitness_landscape() == Constants.FITNESS_LANDSCAPE_CIRCULAR:
			intXSubM = (self.get_high_phenotype() - 1) / 2

		if self.m_objSelector.get_continuous_function_form() == Constants.CONTINUOUS_FUNCTION_FORM_UNIFORM:
			if 2 * abs(paramPunisher) - intXSubM < 0:
				raise AssertionError("Your punishment mean is too small. It will permit negative fitness values.")
				# Exit Property

		elif self.m_objSelector.get_continuous_function_form() == Constants.CONTINUOUS_FUNCTION_FORM_LINEAR:
			if 3 * abs(paramPunisher) - 2 * intXSubM < 0:
				raise AssertionError("Your punishment mean is too small. It will permit negative fitness values.")
					# Exit Property

		elif self.m_objSelector.get_continuous_function_form() == Constants.CONTINUOUS_FUNCTION_FORM_EXPONENTIAL:
			pass
				# Not relevant

# Region " Collection utilities"

	def populate_with_random_behaviors(self):
		# Fills this population with self.get_num_behaviors() from self.get_low_phenotype() to self.get_high_phenotype().

		self.m_behavior_list.clear()
		self.m_objRandom.set_highest_integer(self.get_high_phenotype())
		self.m_objRandom.set_lowest_integer(self.get_low_phenotype())

		for _ in range(self.get_num_behaviors()):
			objBehavior = Behavior(self.m_objRandom.get_rectangular_integer(), self.m_bitsInHighPhenotype)
			# Pad with leading zeros if necessary
			objBehavior.pad_to(self.m_bitsInHighPhenotype)
			self.add_behavior(objBehavior)

	def add_behavior(self, newBehavior):
		self.m_behavior_list.append(newBehavior)

	def remove_behavior(self, oldBehavior):
		self.m_behavior_list.remove(oldBehavior)

	def remove_behavior_at(self, index):
		del self.m_behavior_list[index]

	def clear_population(self):
		self.m_behavior_list.clear()
		self.set_sdid(0)
		self.set_use_gray_codes(False)
		self.set_low_phenotype(0)
		self.set_high_phenotype(0)
		self.set_num_behaviors(0)
		self.set_percent_to_replace(0)
		self.set_fitness_method(0)
		self.set_fitness_landscape(0)
		self.m_readyForNextEmission = True  # Default value upon class instantiation.
		self.m_blnSelection = False  # Default value upon class instantiation.
		self.m_objRW.clear_associative_strengths()

	def reset_population(self):
		# This procedure is called to start over after FitParentException is thrown.
		self.populate_with_random_behaviors()
		self.set_ready_to_emit(True)
		self.m_objRW.clear_associative_strengths()
		# Reset self.m_objRandom to emit behaviors at random
		self.m_objRandom.set_lowest_integer(0)
		self.m_objRandom.set_highest_integer(self.get_num_behaviors() - 1)

