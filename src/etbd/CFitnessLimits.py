'''
Created on May 22, 2021
Translated May 23, 2021

@author: bleem
'''
from src.common import Constants


class CFitnessLimits(object):
    '''
    classdocs
    '''

    # Calculates maximum and minimum fitness values for reinforcement and punishment when using uniform and linear FDFs (not necessary for exponential FDFs)

    def __init__(self, ContinuousFunctionForm, FitnessLandscape, LowPhenotype, HighPhenotype):
        self.m_ContinuousFunctionForm = None
        self.m_FitnessLandscape = None
        self.m_LowPhenotype = self.m_HighPhenotype = None

        self.m_intMinFitness = self.m_intMaxFitness = None

        self.m_ContinuousFunctionForm = ContinuousFunctionForm
        self.m_FitnessLandscape = FitnessLandscape
        self.m_LowPhenotype = LowPhenotype
        self.m_HighPhenotype = HighPhenotype

    def get_minimum_fitness(self):
        return self.m_intMinFitness

    def get_maximum_fitness(self):
        return self.m_intMaxFitness

    def calculate_fitness_limits(self, selectionParameter, emittedPhenotype):

        # selectionParameter will be positive for reinforcement, negative for punishment

        intToLow = None
        intToHigh = None

        if selectionParameter > 0:
            # Reinforforcement.
            # This does not take into account the possibility that self.m_intMaxFitness may be larger than permitted by the flat or circular fitness landscape.
            if self.m_ContinuousFunctionForm == Constants.CONTINUOUS_FUNCTION_FORM_LINEAR:
                self.m_intMinFitness = 0
                self.m_intMaxFitness = 3 * selectionParameter  # This is the root (selectionParameter is the mean of the FDF).
            elif self.m_ContinuousFunctionForm == Constants.CONTINUOUS_FUNCTION_FORM_UNIFORM:
                self.m_intMinFitness = 0
                self.m_intMaxFitness = 2 * selectionParameter  # This is the root (selectionParameter is the mean of the FDF).
            else:
                raise AssertionError("Trouble in CFitnessLimits:  Unknown function form.")

        elif selectionParameter < 0:
            # Punishment.
            # Calculate the maximum fitness.
            if self.m_FitnessLandscape == Constants.FITNESS_LANDSCAPE_FLAT:
                intToLow = abs(emittedPhenotype - self.m_LowPhenotype)
                intToHigh = abs(self.m_HighPhenotype - emittedPhenotype)
                if intToHigh >= intToLow:
                    self.m_intMaxFitness = intToHigh
                else:
                    self.m_intMaxFitness = intToLow
            if self.m_FitnessLandscape == Constants.FITNESS_LANDSCAPE_CIRCULAR:
                self.m_intMaxFitness = int((self.m_HighPhenotype + 1) / 2 - 1)  # Maximum fitness is half the phenotype range.
            else:
                raise AssertionError("Trouble CFitnessLimits:  Unknown finess landscape.")

            # Calculate the minimum fitness for the specific FDF form.  (These expressions are worked out from
            # equations in "9.  Notebook on Punishment", pp. 13ff.)
            if self.m_ContinuousFunctionForm == Constants.CONTINUOUS_FUNCTION_FORM_LINEAR:
                self.m_intMinFitness = 3 * abs(selectionParameter) - 2 * self.m_intMaxFitness
            elif self.m_ContinuousFunctionForm == Constants.CONTINUOUS_FUNCTION_FORM_UNIFORM:
                self.m_intMinFitness = 2 * abs(selectionParameter) - self.m_intMaxFitness
            else:
                raise AssertionError("Trouble in CFitnessLimits:  Unknown function form.")

        else:
            raise AssertionError("Trouble in CFitnessLimits:  The reinforcer or punisher has no value.")
