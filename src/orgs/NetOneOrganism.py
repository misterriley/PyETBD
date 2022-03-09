'''
Created on Dec 7, 2021

@author: bleem
'''
import numpy

from src.common.Behavior import Behavior
from src.orgs.AnOrganism import AnOrganism


class NetOneOrganism(AnOrganism):

	def __init__(self, json_data):
		super().__init__(json_data)
		self.num_hidden_nodes = json_data.get_num_hidden_nodes()
		self.num_output_nodes = json_data.get_num_output_nodes()
		self.hidden_firing_nodes = json_data.get_num_firing_hidden_nodes()
		self.mutation_rate = json_data.get_net_one_mutation_rate_multiplier() * json_data.get_mutation_rate()
		self.net_one_magnitude_slope = json_data.get_net_one_magnitude_slope()
		self.net_one_magnitude_intercept = json_data.get_net_one_magnitude_intercept()
		self.net_one_neutral_magnitude = json_data.get_net_one_neutral_magnitude()

	def reset_state(self):
		# real-valued synapse matrix, dimension is h x o (h = num hidden, o = num output)
		synapse_matrix_shape = (self.num_hidden_nodes, self.num_output_nodes)
		self.synapses = 2 * numpy.random.binomial(1, .5, size = synapse_matrix_shape) - 1

		# initialize the hidden and output nodes to zero
		self.hidden_nodes = numpy.zeros(self.num_hidden_nodes, dtype = float)
		self.output_nodes = numpy.zeros(self.num_output_nodes, dtype = float)

		# an internal array for use in matrix multiplication
		self.raw_outputs = numpy.zeros(self.num_output_nodes, dtype = float)

	def is_ready_to_emit(self):
		return True

	def emit_behavior(self):
		self.generate_hiddens()

		# now build the raw outputs, which will then be passed through the activation function
		numpy.matmul(self.hidden_nodes, self.synapses, out = self.raw_outputs)

		# lambda functions with explicit logical operators don't work when applied
		# across an array, so we must use numpy.where()
		#
		# the activation for net one is a step function
		# y = 1  if x > 0
		# y = .5 if x == 0
		# y = 0  if x < 0
		activation = lambda x: numpy.where(x > 0, 1, numpy.where(x < 0, 0, .5))

		# now apply the activation function to the raw output and fire based on these probabilities
		probs = activation(self.raw_outputs)
		rands = numpy.random.uniform(size = self.num_output_nodes)
		self.output_nodes = (probs > rands).astype(int)
		return Behavior(numpy.concatenate(([None], self.output_nodes)))  # ETBD comes from VB that is one-indexed and I haven't changed that yet

	def generate_hiddens(self):
		# for type one, we have exactly two nodes that fire
		self.hidden_nodes.fill(0)
		on_bits = numpy.random.choice(range(len(self.hidden_nodes)), self.hidden_firing_nodes, replace = False)
		self.hidden_nodes[on_bits] = 1

	@staticmethod
	def convert_selection_param(selectionParameter, net_one_magnitude_intercept, net_one_magnitude_slope):
		# the selection parameter comes in as an FDF, must go out as a probability of flipping synapses
		# selectionParameter == infinity --> return 0
		# selectionParameter == 0 --> return 1
		return net_one_magnitude_intercept + net_one_magnitude_slope * numpy.log10(selectionParameter / 40)

	def set_selection(self, selectionParameter, value):

		if value:
			converted_selection_param = self.convert_selection_param(selectionParameter, self.net_one_magnitude_intercept, self.net_one_magnitude_slope)
		else:
			converted_selection_param = self.net_one_neutral_magnitude

		# for net type one, reinforcement probabilistically flips some synapses toward the output
		target_weights = numpy.array([2 * self.output_nodes - 1, ] * self.num_hidden_nodes)
		rands = numpy.random.uniform(size = target_weights.shape)
		self.synapses = numpy.where(rands < converted_selection_param, target_weights, self.synapses)

		self.apply_mutation()

	def apply_mutation(self):

		# the following code would flip each bit independently - it doesn't seem to matter which one I use
		#
		# # rands = numpy.random.uniform(size = self.num_hidden_nodes)
		#
		# # flips = rands < self.mutation_rate / 100.0
		# # flipped_nodes = flips.nonzero()[0]
		# # locs = numpy.random.randint(0, self.num_output_nodes, size = len(flipped_nodes))
		# # for i in range(len(flipped_nodes)):
		# 	# self.synapses[flipped_nodes[i], locs[i]] *= -1
		#
		#

		# mutation in net one means randomly flipping some weights 1 --> -1 or -1 --> 1
		flipped_weights = self.synapses * -1

		rands = numpy.random.uniform(size = flipped_weights.shape)
		mutation_rate = self.mutation_rate

		mutation_prob = (mutation_rate / 100.0) / self.num_output_nodes

		self.synapses = numpy.where(rands < mutation_prob, flipped_weights, self.synapses)

