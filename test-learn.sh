for learner in 0 1
do
    for experiment in 0 2 4 5 6 8 9 10
    do
        for trial in 1 2 3 4 #need to extend to 10 total
        do
            python test-learn.py $learner $experiment $trial > big/transcripts/$learner-$experiment-$trial.txt &
        done
    done

    for experiment in 1 3 7 
    do
        python test-learn.py $learner $experiment 0  > big/transcripts/$learner-$experiment-0.txt &
    done
done