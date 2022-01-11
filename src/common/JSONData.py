'''
Created on May 24, 2021

@author: bleem
'''
import json

from src.common import Constants
from src.common import Converter

# Vanilla ETBD parameters
_EXPERIMENTS = "experiments"
_STAR_JSON = "*.json"
_SDID = "SDID"
_SCHED_TYPE_1 = "schedule_1_type"
_SCHED_TYPE_2 = "schedule_2_type"
_FDF_1 = "FDF_1"
_FDF_2 = "FDF_2"
_T_1_LO = "target_class_1_min"
_T_1_HI = "target_class_1_max"
_T_2_LO = "target_class_2_min"
_T_2_HI = "target_class_2_max"
_PUNISH_RI_IS_ENABLED = "punish_ri_is_enabled"
_EQUAL_PUNISHMENT_RI = "equal_punishment_ri"
_MUT_FUNC_PARAM = "mut_func_param"
_PROP_PUNISH_IS_ENABLED = "prop_punish_is_enabled"
_PROPORTION_PUNISHMENT = "proportion_punishment"
_PUNISH_1_RI_IS_ENABLED = "punish_1_ri_is_enabled"
_SINGLE_PUNISHMENT_RI = "single_punishment_ri"
_SCHED_VALUE_1 = "schedule_1_scale"
_SCHED_VALUE_2 = "schedule_2_scale"
_OUTPUT_PATH = "output_path"
_FILE_STUB = "file_stub"
_GENERATIONS = "run_duration"
_REPETITIONS = "repetitions"
_CHECK_IS_PUNISHMENT_OK = "check_is_punishment_ok"
_USE_GRAY_CODES = "use_gray_codes"
_DECAY_OF_TRANSFER = "decay_of_transfer"
_FOMO_A = "fomo_a"
_ADD_VISCOSITY = "add_viscosity"
_VISCOSITY_TICKS = "viscosity_ticks"
_VISCOSITY_SELECTED_INDEX = "viscosity_selected_index"
_NUM_BEHAVIORS = "num_behaviors"
_LOW_PHENOTYPE = "low_phenotype"
_HIGH_PHENOTYPE = "high_phenotype"
_PERCENT_TO_REPLACE = "percent_to_replace"
_PERCENT_TO_REPLACE_2 = "percent_to_replace_2"
_FITNESS_METHOD = "fitness_method"
_FITNESS_LANDSCAPE = "fitness_landscape"
_PUNISHMENT_METHOD = "punishment_method"
_ALPHA = "alpha"
_BETA_0 = "beta_0"
_BETA_1 = "beta_1"
_SELECTION_METHOD = "selection_method"
_CONTINUOUS_FUNCTION_FORM = "continuous_function_form"
_MATCHMAKING_METHOD = "matchmaking_method"
_RECOMBINATION_METHOD = "recombination_method"
_MUTATION_METHOD = "mutation_method"
_MUTATION_RATE = "mutation_rate"
_SCHEDULES = "schedules"
_CROSSOVER_POINTS = "crossover_points"
_GAUSSIAN_MUTATION_SD = "gaussian_mutation_sd"
_MUTATION_BOUNDARY = "mutation_boundary"
_RESET_BETWEEN_RUNS = "reset_between_runs"

# Non-ETBD organisms
_ORG_TYPE = "org_type"
_NUM_HIDDEN_NODES = "num_hidden_nodes"
_NUM_OUTPUT_NODES = "num_output_nodes"
_NET_ONE_NUM_FIRING_HIDDEN_NODES = "net_one_num_firing_hidden_nodes"
_NET_ONE_MAGNITUDE_SLOPE = "net_one_magnitude_slope"
_NET_ONE_MAGNITUDE_INTERCEPT = "net_one_magnitude_intercept"

# Stubbs and Pliskoff schedules
_USE_SP_SCHEDULES = "use_sp_schedules"
_SP_MEAN = "sp_mean"
_SP_RATIO = "sp_ratio"
_SP_FDF = "sp_FDF"
_SP_STOP_COUNT = "sp_stop_count"

