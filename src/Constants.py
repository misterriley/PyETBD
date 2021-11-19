'''
Created on May 21, 2021
Translated May 23, 2021

@author: bleem
'''

SD_COLOR_RED = 0
SD_COLOR_ORANGE = 1
SD_COLOR_YELLOW = 2
SD_COLOR_GREEN = 3
SD_COLOR_BLUE = 4
SD_COLOR_INDIGO = 5
SD_COLOR_VIOLET = 6
SD_COLOR_NULL = -999  # Added at Nick's request

FITNESS_METHOD_MIDPOINT = 1
FITNESS_METHOD_INDIVIDUAL = 2
FITNESS_METHOD_ENTIRE_CLASS = 3

FITNESS_LANDSCAPE_FLAT = 1
FITNESS_LANDSCAPE_CIRCULAR = 2

PUNISHMENT_METHOD_REPEL_FOLD = 1
PUNISHMENT_METHOD_REPEL_WRAP = 2
PUNISHMENT_METHOD_FORCED_MUTATION = 3

CONTINUOUS_FUNCTION_FORM_NOT_APPLICABLE = 0
CONTINUOUS_FUNCTION_FORM_LINEAR = 1
CONTINUOUS_FUNCTION_FORM_UNIFORM = 2
CONTINUOUS_FUNCTION_FORM_EXPONENTIAL = 3

RECOMBINATION_METHOD_BITWISE = 1
RECOMBINATION_METHOD_CROSSOVER = 2
RECOMBINATION_METHOD_CLONE = 3

SELECTION_METHOD_TRUNCATION = 1
SELECTION_METHOD_TOURNAMENT = 2
SELECTION_METHOD_CONTINUOUS = 3

MUTATION_METHOD_GAUSSIAN = 1
MUTATION_METHOD_BIT_FLIP_BY_INDIVIDUAL = 2
MUTATION_METHOD_BIT_FLIP_BY_BIT = 3
MUTATION_METHOD_RANDOM_INDIVIDUAL = 4

MUTATION_BOUNDARY_WRAP = 1
MUTATION_BOUNDARY_DISCARD = 2

MATCHMAKING_METHOD_SEARCH = 1
MATCHMAKING_METHOD_MATING_POOL = 2  # May want to delay implementing this.

SCHED_TYPE_RI = 0
SCHED_TYPE_RR = 1
SCHED_TYPE_EXT = 2
SCHED_TYPE_PROB = 3
