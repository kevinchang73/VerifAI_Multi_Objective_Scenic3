import sys
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

infile = open(sys.argv[1], 'r') # *.txt
mode = sys.argv[2] # multi / single
order = sys.argv[3] # -1 / 0 / 1

# error weights
result_count_0 = [[] for i in range(2)]
result_count_1 = [[] for i in range(2)]
# counterexample types
counterexample_type_0 = [{} for i in range(2)]
counterexample_type_1 = [{} for i in range(2)]
curr_source = 0
lines = infile.readlines()
infile.close()

count = 0

for i in range(len(lines)):
    if order == '0':
        curr_source = 0
    elif order == '1':
        curr_source = 1
    if mode == 'multi':
        if 'RHO' in lines[i]:
            line = lines[i+1].strip().split(' ')
            val1 = []
            for s in line:
                if s != '':
                    val1.append(float(s) < 0)
            assert len(val1) == 2, 'Invalid length of rho'
            result_count_0[curr_source].append(val1[0]*2 + val1[1]*1)
            if tuple(1*np.array([val1[0], val1[1]])) in counterexample_type_0[curr_source]:
                counterexample_type_0[curr_source][tuple(1*np.array([val1[0], val1[1]]))] += 1
            else:
                counterexample_type_0[curr_source][tuple(1*np.array([val1[0], val1[1]]))] = 1

            line = lines[i+2].strip().split(' ')
            val2 = []
            for s in line:
                if s != '':
                    val2.append(float(s) < 0)
            assert len(val2) == 2, 'Invalid length of rho'
            result_count_1[curr_source].append(val2[1]*2 + val2[0]*1)
            if tuple(1*np.array([val2[1], val2[0]])) in counterexample_type_1[curr_source]:
                counterexample_type_1[curr_source][tuple(1*np.array([val2[1], val2[0]]))] += 1
            else:
                counterexample_type_1[curr_source][tuple(1*np.array([val2[1], val2[0]]))] = 1

            if order == '-1':
                curr_source = 1 - curr_source
            
            count += 1
            if count == 900:
                break
    else:
        if 'Actual rho' in lines[i]:
            line = lines[i+1].strip().split(' ')
            val1 = []
            for s in line:
                if s != '':
                    val1.append(float(s) < 0)
            assert len(val1) == 4, 'Invalid length of rho'
            result_count_0[curr_source].append(val1[0]*2 + val1[1]*1)
            if tuple(1*np.array([val1[0], val1[1]])) in counterexample_type_0[curr_source]:
                counterexample_type_0[curr_source][tuple(1*np.array([val1[0], val1[1]]))] += 1
            else:
                counterexample_type_0[curr_source][tuple(1*np.array([val1[0], val1[1]]))] = 1

            line = lines[i+2].strip().split(' ')
            val2 = []
            for s in line:
                if s != '':
                    val2.append(float(s) < 0)
            assert len(val2) == 4, 'Invalid length of rho'
            result_count_1[curr_source].append(val2[3]*2 + val2[2]*1)
            if tuple(1*np.array([val2[3], val2[2]])) in counterexample_type_1[curr_source]:
                counterexample_type_1[curr_source][tuple(1*np.array([val2[3], val2[2]]))] += 1
            else:
                counterexample_type_1[curr_source][tuple(1*np.array([val2[3], val2[2]]))] = 1

print('Error weights')
print('segment 0:')
for i in range(1):
    print('average:', np.mean(result_count_0[i]), 'max:', np.max(result_count_0[i]), 'percentage:', float(np.count_nonzero(result_count_0[i])/len(result_count_0[i])), result_count_0[i])
print('segment 1:')
for i in range(1):
    print('average:', np.mean(result_count_1[i]), 'max:', np.max(result_count_1[i]), 'percentage:', float(np.count_nonzero(result_count_1[i])/len(result_count_1[i])), result_count_1[i])

print('\nCounterexample types')
print('segment 0:')
for i in range(1):
    print('Types:', len(counterexample_type_0[i]))
    for key, value in reversed(sorted(counterexample_type_0[i].items(), key=lambda x: x[0])):
        print("{} : {}".format(key, value))
print('segment 1:')
for i in range(1):
    print('Types:', len(counterexample_type_1[i]))
    for key, value in reversed(sorted(counterexample_type_1[i].items(), key=lambda x: x[0])):
        print("{} : {}".format(key, value))
print()
