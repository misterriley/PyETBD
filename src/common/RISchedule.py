'''
Created on May 21, 2021
Translated May 24, 2021

@author: bleem
'''

from src.common.CRandomNumber import CRandomNumber


class RISchedule(object):
    '''
    classdocs
    
    'Arranges a Random Interval Schedule.  

    'The mean of the schedule can be passed to the constructor or it can be set via the Mean property. 
    'A schedule object can also save and return obtained IRIs if desired.  To do so, set the SaveIRIs property to true 
    'from the calling program before the schedule is run, and then retrieve the IRIs from the IRIArray property after
    'the run is complete.

    'Usage:
    'Call the TickTock procedure every time tick, e.g., after each behavioral emission.  This advances the schedule timer.
    'If a target behavior is emitted, call the TickTock procedure as usual, then query the ReinforcementSetUp function 
    'to determine whether reinforcement is available.
    '''

    def __init__(self, dblMean = 0):
        self.m_mean = dblMean
        self.m_dblCurrentInterval = 0
        self.m_intTicksIntoInterval = 0  # Time (ticks) since the last reinforcement.
        self.m_blnSaveIRIs = False
        self.m_IRIArray = list()
        self.m_objRandom = CRandomNumber()

    def get_mean(self):
        return self.m_mean

    def set_mean(self, value):
        self.m_mean = value
        self.m_objRandom.set_mean(self.m_mean)
        self.get_new_interval()
        self.m_intTicksIntoInterval = 0
        self.m_IRIArray = list()

    def set_save_IRIs(self, value):
        self.m_blnSaveIRIs = value

    def get_save_IRIs(self):
        return self.m_blnSaveIRIs

    def get_IRI_array(self):
        return self.m_IRIArray

    def get_new_interval(self):
        self.m_dblCurrentInterval = self.m_objRandom.get_exponential_double()

    def tick_tock(self):
        self.m_intTicksIntoInterval += 1

    def is_reinforcement_set_up(self):
        if self.m_intTicksIntoInterval >= self.m_dblCurrentInterval:
            if self.m_blnSaveIRIs:
                self.m_IRIArray.append(self.m_intTicksIntoInterval)
            self.get_new_interval()
            self.m_intTicksIntoInterval = 0
            return True
        else:
            return False

