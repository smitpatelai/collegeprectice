import numpy as np
from numpy.ma.core import transpose

#10 , 20 ,masking
#shape manipulation

runs = np.array([
    [124,93,24,100],
    [264,209,168,98],
    [49,68,7,120]
])


print("runs",runs)
print(runs.shape)



#reshape
#reshape = runs.reshape(2,6)
# print(reshape)

reshape = runs.reshape(-1,3)
print(reshape)

transpose = runs.T
print(transpose)
print(transpose.shape)



#stacking
new_player = np.array([
    [100,22,33,44]
])
print(new_player)
runs =np.vstack((new_player,runs))
print(runs)


new_match = np.array(([1],[2],[3],[4]))
runs = np.hstack((new_match,runs))

# counts
new_data = np.array([
    [43,45,46,47,48]
])

concate = np.concatenate((new_data,runs[:2]),axis=0)
print(concate)

print(runs)

team_a , team_b = np.split(runs,2)
print(team_a)
print(team_b)

score = [50,100]
data_exists = np.isin(runs,score)
print(data_exists)
