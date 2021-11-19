'''
Created on May 22, 2021
Translated May 23, 2021

@author: bleem
'''

import BaseConverter, BinaryConvertBoolean, CGrayCodes


class Behavior(object):
	'''
	classdocs
	'''

	def __init__(self, value = None, num_bits = 0):

		assert num_bits == 10 or not isinstance(value, int)

		self.m_blnBinaryBits = None
		self.m_blnGrayBits = None
		self.m_fitness = None

		if value is not None:
			if isinstance(value, int):
				self.set_integer_value(value, num_bits)
			else:
				self.set_binary_bits(value)

	# Can create the binary Boolean array that represents this behavior by passing to the constructor either the
	# Boolean array itself, or the integer value that represents the behavior, or by setting the BinaryBits,
	# GrayBits, self.get_integer_value(), BinaryBitString, or GrayBitString property of this class.  All methods of
	# creating the behavior eventually call the BinaryBits property.

	# Note comments for the GrayBits property below.

	def get_num_bits(self):
		return len(self.m_blnBinaryBits) - 1

	def get_binary_bits(self):
		return self.m_blnBinaryBits

	def set_binary_bits(self, value):

		self.m_blnBinaryBits = value
		self.m_blnGrayBits = CGrayCodes.binary_to_gray_booleans(self.m_blnBinaryBits)

	def get_gray_bits(self):
	# All elements of this procedure have been tested.  However, when first using it in an experiment
	# it would be prudent to double check the conversions for accuracy.

		# returns a Boolean array that represents the Gray code bit string.  The zeroth element is not
		# part of the bit string.
		return self.m_blnGrayBits

	def set_gray_bits(self, value):
		binary_bits = CGrayCodes.gray_to_binary_booleans(value)
		# Converts the passed Gray code Boolean array to a binary Boolean array
		self.set_binary_bits(binary_bits)

	def get_integer_value(self):
		# returns the integer value of the bit string represented by the Boolean array.
		return BinaryConvertBoolean.convert_to_base_10(self.m_blnBinaryBits)

	def set_integer_value(self, value, num_bits):
		self.set_binary_bits(BinaryConvertBoolean.convert_from_base_10(value, num_bits))

	def get_binary_bit_string(self):
		return self.pad_string(BaseConverter.convert_from_base_10(self.get_integer_value(), 2))

	def set_binary_bit_string(self, value):
		self.set_integer_value(BaseConverter.convert_to_base_10(value, 2))

	def get_gray_bit_string(self):
		# returns the Gray code bit string represented by the Boolean array, padded to self.get_num_bits() characters.
		return self.pad_string(CGrayCodes.integer_to_gray(self.get_integer_value()))

	def set_gray_bit_string(self, value):
		# Creates the binary Boolean array from the passed bit string by setting the self.get_integer_value() property.
		self.set_integer_value(CGrayCodes.gray_to_integer(value))

	def get_fitness(self):
		return self.m_fitness

	def set_fitness(self, value):
		self.m_fitness = value

	def pad_to(self, intTotalBits):

		# Pads the Boolean array with leading zeros such that NumBits = intTotalBits.
		# This procedure is called by the Behaviors class for each behavior in the population.
		# Padding when the behavior is created makes later repeated recombination and mutation
		# operations more efficient (I think).  This procedure may also be called by other calling
		# routines.

		if intTotalBits == self.get_num_bits():
			return  # No padding necessary.

		intPaddingBits = intTotalBits - self.get_num_bits()
		newBooleanBinaryBits = [False] * (intTotalBits + 1)
		newBooleanBinaryBits[0] = None

		# Append the existing bits (ignores the zeroth bit in m_blnBinaryBits()).  Before
		# the append, all the bits in newBooleanBinaryBits are zero (False).
		for i in range(1, self.get_num_bits() + 1):
			newBooleanBinaryBits[intPaddingBits + i] = self.m_blnBinaryBits[i]

		# Set the BinaryBits property of the class to register the padded representation of the behavior
		self.set_binary_bits(newBooleanBinaryBits)

	def pad_string(self, stringToPad):

		# Called by BinaryBitString and GrayBitString properties to generate equal-length
		# strings for all behaviors in a population after PadTo has been applied to the
		# behaviors in the population (thus setting the correct self.get_num_bits()).

		stringPad = "0" * (self.get_num_bits() - stringToPad.Length)

		return stringPad + stringToPad
