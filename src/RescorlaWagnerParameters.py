'''
Created on May 23, 2021
Translated May 24, 2021

@author: bleem
'''


class RescorlaWagnerParameters(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.Lambda = None  # Maximum associative strength.  Conventionally set equal to 1 for the US.
    #                                                     Conventionally set equal to 0 in the absence of the US.
        self.Alpha = None  # CS salience.  Conventionally 0 <= alpha <= 1.
        self.Beta1 = None  # US-presence salience.  Conventionally 0 <= beta1 <= 1.
        self.Beta0 = None  # US-absence salience.  Conventionally 0 <= beta0 <= 1.
        self.BergA = None  # Exponent on the increment to associative strength (which is the second term on the right of the R-W equation)

    def get_lambda(self):
        return self.__Lambda

    def get_alpha(self):
        return self.__Alpha

    def get_beta_1(self):
        return self.__Beta1

    def get_beta_0(self):
        return self.__Beta0

    def get_berg_a(self):
        return self.__BergA

    def set_lambda(self, value):
        self.__Lambda = value

    def set_alpha(self, value):
        self.__Alpha = value

    def set_beta_1(self, value):
        self.__Beta1 = value

    def set_beta_0(self, value):
        self.__Beta0 = value

    def set_berg_a(self, value):
        self.__BergA = value

