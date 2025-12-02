import sys
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

infile = open(sys.argv[1], 'r') # *.txt
mode = sys.argv[2] # multi / single
order = sys.argv[3] # -1 / 0 / 1

# error weights
result_count_0 = [[] for i in range(3)]
result_count_1 = [[] for i in range(3)]
# counterexample types
counterexample_type_0 = [{} for i in range(3)]
counterexample_type_1 = [{} for i in range(3)]
#result_count_0 = np.zeros(shape=(2,4), dtype=int) # result_count_0[i] = [count of 00, 01, 10, 11 in segment 0] sampled from sampler i
#result_count_1 = np.zeros(shape=(2,4), dtype=int) # result_count_1[i] = [count of 00, 01, 10, 11 in segment 1] sampled from sampler i
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
        if 'Rho' in lines[i]:
            line = lines[i].strip()
            seg1 = line[line.find('[[')+2:line.find(']')].split(' ')
            val1 = []
            for s in seg1:
                if s != '':
                    val1.append(float(s) < 0)
            assert len(val1) == 4, 'Invalid length of rho'
            result_count_0[curr_source].append(val1[0]*2 + val1[1]*1)
            if tuple(1*np.array([val1[0], val1[1]])) in counterexample_type_0[curr_source]:
                counterexample_type_0[curr_source][tuple(1*np.array([val1[0], val1[1]]))] += 1
            else:
                counterexample_type_0[curr_source][tuple(1*np.array([val1[0], val1[1]]))] = 1
            #result_count_0[curr_source][val1[0]*2 + val1[1]*1] += 1

            line = lines[i+1].strip()
            seg2 = line[line.find('[')+1:line.find(']]')].split(' ')
            val2 = []
            for s in seg2:
                if s != '':
                    val2.append(float(s) < 0)
            assert len(val2) == 4, 'Invalid length of rho'
            result_count_1[curr_source].append(val2[3]*2 + val2[2]*1)
            if tuple(1*np.array([val2[3], val2[2]])) in counterexample_type_1[curr_source]:
                counterexample_type_1[curr_source][tuple(1*np.array([val2[3], val2[2]]))] += 1
            else:
                counterexample_type_1[curr_source][tuple(1*np.array([val2[3], val2[2]]))] = 1
            #result_count_1[curr_source][val2[3]*2 + val2[2]*1] += 1

            if order == '-1':
                curr_source = 1 - curr_source
            
            count += 1
            if count == 900:
                break
    else:
        if 'Actual rho' in lines[i]:
            line = lines[i].strip()
            seg1 = line[line.find('[')+1:line.find(']')].split(' ')
            val1 = []
            for s in seg1:
                if s != '':
                    val1.append(float(s) < 0)
            assert len(val1) == 4, 'Invalid length of rho'
            result_count_0[curr_source].append(val1[0]*2 + val1[1]*1)
            if tuple(1*np.array([val1[0], val1[1]])) in counterexample_type_0[curr_source]:
                counterexample_type_0[curr_source][tuple(1*np.array([val1[0], val1[1]]))] += 1
            else:
                counterexample_type_0[curr_source][tuple(1*np.array([val1[0], val1[1]]))] = 1
            #result_count_0[curr_source][val1[0]*2 + val1[1]*1] += 1

            seg2 = line[line.find('] [')+3:-1].split(' ')
            val2 = []
            for s in seg2:
                if s != '':
                    val2.append(float(s) < 0)
            assert len(val2) == 4, 'Invalid length of rho'
            result_count_1[curr_source].append(val2[3]*2 + val2[2]*1)
            if tuple(1*np.array([val2[3], val2[2]])) in counterexample_type_1[curr_source]:
                counterexample_type_1[curr_source][tuple(1*np.array([val2[3], val2[2]]))] += 1
            else:
                counterexample_type_1[curr_source][tuple(1*np.array([val2[3], val2[2]]))] = 1
            #result_count_1[curr_source][val2[3]*2 + val2[2]*1] += 1

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

#rows = ['from sampler 0', 'from sampler 1']
##cols = ['(r0, r1) = 00', '(r0, r1) = 01', '(r0, r1) = 10', '(r0, r1) = 11']
#print('Falsification result in segment 0:')
#print(result_count_0[0][0], result_count_0[0][1], result_count_0[0][2], result_count_0[0][3])
#print(result_count_0[1][0], result_count_0[1][1], result_count_0[1][2], result_count_0[1][3])
##df = pd.DataFrame(result_count_0, columns=cols, index=rows)
##print('Falsification result in segment 0:\n', df, '\n')
##cols = ['(r3, r2) = 00', '(r3, r2) = 01', '(r3, r2) = 10', '(r3, r2) = 11']
#print('Falsification result in segment 1:')
#print(result_count_1[0][0], result_count_1[0][1], result_count_1[0][2], result_count_1[0][3])
#print(result_count_1[1][0], result_count_1[1][1], result_count_1[1][2], result_count_1[1][3])
##df = pd.DataFrame(result_count_1, columns=cols, index=rows)
##print('Falsification result in segment 1:\n', df)
