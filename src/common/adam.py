'''
Created on Mar 8, 2022

@author: bleem
'''

import numpy as np


class AdamObject:

	def __init__(self, value, beta1 = .9, beta2 = .999, epsilon = 10 ** -8, gamma = .001):
		self.value = value
		self.beta1 = beta1
		self.beta2 = beta2
		self.epsilon = epsilon
		self.gamma = gamma
		self.m = np.zeros(self.value.shape) if type(self.value) == np.ndarray else 0
		self.v = np.zeros(self.value.shape) if type(self.value) == np.ndarray else 0
		self.steps = 0

	def apply_gradient(self, gradients):
		self.steps += 1
		self.m = self.beta1 * self.m + (1 - self.beta1) * gradients
		self.v = self.beta2 * self.v + (1 - self.beta2) * np.square(gradients)
		m_hat = self.m / (1 - self.beta1 ** self.steps)
		v_hat = self.v / (1 - self.beta2 ** self.steps)
		self.value = self.value - self.gamma * m_hat / (np.sqrt(v_hat) + self.epsilon)

	def get_value(self):
		return self.value

	def __str__(self):
		return str(self.value)
