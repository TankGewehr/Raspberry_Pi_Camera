import numpy as np
import cv2

img_path=".\icons\example.png"
img=cv2.imread(img_path)



while (True):
    cv2.imshow('Picture',img)

    if cv2.waitKey(1)==27:
        break
cv2.destroyAllWindows()