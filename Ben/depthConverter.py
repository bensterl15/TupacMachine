import numpy as np
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from skimage import color
from skimage.transform import downscale_local_mean
import math

image_name = 'Cubic_Structure.jpg'
depth_name = 'Cubic_Depth.jpg'

screen = color.rgb2gray(mpimg.imread(image_name))
screen = downscale_local_mean(screen,(10,10))
#To adjust "correctly" we need two parameters, theta (the angle apart from the eyes)
#and the focal distance (how far back the eyes are)
theta = np.pi/6
f = 2

#We need a pixel density parameter, I don't know this for sure, but let's assume:
p_density = 75

width = screen.shape[0]
height = screen.shape[1]

eye_displacement = np.floor(p_density*f*np.tan(theta))

depth = color.rgb2gray(mpimg.imread(depth_name))
depth = downscale_local_mean(depth,(10,10))
depth = depth/4+0.25;

l_depth_scaling = np.matlib.repmat(list(range(int(height - eye_displacement)))[::-1] + list(range(int(eye_displacement))),width,1)
r_depth_scaling = np.matlib.repmat(list(range(int(eye_displacement)))[::-1] + list(range(int(height - eye_displacement))),width,1)

l_depth_scaling = np.multiply(l_depth_scaling,np.array(depth))

l_depth_scaling = l_depth_scaling / l_depth_scaling.max() + 1
r_depth_scaling = r_depth_scaling / r_depth_scaling.max() + 1

#plt.imshow(l_depth_scaling,cmap='Greys',interpolation='nearest')
#plt.show()

left = np.zeros((width, int(2.5*height)))
right = np.zeros((width, int(2.5*height)))
orientation = 0

for i in range(1,width+1):
	for j in range(1,height+1):
		index_j = j-1
		index_i = i-1		
		# Left Image Loop
		val = screen[index_i][index_j]
		depth = l_depth_scaling[index_i][index_j]

		if j < height - eye_displacement - 1:
			orientation = -1
		else:
			orientation = 1

		new_height = j + height + orientation * depth * abs(height - eye_displacement - j)
		left[index_i][abs(math.floor(new_height)) - 1] = val

		# Right Image Loop
		depth = r_depth_scaling[index_i][index_j]
		if j < eye_displacement + 1:
			orientation = -1
		else:
			orientation = 1

		new_height = j + orientation * depth * abs(j-eye_displacement)
		right[index_i][abs(math.floor(new_height))] = val

threshold = 30/255
for k in range(2):
	for i in range(width):
		for j in range(2*height-1):
			if right[i][j] < threshold:
				right[i][j] = right[i][j-1] + right[i][j+1]/2
			if left[i][j] < threshold:
				left[i][j] = left[i][j-1] + left[i][j+1]/2

fig = plt.figure()
plt.subplot(121)
plt.imshow(left,cmap='Greys',interpolation='nearest')
plt.subplot(122)
plt.imshow(right,cmap='Greys',interpolation='nearest')
fig.savefig('plot.png')
