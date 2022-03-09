'''
Created on Mar 4, 2022

@author: bleem
'''

from statistics import mean
import winsound

from sklearn.linear_model import LinearRegression
import numpy

from src.common import JSONData, Tallies
from src.common.adam import AdamObject
from src.common.frmExperiment import frmExperiment
from src.orgs.frmBuildOrganism import frmBuildOrganism
import multiprocessing as mp

DIR = "../../inputs/"

BT = DIR + "bias_test.json"
R_ONLY = DIR + "rate_only.json"
E_1 = DIR + "experiment_1.json"
E_2_1 = DIR + "experiment_2_1.json"
E_2_2_1 = DIR + "experiment_2_2_1.json"
E_2_2_2 = DIR + "experiment_2_2_2.json"
E_3_1 = DIR + "experiment_3_1.json"
E_3_2 = DIR + "experiment_3_2.json"

AR_TARGET = .83
AM_TARGET = .68
CO_TARGET = 5692.8

HALF_NUM_THREADS = 8
DELTA_MULTIPLIER = 0.1


def clamp(value, min_, max_):
	if value < min_: return min_
	if value > max_: return max_
	return value


class Optimizing:

	def get_loss(self, input_data):  # mag_slope, mag_intercept, reb_constant, return_dict, key):

		mag_slope, mag_intercept, reb_constant, return_dict, key = input_data
		data = JSONData.load_file(E_1, print_status = True)

		data.set_net_one_magnitude_slope(mag_slope)
		data.set_net_one_magnitude_intercept(mag_intercept)
		data.set_net_one_neutral_magnitude(reb_constant)

		org_builder = frmBuildOrganism()
		org_builder.create_an_organism(data)
		exp_runner = frmExperiment(org_builder)
		exp_runner.run(data, print_status = True, write_outfile = False)
		objConc = exp_runner.getObjConcs()[0]

		ar_array = []
		am_array = []
		changeovers_array = []

		for intRep in range(objConc.get_num_repetitions()):

			x = []
			y = []

			total_changeovers = 0

			for intSched in range(objConc.get_num_schedules()):
				r1, r2, _, _, b1, b2, changeovers = objConc.getTallies(intRep, intSched)
				total_changeovers += changeovers

				if r1 * r2 * b1 * b2 != 0:
					logR = Tallies.safe_log_of_ratio(r1, r2)
					logB = Tallies.safe_log_of_ratio(b1, b2)

					mu_1 = objConc.get_experiment_info().get_FDF_mean_1(intSched)
					mu_2 = objConc.get_experiment_info().get_FDF_mean_2(intSched)

					logM = Tallies.safe_log_of_ratio(mu_2, mu_1)

					x.append([logR, logM])
					y.append(logB)

			reg = LinearRegression().fit(x, y)
			ar_array.append(reg.coef_[0])
			am_array.append(reg.coef_[1])
			changeovers_array.append(total_changeovers)

		ar_avg = mean(ar_array)
		am_avg = mean(am_array)
		changeovers_avg = mean(changeovers_array)

		return_dict[key] = (ar_avg, am_avg, changeovers_avg)


mag_slope = AdamObject(-0.596, gamma = 0.003)
mag_intercept = AdamObject(0.463, gamma = 0.003)
reb_constant = AdamObject(0.0592, gamma = 0.0003)

adams = [mag_slope, mag_intercept, reb_constant]

min_loss = None

if __name__ == "__main__":

	index = 1
	with mp.Pool(processes = 2 * HALF_NUM_THREADS) as pool:

		manager = mp.Manager()
		return_dict = manager.dict()

		while(True):

			args_list = []
			print("index:\t\t" + str(index))
			print("slope:\t\t" + str(mag_slope.get_value()))
			print("intercept:\t" + str(mag_intercept.get_value()))
			print("reb:\t\t" + str(reb_constant.get_value()))

			f = open("optimizing.txt", "a")

			f.write("slope:\t\t" + str(mag_slope) + "\n")
			f.write("intercept:\t" + str(mag_intercept) + "\n")
			f.write("reb:\t\t" + str(reb_constant) + "\n")

			f.close()

			delta = abs(adams[index].get_value() * DELTA_MULTIPLIER)

			params = (mag_slope.get_value() - (delta / 2 if index == 0 else 0),
					mag_intercept.get_value() - (delta / 2 if index == 1 else 0),
					reb_constant.get_value() - (delta / 2 if index == 2 else 0),
					return_dict)

			for i in range(HALF_NUM_THREADS):
				args_list.append(params + (i,))

			params_altered = (mag_slope.get_value() + (delta / 2 if index == 0 else 0),
							mag_intercept.get_value() + (delta / 2 if index == 1 else 0),
							reb_constant.get_value() + (delta / 2 if index == 2 else 0),
							return_dict)

			for i in range(HALF_NUM_THREADS):
				args_list.append(params_altered + (i + HALF_NUM_THREADS,))

			func = Optimizing().get_loss

			pool.map(func, args_list)

			# loss = 0
			# altered_loss = 0
			sum_ar = numpy.zeros((2,))
			sum_am = numpy.zeros((2,))
			sum_co = numpy.zeros((2,))

			for k in return_dict:
				idx = 0 if k < HALF_NUM_THREADS else 1
				sum_ar[idx] += return_dict[k][0]
				sum_am[idx] += return_dict[k][1]
				sum_co[idx] += return_dict[k][2]

			avg_ar = sum_ar / HALF_NUM_THREADS
			avg_am = sum_am / HALF_NUM_THREADS
			avg_co = sum_co / HALF_NUM_THREADS

			ar_diff = (avg_ar - AR_TARGET) / AR_TARGET
			am_diff = (avg_am - AM_TARGET) / AM_TARGET
			co_diff = (avg_co - CO_TARGET) / CO_TARGET

			loss_0 = ar_diff[0] ** 2 + am_diff[0] ** 2 + co_diff[0] ** 2
			loss_1 = ar_diff[1] ** 2 + am_diff[1] ** 2 + co_diff[1] ** 2

			avg_loss = (loss_0 + loss_1) / (2 * HALF_NUM_THREADS)
			is_best = False
			if min_loss is None or min_loss > avg_loss:
				min_loss = avg_loss
				is_best = True

			print("average loss:\t" + str(avg_loss) + ("*" if is_best else ""))
			print("average ar:\t" + str(numpy.sum(sum_ar) / (2 * HALF_NUM_THREADS)))
			print("average am:\t" + str(numpy.sum(sum_am) / (2 * HALF_NUM_THREADS)))
			print("average co:\t" + str(numpy.sum(sum_co) / (2 * HALF_NUM_THREADS)))

			gradient = ((loss_1 - loss_0) / HALF_NUM_THREADS) / delta
			print("gradient:\t" + str(gradient))

			adams[index].apply_gradient(gradient)
			index = (index + 1) % 3
			print("")

			winsound.PlaySound("..\\..\\resources\\22Fillywhinnygrunt2000.wav", 0)

