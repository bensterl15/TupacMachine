import slmpy
import time

slm = slmpy.SLMdisplay(isImageLock = False)
resX, resY = slm.getSize()
X,Y = np.meshgrid(np.linspace(0,resX,resX),np.linspace(0,resY,resY))
# The image we want on the green layer
greenIMG = np.round((2**8-1)*(0.5+0.5*np.sin(2*np.pi*X/50)))
# We need a third dimension corresponding to the color layer
greenIMG.shape = greenIMG.shape[0], greenIMG.shape[1], 1
# The two other layers are blank arrays
blankImage = np.zeros([greenIMG.shape[0], greenIMG.shape[1], 1])
# We merge the three layers in a (resY,resX,3) color array
color_array = np.concatenate((blankImage,greenIMG,blankImage), axis=2).astype('uint8')
# The image is sent to the slm
slm.updateArray(color_array)
# Wait 10 seconds
time.sleep(10)
# Close the window
slm.close