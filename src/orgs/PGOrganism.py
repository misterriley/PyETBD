'''
Created on Feb 1, 2022

@author: bleem
'''

from src.common.Behavior import Behavior
from src.orgs.AnOrganism import AnOrganism
import numpy as np


class PGOrganism(AnOrganism):

	def __init__(self, json_data):
		super().__init__(json_data)
		self.num_slots = json_data.get_ml_num_slots()  # must be at least 3 or this code will not work
		self.learning_rate = json_data.get_ml_learning_rate()
		# self.discount_rate = json_data.get_ml_discount_rate()
		# self.reward_multiplier = json_data.get_ml_reward_multiplier()
		self.reward_exponent = json_data.get_ml_reward_exponent()
		self.reset_state()
		self.num_bits = json_data.get_num_output_nodes()

		self.slot_one_output = Behavior(json_data.get_t_1_lo(0), self.num_bits)
		self.slot_two_output = Behavior(json_data.get_t_2_lo(0), self.num_bits)

		self.pessimism = json_data.get_ml_pessimism()
		self.extinction = json_data.get_ml_extinction()

		for i in range(json_data.get_low_phenotype(), json_data.get_high_phenotype()):
			if i >= json_data.get_t_1_lo(0) and i <= json_data.get_t_1_hi(0):
				continue
			if i >= json_data.get_t_2_lo(0) and i <= json_data.get_t_2_hi(0):
				continue

			self.other_output = Behavior(i, self.num_bits)
			break

	def reset_state(self):
		self.policy_params = [1 / self.num_slots] * self.num_slots

	def is_ready_to_emit(self):
		return True

	def emit_behavior(self):
		output_slot = np.random.choice(a = range(self.num_slots), size = 1, p = self.policy_params)[0]

		self.last_output = output_slot

		if output_slot == 1:
			return self.slot_one_output
		if output_slot == 2:
			return self.slot_two_output

		return self.other_output

	def set_selection(self, FDF_mean, is_reinforced):
		if is_reinforced:
			break_here = 0

		grad_log_pi = np.array([0] * self.num_slots)
		grad_log_pi[self.last_output] = 1 / (self.policy_params[self.last_output])
		reward = (40 / FDF_mean) ** self.reward_exponent if is_reinforced else 0
		self.policy_params += self.learning_rate * reward * grad_log_pi
		self.policy_params[self.last_output] *= self.pessimism
		self.policy_params /= np.sum(self.policy_params)

		self.policy_params += self.extinction
		self.policy_params /= np.sum(self.policy_params)

