'''
Created on Nov 18, 2021

@author: bleem
'''
from src.common import Constants

_MUT_METHOD_DICT = {
	"BITFLIP BY INDIVIDUAL":Constants.MUTATION_METHOD_BIT_FLIP_BY_INDIVIDUAL,
	"BITFLIP BY BIT":Constants.MUTATION_METHOD_BIT_FLIP_BY_BIT,
	"GAUSSIAN":Constants.MUTATION_METHOD_GAUSSIAN,
	"RANDOM INDIVIDUAL":Constants.MUTATION_METHOD_RANDOM_INDIVIDUAL
	}

_RECOMB_METHOD_DICT = {
	"BITWISE": Constants.RECOMBINATION_METHOD_BITWISE,
	"CLONE": Constants.RECOMBINATION_METHOD_CLONE,
	"CROSSOVER": Constants.RECOMBINATION_METHOD_CROSSOVER
	}

_MATCHMAKING_METHOD_DICT = {
	"MATING POOL": Constants.MATCHMAKING_METHOD_MATING_POOL,
	"SEARCH": Constants.MATCHMAKING_METHOD_SEARCH
	}

_CONT_FUNC_FORM_DICT = {
	"EXPONENTIAL": Constants.CONTINUOUS_FUNCTION_FORM_EXPONENTIAL,
	"LINEAR": Constants.CONTINUOUS_FUNCTION_FORM_LINEAR,
	"NA": Constants.CONTINUOUS_FUNCTION_FORM_NOT_APPLICABLE,
	"UNIFORM": Constants.CONTINUOUS_FUNCTION_FORM_UNIFORM
	}

_SEL_METHOD_DICT = {
	"CONTINUOUS": Constants.SELECTION_METHOD_CONTINUOUS,
	"TOURNAMENT": Constants.SELECTION_METHOD_TOURNAMENT,
	"TRUNCATION": Constants.SELECTION_METHOD_TRUNCATION
	}

_PUN_METHOD_DICT = {
	"FORCED MUTATION": Constants.PUNISHMENT_METHOD_FORCED_MUTATION,
	"REPEL FOLD": Constants.PUNISHMENT_METHOD_REPEL_FOLD,
	"REPEL WRAP": Constants.PUNISHMENT_METHOD_REPEL_WRAP
	}

_FITNESS_METHOD_DICT = {
	"MIDPOINT": Constants.FITNESS_METHOD_MIDPOINT,
	"INDIVIDUAL": Constants.FITNESS_METHOD_INDIVIDUAL,
	"ENTIRE_CLASS": Constants.FITNESS_METHOD_ENTIRE_CLASS
	}

_FITNESS_LANDSCAPE_DICT = {
	"CIRCULAR": Constants.FITNESS_LANDSCAPE_CIRCULAR,
	"FLAT": Constants.FITNESS_LANDSCAPE_FLAT
	}

_SCHED_TYPE_DICT = {
	"RI": Constants.SCHED_TYPE_RI,
	"RR": Constants.SCHED_TYPE_RR,
	"PROB": Constants.SCHED_TYPE_PROB,
	"EXT": Constants.SCHED_TYPE_EXT,
	"SP": Constants.SCHED_TYPE_SP
	}

_MUT_BOUNDARY_DICT = {
	"WRAP": Constants.MUTATION_BOUNDARY_WRAP,
	"DISCARD": Constants.MUTATION_BOUNDARY_WRAP
	}

_SD_COLOR_DICT = {
	"RED": Constants.SD_COLOR_RED,
	"ORANGE": Constants.SD_COLOR_ORANGE,
	"YELLOW": Constants.SD_COLOR_YELLOW,
	"GREEN": Constants.SD_COLOR_GREEN,
	"BLUE": Constants.SD_COLOR_BLUE,
	"INDIGO": Constants.SD_COLOR_INDIGO,
	"VIOLET": Constants.SD_COLOR_VIOLET,
	"NULL": Constants.SD_COLOR_NULL
	}

