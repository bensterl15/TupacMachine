import numpy as np
import skimage
import argparse
import matplotlib.pyplot as plt
from time import time

parser = argparse.ArgumentParser()
parser.add_argument('--display',action = 'store_true',help='')
parser.add_argument('--sanity_check',action = 'store_true',help='')
parser.add_argument('--progress',action = 'store_true', help='')
parser.add_argument('--h',default = 512,type=int,help='')
parser.add_argument('--w',default = 512,type=int,help='')
parser.add_argument('--imagedir',default='peppers.png',help='')
parser.add_argument('--threshold',default = 0.1,help='')
parser.add_argument('--iter',default=1,type=int,help='')
parser.add_argument('--subroutine',action = 'store_true',help='')
args = parser.parse_args()


def transform(display,M,imagedir):
	N = 512
	I0 = plt.imread(imagedir)
	I0 = skimage.transform.resize(I0,[N,N])
	I0 = skimage.color.rgb2gray(I0)
	ampI0 = np.abs(I0)
	avI0 = np.mean(I0)
	I = I0
	k = 0
	err = 1
	tic_total = time()
	#GS algorithm Loop
	while (err > args.threshold and k < args.iter):
		k += 1
		if args.progress:
			elapsed = time()-tic_total
			print('time elapsed so far: '+str(elapsed))
			print('iteration '+str(k))
			print('error ' + str(err))

		IF = np.fft.fftshift(np.fft.fft2(np.fft.fftshift(I)))
		angIF = np.angle(IF)
		IF2 = np.exp(1j*angIF)
		g = np.fft.fftshift(np.fft.ifft2(np.fft.fftshift(IF2)))
		avg = np.mean(np.abs(g))
		g = g*avI0/avg
		ampg = np.abs(g)
		angg = np.angle(g)
		dif2 = (ampg-ampI0)**2
		err = np.sqrt(np.sum(dif2)/(N**2))
		I = ampI0*np.exp(1j*angg)
		if args.subroutine:
			if k == 2:
				g1 = g/np.max(np.abs(g))

		if k > 150:
			break
	g = g/np.max(np.abs(g))

	h = np.floor(255*angIF) # SLM is 8 bit.




	# Binary CG hologram
#	h = np.zeros((N,N))
#	for n in range(0,N):
#		for m in range(0,N):
#			h[n,m] = np.cos(angIF[m,n])
#			if h[n,m] > 0:
#				h[n,m] = 1
#			else:
#				h[n,m] = 0
	h = skimage.transform.resize(h,M)
	if args.display:
		plot = plt.subplot()
		plot.imshow(h, cmap ="gray")
		plt.show()

	if args.sanity_check:
		plot = plt.subplot()
		plot.imshow(np.abs(g),cmap='gray')
		plt.show()
	
	if args.subroutine:
		# This space is for misc things.
		ax1 = plt.subplot(221)
		ax1.imshow(I0,cmap = "gray")
		ax1.axes.get_xaxis().set_visible(False)
		ax1.axes.get_yaxis().set_visible(False)
		ax1.title.set_text('Original Image')

		ax2 = plt.subplot(222)
		ax2.imshow(h, cmap ="gray")
		ax2.axes.get_xaxis().set_visible(False)
		ax2.axes.get_yaxis().set_visible(False)
		ax2.title.set_text('Phase Mask for SLM')

		ax3 = plt.subplot(223)
		ax3.imshow(np.abs(g1),cmap='gray') 
		ax3.axes.get_xaxis().set_visible(False)
		ax3.axes.get_yaxis().set_visible(False)
		ax3.title.set_text('Reconstruction (2nd iteration)')

		ax4 = plt.subplot(224)
		ax4.imshow(np.abs(g),cmap = 'gray')
		ax4.axes.get_xaxis().set_visible(False)
		ax4.axes.get_yaxis().set_visible(False)
		ax4.title.set_text('Reconstruction (20th iteration)')


		plt.show()





	return h



if __name__ == '__main__':
	transform(args.display,[args.h,args.w],args.imagedir)
