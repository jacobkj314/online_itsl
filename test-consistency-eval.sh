for learner in 0 1
do
    for experiment in 0 1 2 3 4 5 6 7 8 9 10
    do
        python test-eval.py $learner $experiment
    done
done