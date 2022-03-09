'''
Created on Mar 4, 2022

@author: bleem
'''

BLOCK_SIZE = 500
import numpy


def safe_log_of_ratio(numerator, denominator):
	return numpy.log10(numerator / denominator) if denominator * numerator > 0 else ""


def tally_schedule(intRep, intSched, intEmittedPheno, blnPhenoReinforced, blnPhenoPunished, write_to_excel, objWS, experiment_info_structure):
	intNumBlocks = int(intEmittedPheno.shape[-1] / 500)  # 500-generation blocks
	intR1Total = intB1Total = intR2Total = intB2Total = intP1Total = intP2Total = 0

	last_tc = None
	changeover_count = 0

	for intBlock in range(intNumBlocks):  # One block per row of worksheet
		intR1, intR2, intP1, intP2, intB1, intB2, changeovers, last_tc = tally_block(intBlock, BLOCK_SIZE, intRep, intSched, intEmittedPheno, blnPhenoReinforced, blnPhenoPunished, last_tc, experiment_info_structure)
		#-------------------------------------------------------------------------------------------------------------------

		# intR1, intB1, intR2, intB2, intP1, and intP2 should now be totalled
		# Write row (intBlock) of worksheet
		strRow = str(intBlock + 2 + intSched * intNumBlocks)  # +2 because Excel is 1-indexed and the header resides at 1
		if write_to_excel:
			objWS[intRep + 1].write_row("A" + strRow + ":G" + strRow, [intSched + 1, intP1, intR1, intB1, intP2, intR2, intB2])  #  This solves the prob!! # +1 because humans are 1-indexed
		intP1Total += intP1
		intP2Total += intP2
		intR1Total += intR1
		intR2Total += intR2
		intB1Total += intB1
		intB2Total += intB2
		changeover_count += changeovers

	return intR1Total, intR2Total, intP1Total, intP2Total, intB1Total, intB2Total, changeover_count


def tally_block(intBlock, blockSize, intRep, intSched, intEmittedPheno, blnPhenoReinforced, blnPhenoPunished, last_tc, experiment_info_structure):
		#This for...next loop should total intR1, intR2, intB2, intP1, and intP2 in 500-generation blocks.----------------------------------

		intB1 = intR1 = intP1 = intR2 = intB2 = intP2 = changeover_count = 0

		for intGen in range(blockSize * intBlock, (intBlock + 1) * blockSize):  # 500-generation blocks
			# Add up intR1, intB1, intR2, intB2, intP1, intP2
			intTargetStatus = check_for_targets(intEmittedPheno[intRep, intSched, intGen], experiment_info_structure)
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

				if last_tc == 2:
					changeover_count += 1

				last_tc = 1

			elif intTargetStatus == 2:
				# Target 2
				intB2 += 1  # Fuuuuuuuuuuuccck!  This was a 2!
				if blnPhenoReinforced[intRep, intSched, intGen]:
					intR2 += 1

				if blnPhenoPunished[intRep, intSched, intGen]:
					intP2 += 1

				if last_tc == 1:
					changeover_count += 1

				last_tc = 2

		return intR1, intR2, intP1, intP2, intB1, intB2, changeover_count, last_tc


def check_for_targets(intPheno, experiment_info_structure):

		# Tests whether intPheno is a target.  returns 1 if it is a target 1 pheno, 2 if it is a target 2 pheno, and 0 if it is not a target pheno
		if intPheno >= experiment_info_structure.get_t_1_lo() and intPheno <= experiment_info_structure.get_t_1_hi():
			# This is a Target 1 pheno
			return 1
		elif intPheno >= experiment_info_structure.get_t_2_lo() and intPheno <= experiment_info_structure.get_t_2_hi():
			# This is a Target 2 pheno
			return 2
		else:
			# This is not a target pheno
			return 0
