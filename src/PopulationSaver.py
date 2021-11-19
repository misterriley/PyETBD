'''
Created on May 22, 2021
Translated May 24, 2021

@author: bleem
'''
from CProbEmitter import CProbEmitter
from CRandomNumber import CRandomNumber


class PopulationSaver(object):
    '''
    classdocs
    '''

    def __init__(self, lowPhenotype, highPhenotype, numBehaviors, intViscosityTicks, blnCreateFromSynthetic):
        '''
        Constructor
        '''
        self.m_populations = []

        # This class saves populations as lists of integer phenotypes. All populations are assumed
        # to have the same number of phenotypes (as would normally be the case for repeated generations of the same population).
        # As currently written, this class also assumes that all phenotype ranges begin at zero.

        self.m_intViscosityTicks, self.m_intNumBehaviors = None
        self.m_lowPhenotype, self.m_highPhenotype = None
        self.m_objRandom = CRandomNumber()
        self.m_lstSyntheticPhenotypes = list()
        self.m_objProbEmitter = CProbEmitter()
        self.m_blnStop = None  # For testing
        self.m_blnCreateFromSynthetic = None

        if lowPhenotype != 0:
            raise AssertionError("To use the PopulationSaver object, the lowest phenotype must be zero.")  # Could surely avoid this limitation if it seemed valuable to do so.
            return

        self.m_lowPhenotype = lowPhenotype
        self.m_highPhenotype = highPhenotype
        self.m_intNumBehaviors = numBehaviors
        self.set_viscosity_ticks(intViscosityTicks)
        self.m_blnCreateFromSynthetic = blnCreateFromSynthetic

        # Set random number generator used to emit behaviors from amalgamated population
        self.m_objRandom.set_lowest_integer(0)
        self.m_objRandom.set_highest_integer(self.m_intNumBehaviors - 1)

    def get_viscosity_ticks(self):
        return self.m_intViscosityTicks

    def set_viscosity_ticks(self, value):
            self.m_intViscosityTicks = value

    def get_num_behaviors(self):
        return self.m_intNumBehaviors

    def set_num_behaviors(self, value):
        self.m_intNumBehaviors = value

    def set_save_population(self, value):

        lstPhenotypes = list()

        for tempBehavior in value:
            lstPhenotypes.append(tempBehavior.get_integer_value())

        if self.get_population_count() == self.get_viscosity_ticks():
            # Remove the first list (zeroth Item) before adding the new one.
            self.remove_population_at(0)

        self.add_population(lstPhenotypes)

        # #For testing
        # for tempInteger in lstPhenotypes
        #    Debug.Print(tempInteger.ToString)
        #
        # Debug.Print("")

    def emit_phenotype(self):

        # Emits a phenotype from the viscious (combined, amalgamated) population
        # This seems to be working correctly.

        # i, j, numPhenotypes= None
        phenotypeCount = [0] * (self.m_highPhenotype - self.m_lowPhenotype)
        phenotypeProb = [0.0] * (self.m_highPhenotype - self.m_lowPhenotype)
        # randomDecimal As Double
        # syntheticPhenotypeCount(self.m_highPhenotype - self.m_lowPhenotype)= None
        totalSyntheticPhenotypes = 0
        # blnGotThemAll = None
        # objRandom As New CRandomNumber #For building synthetic population
        # intPhenotypeIndex= None

        # Calculate the total number of phenotypes across the saved populations
        numPhenotypes = self.get_num_behaviors() * self.get_population_count()

        # Tally the phenotypes across lists (populations)
        for lstPhenotypes in self.m_populations:
            for i in range(len(lstPhenotypes)):
                phenotypeCount[lstPhenotypes[i]] += 1

        # Calculate the relative frequencies of the phenotypes
        for i in range(len(phenotypeCount)):
            phenotypeProb[i] = phenotypeCount[i] / numPhenotypes

        if self.m_blnCreateFromSynthetic:
            # Prepare synthetic population of phenotypes---this appears to not be working correctly
            # Inspect the list of synthetic phenotypes to see what is going on.
            self.m_lstSyntheticPhenotypes.clear()

            while True:
                for i in range(len(phenotypeProb)):
                    if phenotypeProb[i] > 0:
                        self.m_objProbEmitter.set_prob_of_emission(phenotypeProb[i])
                        if self.m_objProbEmitter.get_emission():
                            # Add this phenotype to the synthetic population
                            self.m_lstSyntheticPhenotypes.append(i)
                            totalSyntheticPhenotypes += 1

                        if totalSyntheticPhenotypes == self.get_num_behaviors():
                            blnGotThemAll = True
                            break

                if blnGotThemAll:
                    break

            # #for testing
            # #----Individual populations
            # for j = 0 To self.get_population_count() - 1
            #    for i = 0 To self.m_intNumBehaviors - 1
            #        Debug.Print(Item(j).Item(i).ToString)
            #
            #    Debug.Print("")
            #
            # #----Amalgamated population
            # for i = 0 To self.m_lstSyntheticPhenotypes.Count - 1
            #    Debug.Print(self.m_lstSyntheticPhenotypes.Item(i).ToString)
            #
            # Debug.Print("+++++++++++++")
            # Debug.Print("")
            # Stop

            # objRandom.set_lowest_integer( self.m_lowPhenotype
            # objRandom.set_highest_integer(self.m_highPhenotype
            # while True:
            #    intPhenotypeIndex = objRandom.get_rectangular_integer()
            #    if phenotypeProb(intPhenotypeIndex) > 0:
            #        self.m_objProbEmitter.set_prob_of_emission(phenotypeProb(intPhenotypeIndex)
            #        if self.m_objProbEmitter.get_emission():
            #            #Add this phenotype to the synthetic population
            #            self.m_lstSyntheticPhenotypes.append(intPhenotypeIndex)
            #            totalSyntheticPhenotypes += 1
            #
            #        if totalSyntheticPhenotypes = self.get_num_behaviors():
            #            blnGotThemAll = True
            #            #Exit Do
            #
            #
            #    if blnGotThemAll

            if totalSyntheticPhenotypes != self.get_num_behaviors(): raise AssertionError("not equal")

            # Alternatively, now that I have a list of synthetic phenotypes, I could just emit one
            # of these at random.

            return self.m_lstSyntheticPhenotypes[self.m_objRandom.get_rectangular_integer()]

        else:

            # Cumulate relative frequencies
            for i in range(1, len(phenotypeProb)):
                phenotypeProb[i] += phenotypeProb[i - 1]

            # Emit a behavior from the viscous population
            randomDecimal = self.m_objRandom.get_rectangular_decimal()
            for i in range(0, len(phenotypeProb)):
                if randomDecimal <= phenotypeProb[i]:
                    break

            return i

    def get_synthetic_phenotypes(self):
        return self.m_lstSyntheticPhenotypes

    def get_population(self, index):
        return self.m_populations[index]

    def set_population(self, index, value):
        self.m_populations[index] = value

    def add_population(self, newPopulation):
        self.m_populations.append(newPopulation)

    def remove_population(self, oldPopulation):
        self.m_populations.remove(oldPopulation)
