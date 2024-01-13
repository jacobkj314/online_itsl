from sys import argv
learner_id, experiment_id, trial_id = map(int, argv[1:])

from Aksenova import *
from Lambert import *

learner = [tsl_args , itsl_args][learner_id]
experiment = experiments[experiment_id]['args']


LEARNER, learner_name, learner_args, learner_kwargs = learner
experiment_name, data, num_samples, evaluator, evaluator_args, evaluator_kwargs = experiment

this = learner_name + experiment_name

with open(f"big3/input_data/{this}_{trial_id}.txt", "w") as writer:
    for w in data:
        writer.write(w + '\n')

globals()[this] = LEARNER(*learner_args, **learner_kwargs)
globals()[this].data = data +[''] # added to eliminate *>< on all tiers
globals()[this].extract_alphabet()
globals()[this].learn()

with open(f"big3/grammars/{this}_{trial_id}.txt", "w") as writer:
    writer.write(str(globals()[this].grammar))

with open(f"big3/generations/{this}_{trial_id}.txt", "w") as writer:
    writer.write('')
for w in globals()[this].generate_sample(10000):
    with open(f"big3/generations/{this}_{trial_id}.txt", "a") as writer:
        writer.write(w + '\n')

with open(f"big3/generations/{this}_{trial_id}.txt", "r") as reader:
    W = reader.readlines()
ratio = evaluator(W, *evaluator_args, **evaluator_kwargs)
with open(f"big3/ratio/{this}_{trial_id}.txt", "w") as writer:
    writer.write(str(ratio))