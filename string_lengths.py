from glob import glob
from statistics import mean, stdev

dictionary = dict()

for file in glob("experiments/input_data/*"):
  language = int(file.split("/")[-1].split("_")[0].split("tsl")[-1])
  words = open(file).read().split("\n")

  if language not in dictionary.keys():
    dictionary[language] = set()
  dictionary[language].update(word for word in words if word is not '')
  
for language in sorted(dictionary.keys()):
  words = dictionary[language]
  lengths = [len(word) for word in words]
  lengths_dict = dict()
  for length in sorted(set(lengths)):
    lengths_dict[length] = 0
    for L in lengths:
      if L == length:
        lengths_dict[length] += 1
        
  mean_length = mean( lengths)
  sd_length   = stdev(lengths)
  print(f"{language}: {mean_length} ({sd_length})")