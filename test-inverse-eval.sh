for learner in 0 1
do
    for experiment in 0 2 4 5 6 8 9 10  1 3 7
    do
        python test-inverse-eval.py $learner $experiment
    done
done