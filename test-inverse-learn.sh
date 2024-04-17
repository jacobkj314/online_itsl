num_strings=5000
for learner in 0 # # # 1
do
    #artificial language experiments
    for experiment in 0 2 4 5 6 8 9 10
    do
        for trial in 1 # # # 2 3 4 5 6 7 8 9 10 #running 10 trials of each experiment: since the input samples are randomly generated, this can result in a different grammar
        do
            python test-inverse-learn.py $learner $experiment $trial $num_strings > experiments/transcripts/$learner-$experiment-$trial-inverse.txt &
        done
    done

    # # # #natural language experiments
    # # # for experiment in 1 3 7 
    # # # do
    # # #     python test-learn.py $learner $experiment 0  > experiments/transcripts/$learner-$experiment-0.txt &
    # # # done
done