# Strucure of the JSON files in PyETBD/exp_files/

PyETBD accepts JSON files as descriptions of sessions for the ETBD. Each session contains a number of experiments, and each experiment runs the organism through a set of reinforcement and possibly punishment schedules. These files are expected to have the following format:


    global parameters
    "experiments":
        [
            {
                experiment 1 parameters
                "schedules":
                    [
                        {
                            schedule 1 parameters
                        },
                        {
                            schedule 2 parameters
                        },
                        
                        ...
                        
                    ]
            },
            {
                experiment 2 parameters
                "schedules":
                
                ...
                
            }
    
            ...
    
        ]

When searching for a parameter, PyETBD will override values set at a high level with those set at a low level. Thus if experiment 1 and schedule 1 have different settings for the same parameter, the schedule-level setting takes precedence.  The order of precedence is default < global < experiment-level < schedule-level. 

The list of parameters and their default values are as follows. Keys for parameters must be quoted. Not all parameters make sense at all levels and will have no effect if set. For instance, setting the output_path parameter at the schedule level would not make sense since several schedules are grouped into an output file. 

Note: not all of these have been tested. Some are never used in practice. 

## Keys

"SDID"
ID value for discriminative stimulus. 
May be integers 0 - 6 for the rainbow colors ROYGBIV, or -999 indicating no SD.
Default: 0 (RED)

"schedule_1_type"
"schedule_2_type"
The types of reinforcement schedules applied to the two target classes.
May be "RI", "VI", "RR", "VR", "PROB" or "EXT".
Default: "RI"

"FDF_1"
"FDF_2"
The fitness density functions for the two target classes.
May be a positive number.
Default: 40

"target_class_1_min"
"target_class_1_max"
"target_class_2_min"
"target_class_2_max"
Boundaries of the target classes.
May be integers between low_phenotype and high_phenotype, inclusive.
Default: 471, 511, 512, and 552

"punish_ri_is_enabled"
Do we enable RI punishment? 
Default: False

"equal_punishment_ri"
The RI value fo equal punishment. Has no effect if punish_ri_is_enabled is False.
Default: 0

"mut_func_param"
A generic parameter passed to the mutation function.
Default: None

"prop_punish_is_enabled"
Do we enable proportion punishment?
Default: False

"proportion_punishment"
The proportion (w.r.t. reinforcement density) that the punishment should be. Has no effect if prop_punish_is_enabled is False.
Default: 0

"punish_1_ri_is_enabled"
Do we enable single-sided RI punishment?
Default: False

"single_punishment_ri"
RI for punishment on target class 1. Has no effect if punish_1_ri_is_enabled is false.
Default: 0

"schedule_1_scale"
"schedule_2_scale"
RI or RR values used by the reinforcement schedules applied to the two target classes.
Default: None. These values must be supplied or PyETBD will not run.

"output_path"
Folder for the output files.
Default: "/outputs/"

"file_stub"
The name of the output xlsx file with no suffix.
Default: "experiments"

"run_duration"
How many generations to run the schedule for.
Default: 20500

"repetitions"
How many times to repeat each schedule.
Default: 1

"check_is_punishment_ok"
Should we do a sanity check on punishment parameters?
Default: False

"use_gray_codes"
Should we use Gray Codes rather than binary for the genotypes?
Default: False

"decay_of_transfer"
Legacy variable.
Default: 0

"fomo_a"
The FOMO exponent for punishment. Has no effect if punishment is not enabled.
Default: 1

"add_viscosity"
Legacy variable.
Default: False

"viscosity_ticks"
Legacy variable.
Default: 0

"viscosity_selected_index"
Legacy variable.
Default: 0

"num_behaviors"
How many behaviors per population.
Default: 100

"low_phenotype"
Lowest value of the phenotype range.
Default: 0

"high_phenotype"
Highest value of the phenotype range.
Default: 1023

"percent_to_replace"
Percent of population to replace when selection occurs.
May be an integer from 0 to 100.
Default: 100

"percent_to_replace_2"
Percent of population to replace when selection *does not* occur.
Default: 100

"fitness_method"
The method of determining the fitness of behaviors in the population. 
May be "MIDPOINT", "INDIVIDUAL", or "ENTIRE CLASS".
Default: "INDIVIDUAL"

"fitness_landscape"
What is the topology of the phenotype space?
May be "CIRCULAR" or "FLAT".
Default "CIRCULAR"

"punishment_method"
What method of punishment do we use?
May be "FORCED MUTATION", "REPEL FOLD" or "REPEL WRAP".
Default: "FORCED MUTATION"

"alpha"
"beta_0"
"beta_1"
Parameters for Rescorla-Wagner associative strength calculations. 
Defaults: 1, 1, 1

"selection_method"
How to do the selection step?
May be "CONTINUOUS", "TOURNAMENT" or "TRUNCATION"
Default: "CONTINUOUS"

"continuous_function_form"
What form does the selection function take? Has no effect if selection_method is not "CONTINUOUS".
May be "EXPONENTIAL", "LINEAR", "UNIFORM", or "NA"
Default: "LINEAR"

"matchmaking_method"
How are parents of the new generation selected?
May be "SEARCH" or "MATING POOL"
Default: "SEARCH"

"recombination_method"
How are new children created from selected parents?
May be "BITWISE", "CLONE", or "CROSSOVER"
Default: "BITWISE"

"mutation_method"
How is mutation applied?
May be "BITFLIP BY INDIVIDUAL", "BITFLIP BY BIT", "GAUSSIAN" or "RANDOM INDIVIDUAL"
Default: "BITFLIP BY INDIVIDUAL"

"mutation_rate"
What percent of new creatures are mutants?
May be integer from 0 to 100
Default: 10

"crossover_points"
How many points for crossover recombination? Has no effect unless recombination_method is CROSSOVER.
Default: 0

"gaussian_mutation_sd"
What is the standard deviation of gaussian applied mutation? Has no effect if mutation_method is not GAUSSIAN.
Default: 10

"mutation_boundary"
How to deal with mutations that go beyond the boundary? Has no effect if mutation_method is no GAUSSIAN.
May be: "WRAP" or "DISCARD"
Default: "WRAP"
