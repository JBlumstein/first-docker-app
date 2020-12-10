import random
import numpy as np

print('Do some math')

rits = []
for i in range(10): rits.append(random.randint(0,10))

print(f'the mean of {rits} is {np.mean(rits)}')