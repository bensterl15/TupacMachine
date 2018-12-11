import numpy as np
import skimage
import argparse
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument('--display',action = 'store_true',help='')
parser.add_argument('--h',default = 512,type=int,help='')
parser.add_argument('--w',default = 1024,type=int,help='')
parser.add_argument('--imagedir',default='peppers.png',help='')
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
	#GS algorithm Loop
	while (err > 0.087):
		k = k+1
		IF = np.fft.fftshift(np.fft.fft2(I))
		angIF = np.angle(IF)
		IF2 = np.exp(1j*angIF)
		g = np.fft.ifft2(np.fft.fftshift(IF2))
		avg = np.mean(np.abs(g))
		g = g*avI0/avg
		ampg = np.abs(g)
		angg = np.angle(g)
		dif2 = (ampg-ampI0)**2
		err = np.sqrt(np.sum(dif2)/(N**2))
		I = ampI0*np.exp(1j*angg)
		if k > 150:
			break
	g = g/np.max(np.abs(g))
	# Binary CG hologram
	h = np.zeros((N,N))
	for n in range(0,N):
		for m in range(0,N):
			h[n,m] = np.sin(angIF[m,n])
			if h[n,m] > 0:
				h[n,m] = 1
			else:
				h[n,m] = 0
	h = skimage.transform.resize(h,M)
	if display:
		plot = plt.subplot()
		plot.imshow(h, cmap ="gray")
		plt.show()

	return h

if __name__ == '__main__':
	transform(args.display,[args.h,args.w],args.imagedir)
