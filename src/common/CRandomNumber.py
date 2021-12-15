'''
Created on May 21, 2021
Translated May 23, 2021

@author: bleem
'''
import numpy


class CRandomNumber(object):

	def __init__(self):
		self.m_lowestInteger = 0
		self.m_highestInteger = 0
		self.m_lowestDouble = 0
		self.m_highestDouble = 0
		self.m_mean = 0
		self.m_sd = 0

	def get_mean(self):
		return self.m_mean

	def set_mean(self, value):
		self.m_mean = value

	def get_sd(self):
		return self.m_sd

	def set_sd(self, value):
		self.m_sd = value

	def get_lowest_double(self):
		return self.m_lowestDouble

	def set_lowest_double(self, value):
		self.m_lowestDouble = value

	def set_highest_double(self, value):
		self.m_highestDouble = value

	def get_highest_double(self):
		return self.m_highestDouble

	def get_highest_integer(self):
		return self.m_highestInteger

	def set_highest_integer(self, value):
		self.m_highestInteger = value

	def get_lowest_integer(self):
		return self.m_lowestInteger

	def set_lowest_integer(self, value):
		self.m_lowestInteger = value

	def get_rectangular_decimal(self):
		return numpy.random.random()

	def get_rectangular_integer(self):
		return numpy.random.randint(self.m_lowestInteger, self.m_highestInteger + 1)

	def get_rectangular_double(self):
		return (self.m_highestDouble - self.m_lowestDouble) * self.get_rectangular_decimal() + self.m_lowestDouble

	def get_gaussian_z(self):
		return self.get_gaussian_deviate()

	def get_gaussian_double(self):
		return self.m_mean + self.get_gaussian_deviate() * self.m_sd

	def get_exponential_double(self):
		return -1 * self.m_mean * numpy.log(1 - self.get_rectangular_decimal())
