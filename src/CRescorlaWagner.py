'''
Created on May 22, 2021
Translated May 23, 2021

@author: bleem
'''


class CRescorlaWagner(object):
    '''
    classdocs
    '''

    def __init__(self, structParameters):
        '''
        Constructor
        '''
        # Module level variables
        self.m_lstAS = [0]  # Trial-by-trial associative strengths.  Remember that this is zero-based.
    #                                            Time steps correspond exactly to the index of this arraylist.  The
    #                                            associative strength on the zeroth time step is always zero.  The
    #                                            number of time steps (including the zeroth) is the Count property of this
    #                                            array list.  The associative strength on the zeroth time step is added to the
    #                                            array list in the constructor.

        self.m_Lambda = structParameters.get_lambda()
        self.m_Alpha = structParameters.get_alpha()
        self.m_Beta1 = structParameters.get_beta_1()
        self.m_Beta0 = structParameters.get_beta_0()
        self.m_BergA = structParameters.get_berg_a()

    def get_lambda(self):
        return self.m_Lambda

    def get_alpha(self):
        return self.m_Alpha

    def get_beta_1(self):
        return self.m_Beta1

    def get_beta_0(self):
        return self.m_Beta0

    def get_berg_a(self):
        return self.m_BergA

    def set_lambda(self, value):
        self.m_Lambda = value

    def set_alpha(self, value):
        self.m_Alpha = value

    def set_beta_1(self, value):
        self.m_Beta1 = value

    def set_beta_0(self, value):
        self.m_Beta0 = value

    def set_berg_a(self, value):
        self.m_BergA = value

    def get_associative_strengths(self):
        return self.m_lstAS

    def reinforcement_is_present(self):

        # Reinforcement occurred on this time step

        previousAS = float(self.m_lstAS[-1])

        thisAS = previousAS + (self.m_Alpha * self.m_Beta1 * (self.m_Lambda - previousAS)) ** self.m_BergA

        self.m_lstAS.append(thisAS)

    def reinforcement_is_absent(self):

        # Reinforcement did not occur on this time step.  Lambda is zero.

        previousAS = float(self.m_lstAS[-1])

        thisAS = previousAS + (self.m_Alpha * self.m_Beta0 * (0 - previousAS)) ** self.m_BergA

        self.m_lstAS.append(thisAS)

    def clear_associative_strengths(self):
        self.m_lstAS = [0]
