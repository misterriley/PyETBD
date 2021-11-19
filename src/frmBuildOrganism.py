'''
Created on May 24, 2021
Translated May 24, 2021

@author: bleem
'''

from AnOrganism import AnOrganism
from Behaviors import Behaviors
from BehaviorsInfo import BehaviorsInfo
from MutationInfo import MutationInfo
from RecombinationInfo import RecombinationInfo
from RescorlaWagnerParameters import RescorlaWagnerParameters
from SampleWoutReplace import SampleWoutReplace
from SelectionInfo import SelectionInfo
import Constants


class frmBuildOrganism(object):
    '''
    classdocs
    '''

    def __init__(self):
        self.m_objOrganism = AnOrganism()
        self.m_intPopulationIndex = None

        self.m_objSampler = SampleWoutReplace()

        self.m_blnExists = None  # Added 10/2017 for error handling

    def exists(self):
        return self.m_blnExists

    def set_exists(self, value):
        self.m_blnExists = value

    def get_creature(self):  # Changed from Public Property to Shared property 10/2017 to make this work with 4.0
        #                                               Changed it back!

        # Envisioned usage:  This form will be part of an MDI application and will be used only to build an
        # organism.  The laboratory part of the form will not be used (although it could be used for testing,
        # etc., or it could be removed altogether).  The user will set all the organism properties on the right
        # hand side of the form by clicking the "Create this population" button for each population (and discriminative
        # stimulus).  This will load up self.m_objOrganism with the desired populations of potential behaviors.

        # Actual experiments will be run by other code.  For example, there might be a schedule form (single,
        # concurrent, chained schedules, with parameters), and an experiment layout and data storage form, and perhaps
        # a data analysis form.  This additional code will access the built organism through the Creature property
        # (this property) of the frmBuildOrganism class (form).  The syntax might be something like this:
        #       Dim myOrganism as New AnOrganism
        #       myOrganism = frmBuildOrganism.Creature
        # The additional code that actually runs the experiments will have no other contact with this form.

        # In normal operation, the experiment-running code will have only three points of contact with the built organism,
        # let's say, myOrganism.  (The following three points are applicable to Version 3.0.  Version 3.1 implements a simpler method
        # of interacting with the built organism.  See the Guide for an explanation.  The Version 3.0 functionality described below is
        # fully retained in Version 3.1.)
        # 1. The correct population in myOrganism is accessed by "turning on the discriminative stimulus" with
        #   syntax like myOrganism.Item(indexOfDiscriminativeStimulus).  The Item returned by this statement is the
        #   population of potential behaviors associated with that discriminative stimulus.
        # 2. Each time tick the population must be queried for a behavioral emssion (as in DoARun below):
        #         emittedBehaviorAsInteger = myOrganism.Item(indexOfDiscriminativeStimulus).EmitBehavior.IntegerValue
        # 3. After the emitted behavior is obtained, the experiment-running code will communicate to myOrganism whether
        #   the behavior is reinforced by setting its Selection property (as in DoARun below).  There are two syntax versions
        #   for doing this:
        #         myOrganism.Item(indexOfDiscriminativeStimulus).Selection(selectionParameter, intMidpoint) = True (if reinforced)/False (if not reinforced).
        #         myOrganism.Item(indexOfDiscriminativeStimulus).Selection(selectionParameter) = True/False
        #   The first syntax is required if midpoint fitness is being used, in which case intMidpoint is the midpoint of
        #   the target class to which the emitted behavior belongs (which, as the code is currently written, must be an integer).
        #   The second syntax can be used for all other fitness methods.  If the first syntax is used for the other fitness
        #   methods, then the passed value of intMidpoint is ignored.  In both cases, the selectionParameter must be passed to the
        #   Selection property.  This is the mean of the parental choosing function for the continuous selection method, the proportion
        #   of the population to be discarded for the truncation selection method, and the number of competitors for the tournament
        #   selection method.

        # That's it.  Each generation, the organism must be queried for an emitted behavior, and then told whether or not that
        # behavior is reinforced.  The organism code does all the rest.

        # A different approach is to load the populations in myOrganism into separate Behaviors classes:
        #       Dim whitePopulation as New Behaviors
        #       Dim redPopulation as New Behaviors
        #       Dim greenPopulation as New Behaviors
        #
        #       whitePopulation = myOrganism.Item(indexOfWhiteSD)
        #       redPopulation = myOrganism.Item(indexOfRedSD)
        #       greenPopulation = myOrganism.Item(indexOfGreenSD)
        # Then the emission and reinforcement statements are executed for whichever discriminative stimulus is in effect, say the
        # white one:
        #       emittedBehaviorAsInteger = whitePopulation.EmitBehavior.IntegerValue
        #       whitePopulation.Selection(selectionParameter, intMidpoint) = True or False

        # Although in normal operation these are the only points of contact between the laboratory code and myOrganism, in fact
        # all the properties of all populations are available to the laboratory code from the myOrganism object via the read-only
        # BehaviorsInfo property of each Behaviors class.

        # Finally, note how kickout is handled in the Try...Catch block in DoARun (see "Defunct procedures no longer used" region).
        # Some form of this must be implemented in the laboratory code.  Kickout occurs if there is a problem getting enough distinct
        # fit behaviors to reproduce.  The code in DoARun shows how the population is restarted from a random state, but the laboratory
        # code must also discard all the data collected up to that point and start over again.  This is the way the old code works,
        # although we can discuss ways of handling this differently by, for example, permitting cloning or "next best" parents in the event
        # of insufficient numbers of fit parents.

        return self.m_objOrganism

    def create_a_population(self, json_data):  # Handles btnDifferent.Click

        # An organism object is instantiated when this form is loaded.

        stuBehaviorsInfo = BehaviorsInfo()
        # Dim objPopulation As Behaviors
        # Dim objStringBuilder As New System.Text.StringBuilder

        self.set_exists(True)  # Added for error handling 10/2017

        # Verify punishment settings if necessary
        if json_data.check_is_punishment_ok():
            if not self.verify_settings_for_punishment():
                return
        else:
            pass
            # No problemo

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

        # Create and populate population of potential behaviors
        objPopulation = Behaviors(stuBehaviorsInfo)

        # Add population to organism
        self.m_objOrganism.add(objPopulation)

# Region " Loaders"

    def load_RW_info(self, json_data):

        stuRWInfo = RescorlaWagnerParameters()

        stuRWInfo.set_alpha(json_data.get_alpha())
        stuRWInfo.set_beta_0(json_data.get_beta_0())
        stuRWInfo.set_beta_1(json_data.get_beta_1())
        stuRWInfo.set_berg_a(1)  # Hard coded to 1 for now.
        stuRWInfo.set_lambda(1)  # Hard coded to 1 for now.

        return stuRWInfo

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

    def verify_settings_for_punishment(self, json_data):
        # Must use continuous exponential selection, and cannot use midpoint fitness method.
        # if cboSelectionMethod.SelectedIndex = 2 And cboContinuousFunctionForm.SelectedIndex = 3 And not cboFitnessMethod.SelectedIndex = 0:
        if json_data.get_selection_method() == Constants.SELECTION_METHOD_TOURNAMENT and json_data.get_fitness_method() != Constants.FITNESS_METHOD_MIDPOINT :
            # All is copacetic.
            return True
        else:
            # All is not copacetic.
            raise AssertionError("For punishment:\n\n     1.  The Continuous Selection Method must be used.\n     2.  The Midpoint Fitness Method cannot be used.\n\nClose this window and make the appropriate selections.")
            return False
