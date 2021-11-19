'''
Created on May 26, 2021

@author: bleem
'''

from frmBuildOrganism import frmBuildOrganism
from frmExperiment import frmExperiment
import JSONData

if __name__ == '__main__':

	data = JSONData.load_file("../exp_files/reinforcement_only.json", print_status = True)
	for exp_index in range(data.get_num_experiments()):
		org_builder = frmBuildOrganism()
		org_builder.create_a_population(data)
		exp_runner = frmExperiment(org_builder)
		exp_runner.run(data)
