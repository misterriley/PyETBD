'''
Created on May 22, 2021
Translated May 23, 2021

@author: bleem
'''

from CProbEmitter import CProbEmitter
from CRandomNumber import CRandomNumber
import Constants, BinaryConvertBoolean, CGrayCodes


class Mutator(object):
    '''
    classdocs
    '''

    def __init__(self, stuMutatorProperties):

        self.m_stuMutationParameters = None
        self.m_lowPhenotype = self.m_highPhenotype = self.m_bitsInHighPhenotype = None
        self.m_blnUseGrayCodes = None
        self.m_objProbEmitter = CProbEmitter()
        self.m_objRandom = CRandomNumber()

        # Set Private properties of the Mutator
        self.set_mutation_parameters(stuMutatorProperties)
        self.set_low_phenotype(stuMutatorProperties.get_low_phenotype())
        self.set_high_phenotype(stuMutatorProperties.get_high_phenotype())
        self.set_use_gray_codes(stuMutatorProperties.use_gray_codes())

        # Set ProbOfEmission parameter of self.m_objProbEmitter.  for BitFlipByIndividual,
        # RandomIndividual, or Gaussian mutation, this is the probability that an _individual_ will mutate;
        # for BitFlipByBit mutation it is the probability that a _bit_ will mutate.
        self.m_objProbEmitter.set_prob_of_emission(stuMutatorProperties.get_rate() / 100)

        # Set properties of the random number generator for the appropriate mutation method.
        if stuMutatorProperties.get_method() == Constants.MUTATION_METHOD_BIT_FLIP_BY_INDIVIDUAL:
            self.m_objRandom.set_lowest_integer(1)
            self.m_objRandom.set_highest_integer(self.m_bitsInHighPhenotype)
        elif stuMutatorProperties.get_method() == Constants.MUTATION_METHOD_BIT_FLIP_BY_BIT:
            # N/A
            pass
        elif stuMutatorProperties.get_method() == Constants.MUTATION_METHOD_RANDOM_INDIVIDUAL:
            self.m_objRandom.set_lowest_integer(self.get_low_phenotype())
            self.m_objRandom.set_highest_integer(self.get_high_phenotype())
        elif stuMutatorProperties.get_method() == Constants.MUTATION_METHOD_GAUSSIAN:
            # Mean of the Gaussian must be set in get_mutant for each behavior passed.
            self.m_objRandom.set_sd(self.get_mutation_parameters().get_sd())

    def get_mutation_parameters(self):
        return self.m_stuMutationParameters

    def set_mutation_parameters(self, value):
        self.m_stuMutationParameters = value

    def get_low_phenotype(self):
        return self.m_lowPhenotype

    def set_low_phenotype(self, value):
        self.m_lowPhenotype = value

    def get_high_phenotype(self):
        return self.m_highPhenotype

    def set_high_phenotype(self, value):
        self.m_highPhenotype = value
        self.m_bitsInHighPhenotype = len(BinaryConvertBoolean.convert_from_base_10(value, 0)) - 1  # Used in bitflip mutation methods.

    def get_use_gray_codes(self):
        return self.m_blnUseGrayCodes

    def set_use_gray_codes(self, value):
        self.m_blnUseGrayCodes = value

    def get_mutant(self, intBehavior):

        # This procedure, which is passed and returns an integer, is necessary only for Cloning when either bit flip
        # mutation method is used with binary bits.  This is because of a bizarro bug that occurs under these conditions
        # that I think is a part of the .NET framework or the VB language.  This procedure avoids that bug.  All other combinations of
        # recombination and mutation methods work fine with the other get_mutant procedure, which is passed and returns a
        # Boolean array.

        # In spite of this, this procedure is now being used for all mutation, thus bypassing the other self.get_mutant
        # procedure entirely.

        # intBehavior is the integer value of a behavior that may become a mutant.
        # self.m_objProbEmitter is set for the correct mutation probability in the constructor.
        # The random number generator is initialized for the correct mutation method in the constructor.

        # Dim intBitToFlip
        # Dim blnBehavior(self.m_bitsInHighPhenotype) As Boolean #Holds the appropriately padded Boolean array that will undergo
        #                                                  bitflip by individual or bitflip by bit mutation.
        # Dim blnBehaviorMutated As Boolean #Flag for BitFlipByBit method.
        # Dim intMutant # for Gaussian mutation method.

        if self.get_mutation_parameters().get_method() == Constants.MUTATION_METHOD_BIT_FLIP_BY_INDIVIDUAL:
            if self.m_objProbEmitter.get_emission():
                # This individual must mutate
                blnBehavior = self.convert_integer_to_boolean(intBehavior)  # returns padded binary bits or Gray code bits as appropriate
                # Determine which bit to flip and flip it
                intBitToFlip = self.m_objRandom.get_rectangular_integer()
                blnBehavior[intBitToFlip] = not blnBehavior[intBitToFlip]
                # return the integer value of the mutant Boolean array
                return self.get_integer_to_return(blnBehavior)
            else:
                # This individual did not mutate; return the integer value that was passed.
                return intBehavior

        elif self.get_mutation_parameters().get_method() == Constants.MUTATION_METHOD_BIT_FLIP_BY_BIT:
            blnBehavior = self.convert_integer_to_boolean(intBehavior)  # returns padded binary bits or Gray code bits as appropriate
            for i in range(1, len(blnBehavior)):
                if self.m_objProbEmitter.get_emission():
                    # This bit must be flipped.
                    blnBehaviorMutated = True
                    blnBehavior[i] = not blnBehavior[i]

            if blnBehaviorMutated:
                # return the integer value of the mutant Boolean array
                return self.get_integer_to_return(blnBehavior)
            else:
                # This behavior did not mutate.
                return intBehavior

        elif self.get_mutation_parameters().get_method() == Constants.MUTATION_METHOD_RANDOM_INDIVIDUAL:
            if self.m_objProbEmitter.get_emission():
                # Select a mutant phenotype from the permitted range and return it.
                # Appropriate properties of the self.m_objRandom (Highest and Lowest integers) were set in the constructor.
                return self.m_objRandom.get_rectangular_integer()
            else:
                # This behavior did not mutate.  return the phenotype that was passed.
                return intBehavior

        elif self.get_mutation_parameters().get_method() == Constants.MUTATION_METHOD_GAUSSIAN:
            if self.m_objProbEmitter.get_emission():
                # Select a mutant phenotype from a Gaussian with mean equal to intBehavior and S.D. that was set
                # in the constructor.
                self.m_objRandom.set_mean(intBehavior)
                if self.get_mutation_parameters().get_boundary() == Constants.MUTATION_BOUNDARY_DISCARD:
                    # Boundary = Discard
                    # Keep trying until the mutant is within range.
                    while True:
                        intMutant = int(self.m_objRandom.GaussianDouble)  # Integer value of the mutant.
                        if intMutant >= self.get_low_phenotype() and intMutant <= self.get_high_phenotype():
                            break
                else:
                    # Boundary = Wrap; this wraps _through zero_
                    intMutant = int(self.m_objRandom.GaussianDouble)  # Integer value of the mutant.
                    if intMutant > self.get_high_phenotype():
                        while True:
                            intMutant = intMutant - (self.get_high_phenotype() - self.get_low_phenotype() + 1)
                            if intMutant <= self.get_high_phenotype():
                                break
                    elif intMutant < self.get_low_phenotype():
                        while True:
                            intMutant = (self.get_high_phenotype() - self.get_low_phenotype() + 1) + intMutant
                            if intMutant >= self.get_low_phenotype():
                                break
                    else:
                        pass
                        # No wrap is necessary

                return intMutant
            else:
                # This behavior did not mutate.  return the phenotype that was passed.
                return intBehavior

    def convert_integer_to_boolean(self, intBehavior):

        # This function is called by the self.get_mutant procedure that is passed an integer whenever one of the bit
        # flip mutation methods is used.

        # Dim blnConvertedInteger(), blnBehavior(self.m_bitsInHighPhenotype) As Boolean
        # Dim bitsInConvertedInteger
        blnBehavior = [None] + [False] * self.m_bitsInHighPhenotype

        if self.get_use_gray_codes():
            # Convert to Boolean Gray code bits
            blnConvertedInteger = CGrayCodes.binary_to_gray_booleans(BinaryConvertBoolean.convert_from_base_10(intBehavior))
        else:
            # Convert to Boolean binary bits
            blnConvertedInteger = BinaryConvertBoolean.convert_from_base_10(intBehavior, 0)

        # Pad Boolean if necessary
        bitsInConvertedInteger = len(blnConvertedInteger) - 1
        if bitsInConvertedInteger < self.m_bitsInHighPhenotype:
            # Copy the elements of blnConvertedInteger into the rightmost elements of blnBehavior
            for i in range(self.m_bitsInHighPhenotype - bitsInConvertedInteger + 1, self.m_bitsInHighPhenotype + 1):
                blnBehavior[i] = blnConvertedInteger[i - (self.m_bitsInHighPhenotype - bitsInConvertedInteger)]

        else:
            # No padding is necessary.  Just copy blnConvertedInteger to blnBehavior
            blnBehavior = blnConvertedInteger

        return blnBehavior

    def get_integer_to_return(self, blnBehavior):

        # This function is called by the self.get_mutant procedure that is passed an integer whenever one of the bit
        # flip mutation methods is used.

        # blnBehavior is the mutant, expressed as a Boolean array of either Gray or binary bits.

        if self.get_use_gray_codes():
            # Gray code bits
            return BinaryConvertBoolean.convert_to_base_10(CGrayCodes.gray_to_binary_booleans(blnBehavior))
        else:
            # Binary bits
            return BinaryConvertBoolean.convert_to_base_10(blnBehavior)

