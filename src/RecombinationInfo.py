'''
Created on May 24, 2021
Translated May 24, 2021

@author: bleem
'''
import Converter


class RecombinationInfo(object):
	'''
	classdocs
	'''

	def __init__(self):
		self.m_method = None
		self.m_points = 0

	def get_method(self):
		return self.m_method

	def get_method_str(self):
		return Converter.convert_recombination_method_to_string(self.m_method)

	def get_points(self):
		return self.m_points

	def set_method(self, value):
		self.m_method = value

	def set_points(self, value):
		self.m_points = value
