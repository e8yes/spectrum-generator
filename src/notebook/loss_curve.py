import re
import numpy as np
import matplotlib.pyplot as plt
from glob import glob
from pandas import read_csv
from pandas import DataFrame

files = glob("*_*_loss")

epoch_numbers = list()
average_losses = list()
upper_losses = list()
lower_losses = list()

for file in files:
    epoch_number = int(re.search("[0-9]+", file)[0])

    df = read_csv(file)
    avg_loss = np.mean(df.iloc[:,1])

    std = np.std(df.iloc[:,1])
    upper_loss = avg_loss + std
    lower_loss = avg_loss - std

    epoch_numbers.append(epoch_number)
    average_losses.append(avg_loss)
    upper_losses.append(upper_loss)
    lower_losses.append(lower_loss)

result = DataFrame({"epoch": epoch_numbers, 
                    "loss": average_losses,
                    "upper_loss": upper_losses,
                    "lower_loss": lower_losses})
result.sort_values("epoch", inplace=True)

print(result)

plt.plot(result.epoch, result.loss)
plt.plot(result.epoch, result.upper_loss)
plt.plot(result.epoch, result.lower_loss)
plt.show()

