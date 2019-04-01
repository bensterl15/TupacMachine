import numpy as np
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from skimage import color
from skimage.transform import downscale_local_mean
from scipy.ndimage import gaussian_filter
import math

def downSampleRows(im,M):
	return downscale_local_mean(im,(M,1))

def downSampleCols(im,M):
	return downscale_local_mean(im,(1,M))

def removeColsOnSides(im,N):
	return im[:,(N):(-N)]	

def removeRowsOnSides(im,N):
	return im[(N):(-N),:]

image_name = 'image.png' #'Cubic_Structure.jpg'
depth_name = 'depth.png' #'Cubic_Depth.jpg'

screen = color.rgb2gray(mpimg.imread(image_name))
screen = removeColsOnSides(screen,192)
screen = downSampleRows(downSampleCols(screen,3),3)

depth = color.rgb2gray(mpimg.imread(depth_name))
depth = removeRowsOnSides(depth,32)
depth = depth/4+0.25

print(screen.shape)
print(depth.shape)

#To adjust "correctly" we need two parameters, theta (the angle apart from the eyes)
#and the focal distance (how far back the eyes are)
theta = np.pi/6
f = 2

#We need a pixel density parameter, I don't know this for sure, but let's assume:
p_density = 75

width = screen.shape[0]
height = screen.shape[1]

eye_displacement = np.floor(p_density*f*np.tan(theta))

l_depth_scaling = np.matlib.repmat(list(range(int(height - eye_displacement)))[::-1] + list(range(int(eye_displacement))),width,1)
r_depth_scaling = np.matlib.repmat(list(range(int(eye_displacement)))[::-1] + list(range(int(height - eye_displacement))),width,1)

l_depth_scaling = np.multiply(l_depth_scaling,np.array(depth))

l_depth_scaling = l_depth_scaling / l_depth_scaling.max() + 1
r_depth_scaling = r_depth_scaling / r_depth_scaling.max() + 1

#plt.imshow(l_depth_scaling,cmap='Greys',interpolation='nearest')
#plt.show()

left = np.zeros((width, int(3*height)))
right = np.zeros((width, int(3*height)))
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

def filterImage(im,width,height):
	threshold = 30/255
	while(np.count_nonzero(im==0) > 2*width):
		for i in range(1,width+1):
			for j in range(2,int(3*height)):
				index_i = i - 1
				index_j = j - 1
				if(im[index_i][index_j] == 0):
					if(im[index_i][index_j - 1] != 0 and im[index_i][index_j + 1] != 0):
						im[index_i][index_j] = (im[index_i][index_j - 1] + im[index_i][index_j + 1])/2
					elif(im[index_i][index_j - 1] != 0):
						im[index_i][index_j] = im[index_i][index_j - 1]
					elif(im[index_i][index_j + 1] != 0):
						im[index_i][index_j] = im[index_i][index_j + 1]
				elif(im[index_i][index_j] < threshold):
					im[index_i][index_j] = (im[index_i][index_j - 1] + im[index_i][index_j + 1])/2
		
		for i in range(width,0,-1):
			for j in range(int(3*height - 1),1,-1):
				index_i = i - 1
				index_j = j - 1
				if(im[index_i][index_j] == 0):
					if(im[index_i][index_j - 1] != 0 and im[index_i][index_j + 1] != 0):
						im[index_i][index_j] = (im[index_i][index_j - 1] + im[index_i][index_j + 1])/2
					elif(im[index_i][index_j - 1] != 0):
						im[index_i][index_j] = im[index_i][index_j - 1]
					elif(im[index_i][index_j + 1] != 0):
						im[index_i][index_j] = im[index_i][index_j + 1]
	im = gaussian_filter(im,sigma=2)
	return im

left = filterImage(left,width,height)
right = filterImage(right,width,height)

left = downscale_local_mean(left,(1,2))
right = downscale_local_mean(right,(1,2))

#Now that we have the images, we create 2D AWGN
#and embed our right and left plots inside it
#(So that the AWGN cancels out of the SLM)

fig = plt.figure()
#plt.subplot(121)
#plt.imshow(right,cmap='Greys',interpolation='nearest')
#plt.subplot(122)
#plt.imshow(left,cmap='Greys',interpolation='nearest')

out_img = np.random.normal(0,1,(1000,2000))
row_offset = 350
col_offset = 100
out_img[row_offset:(row_offset + right.shape[0]),col_offset:(col_offset + right.shape[1])] = right
out_img[row_offset:(row_offset + left.shape[0]),(out_img.shape[1] - col_offset - left.shape[1]):(out_img.shape[1] - col_offset)] = left
plt.axis('off')
plt.imshow(out_img,cmap='Greys',interpolation='nearest')
fig.savefig('plot.png',transparent=True)
