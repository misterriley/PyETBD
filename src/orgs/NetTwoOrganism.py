'''
Created on Dec 7, 2021

@author: bleem
'''

import numpy

from src.common.Behavior import Behavior
from src.orgs.AnOrganism import AnOrganism


class NetTwoOrganism(AnOrganism):

	def __init__(self, json_data):
		super().__init__(json_data)
		self.num_hidden_nodes = json_data.get_net_two_num_hidden_nodes()
		self.num_hidden_firing_nodes = json_data.get_num_firing_hidden_nodes()
		self.num_output_nodes = json_data.get_num_output_nodes()

		# divide by 100 since raw mutation rate is expressed as a percent (e.g., 10 means 10%)
		self.mutation_multiplier = 1 - 2 * json_data.get_mutation_rate() / (100 * self.num_output_nodes)  # Appendix A for derivation

		self.net_two_selection_strength_multiplier = json_data.get_net_two_selection_strength_multiplier()
		self.net_two_selection_strength_exponent = json_data.get_net_two_selection_strength_exponent()
		self.net_two_neutral_magnitude = json_data.get_net_two_neutral_magnitude()

		self.reset_state()

	def reset_state(self):
		# real-valued synapse matrix, dimension is h x o (h = num hidden, o = num output)
		synapse_matrix_shape = (self.num_hidden_nodes, self.num_output_nodes)
		self.synapses = numpy.zeros(synapse_matrix_shape, dtype = float)

		# initialize the hidden and output nodes to zero
		self.hidden_nodes = numpy.zeros(self.num_hidden_nodes, dtype = float)
		self.output_nodes = numpy.zeros(self.num_output_nodes, dtype = float)

		# an internal array for use in matrix multiplication
		self.raw_outputs = numpy.zeros(self.num_output_nodes, dtype = float)

	def is_ready_to_emit(self):
		return True

	def emit_behavior(self):

		self.generate_hiddens()
		numpy.matmul(self.hidden_nodes, self.synapses, out = self.raw_outputs)

		# logistic sigmoid activation function for net two
		# the -4 creates a derivative of y'= 1 at x = 0, which simplifies the math elsewhere
		activation = lambda x: 1 / (1 + numpy.exp(-4 * x))
		probs = activation(self.raw_outputs)
		rands = numpy.random.uniform(size = self.num_output_nodes)
		self.output_nodes = (probs > rands).astype(int)
		return Behavior(numpy.concatenate(([None], self.output_nodes)))  # ETBD comes from VB that is one-indexed and I haven't changed that yet

	def generate_hiddens(self):
		# for type two, each node fires independently
		self.hidden_nodes.fill(0)
		on_bits = numpy.random.choice(range(len(self.hidden_nodes)), self.num_hidden_firing_nodes, replace = False)
		self.hidden_nodes[on_bits] = 1

	def convert_selection_parameter(self, selectionParameter):
		net_two_selection_parameter = self.net_two_selection_strength_multiplier * ((selectionParameter / 40) ** self.net_two_selection_strength_exponent)
		return net_two_selection_parameter

	def set_selection(self, selectionParameter, reinforced):

		shift_strength = self.net_two_neutral_magnitude
		if reinforced:
			shift_strength += self.convert_selection_parameter(selectionParameter)

		# the encoding of the outputs in synapse space: 1 --> 1, 0 --> -1
		synapse_shift = 2 * self.output_nodes - 1

		# the direction of the shift is the output masked by the hidden firing pattern, which is the outer product
		# this rule is discussed in the appendix
		target_weights = numpy.outer(self.hidden_nodes, synapse_shift)
		delta = target_weights * shift_strength

		# for net type two, reinforcement shifts all weights toward the output, so long as the hidden neuron has fired
		self.synapses += delta

		self.apply_mutation()

	def apply_mutation(self):
		# mutation in net two means contracting the synapse matrix toward zero
		self.synapses *= self.mutation_multiplier
