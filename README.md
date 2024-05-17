# TSL/ITSL Online Learner

This is a Python 3 implementation of the TSL grammar learner presented by Dakotah Lambert's 2021 "Grammar Interpretations and Learning TSL Online" (https://proceedings.mlr.press/v153/lambert21a/lambert21a.pdf),
as well as an implementation of a novel ITSL grammar learner based on the TSL learner algorithm.

Additionally, scripts for testing consistency and completeness of the grammars inferred by this learner on several patterns are found in Aksenova.py (using the pipeline from Aksënova 2020, found at https://www.proquest.com/docview/2436889255?pq-origsite=gscholar&fromopenview=true).

Please cite as:

*Johnson, Jacob K., and Aniello De Santo. "Online Learning of ITSL Grammars." Society for Computation in Linguistics (2024).*

The main implementations and some helper functions for usage are located in Lambert.py or the interactive Lambert.ipynb

To run learning/generation, run:
    `bash test-learn.py`
To run evaluation of generated strings, run:
    `bash test-eval.py`
Note that this will take a long time to run, so you may wish to change the number of strings generated (`num_strings`), change the number of trials run, or select only certain learners/experiments (within test-learn.sh)