print("Heya there worlderoni! Howya doin?")

import matplotlib.pyplot as plt
import matplotlib.image as mpimg

img = mpimg.imread('nachogirlwithback.png')
#img = img[:,:,0]; #Allows only RGB values by replacing the 0
plt.imshow(img)
plt.show()
