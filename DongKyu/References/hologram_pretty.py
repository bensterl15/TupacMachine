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
	#Gerchberg–Saxton algorithm Loop
	while (err > args.threshold or k < args.iter):
		k += 1
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
		if k > 150:
			break
	g = g/np.max(np.abs(g))
	h = np.floor(255*angIF) # SLM is 8 bit.

