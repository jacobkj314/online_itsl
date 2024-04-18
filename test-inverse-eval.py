'''
from sys import argv
learner_id, experiment_id, trial_id, num_strings = map(int, argv[1:])

from Aksenova import *
from Lambert import *

out_dir = "experiments"

learner = [tsl_args , itsl_args][learner_id]
experiment = experiments[experiment_id]['args']


LEARNER, learner_name, learner_args, learner_kwargs = learner
experiment_name, data, num_samples, evaluator, evaluator_args, evaluator_kwargs = experiment

this = learner_name + experiment_name

with open(f"{out_dir}/input_data/{this}_{trial_id}.txt", "w") as writer:
    for w in data:
        writer.write(w + '\n')

globals()[this] = LEARNER(*learner_args, **learner_kwargs)
globals()[this].data = data +[''] # added to eliminate *>< on all tiers
globals()[this].extract_alphabet()
globals()[this].learn()

with open(f"{out_dir}/grammars/{this}_{trial_id}.txt", "w") as writer:
    writer.write(str(globals()[this].grammar))

with open(f"{out_dir}/generations/{this}_{trial_id}.txt", "w") as writer:
    writer.write('')
for w in globals()[this].generate_sample(num_strings, use_iterator=True):
    with open(f"{out_dir}/generations/{this}_{trial_id}.txt", "a") as writer:
        writer.write(w + '\n')

# # # # # # # 

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
        W += reader.read().splitlines()
ratio = evaluator(tqdm(W), *evaluator_args, **evaluator_kwargs)
print(this, f"{ratio*100}%")
print()
with open(f"{out_dir}/ratio/{this}.txt", "w") as writer:
    writer.write(str(ratio))
'''

# # # # #

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

import Lambert
from Lambert import Set

out_dir = "experiments"

learner_name = ["tsl", "itsl"][learner_id]# # # # # [tsl_args , itsl_args][learner_id]
experiment = experiments[experiment_id]['args']


experiment_name, data, num_samples, evaluator, evaluator_args, evaluator_kwargs = experiment

this = learner_name + experiment_name


from glob import glob
G = []

from tqdm import tqdm

#read in grammars
for file_path in glob(f"{out_dir}/grammars/{this}_*.txt"):
    with open(file_path) as reader:
        g = (Lambert.TSL_Learner if (learner_name == "tsl") else Lambert.ITSL_Learner)()
        grammar_as_string = reader.read()
        grammar_tuple = eval(grammar_as_string) # I know this is bad! But saving to a string instead of, say, pickle allows the grammars to be human-readable on the disk
        if learner_name == "tsl":
            g.k = grammar_tuple[0]
        else:
            g.k, g.m = grammar_tuple[0]
        g.G_l = grammar_tuple[1]
        g.G_s = grammar_tuple[2]

        G.append(g)


from statistics import mean, stdev

#read in target strings
W = []
with open(f"{out_dir}/target_strings/{experiment_name}.txt",) as reader:
    W += reader.read().splitlines()

#get ratio evaluator function
def evaluator_function(g, W):
    return mean(g.scan(w) for w in W)

ratios = [evaluator_function(g, W) for g in G]
ratio = mean(ratios)
ratio_stdev = 0.0 if len(ratios) < 2 else stdev(ratios)

print(this, "completeness:", f"{ratio*100}% ({ratio_stdev*100}%)")

with open(f"{out_dir}/ratio_completeness/{this}.txt", "w") as writer:
    writer.write(str(ratio))
    writer.write("\n")
    writer.write(str(ratio_stdev))