# Vanilla ETBD parameters
_DEFAULT_MUTATION_RATE = 10
_DEFAULT_MUTATION_METHOD = "BITFLIP BY INDIVIDUAL"
_DEFAULT_RECOMBINATION_METHOD = "BITWISE"
_DEFAULT_MATCHMAKING_METHOD = "SEARCH"
_DEFAULT_CONTINUOUS_FUNCTION_FORM = "LINEAR"
_DEFAULT_SELECTION_METHOD = "CONTINUOUS"
_DEFAULT_BETA_1 = 1
_DEFAULT_BETA_0 = 1
_DEFAULT_ALPHA = 1
_DEFAULT_PUNISHMENT_METHOD = "FORCED MUTATION"
_DEFAULT_FITNESS_LANDSCAPE = "CIRCULAR"
_DEFAULT_FITNESS_METHOD = "INDIVIDUAL"
_DEFAULT_PERCENT_TO_REPLACE_2 = 100
_DEFAULT_PERCENT_TO_REPLACE = 100
_DEFAULT_HIGH_PHENOTYPE = 1023
_DEFAULT_LOW_PHENOTYPE = 0
_DEFAULT_NUM_BEHAVIORS = 100
_DEFAULT_SDID = Constants.SD_COLOR_RED
_DEFAULT_SCHED_TYPE = "VI"
_DEFAULT_FDF = 40
_DEFAULT_T_1_LO = 471
_DEFAULT_T_1_HI = 511
_DEFAULT_T_2_LO = 512
_DEFAULT_T_2_HI = 552
_DEFAULT_PUNISH_RI_IS_ENABLED = False
_DEFAULT_EQUAL_PUNISHMENT_RI = 0
_DEFAULT_MUT_FUNC_PARAM = None
_DEFAULT_PROP_PUNISH_IS_ENABLED = False
_DEFAULT_PROPORTION_PUNISHMENT = 0
_DEFAULT_PUNISH_1_RI_IS_ENABLED = False
_DEFAULT_SINGLE_PUNISHMENT_RI = 0
_DEFAULT_SCHED_VALUE = None
_DEFAULT_OUTPUT_PATH = None
_DEFAULT_FILE_STUB = "experiment"
_DEFAULT_GENERATIONS = 20500
_DEFAULT_REPETITIONS = 1
_DEFAULT_CHECK_IS_PUNISHMENT_OK = False
_DEFAULT_USE_GRAY_CODES = False
_DEFAULT_DECAY_OF_TRANSFER = 0
_DEFAULT_FOMO_A = 1
_DEFAULT_ADD_VISCOSITY = False
_DEFAULT_VISCOSITY_TICKS = 0
_DEFAULT_VISCOSITY_SELECTED_INDEX = 0
_DEFAULT_CROSSOVER_POINTS = 0
_DEFAULT_GAUSSIAN_MUTATION_SD = 10
_DEFAULT_MUTATION_BOUNDARY = Constants.MUTATION_BOUNDARY_WRAP
_DEFAULT_RESET_BETWEEN_RUNS = True

# Non-ETBD organisms
_DEFAULT_ORG_TYPE = "ETBD"
_DEFAULT_NUM_HIDDEN_NODES = 100
_DEFAULT_NUM_OUTPUT_NODES = 10
_DEFAULT_NONFHN = 2
_DEFAULT_NET_ONE_MAGNITUDE_SLOPE = -.378
_DEFAULT_NET_ONE_MAGNITUDE_INTERCEPT = .2

# Stubbs and Pliskoff schedules
_DEFAULT_USE_SP_SCHEDULES = False
_DEFAULT_SP_DENSITY = None
_DEFAULT_SP_RATIO = 1
_DEFAULT_SP_FDF = 40
_DEFAULT_SP_STOP_COUNT = 10


def load_file(input_file = None, print_status = False):
	if input_file is None:
		return None

	with open(input_file,) as exp_file:
		if print_status:
			print("reading from " + input_file)
		data = json.load(exp_file)
		return JSONData(data)


