# TSL Online Learner

This is an implementation of the TSL grammar learner presented by Dakotah Lambert's 2021 "Grammar Interpretations and Learning TSL Online" (https://proceedings.mlr.press/v153/lambert21a/lambert21a.pdf)

The main implementation and some helper functions for usage are located in Lambert.py



Additionally, a notebook for testing the consistency of the grammars formed by this learner on several patterns are found in MITSL2IA_notebook.ipynb and MTSL2IA_notebook.ipynb (using the pipeline from Aksënova 2020, found at https://www.proquest.com/docview/2436889255?pq-origsite=gscholar&fromopenview=true)


Finally, because this TSL learner appears to also learn MTSL languages, mtsl_random.py contains code to randomly generate MTSL2 grammars and attempt to get the algorithm to learn them. 
Usage: `python mtsl_random.py <length of longest string in the input sample> <length of strings to test on> [quick]`
for example: `python mtsl_random.py 7 9 quick`
