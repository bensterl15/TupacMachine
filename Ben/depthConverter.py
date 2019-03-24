import numpy as np
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from skimage import color
from skimage.transform import downscale_local_mean

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
depth = depth/(255*4) + 0.25

l_depth_scaling = np.matlib.repmat(list(range(int(height - eye_displacement)))[::-1] + list(range(int(eye_displacement))),width,1)
r_depth_scaling = np.matlib.repmat(list(range(int(eye_displacement)))[::-1] + list(range(int(height - eye_displacement))),width,1)

#l_depth_scaling = np.multiply(l_depth_scaling,np.array(depth))
for i in range(l_depth_scaling.shape[0]):
	for j in range(l_depth_scaling.shape[1]):
		l_depth_scaling[i,j] = l_depth_scaling[i,j]*depth[i,j]

l_depth_scaling = l_depth_scaling / l_depth_scaling.max() + 1
r_depth_scaling = r_depth_scaling / r_depth_scaling.max() + 1



plt.imshow(l_depth_scaling,cmap='Greys',interpolation='nearest')
plt.show()
