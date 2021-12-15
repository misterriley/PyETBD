'''
Created on May 23, 2021
Translated May 24, 2021

@author: bleem
'''

from src.common.CRandomNumber import CRandomNumber


class CProbEmitter(object):
    '''
    classdocs
    '''

    def __init__(self):
        self.m_probOfEmission = None
        self.m_objRandom = CRandomNumber()
        # This class emits events with a probability specified by the user.

        #Usage-------------------------------------------------------------
        # User must set the ProbOfEmission property from the calling program.
        # User then queries the Emission property.  If this property is True, then an event has been emitted.
        #   If it is false, then an event has not been emitted.  If this property is queried repeatedly, then
        #   the observed relative frequency of emission will be found to equal the ProbOfEmission.

        # This is the probability of emission
    def get_prob_of_emission(self):
        return self.m_probOfEmission

    def set_prob_of_emission(self, value):
        self.m_probOfEmission = value

    def get_emission(self):
        if self.m_objRandom.get_rectangular_decimal() <= self.m_probOfEmission:
            return True
        else:
            return False
