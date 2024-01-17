rm -rf big3

rm big/*/*tsl8*
rm big/*/*tsl14*

cp big2/input_data/* big/input_data/
cp big2/grammars/* big/grammars/

cp big3000/input_data/* big/input_data/
cp big3000/grammars/* big/grammars/
cp big3000/generations/* big/generations/

cp big-nat/input_data/* big/input_data/
cp big-nat/grammars/* big/grammars/
cp big-nat/generations/* big/generations/