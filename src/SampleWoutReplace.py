'''
Created on May 22, 2021
Translated May 24, 2021

@author: bleem
'''


class SampleWoutReplace(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        # Facilitates sampling integers without replacement from a set of unique integers.

        #USAGE-----------------------------------------------------------------------------------------
        # Instantiate an instance of this class in the calling program, say m_objSampler.
        # Pass an integer to the function OK.  If the integer is present in m_objSampler (i.e., it has
        # already been sampled and is in m_intList), then the function returns False, otherwise it adds
        # the integer to m_intList and returns True.
        #
        # Typical syntax in the calling code is something like this, where m_objSampler is an
        # instantiation of this class:
        #
        #            m_objSampler.Clear()
        #            For i = 1 to nOfSample
        #                Do
        #                    intItem = m_objRandom.RectangularInteger
        #                Loop Until m_objSampler.OK(intItem)
        #                #At this point intItem is sampled without replacement from the range specified
        #                #by the random number generator, and it can be added to a list or array that
        #                #contains the sample.
        #                #.
        #                #.
        #                #.
        #            Next

        # Be sure to call the Clear member of this class, as shown in the example above, before each new
        # round of sampling.

        # Note:  it would be easy to add other data types by overloading the OK function and creating
        # the appropriate List<T> classes...or actually, by doing the generic thing.

        self.m_intList = list()

    def OK(self, intSampledInteger):

        blnPresentInList = False

        # Check m_intList for presence of intSampledInteger
        for intNumber in self.m_intList:
            if intSampledInteger == intNumber:
                # The integer is already in m_intList
                blnPresentInList = True
                break

        # If intSampledInteger is in m_intList, return False, otherwise add it to m_intList and return True.
        if blnPresentInList:
            return False  # Not OK.  This integer has already been sampled.
        else:
            self.m_intList.append(intSampledInteger)
            return True  # OK to use this integer.

    def remove(self, intToRemoveFromList):
        self.m_intList.remove(intToRemoveFromList)

    def clear(self):

        # Clears all integers from m_intList
        self.m_intList.clear()
