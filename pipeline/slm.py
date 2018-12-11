import slmpy
import numpy as np
import time
from PIL import Image

def image2pixelarray(filepath):
    """
    Parameters
    ----------
    filepath : str
    Path to an image file

    Returns
    -------
    list
        A list of lists which make it simple to access the greyscale value by
        im[y][x]
    """
    im = Image.open(filepath).convert('L')
    (width, height) = im.size
    greyscale_map = list(im.getdata())
    greyscale_map = np.array(greyscale_map)
    greyscale_map = greyscale_map.reshape((height, width))
    return greyscale_map
  
