'''
Created on May 22, 2021
Translated May 23, 2021

@author: bleem
'''

from src.common import BinaryConvertBoolean


def binary_to_gray_booleans(blnBinaryBits):
	# 'Converts a binary number represented as a Boolean array to Gray code represented as a Boolean array.

	blnGrayBits = [None] * len(blnBinaryBits)

	blnGrayBits[1] = blnBinaryBits[1]
	for i in range(2, len(blnBinaryBits)):
		blnGrayBits[i] = blnBinaryBits[i] ^ blnBinaryBits[i - 1]

	return blnGrayBits


def gray_to_binary_booleans(blnGrayBits):
	raise NotImplementedError


def integer_to_gray(intToConvert):
	raise NotImplementedError


def gray_to_integer(blnGrayBits):
	raise NotImplementedError


if __name__ == '__main__':
	for i in range(10):
		blnBits = BinaryConvertBoolean.convert_from_base_10(i)
		grayBits = binary_to_gray_booleans(blnBits)

		print(blnBits)
		print(grayBits)
		print("")
