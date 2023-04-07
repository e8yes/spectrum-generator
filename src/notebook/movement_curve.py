import re
import numpy as np
import matplotlib.pyplot as plt
from glob import glob
from pandas import DataFrame

files = glob("user_profile_*")

all_profiles = list()

for file in files:
    epoch_number = int(re.search("[0-9]+", file)[0])
    profile = np.loadtxt(file)

    all_profiles.append((epoch_number, profile))

all_profiles = sorted(all_profiles, key=lambda tp: tp[0])


epoch_numbers = list()
total_displacements = list()
total_movements = list()

for epoch_number, profile in all_profiles:
    diff = profile - all_profiles[0][1]
    total_movement = np.sum(diff)
    total_displacement = np.sqrt(np.sum(diff*diff))

    epoch_numbers.append(epoch_number)
    total_displacements.append(total_displacement)
    total_movements.append(total_movement)
    

result = DataFrame({"epoch": epoch_numbers, 
                    "displacement": total_displacements,
                    "movement": total_movements})
result.sort_values("epoch", inplace=True)

plt.plot(result.epoch, result.displacement, label="displacement")
plt.plot(result.epoch, result.movement, label="movement")
plt.legend(loc="upper left")
plt.show()

