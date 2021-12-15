'''
Created on May 22, 2021
Translated May 23, 2021

@author: bleem
'''
from src.common.Behavior import Behavior


class CRepulsionPunishment(object):
    '''
    classdocs
    '''

    def __init__(self, intLowPhenotype, intHighPheotype, intBitsInHighPhenotype, dblKelleyN):
        '''
        Constructor
        '''
        self.m_intLowPhenotype = None
        self.m_intHighPhenotype = None
        self.m_intBitsInHighPhenotype = None
        self.m_dblKelleyN = None

        self.m_intHighPhenotype = intHighPheotype
        self.m_intLowPhenotype = intLowPhenotype
        self.m_intBitsInHighPhenotype = intBitsInHighPhenotype
        self.m_dblKelleyN = dblKelleyN

    def repel_behaviors(self, lstBehaviors, intEmittedPhenotype, paramPunisher, lstRepelledBehaviors):

        # This does not appear to be used in the current code [3/2015].

        # Build the list of repelled behaviors
        # From sheet "Linear repulsion punishment" in workbook "Repulsion Punishment 1.xlsx" in folder "...\Projects\Research\Punishment".
        for tempBehavior in lstBehaviors:
            if tempBehavior.get_integer_value() < intEmittedPhenotype:
                intEndPhenotype = self.m_intLowPhenotype
            else:
                intEndPhenotype = self.m_intHighPhenotype

            intRepelledPhenotype = intEmittedPhenotype + paramPunisher * (intEndPhenotype - tempBehavior.get_integer_value())
            objRepelledBehavior = Behavior(intRepelledPhenotype)
            objRepelledBehavior.pad_to(self.m_intBitsInHighPhenotype)
            lstRepelledBehaviors.append(objRepelledBehavior)

    def repel_behaviors_2(self, lstBehaviors, intEmittedPhenotype, paramPunisher, lstRepelledBehaviors):

        # This also does not appear to be used in the current code [3/2015].

        # Calculate x-sub-m (intMaxRepell)
        if self.m_intHighPhenotype - intEmittedPhenotype > intEmittedPhenotype - self.m_intLowPhenotype:
            intMaxRepell = self.m_intHighPhenotype - intEmittedPhenotype
        else:
            intMaxRepell = intEmittedPhenotype - self.m_intLowPhenotype

        # Build the list of repelled behaviors
        # From sheet "Linear repulsion punishment - 2" in workbook "Kelley Repulsion Punishment 2.xlsx" in folder "...\Projects\Research\Punishment".
        for tempBehavior in lstBehaviors:
            if tempBehavior.get_integer_value() >= intEmittedPhenotype:
                intRepelledPhenotype = tempBehavior.get_integer_value() + paramPunisher * (intMaxRepell - tempBehavior.get_integer_value() + intEmittedPhenotype)
            else:
                intRepelledPhenotype = tempBehavior.get_integer_value() - paramPunisher * (intMaxRepell - intEmittedPhenotype + tempBehavior.get_integer_value())

            if intRepelledPhenotype < self.m_intLowPhenotype or intRepelledPhenotype > self.m_intHighPhenotype:
                intRepelledPhenotype = intEmittedPhenotype - intRepelledPhenotype + intEmittedPhenotype

            objRepelledBehavior = Behavior(intRepelledPhenotype)
            objRepelledBehavior.pad_to(self.m_intBitsInHighPhenotype)
            lstRepelledBehaviors.append(objRepelledBehavior)

    def kelley_repel_behaviors_2(self, lstBehaviors, intEmittedPhenotype, paramPunisher, lstRepelledBehaviors):

        # MsgBox("Doing the fold, baby!")

        # Calculate x-sub-m (intMaxRepell)
        # intEmittedPhenotype is the punished phenotype [3/2015]
        if self.m_intHighPhenotype - intEmittedPhenotype > intEmittedPhenotype - self.m_intLowPhenotype:
            intMaxRepell = self.m_intHighPhenotype - intEmittedPhenotype
        else:
            intMaxRepell = intEmittedPhenotype - self.m_intLowPhenotype

        # Build the list of repelled behaviors
        # Hand written...don't lose it (transfer to notebook)! [Easy enough to reconstruct from the code - 3/2015]
        for tempBehavior in lstBehaviors:
            if tempBehavior.get_integer_value() >= intEmittedPhenotype:
                intRepelledPhenotype = tempBehavior.get_integer_value() + paramPunisher * intMaxRepell * (1 - abs(tempBehavior.get_integer_value() - intEmittedPhenotype) / intMaxRepell) ** self.m_dblKelleyN
                # intRepelledPhenotype = tempBehavior.get_integer_value() + paramPunisher * (intMaxRepell - tempBehavior.get_integer_value() + intEmittedPhenotype)
            else:
                intRepelledPhenotype = tempBehavior.get_integer_value() - paramPunisher * intMaxRepell * (1 - abs(tempBehavior.get_integer_value() - intEmittedPhenotype) / intMaxRepell) ** self.m_dblKelleyN
                # intRepelledPhenotype = tempBehavior.get_integer_value() - paramPunisher * (intMaxRepell - intEmittedPhenotype + tempBehavior.get_integer_value())

            # The following If...Then block does not look right.  Okay, I see what I'm doing. [3/2015]
            # See my 9. Notebook on Punishment, p. 42, for the explanation. You could call this "folding back" an overshoot. [3/2015]
            if intRepelledPhenotype < self.m_intLowPhenotype or intRepelledPhenotype > self.m_intHighPhenotype:
                # MsgBox("Punished phenotype:  " & CStr(intEmittedPhenotype) & "   Phenotype to be repelled:  " & CStr(tempBehavior.get_integer_value()) & "   Repelled phenotype " & CStr(intRepelledPhenotype))
                intRepelledPhenotype = intEmittedPhenotype - intRepelledPhenotype + intEmittedPhenotype
                # MsgBox("Corrected repelled phenotype:  " & CStr(intRepelledPhenotype))

            objRepelledBehavior = Behavior(intRepelledPhenotype)
            objRepelledBehavior.pad_to(self.m_intBitsInHighPhenotype)
            lstRepelledBehaviors.append(objRepelledBehavior)

    def circular_repel(self, lstBehaviors, intEmittedPhenotype, paramPunisher, lstRepelledBehaviors, _):

        # Implements circular repulsion punishment.  Instead of folding back the overshoots, it wraps them around to the other end of the phenotype range.
        # However this now implements differential repulsion punishment, unless dblValueAdjustment = 1. (5/2018)

        dblValueAdjustment = 1

        # This implementation follows the algorithm developed on pp. 40ff of 9. Notebook on Pushiment, and repeated with slight modifications
        # in the document, "Repulsion Punishment for Circular Landscapes.docx"

        # MsgBox("Doing the wrap, baby!")
        # MsgBox(self.m_dblKelleyN.ToString)
        # Stop

        intHalfRange = (self.m_intHighPhenotype + 1) / 2  # This is half the phenotype range, which is used often in this procedure
        # blnEasterly # TRUE = Punished phenotype lies in the east or is due south; FALSE = Punished phenotype lies in the west or is due north
        # objRepelledBehavior = None

        # Given intEmittedPhenotype,
        intPunishedPhenotype = intEmittedPhenotype  # For naming clarity. This is phi-sub-P in the algorithm
        # intFarthestPhenotype = None

        # For each behavior in lstBehaviors:
        # intFarthestRepulsion, intDistanceFromPunished = None
        # intDistanceToRepel, intRepelledPhenotype = None

        # Find farthest Phenotype, phi-sub-F in algorithm (from Equation 2 in the document)
        if intPunishedPhenotype < intHalfRange:
            # Punished phenotype lies in the east or is due south
            intFarthestPhenotype = intPunishedPhenotype + intHalfRange
            blnEasterly = True
        else:
            # Punished phenotype lies in the west or is due north
            intFarthestPhenotype = intPunishedPhenotype - intHalfRange
            blnEasterly = False

        # Build the list of repelled behaviors
        for tempBehavior in lstBehaviors:
            intFarthestRepulsion = self.farthest_repulsion(tempBehavior.get_integer_value(), intFarthestPhenotype)  # f-sub-i in algorithm;
            #                                                                                           from Equation 3 in the document
            intDistanceFromPunished = intHalfRange - intFarthestRepulsion  # d-sub i in algorithm; from Equation 4 in the document
            #Looks like the adjustment for relative reinforcer value must occur in the following line (5/2018)*************************************
            # Will have to pass relative reinforcer value to this procedure.
            intDistanceToRepel = int(dblValueAdjustment * paramPunisher * intHalfRange * (1 - intDistanceFromPunished / intHalfRange) ** self.m_dblKelleyN)  # d-sub-ir in
            #                                      the algorithm; from Equation 7 in the document, which does not always give an integer result.
            # intDistanceToRepel = CInt(paramPunisher * intHalfRange * (1 - intDistanceFromPunished / intHalfRange) ** self.m_dblKelleyN) # d-sub-ir in
            #                                      the algorithm; from Equation 7 in the document, which does not always give an integer result.
            intRepelledPhenotype = self.repell_phenotype(tempBehavior.get_integer_value(), intFarthestPhenotype, intPunishedPhenotype, blnEasterly, intDistanceToRepel)
            # Add to the list of repelled behaviors
            objRepelledBehavior = Behavior(intRepelledPhenotype)
            objRepelledBehavior.pad_to(self.m_intBitsInHighPhenotype)
            lstRepelledBehaviors.append(objRepelledBehavior)

    def farthest_repulsion(self, intIthPhenotype, intFarthestPhenotype):

        # Called by CircularRepel to find the farthest the ith phenotype can be repelled, f-sub-i in the algorithm

        # intSeparationFromFarthest = None

        intSeparationFromFarthest = abs(intFarthestPhenotype - intIthPhenotype)

        if intSeparationFromFarthest < self.m_intHighPhenotype + 1 - intSeparationFromFarthest:
            return intSeparationFromFarthest
        else:
            return self.m_intHighPhenotype + 1 - intSeparationFromFarthest

    def repell_phenotype(self, intIthPhenotype, intFarthestPhenotype, intPunishedPhenotype, blnEasterly, intDistanceToRepel):

        # Called by CircularRepel.
        # Determines the direction of repulsion, calculates the repelled phenotype, and then corrects for (i.e., wraps) any overshoots.
        # The algorithm implemented here is explained in the document.

        # intRepelledPhenotype = None

        if blnEasterly:
            # Punished phenotype lies in the east or is due south; phi-sub-F > phi-sub-P
            if intPunishedPhenotype <= intIthPhenotype < intFarthestPhenotype:
                # ith phenotype lies between phi-sub-F and phi-sub-p; repel right
                intRepelledPhenotype = intIthPhenotype + intDistanceToRepel
            else:
                # repel left
                intRepelledPhenotype = intIthPhenotype - intDistanceToRepel

        else:
            # Punished phenotype lies in the west or is due north; phi-sub-F < phi-sub-P
            if intPunishedPhenotype >= intIthPhenotype > intFarthestPhenotype:
                # ith phenotype lies between phi-sub-F and phi-sub-p; repel left
                intRepelledPhenotype = intIthPhenotype - intDistanceToRepel
            else:
                # repel right
                intRepelledPhenotype = intIthPhenotype + intDistanceToRepel

        # Correct for overshoots (from Equations 8 and 9 in the document).
        # These corrections cause the repelled phenotypes to wrap around the circular landscape.
        if intRepelledPhenotype > self.m_intHighPhenotype:
            intRepelledPhenotype = intRepelledPhenotype - (self.m_intHighPhenotype + 1)
        if intRepelledPhenotype < 0:
            intRepelledPhenotype = intRepelledPhenotype + (self.m_intHighPhenotype + 1)

        return intRepelledPhenotype

