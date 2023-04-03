import cv2

cap1 = cv2.VideoCapture(0)
# cap2 = cv2.VideoCapture(1)

while True:
    _, frame1 = cap1.read()
    # _, frame2 = cap2.read()
    cv2.imshow("image1",frame1)
    # cv2.imshow("image2",frame2)
    cv2.waitKey(3)
