'''
Created on Nov 17, 2021

@author: bleem
'''
import os

import numpy
import xlsxwriter

from src.common import Constants, Converter, Tallies

DEFAULT_OUTPUT_DIR = "../../outputs/"


class CWriteData(object):

	# Private m_stuBehaviorsInfo
	# Private m_stuExperimentInfo
	# Private m_outFilePath
	# Private m_intRepetitions
	# Private m_intGenerations
	# Private m_intPhenoReinforced(,,)
	# Private m_intPhenoPunished(,,)

	def __init__(self, stuBehaviorsInfo, stuExperimentInfo, strOutFilePath, strFileStub, intRepetitions, intGenerations):
		self.m_stuBehaviorsInfo = None
		self.m_stuExperimentInfo = None
		self.m_outFilePath = None
		self.m_intRepetitions = None
		self.m_intGenerations = None
		self.m_intPhenoReinforced = None
		self.m_intPhenoPunished = None

		# 'Set properties
		self.set_behaviors_info_structure(stuBehaviorsInfo)
		self.set_experiment_info_structure(stuExperimentInfo)
		self.set_out_file_path(strOutFilePath)
		self.set_file_stub(strFileStub)
		self.set_repetitions(intRepetitions)
		self.set_generations(intGenerations)
		# 'MsgBox("Punishment mag:  " + eis.get_punishment_mag().__str__() + "	 get_mut_func_param():  " + eis.get_mut_func_param())
		# 'Stop

	def set_num_actual_generations(self, value):
		self.m_num_actual_generations = value

	def get_file_stub(self):
		return self.m_fileStub

	def get_behaviors_info_structure(self):
		return self.m_stuBehaviorsInfo

	def set_behaviors_info_structure(self, value):
		self.m_stuBehaviorsInfo = value

	def get_experiment_info_structure(self):
		return self.m_stuExperimentInfo

	def set_experiment_info_structure(self, value):
		self.m_stuExperimentInfo = value

	def get_out_file_path(self):
		return self.m_outFilePath

	def set_file_stub(self, value):
		self.m_fileStub = value

	def set_out_file_path(self, value):
		if value is not None:
			self.m_outFilePath = value
		else:
			self.exp_index = 1
			while True:
				dir_path = DEFAULT_OUTPUT_DIR + str(self.exp_index) + "/"
				if not os.path.exists(dir_path):
					os.makedirs(dir_path)
					print("making directory " + dir_path)
					self.m_outFilePath = dir_path
					break
				self.exp_index += 1

	def get_out_file_identifier(self):
		return self.exp_index

	def get_repetitions(self):
		return self.m_intRepetitions

	def set_repetitions(self, value):
		self.m_intRepetitions = value

	def get_generations(self):
		return self.m_intGenerations

	def set_generations(self, value):
		self.m_intGenerations = value

	def write_line(self, outFile, string):
		outFile.write(string + "\n")

	def write_csv(self, blnPhenoReinforced, blnPhenoPunished, intEmittedPheno):

		if not os.path.exists(self.get_out_file_path()):
			os.makedirs(self.get_out_file_path())

		# MsgBox("Punishment mag:  " + eis.get_punishment_mag().__str__() + "	 get_mut_func_param():  " + eis.get_mut_func_param())
		# Stop  These are correct at this point, what the hell?  This actually never was a problem.  I am in idiot.

		csvFile = self.get_out_file_path() + "\\" + self.get_file_stub() + ".csv"  # Will have to add the experiment number designator to the OutFilePath
		with open(csvFile, "w") as outFile:

			# strLineToWrite
			# outLine(), numOutLines, i, j

			self.write_csv_etbd_params(outFile)
			self.write_csv_exp_params(outFile)
			self.write_csv_non_etbd_params(outFile)
			self.write_csv_detailed_outputs(outFile, blnPhenoReinforced, blnPhenoPunished, intEmittedPheno)

		# outFile.Close()

		# Set csvFile and outFile to Nothing?

		# MsgBox("Done writing .csv file")

	def write_csv_detailed_outputs(self, outFile, blnPhenoReinforced, blnPhenoPunished, intEmittedPheno):
		# Write phenotypes
		self.write_line(outFile, "")
		self.write_line(outFile, "Phenos,SR+,Punish")
		eis = self.get_experiment_info_structure()
		# #Build lines to write to the file
		# numOutLines = self.get_generations() / 10
		# outLine(numOutLines)
		# #for j = 0 To numOutLines - 1
		# #	#Strings of the form:  phenotype(1) + "," + T/F(1) + "," + phenotype(2) + "," + T/F(2) + ","....+ phenotype(10) + "," + T/F(10)
		# #	for i in range(10
		# #		outLine(j + i) = intEmittedPheno[)

					# Convert boolean reinforcement array to integer array.
		m_intPhenoReinforced = numpy.zeros(shape = (self.get_repetitions(), eis.get_num_schedules(), self.get_generations()), dtype = int)
		for k in range(self.get_repetitions()):
			for j in range(eis.get_num_schedules()):
				for i in range(self.get_generations()):
					if blnPhenoReinforced[k, j, i]:
						m_intPhenoReinforced[k, j, i] = 1
					else:
						m_intPhenoReinforced[k, j, i] = 0

		# Convert boolean punishment array to integer array.
		m_intPhenoPunished = numpy.zeros(shape = (self.get_repetitions(), eis.get_num_schedules(), self.get_generations()), dtype = int)
		for k in range(self.get_repetitions()):
			for j in range(eis.get_num_schedules()):
				for i in range(self.get_generations()):
					if blnPhenoPunished[k, j, i]:
						m_intPhenoPunished[k, j, i] = 1
					else:
						m_intPhenoPunished[k, j, i] = 0

		# Write 10 phenos per line
		for k in range(self.get_repetitions()):
			self.write_line(outFile, "Repetition " + str(k))
			for j in range(eis.get_num_schedules()):
				self.write_line(outFile, "Schedule " + str(j))
				num_gens = int(self.m_num_actual_generations[k, j]) if eis.get_use_sp_schedules() else self.get_generations()
				for i in range(0, num_gens, 10):
					# strLineToWrite = ""
					# for m = 0 To 9
					# 	#Evidently I don't have to cast to strings here.  Guess  that Option thing is not set.
					# 	strLineToWrite = strLineToWrite + intEmittedPheno[k, j, i + m) + "," + m_intPhenoReinforced[k, j, i + m) + "," + m_intPhenoPunished[k, j, i + m) + ","
					#
					# self.write_line(outFile, strLineToWrite)
					# #Did not completely modify the following for punishment before implementing the For...Next loop above to write the line.
					# #self.write_line(outFile, str(intEmittedPheno[k, j, i]) + "," + str(m_intPhenoReinforced[k, j, i]) + "," + str(m_intPhenoPunished[k, j, i]) + "," + str(intEmittedPheno[k, j, i + 1]) + "," + str(m_intPhenoReinforced[k, j, i + 1]) + "," + str(m_intPhenoPunished[k, j, i + 1]) + "," + str(intEmittedPheno[k, j, i + 2]) + "," + str(m_intPhenoReinforced[k, j, i + 2]) + "," + str(m_intPhenoPunished[k, j, i + 2]) + "," + str(intEmittedPheno[k, j, i + 3]) + "," + str(m_intPhenoReinforced[k, j, i + 3]) + "," + str(intEmittedPheno[k, j, i + 4]) + "," + str(m_intPhenoReinforced[k, j, i + 4]) + "," + str(intEmittedPheno[k, j, i + 5]) + "," + str(m_intPhenoReinforced[k, j, i + 5]) + "," + str(intEmittedPheno[k, j, i + 6]) + "," + str(m_intPhenoReinforced[k, j, i + 6]) + "," + str(intEmittedPheno[k, j, i + 7]) + "," + str(m_intPhenoReinforced[k, j, i + 7]) + "," + str(intEmittedPheno[k, j, i + 8]) + "," + str(m_intPhenoReinforced[k, j, i + 8]) + "," + str(intEmittedPheno[k, j, i + 9]) + "," + str(m_intPhenoReinforced[k, j, i + 9)))

					self.write_line(outFile, str(intEmittedPheno[k, j, i]) + ","
								+str(m_intPhenoReinforced[k, j, i]) + ","
								+str(m_intPhenoPunished[k, j, i]) + ","
								+str(intEmittedPheno[k, j, i + 1]) + ","
								+str(m_intPhenoReinforced[k, j, i + 1]) + ","
								+str(m_intPhenoPunished[k, j, i + 1]) + ","
								+str(intEmittedPheno[k, j, i + 2]) + ","
								+str(m_intPhenoReinforced[k, j, i + 2]) + ","
								+str(m_intPhenoPunished[k, j, i + 2]) + ","
								+str(intEmittedPheno[k, j, i + 3]) + ","
								+str(m_intPhenoReinforced[k, j, i + 3]) + ","
								+str(m_intPhenoPunished[k, j, i + 3]) + ","
								+str(intEmittedPheno[k, j, i + 4]) + ","
								+str(m_intPhenoReinforced[k, j, i + 4]) + ","
								+str(m_intPhenoPunished[k, j, i + 4]) + ","
								+str(intEmittedPheno[k, j, i + 5]) + ","
								+str(m_intPhenoReinforced[k, j, i + 5]) + ","
								+str(m_intPhenoPunished[k, j, i + 5]) + ","
								+str(intEmittedPheno[k, j, i + 6]) + ","
								+str(m_intPhenoReinforced[k, j, i + 6]) + ","
								+str(m_intPhenoPunished[k, j, i + 6]) + ","
								+str(intEmittedPheno[k, j, i + 7]) + ","
								+str(m_intPhenoReinforced[k, j, i + 7]) + ","
								+str(m_intPhenoPunished[k, j, i + 7]) + ","
								+str(intEmittedPheno[k, j, i + 8]) + ","
								+str(m_intPhenoReinforced[k, j, i + 8]) + ","
								+str(m_intPhenoPunished[k, j, i + 8]) + ","
								+str(intEmittedPheno[k, j, i + 9]) + ","
								+str(m_intPhenoReinforced[k, j, i + 9]) + ","
								+str(m_intPhenoPunished[k, j, i + 9]))

	def write_csv_non_etbd_params(self, outFile):
		bis = self.get_behaviors_info_structure()
		eis = self.get_experiment_info_structure()
		ot = eis.get_organism_type()

		if ot == Constants.ORG_TYPE_ETBD:
			return

		is_one = ot == Constants.ORG_TYPE_NET_ONE
		is_two = ot == Constants.ORG_TYPE_NET_TWO
		is_net = is_one or is_two

		self.write_line(outFile, "")
		self.write_line(outFile, "Non-ETBD settings")
		self.write_line(outFile, "Organism Type," + Converter.convert_org_type_to_string(ot))
		if is_net:
			self.write_line(outFile, "Hidden Nodes," + str(bis.get_num_hidden_nodes()))
			self.write_line(outFile, "Output Nodes," + str(bis.get_num_output_nodes()))
		if is_one:
			self.write_line(outFile, "Firing Hidden Nodes," + str(bis.get_num_firing_hidden_nodes()))
			self.write_line(outFile, "Magnitude slope," + str(bis.get_net_one_magnitude_slope()))
			self.write_line(outFile, "Magnitude intercept," + str(bis.get_net_one_magnitude_intercept()))
			self.write_line(outFile, "REB Constant," + str(bis.get_net_one_neutral_magnitude()))

	def write_csv_exp_params(self, outFile):
		# Write experiment information

		eis = self.get_experiment_info_structure()
		self.write_line(outFile, "")
		self.write_line(outFile, "Experiment")
		self.write_line(outFile, "SD," + eis.get_sd())
		self.write_line(outFile, ",Sched 1,Sched 2")
		self.write_line(outFile, "Type," + eis.get_sched_type_1_str() + "," + eis.get_sched_type_2_str())
		self.write_line(outFile, "Lo Bound," + eis.get_t_1_lo().__str__() + "," + eis.get_t_2_lo().__str__())
		self.write_line(outFile, "Hi Bound," + eis.get_t_1_hi().__str__() + "," + eis.get_t_2_hi().__str__())
		self.write_line(outFile, "Equal punishment RI," + eis.get_equal_punishment_ri(0).__str__())
		self.write_line(outFile, "Single punishment RI," + eis.get_single_punishment_ri(0).__str__())
		self.write_line(outFile, "Proportional Punishment RI factor," + eis.get_proportion_punishment(0).__str__())
		self.write_line(outFile, "Punishment magnitude," + eis.get_punishment_mag().__str__())
		if eis.get_equal_punishment_ri(0) == 0 and eis.get_single_punishment_ri(0) == 0 and eis.get_proportion_punishment(0) == 0:
			self.write_line(outFile, "Punishment function parameter, N/A")
		else:
			self.write_line(outFile, "Punishment function parameter," + eis.get_mut_func_param().__str__())

		self.write_line(outFile, "Schedules (Magnitudes):")
		for i in range(eis.get_num_schedules()):
			to_write = str(i) + "," + str(eis.get_sched_value_1(i)) + "(" + str(eis.get_FDF_mean_1(i)) + ")," + str(eis.get_sched_value_2(i)) + "(" + str(eis.get_FDF_mean_2(i)) + ")"
			self.write_line(outFile, to_write)

	def write_csv_etbd_params(self, outFile):

		# Write organism information.  Note that not all the organism info is written, only the most common settings.
		eis = self.get_experiment_info_structure()
		bis = self.get_behaviors_info_structure()

		self.write_line(outFile, "Organism")
		self.write_line(outFile, "SD," + bis.get_sd_str())
		self.write_line(outFile, "Dec. of T.," + bis.get_decay_of_transfer().__str__())
		self.write_line(outFile, "Gray," + bis.get_use_gray_codes().__str__())
		self.write_line(outFile, "Lo P," + bis.get_low_phenotype().__str__())
		self.write_line(outFile, "Hi P," + bis.get_high_phenotype().__str__())
		self.write_line(outFile, "Behaviors," + bis.get_num_behaviors().__str__())
		self.write_line(outFile, "%Replace," + bis.get_percent_to_replace().__str__())
		self.write_line(outFile, "%Replace2," + bis.get_percent_to_replace_2().__str__())
		if eis.get_equal_punishment_ri(0) == 0 and eis.get_single_punishment_ri(0) == 0 and eis.get_proportion_punishment(0) == 0:
			self.write_line(outFile, "Punish,N/A")
			self.write_line(outFile, "FOMO a,N/A")
		else:
			self.write_line(outFile, "Punish," + bis.get_punishment_method_str())
			self.write_line(outFile, "FOMO a," + bis.get_fomo_a().__str__())

		self.write_line(outFile, "Fitness M," + bis.get_fitness_method_str())
		self.write_line(outFile, "Fitness L," + bis.get_fitness_landscape_str())
		self.write_line(outFile, "Mutation," + bis.get_mutation_info().get_method_str())
		self.write_line(outFile, "Rate," + bis.get_mutation_info().get_rate().__str__())
		self.write_line(outFile, "Recomb," + bis.get_recombination_info().get_method_str())
		self.write_line(outFile, "Selection," + bis.get_selection_info().get_selection_method_str())
		self.write_line(outFile, "Form," + bis.get_selection_info().get_continuous_function_form_str())

	def write_excel(self, blnPhenoReinforced, blnPhenoPunished, intEmittedPheno):

		excel_file = self.get_out_file_path() + "/ETBD_output_" + str(self.get_out_file_identifier()) + ".xlsx"

		try:
			with xlsxwriter.Workbook(excel_file) as objWB:
				objWS = list()
				# Dim objWB As Excel.Workbook
				# Dim objWS(self.get_repetitions() + 1) As Excel.Worksheet
				# Dim i
				# Dim strRow
				# Dim intRep, intSched, intBlock, intNumBlocks, intR1, intB1, intR2, intB2, intP1, intP2, intTargetStatus #for writing to the worksheets

				# objExcel.Visible = True #  if this is not set, then Excel just runs in the background.
				# 						  I guess you can't write directly to an Excel file on the hard drive.  Maybe you can with the Streamwriter thing.

				# objWB = objExcel.Workbooks.Add() # Add a workbook.  The program is instantiated without a workbook.

				for i in range(self.get_repetitions() + 1):
					if i == 0:
						objWS.append(objWB.add_worksheet("Experiment"))
					else:
						objWS.append(objWB.add_worksheet("Repetition " + str(i)))

				self.write_excel_cover_sheet(objWS)

				# Write 500-generation block summary data to appropriate sheets

				for intRep in range(self.get_repetitions()):  # One repetition per worksheet
					self.write_repetition_sheet(intRep, objWS, intEmittedPheno, blnPhenoReinforced, blnPhenoPunished)

				if self.m_stuExperimentInfo.get_use_sp_schedules():
					objWS.append(objWB.add_worksheet("SP analysis"))
					self.write_sp_analysis(objWS[-1], blnPhenoReinforced, intEmittedPheno)

			# os.system("start EXCEL.EXE " + excel_file)

		except EnvironmentError as err:
			print(err)

	def write_sp_analysis(self, exp_sheet, blnPhenoReinforced, intEmittedPheno):
		row = self.write_excel_and_increment_row(exp_sheet, ["Schedule", "Reinforcer Index (up to)", "RI", "Ratio", "B1", "B2", "log(B1/B2)"], 1)

		eis = self.get_experiment_info_structure()
		rtc_seq_responses = {}
		for intSched in range(eis.get_num_schedules()):

			count_1_list = [0] * eis.get_sp_stop_count(intSched)
			count_2_list = [0] * eis.get_sp_stop_count(intSched)

			for intRep in range(eis.get_num_repetitions()):
				current_reinforcer = 0
				count_1 = 0
				count_2 = 0

				intNumGens = int(self.m_num_actual_generations[intRep, intSched])

				last_rtc = None
				second_last_rtc = None
				third_last_rtc = None

				for intGen in range(intNumGens):
					pheno = intEmittedPheno[intRep, intSched, intGen]
					tc = Tallies.check_for_targets(pheno, eis)
					if tc != 0:
						key = "_" + str(tc)
						self.safe_increment_value(rtc_seq_responses, key)
						if last_rtc is not None:
							key = str(last_rtc) + key
							self.safe_increment_value(rtc_seq_responses, key)
						if second_last_rtc is not None:
							key = str(second_last_rtc) + key
							self.safe_increment_value(rtc_seq_responses, key)
						if third_last_rtc is not None:
							key = str(third_last_rtc) + key
							self.safe_increment_value(rtc_seq_responses, key)

						if tc == 1:
							count_1 += 1
						elif tc == 2:
							count_2 += 1

						if blnPhenoReinforced[intRep, intSched, intGen]:
							count_1_list[current_reinforcer] += count_1
							count_2_list[current_reinforcer] += count_2

							count_1 = 0
							count_2 = 0

							current_reinforcer += 1
							third_last_rtc = second_last_rtc
							second_last_rtc = last_rtc
							last_rtc = tc

			for intReinforcer in range(eis.get_sp_stop_count(intSched)):
				c1 = count_1_list[intReinforcer]
				c2 = count_2_list[intReinforcer]
				row = self.write_excel_and_increment_row(exp_sheet, [intSched + 1, intReinforcer + 1, eis.get_sp_mean(intSched), eis.get_sp_ratio(intSched), c1, c2, Tallies.safe_log_of_ratio(c1, c2)], row)

		row = self.write_excel_and_increment_row(exp_sheet, ["R pattern", "Pattern Length", "log(B1/B2)"], row)

		row = self.write_log_ratio_from_key(exp_sheet, rtc_seq_responses, "", row)
		for last_rtc in range(1, 3):
			key = str(last_rtc)
			row = self.write_log_ratio_from_key(exp_sheet, rtc_seq_responses, key, row)
			for second_last_rtc in range(1, 3):
				key2 = str(second_last_rtc) + key
				row = self.write_log_ratio_from_key(exp_sheet, rtc_seq_responses, key2, row)
				for third_last_rtc in range(1, 3):
					key3 = str(third_last_rtc) + key2
					row = self.write_log_ratio_from_key(exp_sheet, rtc_seq_responses, key3, row)

	def write_log_ratio_from_key(self, exp_sheet, dictionary, key, row_num):
		b1 = dictionary.get(key + "_1", 0)
		b2 = dictionary.get(key + "_2", 0)
		row = self.write_excel_and_increment_row(exp_sheet, [key, len(key), Tallies.safe_log_of_ratio(b1, b2)], row_num)
		return row

	def safe_increment_value(self, library, key):
		if key in library:
			library[key] += 1
		else:
			library[key] = 1

	def write_excel_cover_sheet(self, objWS):
		# Write Organism info to "Experiment" sheet.  Note that not all the organism info is written, only the most common settings.
		exp_sheet = objWS[0]
		self.write_excel_etbd_params(exp_sheet)
		last_row_num = self.write_excel_exp_params(exp_sheet)
		self.write_excel_non_etbd_params(exp_sheet, last_row_num)

	def write_excel_and_increment_row(self, excel_sheet, data, row_num):
		excel_sheet.write_row("A" + str(row_num), data)
		return row_num + 1

	def write_excel_non_etbd_params(self, exp_sheet, last_row_num):
		bis = self.get_behaviors_info_structure()
		eis = self.get_experiment_info_structure()
		ot = eis.get_organism_type()

		if ot == Constants.ORG_TYPE_ETBD:
			return

		is_one = ot == Constants.ORG_TYPE_NET_ONE
		is_two = ot == Constants.ORG_TYPE_NET_TWO
		# is_net = is_one or is_two
		is_pg = ot == Constants.ORG_TYPE_PG
		is_ql = ot == Constants.ORG_TYPE_QL

		row = last_row_num + 2
		row = self.write_excel_and_increment_row(exp_sheet, ["Non-ETBD settings"], row)
		row = self.write_excel_and_increment_row(exp_sheet, ["Organism Type", Converter.convert_org_type_to_string(ot)], row)
		row = self.write_excel_and_increment_row(exp_sheet, ["Output Nodes", bis.get_num_output_nodes()], row)
		row = self.write_excel_and_increment_row(exp_sheet, ["Firing Hidden Nodes", bis.get_num_firing_hidden_nodes()], row)

		# row = self.write_excel_and_increment_row(exp_sheet, ["COD", eis.get_COD()], row)

		if is_one:
			row = self.write_excel_and_increment_row(exp_sheet, ["Hidden Nodes", bis.get_num_hidden_nodes()], row)
			row = self.write_excel_and_increment_row(exp_sheet, ["Magnitude slope", bis.get_net_one_magnitude_slope()], row)
			row = self.write_excel_and_increment_row(exp_sheet, ["Magnitude intercept", bis.get_net_one_magnitude_intercept()], row)
			row = self.write_excel_and_increment_row(exp_sheet, ["REB Constant", bis.get_net_one_neutral_magnitude()], row)
		if is_two:
			row = self.write_excel_and_increment_row(exp_sheet, ["NET_TWO_NUM_HIDDEN_NODES", bis.get_net_two_num_hidden_nodes()], row)
			row = self.write_excel_and_increment_row(exp_sheet, ["NET_TWO_NEUTRAL_MAGNITUDE", bis.get_net_two_neutral_magnitude()], row)
			row = self.write_excel_and_increment_row(exp_sheet, ["NET_TWO_SELECTION_STRENGTH_MULTIPLIER", bis.get_net_two_selection_strength_multiplier()], row)
			row = self.write_excel_and_increment_row(exp_sheet, ["NET_TWO_SELECTION_STRENGTH_EXPONENT", bis.get_net_two_selection_strength_exponent()], row)
		if is_pg:
			row = self.write_excel_and_increment_row(exp_sheet, ["LEARNING_RATE", bis.get_ml_learning_rate()], row)
			row = self.write_excel_and_increment_row(exp_sheet, ["NUM_SLOTS", bis.get_ml_num_slots()], row)
			# row = self.write_excel_and_increment_row(exp_sheet, ["REWARD_MULTIPLIER", bis.get_ml_reward_multiplier()], row)
			row = self.write_excel_and_increment_row(exp_sheet, ["REWARD_EXPONENT", bis.get_ml_reward_exponent()], row)
			row = self.write_excel_and_increment_row(exp_sheet, ["PESSIMISM", bis.get_ml_pessimism()], row)
			row = self.write_excel_and_increment_row(exp_sheet, ["EXTINCTION", bis.get_ml_extinction()], row)
		if is_ql:
			row = self.write_excel_and_increment_row(exp_sheet, ["DISCOUNT_RATE", bis.get_ml_discount_rate()], row)
			row = self.write_excel_and_increment_row(exp_sheet, ["EPSILON", bis.get_ml_epsilon()], row)
			row = self.write_excel_and_increment_row(exp_sheet, ["LEARNING_RATE", bis.get_ml_learning_rate()], row)
			row = self.write_excel_and_increment_row(exp_sheet, ["NUM_SLOTS", bis.get_ml_num_slots()], row)
			row = self.write_excel_and_increment_row(exp_sheet, ["REWARD_MULTIPLIER", bis.get_ml_reward_multiplier()], row)
			row = self.write_excel_and_increment_row(exp_sheet, ["REWARD_EXPONENT", bis.get_ml_reward_exponent()], row)

	def write_excel_exp_params(self, exp_sheet):

		eis = self.get_experiment_info_structure()
		exp_sheet.write("A32", "Schedules(Magnitudes):")
		for i in range(eis.get_num_schedules()):
			row_num = i + 33
			strRow = str(row_num)
			write_list = [i + 1]  # +1 because humans are 1-indexed
			if eis.get_use_sp_schedules():
				write_list.append("RI " + eis.get_sp_mean(i).__str__() + " ratio " + eis.get_sp_ratio(i).__str__() + " (FDF mean " + eis.get_sp_FDF(i).__str__() + ")")
			else:
				write_list.append(eis.get_sched_value_1(i).__str__() + "(" + eis.get_FDF_mean_1(i).__str__() + ")")
				write_list.append(eis.get_sched_value_2(i).__str__() + "(" + eis.get_FDF_mean_2(i).__str__() + ")")
			exp_sheet.write_row("A" + strRow + ":C" + strRow, write_list)

		return row_num

	def write_excel_etbd_params(self, exp_sheet):

		bis = self.get_behaviors_info_structure()
		eis = self.get_experiment_info_structure()

		exp_sheet.write("A1", "Organism")
		exp_sheet.write_row("A2:B2", ["SD", bis.get_sd_str()])
		exp_sheet.write_row("A3:B3", ["Dec. of T.", bis.get_decay_of_transfer()])
		exp_sheet.write_row("A4:B4", ["Gray", bis.get_use_gray_codes().__str__()])
		exp_sheet.write_row("A5:B5", ["Lo P", bis.get_low_phenotype()])
		exp_sheet.write_row("A6:B6", ["Hi P", bis.get_high_phenotype()])
		exp_sheet.write_row("A7:B7", ["Behaviors", bis.get_num_behaviors()])
		exp_sheet.write_row("A8:B8", ["%Replace", bis.get_percent_to_replace()])
		exp_sheet.write_row("A9:B9", ["%Replace2", bis.get_percent_to_replace_2()])
		if eis.get_equal_punishment_ri(0) == 0 and eis.get_single_punishment_ri(0) == 0 and eis.get_proportion_punishment(0) == 0:
			exp_sheet.write_row("A10:B10", ["Punish", "N/A"])
			exp_sheet.write_row("A11:B11", ["FOMO a", "N/A"])
		else:
			exp_sheet.write_row("A10:B10", ["Punish", bis.get_punishment_method_str()])
			exp_sheet.write_row("A11:B11", ["FOMO a", bis.get_fomo_a()])

		exp_sheet.write_row("A12:B12", ["Fitness M", bis.get_fitness_method_str()])
		exp_sheet.write_row("A13:B13", ["Fitness L", bis.get_fitness_landscape_str()])
		exp_sheet.write_row("A14:B14", ["Mutation", bis.get_mutation_info().get_method_str()])
		exp_sheet.write_row("A15:B15", ["Rate", bis.get_mutation_info().get_rate()])
		exp_sheet.write_row("A16:B16", ["Recomb", bis.get_recombination_info().get_method_str()])
		exp_sheet.write_row("A17:B17", ["Selection", bis.get_selection_info().get_selection_method_str()])
		exp_sheet.write_row("A18:B18", ["Form", bis.get_selection_info().get_continuous_function_form_str()])

		# Write Experiment info to "Experiment" sheet
		exp_sheet.write("A20", "Experiment")
		exp_sheet.write_row("A21:B21", ["SD", eis.get_sd_str()])
		exp_sheet.write_row("B22:C22", ["Sched1", "Sched2"])
		exp_sheet.write_row("A23:C23", ["Type", eis.get_sched_type_1_str(), eis.get_sched_type_2_str()])
		exp_sheet.write_row("A24:C24", ["Mag", "See A32"])
		exp_sheet.write_row("A25:C25", ["Lo Bound", eis.get_t_1_lo(), eis.get_t_2_lo()])
		exp_sheet.write_row("A26:C26", ["Hi Bound", eis.get_t_1_hi(), eis.get_t_2_hi()])
		exp_sheet.write_row("A27:B27", ["Equal punishment RI", eis.get_equal_punishment_ri(0)])
		exp_sheet.write_row("A28:B28", ["Single punishment RI", eis.get_single_punishment_ri(0)])
		exp_sheet.write_row("A29:B29", ["Proportional punishment RI factor", eis.get_proportion_punishment(0)])
		exp_sheet.write_row("A30:B30", ["Punishment magnitude", eis.get_punishment_mag()])
		if eis.get_equal_punishment_ri(0) == 0 and eis.get_single_punishment_ri(0) == 0 and eis.get_proportion_punishment(0) == 0:
			exp_sheet.write_row("A31:B31", ["Punishment function parameter", "N/A"])
		else:
			exp_sheet.write_row("A31:B31", ["Punishment function parameter", eis.get_mut_func_param()])

	def write_repetition_sheet(self, intRep, objWS, intEmittedPheno, blnPhenoReinforced, blnPhenoPunished):
		eis = self.get_experiment_info_structure()

		# Write column headers for this repetition
		objWS[intRep + 1].write_row("A1:G1",
								["Sched", "P1", "R1", "B1", "P2", "R2", "B2",
								"Sched (Total)", "P1", "R1", "B1", "P2", "R2", "B2", "log(P1/P2)", "log(M1/M2)", "log(R1/R2)", "log(B1/B2)", "changeovers",
								"GML Parameters", "a", "log b", "cGML Parameters", "ar", "am", "log b"])  # This works fine.

		# write out a summary for GML fits
		n_sched = eis.get_num_schedules()
		max_sched_loc = str(n_sched + 1)
		yx_locs = "R2:R" + max_sched_loc + ", Q2:Q" + max_sched_loc
		slope_formula = "=SLOPE(" + yx_locs + ")"
		intercept_formula = "=INTERCEPT(" + yx_locs + ")"
		objWS[intRep + 1].write_row("U2:V2", [slope_formula, intercept_formula])

		linest_formula = "=LINEST(R2:R" + max_sched_loc + ",P2:Q" + max_sched_loc + ",TRUE,TRUE)"
		objWS[intRep + 1].write_dynamic_array_formula("X2", linest_formula)

		total_changeovers = 0

		for intSched in range(n_sched):

			r1, r2, p1, p2, b1, b2, changeover_count = Tallies.tally_schedule(intRep, intSched, intEmittedPheno, blnPhenoReinforced, blnPhenoPunished, True, objWS, self.get_experiment_info_structure())

			# Write out the totals for each schedule
			total_row_index = intSched + 2
			xl_locs = "H" + str(total_row_index) + ":S" + str(total_row_index)
			lp = Tallies.safe_log_of_ratio(p1, p2)
			lr = Tallies.safe_log_of_ratio(r1, r2)
			lm = Tallies.safe_log_of_ratio(eis.get_FDF_mean_2(intSched), eis.get_FDF_mean_1(intSched))  # backwards cause inversely proportional to magnitude
			lb = Tallies.safe_log_of_ratio(b1, b2)

			objWS[intRep + 1].write_row(xl_locs, [intSched + 1, p1, r1, b1, p2, r2, b2, lp, lm, lr, lb, changeover_count])
			total_changeovers += changeover_count

		objWS[intRep + 1].write("S" + str(n_sched + 2), total_changeovers)

