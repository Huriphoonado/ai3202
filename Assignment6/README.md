# Bayes Net Disease Predictor

The bulk of the work in this assignment was put into solving conditional probabilities. Because of the way it was implemented, given beliefs must be true and are provided as capital letters e.g. -g"~p|DS"

## Sample Queries

```
$ python Payne_Assignment6.py -pS.5  -g"s|"
0.5

$ python Payne_Assignment6.py -jpsc
0.0081

$ python Payne_Assignment6.py -g"d|S"
0.3112

$ python Payne_Assignment6.py -g"~p|DS"
0.101999371856

$ python Payne_Assignment6.py -g"~p|SD"
0.101999371856

$ python Payne_Assignment6.py -pS.5  -mD
0.3061075
```