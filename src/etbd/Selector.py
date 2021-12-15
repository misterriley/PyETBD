'''
Created on May 22, 2021
Translated May 24, 2021

@author: bleem
'''

import math

from src.common import Constants
from src.common.CRandomNumber import CRandomNumber
from src.common.SampleWoutReplace import SampleWoutReplace


class Selector(object):
    '''
    classdocs
    '''

    def __init__(self, stuSelectionProperties):
        '''
        Constructor
        '''
        self.m_truncationProportion = None  # Selection parameter, must be set with every selection event
        self.m_tournamentCompetitors = None  # Selection parameter, must be set with every selection event
        self.m_continuousMean = None  # Selection parameter, must be set with every selection event

        self.m_selectionMethod = None
        self.m_continuousFunctionForm = None
        self.m_highPhenotype = None  # Added (spring 2012) to implement punishment
        self.m_lowPhenotype = None  # Added (spring 2012) to implement punishment
        self.m_fitnessLandscape = None  # Added (spring 2012) to implement punishment
        self.m_justEmittedPhenotype = None  # Added (spring 2012) to implement normalized exponential FDF over a flat fitness landscape
        self.m_matchmakingMethod = None

        # The following are for truncation selection and tournament selection
        self.m_truncationProportionJustSet = None  # Flag for truncation selection.
        self.m_tournamentCometitorsJustSet = None  # Flag for tournament selection.
        self.m_listOfFitnesses = []  # x = fitness, y = index of behavior from population with that fitness

        # #For speeding up exponential punishment.  THIS DOES NOT PRODUCE SUBSTANTIAL REDUCTIONS IN DWELL TIMES FOR THE EXPONENTIAL.
        # self.m_intSmallestsNonZeroFitness, self.m_intLargestFitness = None

        #------------------------------------------

        self.m_objRandom = CRandomNumber()  # Nothing needs to be set for Continuous selection method (.get_rectangular_decimal()
        #                                          property used in DrawRandomFitness)
        #                                          For Truncation selection set lowest and highest integer in first pass through
        #                                          GetParentIndex function.
        #                                          For Tournament selection set lowest and highest integer in first pass through
        #                                          GetParentIndex function.

        # Set properties of the Selector
        self.set_selection_method(stuSelectionProperties.get_selection_method())
        self.set_continuous_function_form(stuSelectionProperties.get_continuous_function_form())  # Used only if selection method is Continuous
        self.set_high_phenotype(stuSelectionProperties.get_high_phenotype())
        self.set_low_phenotype(stuSelectionProperties.get_low_phenotype())
        self.set_fitness_landscape(stuSelectionProperties.get_fitness_landscape())
        self.set_matchmaking_method(stuSelectionProperties.get_matchmaking_method())

    def set_generic_selection_parameter(self, value):

        if self.get_selection_method() == Constants.SELECTION_METHOD_CONTINUOUS:
            # self.set_truncation_proportion(0)
            # self.set_tournament_competitors(0)
            #For testing punishment----------------------------------------------------------------------
            # self.set_continuous_mean(-value)
            #--------------------------------------------------------------------------------------------
            self.set_continuous_mean(value)
        elif self.get_selection_method() == Constants.SELECTION_METHOD_TOURNAMENT:
            # self.set_truncation_proportion(0)
            self.set_tournament_competitors(int(value))
            # self.set_continuous_mean(0)
        elif self.get_selection_method() == Constants.SELECTION_METHOD_TRUNCATION:
            self.set_truncation_proportion(value)
            # self.set_tournament_competitors(0)
            # self.set_continuous_mean(0)
        else:
            raise AssertionError("Problem in GenericSelectionParameter procedure in Selector.vb")

        # Proportion of population to discard (based on fitness).  Parents are chosen at random from the behaviors
        # that remain.
        # May be set only when there is a selection event.
    def get_truncation_proportion(self):
            return self.m_truncationProportion

    def set_truncation_proportion(self, value):
        self.m_truncationProportion = value
        # Set a flag here to indicate that this property was just set, which means that when the
        # first parent is requested, the population must be ordered by fitness and stored.  It must be
        # done this way because the population is not passed to this property, but rather to the GetParentIndex
        # function.  Hence, the ordered list of fitnesses cannot be prepared here.
        self.m_truncationProportionJustSet = True
        self.m_listOfFitnesses = None

    # Number of competitors to draw for tournaments
    # May be set only when there is a selection event.
    def get_tournament_competitors(self):
        return self.m_tournamentCompetitors

    def set_tournament_competitors(self, value):
        self.m_tournamentCompetitors = value
        # Set flag to indicate that this property was just set.  Need the passed population in GetParentIndex to get
        # the number of behaviors in the population; this is needed to set the lowest and highest integers of the random
        # number generator.
        self.m_tournamentCometitorsJustSet = True
        self.m_listOfFitnesses = None

    # Mean of the parental choosing function
    # May be set only when there is a selection event.
    def get_continuous_mean(self):
        return self.m_continuousMean

    def set_continuous_mean(self, value):
        self.m_continuousMean = value

    def get_selection_method(self):
        return self.m_selectionMethod

    def set_selection_method(self, value):
        self.m_selectionMethod = value

    # Used only if selection method is Continuous
    def get_continuous_function_form(self):
        return self.m_continuousFunctionForm

    def set_continuous_function_form(self, value):
        self.m_continuousFunctionForm = value

    def get_high_phenotype(self):
        return self.m_highPhenotype

    def set_high_phenotype(self, value):
        self.m_highPhenotype = value

    def get_low_phenotype(self):
        return self.m_lowPhenotype

    def set_low_phenotype(self, value):
        self.m_lowPhenotype = value

    def get_fitness_landscape(self):
        return self.m_fitnessLandscape

    def set_fitness_landscape(self, value):
        self.m_fitnessLandscape = value

