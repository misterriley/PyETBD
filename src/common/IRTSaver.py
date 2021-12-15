'''
Created on May 21, 2021
Translated May 23, 2021

@author: bleem
'''


class IRTSaver(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.m_irts = []

        # This class saves lists of cumulative IRTs for the populations in the built organism.
        # This class must be initialized by means of the LoadSD procedure to conform to the built organism's populations.
        # As currently written, the lab code creates a fresh IRTSaver object each time an organism is loaded.

        self.m_SDColor = None
        self.m_lstOfColors = list()
        self.m_indexOfIRTList = None

    def get_sd_color(self):
            return self.m_SDColor

    def set_sd_color(self, value):
            # Sets a reference to the correct population.  Hence this property
            # must be set before IRTs can be loaded or read.
            # However, before this property can be set, initialization must have occured
            # via the LoadSD procedure
            # i As Integer
            self.m_SDColor = value
            for i in range(len(self.m_lstOfColors)):
                if self.m_lstOfColors[i] == self.m_SDColor:
                    break

            self.m_indexOfIRTList = i

    def get_list_of_IRTs(self):
        return self.get_list_of_IRTs(self.m_indexOfIRTList)

    def get_list_of_IRTs_by_index(self, index):
        return self.m_irts[index]

    def set_list_of_IRTs_by_index(self, index, value):
            self.m_irts[index] = value

    def load_IRTs(self, lstCumIRTs):

        # SDColor must be set first so that the correct population will be accessed

        if self.get_list_of_IRTs()[0] == 0:
            # There is an initial dummy list at this index.
            # Remove it and insert the passed list of cumulative IRTs
            self.m_irts[self.m_indexOfIRTList] = lstCumIRTs
        else:
            # Continue the cumulation
            self.get_list_of_IRTs().append(self.get_list_of_IRTs()[-1] + lstCumIRTs[0])  # First additional IRT
            for i in range(1, len(lstCumIRTs)):
                self.get_list_of_IRTs().append(self.get_list_of_IRTs()[-1] + (lstCumIRTs[i] - lstCumIRTs[i - 1]))

    def load_SD(self, colorOfSD):

        # Repeated calls to this procedure initializes the object

        # This list of SD colors mirrors the list of SD colors in the built organism.
        # Hence given an SD color, its index in this list is the same as its index in the built organism.
        # This procedure is called by the lab code when the organism is loaded such that the number and order of the SDs
        # in self.m_lstOfColors is identical to the number and order of SDs in the built organism.

        self.m_lstOfColors.append(colorOfSD)

        # Make a dummy list of IRTs for each SD color
        for _ in range(len(self.m_lstOfColors)):
            self.m_irts.append([0])

        # The IRTSaver object now has the same number of lists of dummy IRTs (each consisting of a single IRT = 0) as there are
        # populations in the built organism
