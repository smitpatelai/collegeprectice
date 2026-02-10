import numpy as np
import matplotlib.pyplot as plt

#R G B
#RED - 255, 0, 0
#GREEN - 0, 255, 0
#BLUE - 0, 0, 255
#BLACK - 0, 0, 0
#WHITE - 255, 255, 255

blackimage = np.zeros((100,100,3),dtype = np.uint8)

print(blackimage[0][0][0])
print(blackimage [0,0,1])
print(blackimage[0,0,2])

# blackimage[0,0,0] = 255
# blackimage[:,:,0] = 255
# blackimage[:,:,1] = 255
# blackimage[:,:,2] = 255

# YELLOW SQUARE
# blackimage[:,:,0] = 255
#blackimage[:,:,1] = 255
#blackimage[:,:,2] = 0

# RED SQUARE
blackimage[: ,:,0] = 65
blackimage[: ,:,1] = 105
blackimage[: ,:,2] = 225

# remove red color
# blackimage[30:70,30:70,0] = 0
# blackimage[30:70,30:70,1] = 255

# row - 0 , col - 0 , block - 0
print(blackimage [0,0,0])
# row - 0 , col - 0 , block - 1
print(blackimage[0,0,1])
# row - 0 , col - 0 , block - 2
print(blackimage[0,0,2])

# pixel
print(blackimage[0,0])
print(blackimage[90,90])

# 255, 105, 180 -- PINK COLOR

# Top border
blackimage[0:6, :, 0] = 255
blackimage[0:6, :, 1] = 105
blackimage[0:6, :, 2] = 180

# Bottom border
blackimage[-6:, :, 0] = 255
blackimage[-6:, :, 1] = 105
blackimage[-6:, :, 2] = 180

# Left border
blackimage[:, 0:6, 0] = 255
blackimage[:, 0:6, 1] = 105
blackimage[:, 0:6, 2] = 180

# Right border
blackimage[:, -6:, 0] = 255
blackimage[:, -6:, 1] = 105
blackimage[:, -6:, 2] = 180

#
plt.imshow(blackimage)
plt.axis("off")
plt.show()


# whiteimage = np.ones((100,100,3),dtype=np.uint8) *240

# plt.imshow(whiteimage)
# plt.axis("off")
# plt.show()