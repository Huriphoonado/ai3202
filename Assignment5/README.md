Willie Payne - CSCI 3202

#Assignment 5

###Implementation of Markov Decision Processes.

The program should be called with command line arguments indicating the world to be used (World1MDO.txt) and then a value for epsilon (0.5, 1000). For example:

```
$ python Payne_Assignment5.py World1MDP.txt 0.5
$ python Payne_Assignment5.py World1MDP.txt 1000
```

#### Results for Different Epsilon Values

I explored values less than 0.5 and greater than 0.5. Overall, all solutions produced equal or suboptimal solutions to  I found that values less than 0.5 do not produce different locations and only slightly change the utility values. Consider the following:

Epsilon = 0.5

```
$ python Payne_Assignment5.py World1MDP.txt 0.5
Location: 0 0 Utility: 5.623
Location: 1 0 Utility: 6.356
Location: 2 0 Utility: 7.603
Location: 3 0 Utility: 8.661
Location: 4 0 Utility: 9.828
Location: 5 0 Utility: 11.314
Location: 6 0 Utility: 12.886
Location: 6 1 Utility: 14.874
Location: 6 2 Utility: 16.941
Location: 6 3 Utility: 19.123
Location: 6 4 Utility: 22.929
Location: 7 4 Utility: 26.590
Location: 7 5 Utility: 29.352
Location: 8 5 Utility: 33.400
Location: 9 5 Utility: 38.039
Location: 9 6 Utility: 43.902
Final Location: 9 7 Reward: 50.000
engr2-25-227-dhcp:Assignment5 williepayn
```

Epsilon = 0.0001

```
$ python Payne_Assignment5.py World1MDP.txt 0.00001
Location: 0 0 Utility: 5.630
Location: 1 0 Utility: 6.362
Location: 2 0 Utility: 7.607
Location: 3 0 Utility: 8.664
Location: 4 0 Utility: 9.830
Location: 5 0 Utility: 11.316
Location: 6 0 Utility: 12.888
Location: 6 1 Utility: 14.875
Location: 6 2 Utility: 16.942
Location: 6 3 Utility: 19.124
Location: 6 4 Utility: 22.930
Location: 7 4 Utility: 26.591
Location: 7 5 Utility: 29.352
Location: 8 5 Utility: 33.400
Location: 9 5 Utility: 38.039
Location: 9 6 Utility: 43.902
Final Location: 9 7 Reward: 50.000
```

This path crosses 17 nodes including one mountain, and one barn.

Then I tried to determine the lowest epsilon value that produces a different solution. I found 450 which produces the following new path:
```
$ python Payne_Assignment5.py World1MDP.txt 450
Location: 0 0 Utility: 0.362
Location: 0 1 Utility: 0.450
Location: 0 2 Utility: 0.875
Location: 0 3 Utility: 1.302
Location: 1 3 Utility: 1.808
Location: 1 4 Utility: 2.511
Location: 1 5 Utility: 2.099
Location: 2 5 Utility: 2.915
Location: 3 5 Utility: 3.766
Location: 4 5 Utility: 4.734
Location: 4 6 Utility: 6.214
Location: 4 7 Utility: 7.783
Location: 5 7 Utility: 12.199
Location: 6 7 Utility: 16.942
Location: 7 7 Utility: 24.920
Location: 8 7 Utility: 36.000
Final Location: 9 7 Reward: 50.000
```

This path also crosses 17 nodes including one barn but it is worse than the previous solution since it crosses 3 mountains.