# Region " Testing procedures and defunct procedures."

    def TestMutator(self, intNumMutants):

        # This procedure is used for testing and studying the Mutator object.  It is not used in the normal
        # operation of the class.

        # returns an array of mutants to the calling program.

        # Each mutant is calculated from a different random behavior.

        # Dim intMutants(intNumMutants) # To hold the mutants
        # Dim blnBehavior() As Boolean # To send a behavior to self.get_mutant
        # Dim blnMutant() As Boolean # To receive a mutant from self.get_mutant
        intBehaviorCount, intMutantCount = 0
        objRandom = CRandomNumber()
        intMutants = [None] * intNumMutants

        objRandom.set_lowest_integer(self.get_low_phenotype())
        objRandom.set_highest_integer(self.get_high_phenotype())

        while True:

            intBehaviorCount += 1
            # Convert a random integer in the permitted range to a Boolean and pad it as necessary.
            if self.get_use_gray_codes():
                # Use Gray code representation of the behavior
                blnBehavior = self.test_pad_boolean(CGrayCodes.binary_to_gray_booleans(BinaryConvertBoolean.convert_from_base_10(objRandom.get_rectangular_integer())))
            else:
                # Use binary bits
                blnBehavior = self.test_pad_boolean(BinaryConvertBoolean.convert_from_base_10(objRandom.get_rectangular_integer()))

            blnMutant = self.get_mutant(blnBehavior)
            if blnMutant[0]:
                # Have a mutant
                intMutantCount += 1
                if self.get_use_gray_codes():
                    # Mutant is represented as Gray code bits.
                    intMutants[intMutantCount] = BinaryConvertBoolean.convert_to_base_10(CGrayCodes.gray_to_binary_booleans(blnMutant))
                else:
                    # Mutant is represented as binary bits.
                    intMutants[intMutantCount] = BinaryConvertBoolean.convert_to_base_10(blnMutant)

            if intMutantCount == intNumMutants:
                break

        # return behavior count (inBehaviorCount) as the zeroth element of the integer array.
        # This is the number of behaviors that were sent to the self.get_mutant procedure.  Depending on
        # MutationInfo.get_rate(), only some of these became mutants.
        intMutants[0] = intBehaviorCount

        return intMutants

    def test_mutator(self, intNumMutants, intBehavior):

        # This procedure is used for testing and studying the Mutator object.  It is not used in the normal
        # operation of the class.

        # returns an array of mutants to the calling program.

        # Each mutant is calculated from the same behavior, intBehavior, passed to the procedure.

        # Dim intMutants(intNumMutants) # To hold the mutants
        # Dim blnBehavior() As Boolean # To send a behavior to self.get_mutant
        # Dim blnMutant() As Boolean # To receive a mutant from self.get_mutant
        intMutantCount, intBehaviorCount = 0
        intMutants = [0] * intNumMutants

        while True:

            intBehaviorCount += 1
            # Convert the passed integer to a Boolean and pad it as necessary.
            if self.get_use_gray_codes():
                # Use Gray code presentation of the behavior
                blnBehavior = self.test_pad_boolean(CGrayCodes.binary_to_gray_booleans(BinaryConvertBoolean.convert_from_base_10(intBehavior)))
            else:
                # Use binary bits
                blnBehavior = self.test_pad_boolean(BinaryConvertBoolean.convert_from_base_10(intBehavior))

            blnMutant = self.get_mutant(blnBehavior)
            if blnMutant[0]:
                # Have a mutant
                intMutantCount += 1
                if self.get_use_gray_codes():
                    # Mutant is represented by Gray code bits.
                    intMutants[intMutantCount] = BinaryConvertBoolean.convert_to_base_10(CGrayCodes.gray_to_binary_booleans(blnMutant))
                else:
                    # Mutant is represented by binary bits.
                    intMutants[intMutantCount] = BinaryConvertBoolean.convert_to_base_10(blnMutant)

            if intMutantCount == intNumMutants:
                break

        # return behavior count (inBehaviorCount) as the zeroth element of the integer array.
        # This is the number of behaviors that were sent to the self.get_mutant procedure.  Depending on
        # MutationInfo.get_rate(), only some of these became mutants.
        intMutants[0] = intBehaviorCount

        return intMutants

    def test_pad_boolean(self, blnBehavior):

        # This procedure is used for testing and studying the Mutator object.  It is not used in the normal
        # operation of the class.

        # Called by the two TestMutator functions.

        # Dim intBitsInHighPhenotype, intBitsToPad

        intBitsInHighPhenotype = len(BinaryConvertBoolean.convert_from_base_10(self.get_high_phenotype())) - 1
        intBitsToPad = intBitsInHighPhenotype - (len(blnBehavior) - 1)
        blnPaddedBoolean = [False] * intBitsInHighPhenotype

        if intBitsToPad == 0:
            # No padding necessary
            return blnBehavior
        else:
            # Pad
            for i in range(1, len(blnBehavior)):
                blnPaddedBoolean[i + intBitsToPad] = blnBehavior[i]

        return blnPaddedBoolean
