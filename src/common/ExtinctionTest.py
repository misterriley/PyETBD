'''
Created on Jan 10, 2022

@author: bleem
'''
import os
import winsound

import numpy
import xlsxwriter

from src.common import Converter, JSONData
from src.orgs.NetTwoOrganism import NetTwoOrganism
from src.orgs.frmBuildOrganism import frmBuildOrganism

TARGET_R_COUNT = 1
EXTINCTION_B_COUNT = 100
REPETITIONS = 10000
PRINT_EVERY = 10
DEFAULT_OUTPUT_DIR = "../../outputs/"
DIR = "../../inputs/"
FILE_NAME = "extinction.json"


def check_for_targets(pheno, t1Lo, t1Hi, t2Lo, t2Hi):
	if pheno >= t1Lo and pheno <= t1Hi:
		return 1
	if pheno >= t2Lo and pheno <= t2Hi:
		return 2
	return 0


def get_out_file_path():
	exp_index = 1
	while True:
		dir_path = DEFAULT_OUTPUT_DIR + str(exp_index) + "/"
		if not os.path.exists(dir_path):
			os.makedirs(dir_path)
			print("making directory " + dir_path)
			return dir_path
			break
		exp_index += 1


def write_excel_and_increment_row(excel_sheet, data, row_num):
		excel_sheet.write_row("A" + str(row_num), data)
		return row_num + 1


if __name__ == '__main__':
	org_builder = frmBuildOrganism()
	json_data = JSONData.load_file(DIR + FILE_NAME)
	org_builder.create_an_organism(json_data)
	org = org_builder.get_creature()
	# load up with reinforcers
	counts = [[0, 0, 0] for i in range(EXTINCTION_B_COUNT)]
	record = [[0 for i in range(REPETITIONS)] for j in range(EXTINCTION_B_COUNT)]

	t1Lo = json_data.get_t_1_lo(0)
	t1Hi = json_data.get_t_1_hi(0)
	t2Lo = json_data.get_t_2_lo(0)
	t2Hi = json_data.get_t_2_hi(0)

	for rep_index in range(REPETITIONS):
		if rep_index % PRINT_EVERY == 0:
			print("starting repetition " + str(rep_index))

		org.reset_state()
		r_count = 0
		while r_count < TARGET_R_COUNT:
			beh = org.emit_behavior()
			pheno = beh.get_integer_value()

			tc = check_for_targets(pheno, t1Lo, t1Hi, t2Lo, t2Hi)
			if tc == 1:
				org.set_selection(40, True)
				r_count += 1
			else:
				org.set_selection(0, False)

		for i in range(EXTINCTION_B_COUNT):
			beh = org.emit_behavior()
			pheno = beh.get_integer_value()
			tc = check_for_targets(pheno, t1Lo, t1Hi, t2Lo, t2Hi)
			counts[i][tc] += 1
			org.set_selection(0, False)
			if tc == 2:
				tc = -1  # easier for correlation calculations
			record[i][rep_index] = tc

	corr_coefs = numpy.corrcoef(record)

	output_path = get_out_file_path()
	excel_file = output_path + "extinction_test.xlsx"
	try:
		with xlsxwriter.Workbook(excel_file) as objWB:
			exp_sheet = objWB.add_worksheet("Experiment")
			row = write_excel_and_increment_row(exp_sheet, ["ORG_TYPE", Converter.convert_org_type_to_string(json_data.get_organism_type())], 1)
			row = write_excel_and_increment_row(exp_sheet, ["MUTATION_RATE", json_data.get_mutation_rate()], row)
			row = write_excel_and_increment_row(exp_sheet, ["FDF_MEAN", json_data.get_FDF_mean_2(0, 0)], row)
			row = write_excel_and_increment_row(exp_sheet, ["TARGET_R_COUNT", TARGET_R_COUNT], row)
			row = write_excel_and_increment_row(exp_sheet, ["REPETITIONS", REPETITIONS], row)
			if isinstance(org, NetTwoOrganism):
				row = write_excel_and_increment_row(exp_sheet, ["NET_TWO_HIDDEN_NODE_FIRING_PROBABILITY", json_data.get_net_two_hidden_node_firing_probability()], row)
				row = write_excel_and_increment_row(exp_sheet, ["NET_TWO_NEUTRAL_MAGNITUDE_CONSTANT", json_data.get_net_two_neutral_magnitude_constant()], row)
				row = write_excel_and_increment_row(exp_sheet, ["NET_TWO_SELECTION_STRENGTH_MULTIPLIER", json_data.get_net_two_selection_strength_multiplier()], row)

			row = write_excel_and_increment_row(exp_sheet, [], row)
			row = write_excel_and_increment_row(exp_sheet, ["POST_REINFORCEMENT_INDEX", "B1/(B1+B2)", "B1", "B2", "Other", "Correlation w/ Output at 0"], row)

			for i in range(EXTINCTION_B_COUNT):
				count_1 = counts[i][1]
				count_2 = counts[i][2]
				if count_1 + count_2 == 0:
					ratio = "0/0"
				else:
					ratio = count_1 / (count_1 + count_2)
				row = write_excel_and_increment_row(exp_sheet, [i, ratio, count_1, count_2, counts[i][0], corr_coefs[i][0]], row)
	except Exception as ex:
		print(ex)

	winsound.PlaySound("..\\..\\resources\\22Fillywhinnygrunt2000.wav", 0)
