'''
Created on May 22, 2021
Translated May 24, 2021

@author: bleem
'''
from src.common import Constants
from src.common.CRandomNumber import CRandomNumber
from src.common.SampleWoutReplace import SampleWoutReplace


class Recombinator(object):
    '''
    classdocs
    '''

    def __init__(self, stuRecombinationInfo):
        '''
        Constructor
        '''
        # This class receives a father and a mother behavior and returns a child
        # This version is GOLD (the Select Case statement in the constructor has been corrected).

        self.m_objRandom = CRandomNumber()
        self.m_objSampler = SampleWoutReplace()

        self.m_stuRecombinationParameters = stuRecombinationInfo

        # Set appropriate properties of self.m_objRandom

        if self.m_stuRecombinationParameters.get_method() == Constants.RECOMBINATION_METHOD_BITWISE:
            self.m_objRandom.set_highest_integer(1)
            self.m_objRandom.set_lowest_integer(0)
        elif self.m_stuRecombinationParameters.get_method() == Constants.RECOMBINATION_METHOD_CLONE:
            self.m_objRandom.set_highest_integer(1)
            self.m_objRandom.set_lowest_integer(0)
        elif self.m_stuRecombinationParameters.get_method() == Constants.RECOMBINATION_METHOD_CROSSOVER:
            pass
            # Set in the appropriate section of get_child

    def get_child(self, blnFather, blnMother):

        # Generates a child from blnFather and blnMother.  The Boolean parents may be represented by either
        # binary bits or Gray code bits.  The Recombinator does not care about this and cannot tell the
        # difference.

        blnChild = [None] * len(blnFather)  # For the child behavior
        # Dim intFlip As Integer # For Bitwise recombination and for cloning.
        numCrossovers = self.m_stuRecombinationParameters.get_points()  # For Crossover recombination.
        # Dim intTemp As Integer #For Crossover recombination.
        intCrossoverLoc = [0] * (numCrossovers + 1)  # For Crossover recombination.
        # Dim blnParentOne(), blnParentTwo() #For Crossover recombination.
        # Dim i, j As Integer

        if self.m_stuRecombinationParameters.get_method() == Constants.RECOMBINATION_METHOD_BITWISE:
            # HighestInteger (1) and LowestInteger (0) properties of the self.m_objRandom were set in the constructor.
            # Let 0 (Heads) represent the father and 1 (Tails) represent the mother.
            for i in range(1, len(blnChild)) :  #  Note that, as always, the zeroth bit is not involved.
                intFlip = self.m_objRandom.get_rectangular_integer()
                if intFlip == 0:
                    # Use Father's bit
                    blnChild[i] = blnFather[i]
                elif intFlip == 1:
                    # Use Mother's bit
                    blnChild[i] = blnMother[i]
                else:
                    raise AssertionError("Trouble in paradise in Recombinator.")

        elif self.m_stuRecombinationParameters.get_method() == Constants.RECOMBINATION_METHOD_CROSSOVER:  # This has been thoroughly tested and works _perfectly_
            #                                for both binary and Gray code bits.
            # Set crossover locations
            self.m_objRandom.set_lowest_integer(1)
            self.m_objRandom.set_highest_integer(len(blnChild) - 2)
            self.m_objSampler.clear()
            for i in range(1, numCrossovers + 1):
                while True:
                    intTemp = self.m_objRandom.get_rectangular_integer()
                if self.m_objSampler.OK(intTemp):
                    break
                intCrossoverLoc[i] = intTemp

            list.sort(intCrossoverLoc)
            # The crossover locations are now set and listed in numerical order in intCrossoverLoc()

            # Determine which parent's bits to start with.  Crossover produces two children.  To select
            # one at random without creating both, simply determine which parent's bits to start with.
            self.m_objRandom.set_lowest_integer(0)
            self.m_objRandom.set_highest_integer(1)
            intTemp = self.m_objRandom.get_rectangular_integer()
            if intTemp == 0:
                # Start with the mother
                blnParentOne = blnMother
                blnParentTwo = blnFather
            elif intTemp == 1:
                # Start with the father
                blnParentOne = blnFather
                blnParentTwo = blnMother
            else:
                raise AssertionError("Trouble in paradise in Recombinator.get_child.")

            # Create child
            for j in range(1, numCrossovers + 1):
                if j % 2 == 0:
                    # Take bits from ParentTwo (j is even)
                    for i in range(intCrossoverLoc[j - 1] + 1, intCrossoverLoc[j] + 1):
                        blnChild[i] = blnParentTwo[i]

                else:
                    # Take bits from ParentOne (j is odd)
                    for i in range(intCrossoverLoc[j - 1] + 1, intCrossoverLoc[j] + 1):
                        blnChild[i] = blnParentOne[i]

            # Add the tail
            if j % 2 == 0:
                # Take the tail from ParentTwo (j is even)
                for i in range(intCrossoverLoc[j - 1] + 1, len(blnFather)):
                    blnChild[i] = blnParentTwo[i]

            else:
                # Take the tail from ParentOne (j is odd)
                for i in range(intCrossoverLoc[j - 1] + 1, len(blnFather)):
                    blnChild[i] = blnParentOne[i]

        elif self.m_stuRecombinationParameters.get_method() == Constants.RECOMBINATION_METHOD_CLONE:

            # With Nick's changes to the cloning code there is no longer a valid mother, so just return the father
            blnChild = blnFather

        return blnChild
