'''
Created on May 21, 2021
Translated May 24, 2021

@author: bleem
'''
from src.common.CRandomNumber import CRandomNumber


class RRSchedule(object):
    '''
    classdocs
    '''

    def __init__(self, intMean = 0):
        self.m_mean = intMean
        self.m_objRandom = CRandomNumber()
        self.m_intPecksIntoRatio = 0
        self.m_IRIArray = list()

    def get_mean(self):
        return self.m_mean

    def set_mean(self, value):
        self.m_mean = value
        self.m_objRandom.set_mean(self.m_mean)
        self.get_new_ratio()
        self.m_intPecksIntoRatio = 0
        self.m_IRIArray = list()

    def get_save_IRIs(self):
        return self.blnSaveIRIs

    def set_save_IRIs(self, value):
        self.m_blnSaveIRIs = value

    def get_IRI_array(self):
        return self.m_IRIArray

    def get_new_ratio(self):
        self.m_intCurrentRatio = int(self.m_objRandom.get_exponential_double())

    def response(self):
        self.m_intPecksIntoRatio += 1

    def tick_tock(self):
        self.m_intTicksIntoIRI += 1

    def is_reinforcement_set_up(self):
        if self.m_intPecksIntoRatio >= self.m_intCurrentRatio:
            if self.m_blnSaveIRIs:
                self.m_IRIArray.append(self.m_intTicksIntoIRI)
            self.get_new_ratio()
            self.m_intPecksIntoRatio = 0
            self.m_intTicksIntoIRI = 0
            return True
        else:
            return False
