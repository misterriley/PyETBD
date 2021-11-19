'''
Created on Nov 17, 2021

@author: bleem
'''
import os

import numpy
import xlsxwriter

DEFAULT_OUTPUT_DIR = "../outputs/"


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
		# 'MsgBox("Punishment mag:  " + self.get_experiment_info_structure().get_punishment_mag().__str__() + "	 get_mut_func_param():  " + self.get_experiment_info_structure().get_mut_func_param())
		# 'Stop

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
			exp_index = 1
			while True:
				dir_path = DEFAULT_OUTPUT_DIR + str(exp_index) + "/"
				if not os.path.exists(dir_path):
					self.m_outFilePath = dir_path
					break
				exp_index += 1

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

		# MsgBox("Punishment mag:  " + self.get_experiment_info_structure().get_punishment_mag().__str__() + "	 get_mut_func_param():  " + self.get_experiment_info_structure().get_mut_func_param())
		# Stop  These are correct at this point, what the hell?  This actually never was a problem.  I am in idiot.

		csvFile = self.get_out_file_path() + "\\" + self.get_file_stub() + ".csv"  # Will have to add the experiment number designator to the OutFilePath
		with open(csvFile, "w") as outFile:

			# strLineToWrite
			# outLine(), numOutLines, i, j

			# Write organism information.  Note that not all the organism info is written, only the most common settings.
			self.write_line(outFile, "Organism")
			bis = self.get_behaviors_info_structure()
			self.write_line(outFile, "SD," + bis.get_sd_str())
			self.write_line(outFile, "Dec. of T.," + bis.get_decay_of_transfer().__str__())
			self.write_line(outFile, "Gray," + bis.get_use_gray_codes().__str__())
			self.write_line(outFile, "Lo P," + bis.get_low_phenotype().__str__())
			self.write_line(outFile, "Hi P," + bis.get_high_phenotype().__str__())
			self.write_line(outFile, "Behaviors," + bis.get_num_behaviors().__str__())
			self.write_line(outFile, "%Replace," + bis.get_percent_to_replace().__str__())
			self.write_line(outFile, "%Replace2," + bis.get_percent_to_replace_2().__str__())
			if self.get_experiment_info_structure().get_equal_punishment_ri() == 0 and self.get_experiment_info_structure().get_single_punishment_ri() == 0 and self.get_experiment_info_structure().get_proportion_punishment() == 0:
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

			# Write experiment information
			self.write_line(outFile, "")
			self.write_line(outFile, "Experiment")
			self.write_line(outFile, "SD," + self.get_experiment_info_structure().get_sd())
			self.write_line(outFile, ",Sched 1,Sched 2")
			self.write_line(outFile, "Type," + self.get_experiment_info_structure().get_sched_type_1_str() + "," + self.get_experiment_info_structure().get_sched_type_2_str())
			self.write_line(outFile, "Lo Bound," + self.get_experiment_info_structure().get_t_1_lo().__str__() + "," + self.get_experiment_info_structure().get_t_2_lo().__str__())
			self.write_line(outFile, "Hi Bound," + self.get_experiment_info_structure().get_t_1_hi().__str__() + "," + self.get_experiment_info_structure().get_t_2_hi().__str__())
			self.write_line(outFile, "Equal punishment RI," + self.get_experiment_info_structure().get_equal_punishment_ri().__str__())
			self.write_line(outFile, "Single punishment RI," + self.get_experiment_info_structure().get_single_punishment_ri().__str__())
			self.write_line(outFile, "Proportional Punishment RI factor," + self.get_experiment_info_structure().get_proportion_punishment().__str__())
			self.write_line(outFile, "Punishment magnitude," + self.get_experiment_info_structure().get_punishment_mag().__str__())
			if self.get_experiment_info_structure().get_equal_punishment_ri() == 0 and self.get_experiment_info_structure().get_single_punishment_ri() == 0 and self.get_experiment_info_structure().get_proportion_punishment() == 0:
				self.write_line(outFile, "Punishment function parameter, N/A")
			else:
				self.write_line(outFile, "Punishment function parameter," + self.get_experiment_info_structure().get_mut_func_param().__str__())

			self.write_line(outFile, "Schedules (Magnitudes):")
			for i in range(self.get_experiment_info_structure().get_num_schedules()):
				to_write = str(i) + "," + str(self.get_experiment_info_structure().get_sched_value_1(i)) + "(" + str(self.get_experiment_info_structure().get_mag_1(i)) + ")," + str(self.get_experiment_info_structure().get_sched_value_2(i)) + "(" + str(self.get_experiment_info_structure().get_mag_2(i)) + ")"
				self.write_line(outFile, to_write)
			# Write phenotypes
			self.write_line(outFile, "")
			self.write_line(outFile, "Phenos,SR+,Punish")
			# #Build lines to write to the file
			# numOutLines = self.get_generations() / 10
			# outLine(numOutLines)
			# #for j = 0 To numOutLines - 1
			# #	#Strings of the form:  phenotype(1) + "," + T/F(1) + "," + phenotype(2) + "," + T/F(2) + ","....+ phenotype(10) + "," + T/F(10)
			# #	for i in range(10
			# #		outLine(j + i) = intEmittedPheno[)
			# #

			# #

			# Convert boolean reinforcement array to integer array.
			m_intPhenoReinforced = numpy.zeros(shape = (self.get_repetitions(), self.get_experiment_info_structure().get_num_schedules(), self.get_generations()), dtype = int)
			for k in range(self.get_repetitions()):
				for j in range(self.get_experiment_info_structure().get_num_schedules()):
					for i in range(self.get_generations()):
						if blnPhenoReinforced[k, j, i]:
							m_intPhenoReinforced[k, j, i] = 1
						else:
							m_intPhenoReinforced[k, j, i] = 0

			# Convert boolean punishment array to integer array.
			m_intPhenoPunished = numpy.zeros(shape = (self.get_repetitions(), self.get_experiment_info_structure().get_num_schedules(), self.get_generations()), dtype = int)
			for k in range(self.get_repetitions()):
				for j in range(self.get_experiment_info_structure().get_num_schedules()):
					for i in range(self.get_generations()):
						if blnPhenoPunished[k, j, i]:
							m_intPhenoPunished[k, j, i] = 1
						else:
							m_intPhenoPunished[k, j, i] = 0

			# Write 10 phenos per line
			for k in range(self.get_repetitions()):
				self.write_line(outFile, "Repetition " + str(k))
				for j in range(self.get_experiment_info_structure().get_num_schedules()):
					self.write_line(outFile, "Schedule " + str(j))
					for i in range(0, self.get_generations(), 10):
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

		# outFile.Close()

		# Set csvFile and outFile to Nothing?

		# MsgBox("Done writing .csv file")

	def write_excel(self, blnPhenoReinforced, blnPhenoPunished, intEmittedPheno):

		xlsx_file = self.get_out_file_path() + "etbd_output.xlsx"

		try:
			with xlsxwriter.Workbook(xlsx_file) as objWB:
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

				# Write Organism info to "Experiment" sheet.  Note that not all the organism info is written, only the most common settings.
				exp_sheet = objWS[0]

				exp_sheet.write("A1", "Organism")
				exp_sheet.write_row("A2:B2", ["SD", self.get_behaviors_info_structure().get_sd_str()])
				exp_sheet.write_row("A3:B3", ["Dec. of T.", self.get_behaviors_info_structure().get_decay_of_transfer()])
				exp_sheet.write_row("A4:B4", ["Gray", self.get_behaviors_info_structure().get_use_gray_codes().__str__()])
				exp_sheet.write_row("A5:B5", ["Lo P", self.get_behaviors_info_structure().get_low_phenotype()])
				exp_sheet.write_row("A6:B6", ["Hi P", self.get_behaviors_info_structure().get_high_phenotype()])
				exp_sheet.write_row("A7:B7", ["Behaviors", self.get_behaviors_info_structure().get_num_behaviors()])
				exp_sheet.write_row("A8:B8", ["%Replace", self.get_behaviors_info_structure().get_percent_to_replace()])
				exp_sheet.write_row("A9:B9", ["%Replace2", self.get_behaviors_info_structure().get_percent_to_replace_2()])
				if self.get_experiment_info_structure().get_equal_punishment_ri() == 0 and self.get_experiment_info_structure().get_single_punishment_ri() == 0 and self.get_experiment_info_structure().get_proportion_punishment() == 0:
					exp_sheet.write_row("A10:B10", ["Punish", "N/A"])
					exp_sheet.write_row("A11:B11", ["FOMO a", "N/A"])
				else:
					exp_sheet.write_row("A10:B10", ["Punish", self.get_behaviors_info_structure().get_punishment_method_str()])
					exp_sheet.write_row("A11:B11", ["FOMO a", self.get_behaviors_info_structure().get_fomo_a()])

				exp_sheet.write_row("A12:B12", ["Fitness M", self.get_behaviors_info_structure().get_fitness_method_str()])
				exp_sheet.write_row("A13:B13", ["Fitness L", self.get_behaviors_info_structure().get_fitness_landscape_str()])
				exp_sheet.write_row("A14:B14", ["Mutation", self.get_behaviors_info_structure().get_mutation_info().get_method_str()])
				exp_sheet.write_row("A15:B15", ["Rate", self.get_behaviors_info_structure().get_mutation_info().get_rate()])
				exp_sheet.write_row("A16:B16", ["Recomb", self.get_behaviors_info_structure().get_recombination_info().get_method_str()])
				exp_sheet.write_row("A17:B17", ["Selection", self.get_behaviors_info_structure().get_selection_info().get_selection_method_str()])
				exp_sheet.write_row("A18:B18", ["Form", self.get_behaviors_info_structure().get_selection_info().get_continuous_function_form_str()])

				# Write Experiment info to "Experiment" sheet
				exp_sheet.write("A20", "Experiment")
				exp_sheet.write_row("A21:B21", ["SD", self.get_experiment_info_structure().get_sd_str()])
				exp_sheet.write_row("B22:C22", ["Sched1", "Sched2"])
				exp_sheet.write_row("A23:C23", ["Type", self.get_experiment_info_structure().get_sched_type_1_str(), self.get_experiment_info_structure().get_sched_type_2_str()])
				exp_sheet.write_row("A24:C24", ["Mag", "See A32"])
				exp_sheet.write_row("A25:C25", ["Lo Bound", self.get_experiment_info_structure().get_t_1_lo(), self.get_experiment_info_structure().get_t_2_lo()])
				exp_sheet.write_row("A26:C26", ["Hi Bound", self.get_experiment_info_structure().get_t_1_hi(), self.get_experiment_info_structure().get_t_2_hi()])
				exp_sheet.write_row("A27:B27", ["Equal punishment RI", self.get_experiment_info_structure().get_equal_punishment_ri()])
				exp_sheet.write_row("A28:B28", ["Single punishment RI", self.get_experiment_info_structure().get_single_punishment_ri()])
				exp_sheet.write_row("A29:B29", ["Proportional punishment RI factor", self.get_experiment_info_structure().get_proportion_punishment()])
				exp_sheet.write_row("A30:B30", ["Punishment magnitude", self.get_experiment_info_structure().get_punishment_mag()])
				if self.get_experiment_info_structure().get_equal_punishment_ri() == 0 and self.get_experiment_info_structure().get_single_punishment_ri() == 0 and self.get_experiment_info_structure().get_proportion_punishment() == 0:
					exp_sheet.write_row("A31:B31", ["Punishment function parameter", "N/A"])
				else:
					exp_sheet.write_row("A31:B31", ["Punishment function parameter", self.get_experiment_info_structure().get_mut_func_param()])

				exp_sheet.write("A32", "Schedules(Magnitudes):")
				for i in range(self.get_experiment_info_structure().get_num_schedules()):
					strRow = str(i + 33)
					write_list = [i + 1]  # +1 because humans are 1-indexed
					write_list.append(self.get_experiment_info_structure().get_sched_value_1(i).__str__() + "(" + self.get_experiment_info_structure().get_mag_1(i).__str__() + ")")
					write_list.append(self.get_experiment_info_structure().get_sched_value_2(i).__str__() + "(" + self.get_experiment_info_structure().get_mag_2(i).__str__() + ")")
					exp_sheet.write_row("A" + strRow + ":C" + strRow, write_list)

				# Write 500-generation block summary data to appropriate sheets
				intNumBlocks = int(self.get_generations() / 500)  # 500-generation blocks
				for intRep in range(self.get_repetitions()):  # One repetition per worksheet
					# Write column headers for this repetition
					objWS[intRep + 1].write_row("A1:G1", ["Sched", "P1", "R1", "B1", "P2", "R2", "B2"])  # This works fine.

					for intSched in range(self.get_experiment_info_structure().get_num_schedules()):

						for intBlock in range(intNumBlocks):  # One block per row of worksheet
							intR1 = intB1 = intR2 = intB2 = intP1 = intP2 = 0  # Initialize totals

							#This for...next loop should total intR1, intR2, intB2, intP1, and intP2 in 500-generation blocks.----------------------------------
							for intGen in range(500 * intBlock, (intBlock + 1) * 500):  # 500-generation blocks
								# Add up intR1, intB1, intR2, intB2, intP1, intP2
								intTargetStatus = self.check_for_targets(intEmittedPheno[intRep, intSched, intGen])
								if intTargetStatus == 0:
									pass
									# Not a target
								elif intTargetStatus == 1:
									# Target 1
									intB1 += 1
									if blnPhenoReinforced[intRep, intSched, intGen]:
										intR1 += 1

									if blnPhenoPunished[intRep, intSched, intGen]:
										intP1 += 1

								elif intTargetStatus == 2:
									# Target 2
									intB2 += 1  # Fuuuuuuuuuuuccck!  This was a 2!
									if blnPhenoReinforced[intRep, intSched, intGen]:
										intR2 += 1

									if blnPhenoPunished[intRep, intSched, intGen]:
										intP2 += 1

							#-------------------------------------------------------------------------------------------------------------------

							# intR1, intB1, intR2, intB2, intP1, and intP2 should now be totalled
							# Write row (intBlock) of worksheet
							strRow = str(intBlock + 2 + intSched * intNumBlocks)  # +2 because Excel is 1-indexed and the header resides at 1
							objWS[intRep + 1].write_row("A" + strRow + ":G" + strRow, [intSched + 1, intP1, intR1, intB1, intP2, intR2, intB2])  #  This solves the prob!! # +1 because humans are 1-indexed

		except EnvironmentError as err:
			print(err)

	def check_for_targets(self, intPheno):

		# Tests whether intPheno is a target.  returns 1 if it is a target 1 pheno, 2 if it is a target 2 pheno, and 0 if it is not a target pheno

		if intPheno >= self.get_experiment_info_structure().get_t_1_lo() and intPheno <= self.get_experiment_info_structure().get_t_1_hi():
			# This is a Target 1 pheno
			return 1
		elif intPheno >= self.get_experiment_info_structure().get_t_2_lo() and intPheno <= self.get_experiment_info_structure().get_t_2_hi():
			# This is a Target 2 pheno
			return 2
		else:
			# This is not a target pheno
			return 0
