'''
Created on May 26, 2021

@author: bleem
'''

import winsound

from src.common import JSONData
from src.common.frmExperiment import frmExperiment
from src.orgs.frmBuildOrganism import frmBuildOrganism

DIR = "../../inputs/"

BT = DIR + "bias_test.json"
R_ONLY = DIR + "rate_only.json"
E_1 = DIR + "experiment_1.json"
E_2_1 = DIR + "experiment_2_1.json"
E_2_2_1 = DIR + "experiment_2_2_1.json"
E_2_2_2 = DIR + "experiment_2_2_2.json"
E_3_1 = DIR + "experiment_3_1.json"
E_3_2 = DIR + "experiment_3_2.json"

if __name__ == '__main__':

	data = JSONData.load_file(E_3_2, print_status = True)

	org_builder = frmBuildOrganism()
	org_builder.create_an_organism(data)
	exp_runner = frmExperiment(org_builder)
	exp_runner.run(data)

	winsound.PlaySound("..\\..\\resources\\22Fillywhinnygrunt2000.wav", 0)
