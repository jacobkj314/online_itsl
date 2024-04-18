from sys import argv
learner_id, experiment_id = map(int, argv[1:])

import sys
from io import StringIO
stdout = sys.stdout
temp_stdout = StringIO()
sys.stdout = temp_stdout
from Aksenova import *
sys.stdout = stdout
temp_stdout.close()

out_dir = "experiments"

learner_name = ["tsl", "itsl"][learner_id]# # # # # [tsl_args , itsl_args][learner_id]
experiment = experiments[experiment_id]['args']


experiment_name, data, num_samples, evaluator, evaluator_args, evaluator_kwargs = experiment

this = learner_name + experiment_name


from glob import glob
W = []

from tqdm import tqdm

for file_path in glob(f"{out_dir}/generations/{this}_*.txt"):
    with open(file_path) as reader:
        W.append(reader.read().splitlines())
ratios = [evaluator(tqdm(i), *evaluator_args, **evaluator_kwargs) for i in W[:5000]]

from statistics import mean, stdev

ratio = mean(ratios)
ratio_stdev = 0.0 if len(ratios) < 2 else stdev(ratios)


print(this, "consistency:", f"{ratio*100}% ({ratio_stdev*100}%)")

print()
with open(f"{out_dir}/ratio_consistency/{this}.txt", "w") as writer:
    writer.write(str(ratio))
    writer.write("\n")
    writer.write(str(ratio_stdev))