_ORG_TYPE_DICT = {
	"ETBD":Constants.ORG_TYPE_ETBD,
	"NET_ONE":Constants.ORG_TYPE_NET_ONE,
	"NET_TWO":Constants.ORG_TYPE_NET_TWO,
	"PG":Constants.ORG_TYPE_PG,
	"QL": Constants.ORG_TYPE_QL
	}


def _generic_convert_to_constant(value, _dict):
	ret = _dict.get(value)
	if ret is None:
		raise AssertionError(str(value) + " not in dict: " + str(_dict))
	return ret


def _generic_const_to_string(value, _dict):
	for k in _dict:
		v = _dict.get(k)
		if v == value:
			return k

	raise AssertionError("Value " + str(value) + " not found in dict " + str(dict))


def convert_to_org_type(value):
	return _generic_convert_to_constant(value, _ORG_TYPE_DICT)


def convert_org_type_to_string(value):
	return _generic_const_to_string(value, _ORG_TYPE_DICT)


def convert_color_to_sd_id(value):
	return _generic_convert_to_constant(value, _SD_COLOR_DICT)


def convert_sd_id_to_color(value):
	return _generic_const_to_string(value, _SD_COLOR_DICT)


def convert_to_mutation_boundary(value):
	return _generic_convert_to_constant(value, _MUT_BOUNDARY_DICT)


def convert_mutation_boundary_to_string(value):
	return _generic_const_to_string(value, _MUT_BOUNDARY_DICT)


def convert_mutation_method_to_string(value):
	return _generic_const_to_string(value, _MUT_METHOD_DICT)


def convert_to_mutation_method(value):
	return _generic_convert_to_constant(value, _MUT_METHOD_DICT)


def convert_to_recombination_method(value):
	return _generic_convert_to_constant(value, _RECOMB_METHOD_DICT)


def convert_recombination_method_to_string(value):
	return _generic_const_to_string(value, _RECOMB_METHOD_DICT)


def convert_to_matchmaking_method(value):
	return _generic_convert_to_constant(value, _MATCHMAKING_METHOD_DICT)


def convert_matchmaking_method_to_string(value):
	return _generic_const_to_string(value, _MATCHMAKING_METHOD_DICT)


def convert_to_continuous_function_form(value):
	return _generic_convert_to_constant(value, _CONT_FUNC_FORM_DICT)


def convert_continuous_function_form_to_string(value):
	return _generic_const_to_string(value, _CONT_FUNC_FORM_DICT)


def convert_to_selection_method(value):
	return _generic_convert_to_constant(value, _SEL_METHOD_DICT)


def convert_selection_method_to_string(value):
	return _generic_const_to_string(value, _SEL_METHOD_DICT)


def convert_to_punishment_method(value):
	return _generic_convert_to_constant(value, _PUN_METHOD_DICT)


def convert_punishment_method_to_string(value):
	return _generic_const_to_string(value, _PUN_METHOD_DICT)


def convert_to_fitness_method(value):
	return _generic_convert_to_constant(value, _FITNESS_METHOD_DICT)


def convert_fitness_method_to_string(value):
	return _generic_const_to_string(value, _FITNESS_METHOD_DICT)


def convert_to_fitness_landscape(value):
	return _generic_convert_to_constant(value, _FITNESS_LANDSCAPE_DICT)


def convert_fitness_landscape_to_string(value):
	return _generic_const_to_string(value, _FITNESS_LANDSCAPE_DICT)


def convert_to_sched_type(value):
	# common aliases
	if value == "VI":
		value = "RI"
	if value == "VR":
		value = "RR"

	return _generic_convert_to_constant(value, _SCHED_TYPE_DICT)


def convert_sched_type_to_string(value):
	return _generic_const_to_string(value, _SCHED_TYPE_DICT)
