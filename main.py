import cv2
import numpy as np
import util_func as func

img = cv2.imread('image/original.jpg', 0)
cimg = cv2.imread('image/original.jpg', 1)
img = cv2.medianBlur(img, 5)
# cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)

ret, thresh = cv2.threshold(img, 30, 255, cv2.THRESH_BINARY_INV)
kernel = np.ones((3, 3), np.uint8)

closing = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=10)
opening = cv2.morphologyEx(closing, cv2.MORPH_OPEN, kernel, iterations=1)

cv2.imwrite("image/opening.png", opening)
masked = cv2.bitwise_and(cimg, cimg, mask=~opening)
cv2.imwrite("image/masked.png", masked)

im2, contours, hierarchy = cv2.findContours(opening, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
# cv2.drawContours(masked, contours, -1, (0,255,255), 5)
array_count = 0

for cnt in contours:
    epsilon = 0.1 * cv2.arcLength(cnt, True)
    approx = cv2.approxPolyDP(cnt, epsilon, True)
    blank_image = np.zeros((120, 120, 3), np.uint8)

    if np.shape(approx)[0] == 4:
        print approx

        if func.is_big_or_small(approx):  # big or small
            continue
        pixels = func.extract_twenty_five_colors(cimg, approx)

        start, end = func.points_in_approx(approx)

        cv2.putText(masked, str(start[0]) + "," + str(start[1]),start,fontFace=cv2.FONT_HERSHEY_PLAIN,fontScale=1,color=(0,255,0))
        cv2.rectangle(masked, start, end, (0, 255, 0), 1)
        cv2.putText(blank_image, str(start[0]) + "," + str(start[1]),(10,10),fontFace=cv2.FONT_HERSHEY_PLAIN,fontScale=1,color=(0,255,0))

        pixel_count = 0
        for width in range(20,101,20):
            for height in range(20,101,20):
                #print width, height
                cv2.circle(blank_image, (width,height), radius=5, color=pixels[pixel_count],thickness=-1,lineType=cv2.LINE_AA)
                pixel_count +=1
        cv2.imwrite("image/processed"+str(array_count)+".png", blank_image)
        array_count += 1

cv2.imwrite("image/rectangled.png", masked)


