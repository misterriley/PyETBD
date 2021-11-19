'''
Created on May 23, 2021
Translated May 24, 2021

@author: bleem
'''
import Converter


class MutationInfo(object):
	'''
	classdocs
	'''

	def init(self):
		self.m_Method = None
		self.m_Boundary = None  # Relevant only for the Gaussian mutation method
		self.m_SD = None  # Standard deviation for Gaussian mutation method
		self.m_Rate = None  # Decimal representing % mutation, e.g., 7.5 (= 7.5% mutation rate)
		self.m_GrayCodes = None  # If True, Gray codes are being used to represent the behaviors.  Mutate accordingly.
		self.m_LowPhenotype = None  #  Lowest phenotype in the range of all phenotypes
		self.m_HighPhenotype = None  # Highest phenotype in the range of all phenotypes

	def get_method(self):
		return self.m_Method

	def get_method_str(self):
		return Converter.convert_mutation_method_to_string(self.m_Method)

	def get_boundary(self):
		return self.m_Boundary

	def get_sd(self):
		return self.m_SD

	def get_rate(self):
		return self.m_Rate

	def use_gray_codes(self):
		return self.m_GrayCodes

	def get_low_phenotype(self):
		return self.m_LowPhenotype

	def get_high_phenotype(self):
		return self.m_HighPhenotype

	def set_method(self, value):
		self.m_Method = value

	def set_boundary(self, value):
		self.m_Boundary = value

	def set_sd(self, value):
		self.m_SD = value

	def set_rate(self, value):
		self.m_Rate = value

	def set_use_gray_codes(self, value):
		self.m_GrayCodes = value

	def set_low_phenotype(self, value):
		self.m_LowPhenotype = value

	def set_high_phenotype(self, value):
		self.m_HighPhenotype = value

