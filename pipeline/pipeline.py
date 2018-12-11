from slm import *
from hologram import *

def scale(image):
    return image*(255/image.max()).astype('uint8')
    
if __name__ == '__main__':
    slm = slmpy.SLMdisplay(isImageLock = False)
    resX, resY = slm.getSize()
    #testIMG = np.round(image2pixelarray(file)).astype('uint8')
    #file = input('Type file name: ')
    #file = file+'.jpg'
    file = 'peppers.png'
    print(file)
    testIMG = transform(False,[resX,resY],file,256)
    im = scale(testIMG)
    slm.updateArray(im)
    time.sleep(10)
    slm.close()