# Property SmallestNonZeroFitness #Added (Winter 2014) to speed up Raillard punishment. Set in Behavior.AssignFlatFitnessValues
#    def get_(self):
#        return self.m_intSmallestsNonZeroFitness
#
#    def set_(self, value):(value)
#        self.m_intSmallestsNonZeroFitness = value
#
#

# Property LargestFitness #Added (Winter 2014) to speed up Raillard punishment. Set in Behavior.AssignFlatFitnessValues
#    def get_(self):
#        return self.m_intLargestFitness
#
#    def set_(self, value):(value)
#        self.m_intLargestFitness = value
#
#

    def get_just_emitted_phenotype(self):
        return self.m_justEmittedPhenotype

    def set_just_emitted_phenotype(self, value):
        self.m_justEmittedPhenotype = value

    def get_matchmaking_method(self):
        return self.m_matchmakingMethod

    def set_matchmaking_method(self, value):
        self.m_matchmakingMethod = value

    def get_parent_index(self, lstPopulation, FatherIndex = -1):

        # returns the index of a parent, drawn on the basis of its fitness.

        #-----The "FatherIndex..." argument is part of Nick#s solution to the mother loop problem, as is
        #-----the "And FatherIndex != itemCounter" clause below, as is the change noted in the CreateNewGeneration procedure
        #-----of Behaviors.vb.  See info in C:\Users\Jack\Documents\Projects\Research\New Computational Laboratory\From Nick
        #-----for more info.

        # Dim targetFitness, indexToReturn, itemCounter, timesThroughLoop, objBehavior As Behavior
        gotOne = False  # Tells whether a behavior with the target fitness was found.
        objSampler = SampleWoutReplace()
        # Dim blnInRange As Boolean # Tells whether a draw fitness value falls within the range of fitnesses that exist in the population

        if self.get_matchmaking_method() == Constants.MATCHMAKING_METHOD_SEARCH:
            if self.get_selection_method() == Constants.SELECTION_METHOD_CONTINUOUS:
                # 1.  Draw a fitness value at random from the appropriate density function.
                # 2.  Find an individual with that fitness and return its index.
                # 3.  Repeat 1 and 2 as necessary.
                # timesThroughLoop = 0  # Probably not necessary to initialize this here.
                # Draw a random fitness value
                while True:
                    # #in the case of the exponential, make sure the targetFitness falls in the range of fitnesses that exist in the population.
                    # #This should speed things up for the exponential.  DOES NOT PRODUCE SUBSTANTIAL IMPROVEMENT (2.2014)<<<<<<<<<<<<<<<<<<<<<<
                    # if self.get_continuous_function_form() = ContinuousFunctionForm.Exponential:
                    #    #Make sure targetFitness falls in the range of fitnesses that exist in the population
                    #    blnInRange = False
                    #    Select Case self.get_continuous_mean() # Not sure this is assigned in the case of Raillard punishment (I believe it is.)
                    #        Case Is < 0
                    #            #Punishment
                    #            #raise AssertionError("in there.")
                    #            while True:
                    #                targetFitness = self.draw_random_fitness()
                    #                if targetFitness <= LargestFitness: blnInRange = True
                    #                if  blnInRange = True
                    #        Case Is > 0
                    #            #Reinforcement
                    #            while True:
                    #                targetFitness = self.draw_random_fitness()
                    #                if targetFitness = 0 Or targetFitness >= SmallestNonZeroFitness: blnInRange = True
                    #                if blnInRange = True
                    #        Case else:
                    #            raise AssertionError("Problem in GetParentIndex targetFitness test.")
                    #
                    # Else
                    targetFitness = self.draw_random_fitness()
                    #
                    ##******************************************************************************************
                    # #This (above) is where, in the case of Raillard punishment, the drawn target fitness can be tested
                    # #to determine whether it falls in the range of fitnesses that exist in the population.
                    # #If it does not, then don#t bother searching for a behavior with that fitness; instead draw a new
                    # #target fitness.  Minimum and maximum fitnesses must be passed to the Selector in order to
                    # #accomplish this.  This might also be useful for preventing the occasional long dwell times
                    # #that occur with strong exponential reinforcement.
                    ##******************************************************************************************
                    # Look for a behavior with targetFitness
                    itemCounter = 0
                    for objBehavior in lstPopulation:
                        if objBehavior.get_fitness() == targetFitness and FatherIndex != itemCounter:
                            gotOne = True
                            indexToReturn = itemCounter
                            break

                        itemCounter += 1

                    # #**********************************************************************************************************For testing 2/2014
                    # #This If...Then block enables bailout from a long dwell time.  It can be entered only when using the
                    # #exponential FDF.  It shouldn#t be necessary for the other FDF forms (famous last words).
                    # #The actual bailout occurs in Behaviors.CreateNewGeneration.
                    # if (Not gotOne) and self.get_continuous_function_form() = ContinuousFunctionForm.Exponential:
                    #    timesThroughLoop += 1
                    #    if timesThroughLoop = 100000:
                    #        #raise AssertionError("1,000 times through loop")
                    #        #Debug.Print("##########")
                    #        #for objBehavior in lstPopulation
                    #        #    Debug.Print(objBehavior.get_fitness().ToString)
                    #        #
                    #        #Turns out that most behaviors are near the target class, and hence have small fitness values.
                    #        #Only a few have large fitness values which are favored in the event of punishment.
                    #        #Stop
                    #        timesThroughLoop = 0
                    #        indexToReturn = -999 #  Bail out
                    #        gotOne = True
                    #
                    #
                    ##***********************************************************************************************************
                    if gotOne:
                        break
                return indexToReturn
            elif self.get_selection_method() == Constants.SELECTION_METHOD_TOURNAMENT:
                # This code seems to be working fine.  But if serious experiments with this selection method
                # are to be run, then the code must be double checked.
                # Draw TournamentCompetitors at random and return the index of the fittest.
                # if this is the first parent index requested for the new generation then set the limits of the random
                # number generator.
                if self.m_tournamentCometitorsJustSet:
                    self.m_objRandom.set_lowest_integer(0)  # Lowest index
                    self.m_objRandom.set_highest_integer(len(lstPopulation) - 1)  # Highest index
                    self.m_tournamentCometitorsJustSet = False

                # Make a list of competitors
                self.m_listOfFitnesses = [(0, 0)] * self.get_tournament_competitors()
                for i in range(self.get_tournament_competitors()):
                    # Have to ensure that an index is selected only once.
                    while True:
                        indexToReturn = self.m_objRandom.get_rectangular_integer()
                        if objSampler.OK(indexToReturn):
                            break
                    objBehavior = lstPopulation[indexToReturn]
                    self.m_listOfFitnesses[i] = objBehavior.get_fitness(), indexToReturn

                # Sort the list
                list.sort(self.m_listOfFitnesses)
                # Return the index of the fittest competitor
                return int(self.m_listOfFitnesses[0][1])
            elif self.get_selection_method() == Constants.SELECTION_METHOD_TRUNCATION:
                # 1.  Prepare a list of behavior indexes ordered by fitness.  Prepare this list the first time
                #    a parent index is requested following a reinforcement (self.m_truncationProportionJustSet = True),
                #    and then use this list to pick the remaining parent indexes for the new population.
                # 2.  Pick one index at random within the fitness limits specified by the truncation proportion, and return it.
                if self.m_truncationProportionJustSet:
                    # This is the first parent index requested for the new generation.
                    # Prepare a list of indexes ordered by fitness.
                    # (Must do this here instead of when the TruncationProportion property is set because
                    # this procedure receives the population.)
                    self.m_listOfFitnesses = [(0, 0)] * len(lstPopulation)
                    intCounter = 0
                    for tempBehavior in lstPopulation:
                        # Both the population collection and the self.m_listOfFitnesses array are zero based
                        self.m_listOfFitnesses[intCounter] = (tempBehavior.get_fitness(), intCounter)
                        intCounter += 1

                    ##For testing------------------------------------------------------------
                    # Dim intTestCounter = 0
                    # for tempBehavior As Behavior in lstPopulation
                    #    Debug.Print(tempBehavior.IntegerValue.ToString & "     " & tempBehavior.get_fitness().ToString & "     " & intTestCounter.ToString)
                    #    intTestCounter += 1
                    #
                    # Debug.Print("")
                    ##-----------------------------------------------------------------------

                    # Sort the list
                    list.sort(self.m_listOfFitnesses)
                    # self.m_listOfFitnesses is now sorted by fitness.  The y member is the index of the
                    # behavior in the original population, with the fitness given by the x member.

                    ##For testing------------------------------------------------------------
                    # Dim behaviorItem As Behavior
                    # for tempCoordinate As Coordinates in self.m_listOfFitnesses
                    #    behaviorItem = CType(lstPopulation.Item(int(tempCoordinate.y)), Behavior)
                    #    Debug.Print(tempCoordinate.x.ToString & "     " & behaviorItem.IntegerValue.ToString)
                    #
                    # Stop
                    ##-----------------------------------------------------------------------
                    # #...

                    # Initialize random number generator
                    self.m_objRandom.set_lowest_integer(0)
                    self.m_objRandom.set_highest_integer(int((1 - self.get_truncation_proportion()) * len(lstPopulation) - 1))

                    self.m_truncationProportionJustSet = False

                # Have a list of indexes in order of fitness.  Draw one at random within the permitted range and return it.
                return int(self.m_listOfFitnesses(self.m_objRandom.get_rectangular_integer())[1])

        if self.get_matchmaking_method() == Constants.MATCHMAKING_METHOD_MATING_POOL:
            # Not yet implemented
            raise AssertionError("The mating pool matchmaking method has not yet been implemented.")
        else:
            raise AssertionError("Problem in GetParent procedure of Selector.")

    def draw_random_fitness(self):

        # Called by GetParentIndex when the Continuous selection method is used.

        # These formulas are taken from the previous version of the code.  They were worked out in my Single Selection
        # notebook, starting around p. 116.  The exponential starts on p.108.  The 0.5 added to the fitness value
        # and the 1 subtracted from the integer rounding are discussed on p. 149 in my Single Selection notebook.  These
        # modifications bear on the issue of integer fitness values.  I don#t know what affect they have on non-integer
        # fitness values.

        # Dim maxFitness, intToLow, intToHigh, holdRandom As Double

        # Calculate the maximum fitness value

        if self.get_fitness_landscape() == Constants.FITNESS_LANDSCAPE_FLAT:
            intToLow = abs(self.get_just_emitted_phenotype() - self.get_low_phenotype())
            intToHigh = abs(self.get_high_phenotype() - self.get_just_emitted_phenotype())
            if intToHigh >= intToLow:
                maxFitness = intToHigh
            else:
                maxFitness = intToLow
        elif self.get_fitness_landscape() == Constants.FITNESS_LANDSCAPE_CIRCULAR:
            maxFitness = int((self.get_high_phenotype() + 1) / 2 - 1)  # Maximum fitness is half the phenotype range.  This is absolutely correct!  Do not fret about it any further!!
        else:
            raise AssertionError("Trouble in paradise.  Selector:DrawRandomFitness")

        # Return a random fitness value from the appropriate FDF.  Don#t forget that self.get_continuous_mean() is negative in the case of punishment.
        if self.get_continuous_function_form() == Constants.CONTINUOUS_FUNCTION_FORM_LINEAR:
            if self.get_continuous_mean() > 0:
                # Use the reinforcement density function.

                # get_rectangular_decimal() generates a uniform decimal from 0 to 1. +.5 - 1 leads to rounding to the nearest integer rather than rounding down. The 3 * gives
                # a regularization. So, this line of code generates a random deviate from a triangular distribution, then rounds to the nearest integer.
                return int(3 * self.get_continuous_mean() * (1 - math.sqrt(1 - self.m_objRandom.get_rectangular_decimal())) + 0.5) - 1
            elif self.get_continuous_mean() < 0:
                # Use the punishment density function. (Worked out on p. 14 of "9. Notebook on Punishment").
                return int(3 * abs(self.get_continuous_mean()) - 2 * maxFitness + 3 * (maxFitness - abs(self.get_continuous_mean())) * math.sqrt(self.m_objRandom.get_rectangular_decimal()) + 0.5) - 1

        elif self.get_continuous_function_form() == Constants.CONTINUOUS_FUNCTION_FORM_EXPONENTIAL:
            # Return int(-self.get_continuous_mean() * Math.Log(1 - self.m_objRandom.get_rectangular_decimal()) + 0.5) - 1 # <- This is the non-normalized version.
            # The following line is worked out in my "Notebook on General Matters", pp. 47ff.
            # Return int(-self.get_continuous_mean() * Math.Log(self.m_objRandom.get_rectangular_decimal() * (Math.Exp(-(1 / self.get_continuous_mean()) * self.get_high_phenotype()) - 1) + 1) + 0.5) - 1
            return int(-1 * self.get_continuous_mean() * math.log(self.m_objRandom.get_rectangular_decimal() * (math.exp(-(1 / self.get_continuous_mean()) * maxFitness) - 1) + 1) + 0.5) - 1
        elif self.get_continuous_function_form() == Constants.CONTINUOUS_FUNCTION_FORM_UNIFORM:
            if self.get_continuous_mean() > 0:
                # Use the reinforcement density function.
                return int(2 * self.get_continuous_mean() * self.m_objRandom.get_rectangular_decimal() + 0.5) - 1
            elif self.get_continuous_mean() < 0:
                # Use the punishment density function.
                holdRandom = self.m_objRandom.get_rectangular_decimal()
                return int(maxFitness * holdRandom + (2 * abs(self.get_continuous_mean()) - maxFitness) * (1 - holdRandom) + 0.5) - 1
            else:
                raise AssertionError("Trouble in Selector:DrawRandomFitness")
