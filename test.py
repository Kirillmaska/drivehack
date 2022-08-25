import cv2

img = cv2.imread('images/inv-0003.jpg')
img = cv2.resize(img, (img.shape[1] *2, img.shape[0] * 2))
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
print(img.shape)
cv2.imshow('Result', img)
cv2.waitKey(0)
cv2.imwrite('kek.jpg', img)