class JSONData(object):
	'''
	classdocs
	'''

	def __init__(self, data_dict = None):
		if data_dict is None:
			data_dict = {_EXPERIMENTS:{}}
		self.data_dict = data_dict

	def get_use_sp_schedules(self, experiment_index):
		return self.get_from_experiment(_USE_SP_SCHEDULES, experiment_index, _DEFAULT_USE_SP_SCHEDULES)

	def get_sp_ratio(self, experiment_index, schedule_index):
		return self.get_from_schedule(_SP_RATIO, experiment_index, schedule_index, _DEFAULT_SP_RATIO)

	def get_sp_mean(self, experiment_index, schedule_index):
		return self.get_from_schedule(_SP_MEAN, experiment_index, schedule_index, _DEFAULT_SP_DENSITY)

	def get_sp_FDF(self, experiment_index, schedule_index):
		return self.get_from_schedule(_SP_FDF, experiment_index, schedule_index, _DEFAULT_SP_FDF)

	def get_sp_stop_count(self, experiment_index, schedule_index):
		return self.get_from_schedule(_SP_STOP_COUNT, experiment_index, schedule_index, _DEFAULT_SP_STOP_COUNT)

	def get_net_one_magnitude_slope(self, experiment_index = 0):
		return self.get_from_experiment(_NET_ONE_MAGNITUDE_SLOPE, experiment_index, _DEFAULT_NET_ONE_MAGNITUDE_SLOPE)

	def get_net_one_magnitude_intercept(self, experiment_index = 0):
		return self.get_from_experiment(_NET_ONE_MAGNITUDE_INTERCEPT, experiment_index, _DEFAULT_NET_ONE_MAGNITUDE_INTERCEPT)

	def get_num_hidden_nodes(self):
		return self.get(_NUM_HIDDEN_NODES, _DEFAULT_NUM_HIDDEN_NODES)

	def get_num_output_nodes(self):
		return self.get(_NUM_OUTPUT_NODES, _DEFAULT_NUM_OUTPUT_NODES)

	def get_net_one_num_firing_hidden_nodes(self):
		return self.get(_NET_ONE_NUM_FIRING_HIDDEN_NODES, _DEFAULT_NONFHN)

	def get_num_experiments(self):
		return len(self.data_dict[_EXPERIMENTS])

	def get_reset_between_runs(self, experiment_index = 0):
		return self.get_from_experiment(_RESET_BETWEEN_RUNS, experiment_index, _DEFAULT_RESET_BETWEEN_RUNS)

	def get_organism_type(self):
		ret = self.get(_ORG_TYPE, _DEFAULT_ORG_TYPE)
		return Converter.convert_to_org_type(ret)

	def get_sd(self, experiment_index = -1):
		ret = self.get_from_experiment(_SDID, experiment_index, _DEFAULT_SDID)
		return Converter.convert_sd_id_to_color(ret)

	def get_sdid(self, experiment_index = -1):
		return self.get_from_experiment(_SDID, experiment_index, _DEFAULT_SDID)

	def get_from_experiment(self, key, experiment_index, default = None):
		default = self.get(key, default)
		experiment = self.get_experiment(experiment_index)
		if experiment is None:
			return default
		return experiment.get(key, default)

	def get_num_schedules(self, experiment_index):
		experiment = self.get_experiment(experiment_index)
		if experiment is None:
			return 0
		schedules = experiment["schedules"]
		if schedules is None:
			return 0
		return len(schedules)

	def get_from_schedule(self, key, experiment_index, schedule_index, default = None):
		default = self.get(key, default)
		experiment = self.get_experiment(experiment_index)
		if experiment is None:
			return default
		default = self.get_from_experiment(key, experiment_index, default)
		schedules = experiment["schedules"]
		if schedules is None or schedule_index >= len(schedules) or schedule_index < 0:
			return default
		schedule = schedules[schedule_index]
		if schedule is None:
			return default
		return schedule.get(key, default)

	def get_schedule(self, schedule_index):
		raise NotImplementedError

	def get(self, key, default = None):
		return self.data_dict.get(key, default)

	def get_experiment(self, experiment_index):
		experiments = self.data_dict[_EXPERIMENTS]
		if experiments is None or experiment_index < 0 or experiment_index >= len(experiments):
			return None
		return experiments[experiment_index]

	def get_sched_type_1(self, experiment_index, schedule_index = -1):
		if self.get_use_sp_schedules(experiment_index):
			ret = "SP"
		else:
			ret = self.get_from_schedule(_SCHED_TYPE_1, experiment_index, schedule_index, _DEFAULT_SCHED_TYPE)
		return Converter.convert_to_sched_type(ret)

	def get_sched_type_2(self, experiment_index, schedule_index = -1):
		if self.get_use_sp_schedules(experiment_index):
			ret = "SP"
		else:
			ret = self.get_from_schedule(_SCHED_TYPE_2, experiment_index, schedule_index, _DEFAULT_SCHED_TYPE)
		return Converter.convert_to_sched_type(ret)

	def get_FDF_mean_1(self, experiment_index, schedule_index):
		return self.get_from_schedule(_FDF_1, experiment_index, schedule_index, _DEFAULT_FDF)

	def get_FDF_mean_2(self, experiment_index, schedule_index):
		return self.get_from_schedule(_FDF_2, experiment_index, schedule_index, _DEFAULT_FDF)

	def get_t_1_lo(self, experiment_index):
		return self.get_from_experiment(_T_1_LO, experiment_index, _DEFAULT_T_1_LO)

	def get_t_1_hi(self, experiment_index):
		return self.get_from_experiment(_T_1_HI, experiment_index, _DEFAULT_T_1_HI)

	def get_t_2_lo(self, experiment_index):
		return self.get_from_experiment(_T_2_LO, experiment_index, _DEFAULT_T_2_LO)

	def get_t_2_hi(self, experiment_index):
		return self.get_from_experiment(_T_2_HI, experiment_index, _DEFAULT_T_2_HI)

	def punish_RI_is_enabled(self):
		return self.get_from_experiment(_PUNISH_RI_IS_ENABLED, _DEFAULT_PUNISH_RI_IS_ENABLED)

	def get_equal_punishment_ri(self, experiment_index):
		return self.get_from_experiment(_EQUAL_PUNISHMENT_RI, experiment_index, _DEFAULT_EQUAL_PUNISHMENT_RI)

	def get_mut_func_param(self, experiment_index):
		return self.get_from_experiment(_MUT_FUNC_PARAM, experiment_index, _DEFAULT_MUT_FUNC_PARAM)

	def prop_punish_is_enabled(self, experiment_index):
		return self.get_from_experiment(_PROP_PUNISH_IS_ENABLED, experiment_index, _DEFAULT_PROP_PUNISH_IS_ENABLED)

	def get_proportion_punishment(self, experiment_index, schedule_index):
		return self.get_from_schedule(_PROPORTION_PUNISHMENT, experiment_index, schedule_index, _DEFAULT_PROPORTION_PUNISHMENT)

	def punish_1_RI_is_enabled(self, experiment_index):
		return self.get_from_experiment(_PUNISH_1_RI_IS_ENABLED, experiment_index, _DEFAULT_PUNISH_1_RI_IS_ENABLED)

	def get_equal_punishment_RI(self, experiment_index, schedule_index = -1):
		return self.get_from_schedule(_EQUAL_PUNISHMENT_RI, experiment_index, schedule_index, _DEFAULT_EQUAL_PUNISHMENT_RI)

	def get_single_punishment_RI(self, experiment_index, schedule_index = -1):
		return self.get_from_schedule(_SINGLE_PUNISHMENT_RI, experiment_index, schedule_index, _DEFAULT_SINGLE_PUNISHMENT_RI)

	def get_sched_value_1(self, experiment_index, schedule_index):
		return self.get_from_schedule(_SCHED_VALUE_1, experiment_index, schedule_index, _DEFAULT_SCHED_VALUE)

	def get_sched_value_2(self, experiment_index, schedule_index):
		return self.get_from_schedule(_SCHED_VALUE_2, experiment_index, schedule_index, _DEFAULT_SCHED_VALUE)

	def get_output_path(self, experiment_index):
		return self.get_from_experiment(_OUTPUT_PATH, experiment_index, _DEFAULT_OUTPUT_PATH)

	def get_file_stub(self, experiment_index):
		return self.get_from_experiment(_FILE_STUB, experiment_index, _DEFAULT_FILE_STUB)

	def get_generations(self, experiment_index):
		return self.get_from_experiment(_GENERATIONS, experiment_index, _DEFAULT_GENERATIONS)

	def get_repetitions(self, experiment_index):
		return self.get_from_experiment(_REPETITIONS, experiment_index, _DEFAULT_REPETITIONS)

	def check_is_punishment_ok(self):
		return self.get(_CHECK_IS_PUNISHMENT_OK, _DEFAULT_CHECK_IS_PUNISHMENT_OK)

	def use_gray_codes(self):
		return self.get(_USE_GRAY_CODES, _DEFAULT_USE_GRAY_CODES)

	def get_decay_of_transfer(self):
		return self.get(_DECAY_OF_TRANSFER, _DEFAULT_DECAY_OF_TRANSFER)

	def get_fomo_a(self):
		return self.get(_FOMO_A, _DEFAULT_FOMO_A)

	def add_viscosity(self):
		return self.get(_ADD_VISCOSITY, _DEFAULT_ADD_VISCOSITY)

	def get_viscosity_ticks(self, experiment_index):
		return self.get_from_experiment(_VISCOSITY_TICKS, experiment_index, _DEFAULT_VISCOSITY_TICKS)

	def get_viscosity_selected_index(self, experiment_index):
		return self.get_from_experiment(_VISCOSITY_SELECTED_INDEX, experiment_index, _DEFAULT_VISCOSITY_SELECTED_INDEX)

	def get_num_behaviors(self):
		return self.get(_NUM_BEHAVIORS, _DEFAULT_NUM_BEHAVIORS)

	def get_low_phenotype(self):
		return self.get(_LOW_PHENOTYPE, _DEFAULT_LOW_PHENOTYPE)

	def get_high_phenotype(self):
		return self.get(_HIGH_PHENOTYPE, _DEFAULT_HIGH_PHENOTYPE)

	def get_percent_to_replace(self):
		return self.get(_PERCENT_TO_REPLACE, _DEFAULT_PERCENT_TO_REPLACE)

	def get_percent_to_replace_2(self):
		return self.get(_PERCENT_TO_REPLACE_2, _DEFAULT_PERCENT_TO_REPLACE_2)

	def get_fitness_method(self):
		ret = self.get(_FITNESS_METHOD, _DEFAULT_FITNESS_METHOD)
		return Converter.convert_to_fitness_method(ret)

	def get_fitness_landscape(self):
		ret = self.get(_FITNESS_LANDSCAPE, _DEFAULT_FITNESS_LANDSCAPE)
		return Converter.convert_to_fitness_landscape(ret)

	def get_punishment_method(self):
		ret = self.get(_PUNISHMENT_METHOD, _DEFAULT_PUNISHMENT_METHOD)
		return Converter.convert_to_punishment_method(ret)

	def get_alpha(self):
		return self.get(_ALPHA, _DEFAULT_ALPHA)

	def get_beta_0(self):
		return self.get(_BETA_0, _DEFAULT_BETA_0)

	def get_beta_1(self):
		return self.get(_BETA_1, _DEFAULT_BETA_1)

	def get_selection_method(self):
		ret = self.get(_SELECTION_METHOD, _DEFAULT_SELECTION_METHOD)
		return Converter.convert_to_selection_method(ret)

	def get_continuous_function_form(self):
		ret = self.get(_CONTINUOUS_FUNCTION_FORM, _DEFAULT_CONTINUOUS_FUNCTION_FORM)
		return Converter.convert_to_continuous_function_form(ret)

	def get_matchmaking_method(self):
		ret = self.get(_MATCHMAKING_METHOD, _DEFAULT_MATCHMAKING_METHOD)
		return Converter.convert_to_matchmaking_method(ret)

	def get_crossover_points(self, experiment_index):
		return self.get_from_experiment(_CROSSOVER_POINTS, experiment_index, _DEFAULT_CROSSOVER_POINTS)

	def get_recombination_method(self):
		ret = self.get(_RECOMBINATION_METHOD, _DEFAULT_RECOMBINATION_METHOD)
		return Converter.convert_to_recombination_method(ret)

	def get_mutation_method(self):
		ret = self.get(_MUTATION_METHOD, _DEFAULT_MUTATION_METHOD)
		return Converter.convert_to_mutation_method(ret)

	def get_gaussian_mutation_sd(self, experiment_index):
		return self.get_from_experiment(_GAUSSIAN_MUTATION_SD, experiment_index, _DEFAULT_GAUSSIAN_MUTATION_SD)

	def get_mutation_boundary(self, experiment_index):
		ret = self.get_from_experiment(_MUTATION_BOUNDARY, experiment_index, _DEFAULT_MUTATION_BOUNDARY)
		return Converter.convert_to_mutation_boundary(ret)

	def get_mutation_rate(self):
		return self.get(_MUTATION_RATE, _DEFAULT_MUTATION_RATE)

