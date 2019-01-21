import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread('nachogirlwithback.png',cv2.IMREAD_UNCHANGED)

"""
cv2.imshow('image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
"""

plt.imshow(img);
plt.plot([50,100],[80,100],"c", linewidth = 5);
plt.show();
