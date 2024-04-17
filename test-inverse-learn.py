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

# # # Start deleted segment
'''
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

'''
# # # Start replacement segment
#load in all the strings that the learner was trained on 
train_data = set()
with open(f"{out_dir}/input_data/{this}_{trial_id}.txt", "r") as reader:
    for line in reader.readlines():
        line = line.strip('\n')
        train_data.add(line)
def in_train_data(w):
    return w in train_data

#generate instances from target grammar
def evaluator_function(w):
    return evaluator([w], *evaluator_args, **evaluator_kwargs)

def generate_from_evaluator(n, use_iterator=False, skip_train_instances=True):
    def generate_with_iterator(n=n):
        alphabet=set(''.join(train_data))
        j = 0
        while True:
            for w in map(''.join, product(alphabet, repeat=j)):
                if evaluator_function(w) and (True if not skip_train_instances else not in_train_data(w)):
                    yield w
                    n -= 1
                    if n == 0:
                        return
            j += 1
    return ((lambda x:x) if use_iterator else list)(tqdm(generate_with_iterator(), total=n))

with open(f"{out_dir}/target_strings/{experiment_name}.txt", "w") as writer:
    writer.write('')
for w in generate_from_evaluator(num_strings, use_iterator=True):
    with open(f"{out_dir}/target_strings/{experiment_name}.txt", "a") as writer:
        writer.write(w + '\n')
