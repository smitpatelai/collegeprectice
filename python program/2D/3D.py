import numpy as np

arr_oned = np.array([10,20,30,40,50])

print(arr_oned)
#index

print(arr_oned[2:4])
print(arr_oned[-1])
print(arr_oned.shape)

arr_twod = np.array([
    [1,2,3],
    [4,5,6]
])


print(arr_twod.shape)
print(arr_twod)

#row access
print(arr_twod[0])

#col access

print(arr_twod[:,1])

#element access --- roe, col number required

print(arr_twod[1][2])


#element access -- row , col number required
print(arr_twod[1][2])
print(arr_twod[1,2])

#row slicing
print(arr_twod[:1])

#col slicing
print(arr_twod[:,:2])

#------------------3D ARRAY-------------------
arr_threed = np.array([
    #first block / layer
    [
        [1,2,3],
        [4,5,6]
    ],
    #second block/layer
    [
        [11,22,33],
        [44,55,66]
    ]
])

print(arr_threed.shape)
print(arr_threed)

#access block
print(arr_threed[1])

#element access
print(arr_threed[0][1][1])
print(arr_threed[1][0][0])

#row access
print(arr_threed[:,0])

#col access
print(arr_threed[:,:,1])

#slicing
print(arr_threed[0,:2,:2])
print(arr_threed[0:1,:2,:2])

#math operations
#block sum
print(arr_threed.sum(axis=0))

#row sum
print(arr_threed.sum(axis=1))

#col sum
print(arr_threed.sum(axis=2))

