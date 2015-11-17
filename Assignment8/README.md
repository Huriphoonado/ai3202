# Hidden Markov Models

Run the program specifying the input file, and then a file to test the algorithm with:

```
$ python Payne_Assignment8.py "typos20.data" "typos20Test.data" >> output.txt
```

The Viterbi algorithm is able to produce slightly more accurate results than the observed data.

```
Observations Error Rate: 0.161433
Viterbi Error Rate: 0.104167
States | Observations | Viterbi
----------------------------
i | i | i | 
n | n | n | 
t | t | t | 
r | r | r | 
o | o | o | 
d | d | d | 
u | u | u | 
c | c | c | 
t | t | t | 
i | i | i | 
o | p | o | 
n | n | n | 
_ | _ | _ | 
t | t | t | 
h | h | h | 
...
```