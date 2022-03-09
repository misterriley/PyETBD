'''
Created on Feb 1, 2022

@author: bleem
'''

from src.common.Behavior import Behavior
from src.orgs.AnOrganism import AnOrganism
import numpy as np


class QLOrganism(AnOrganism):

	def __init__(self, json_data):
		super().__init__(json_data)
		self.num_slots = json_data.get_ml_num_slots()  # must be at least 3 or this code will not work
		self.learning_rate = json_data.get_ml_learning_rate()
		self.discount_rate = json_data.get_ml_discount_rate()
		self.reward_multiplier = json_data.get_ml_reward_multiplier()
		self.reward_exponent = json_data.get_ml_reward_exponent()
		self.reset_state()
		self.num_bits = json_data.get_num_output_nodes()

		self.slot_one_output = Behavior(json_data.get_t_1_lo(0), self.num_bits)
		self.slot_two_output = Behavior(json_data.get_t_2_lo(0), self.num_bits)

		self.epsilon = json_data.get_ml_epsilon()

		# self.pessimism = json_data.get_ml_pessimism()
		# self.extinction = json_data.get_ml_extinction()

		for i in range(json_data.get_low_phenotype(), json_data.get_high_phenotype()):
			if i >= json_data.get_t_1_lo(0) and i <= json_data.get_t_1_hi(0):
				continue
			if i >= json_data.get_t_2_lo(0) and i <= json_data.get_t_2_hi(0):
				continue

			self.other_output = Behavior(i, self.num_bits)
			break

	def reset_state(self):
		self.q_values = [0] * self.num_slots

	def get_probs(self):
		# using an epsilon-greedy policy

		max_q = np.max(self.q_values)

		probs = np.zeros(shape = (self.num_slots,))
		if max_q == 0:
			# This assumes there will never be negative q-values
			probs += 1 / self.num_slots
		else:
			max_val = np.argmax(self.q_values)
			probs[max_val] = 1 - self.epsilon
			probs += self.epsilon / self.num_slots
		return probs

	def is_ready_to_emit(self):
		return True

	def emit_behavior(self):
		output_slot = np.random.choice(a = range(self.num_slots), size = 1, p = self.get_probs())[0]

		self.last_output = output_slot

		if output_slot == 1:
			return self.slot_one_output
		if output_slot == 2:
			return self.slot_two_output

		return self.other_output

	def set_selection(self, FDF_mean, is_reinforced):

		if is_reinforced:
			reward = self.reward_multiplier * (40 / FDF_mean) ** self.reward_exponent
		else:
			reward = 0

		state_value = reward + self.discount_rate * np.max(self.q_values)
		curr_q = self.q_values[self.last_output]

		self.q_values[self.last_output] = curr_q + self.learning_rate * (state_value - curr_q)

