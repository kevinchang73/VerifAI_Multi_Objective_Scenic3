import sys
import matplotlib.pyplot as plt
import numpy as np
import os

directory = sys.argv[1]
all_files = os.listdir(directory)
all_files = [f for f in all_files if f.endswith('.csv') and f.startswith(sys.argv[2]+'.')]
mode = sys.argv[3] # multi / single

fig = plt.figure()
ax = fig.add_subplot(projection='3d')
count = 0
ego_speed = []
ego_brake = []
adv_speed = []
adv1_dist = []
for file in all_files:
    infile = open(directory+'/'+file, 'r')
    lines = infile.readlines()
    if mode == 'single':
        for i in range(1, len(lines)):
            line = lines[i] #TODO: identify the counterexamples
            ego_speed.append(float(line.split(',')[-10]))
            ego_brake.append(float(line.split(',')[-11]))
            adv_speed.append(float(line.split(',')[-12]))
            adv1_dist.append(float(line.split(',')[-13]))
    else:
        for i in range(1, len(lines), 3):
            line1 = lines[i]
            line2 = lines[i+1]
            line3 = lines[i+2] #TODO: identify the counterexamples
            ego_speed.append(float(line1.split(',')[-10]))
            ego_brake.append(float(line1.split(',')[-11]))
            adv_speed.append(float(line1.split(',')[-12]))
            adv1_dist.append(float(line1.split(',')[-13]))

ax.scatter(ego_speed, adv_speed, adv1_dist)
ax.set_xlabel('EGO_SPEED')
ax.set_ylabel('ADV_SPEED')
ax.set_zlabel('ADV1_DIST')
plt.savefig(directory+'/'+sys.argv[2]+'_scatter.png')

print("Standard deviation of ego_speed:", np.std(ego_speed), len(ego_speed))
print("Standard deviation of adv_speed:", np.std(adv_speed), len(adv_speed))
print("Standard deviation of ego_brake:", np.std(ego_brake), len(ego_brake))
print("Standard deviation of adv1_dist:", np.std(adv1_dist), len(adv1_dist))
print()
