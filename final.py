#
# import cv2
# import imutils
# import time
# from threading import *
#
# camlink1 = "rtsp://admin1:admin@123@10.1.89.121:554/axis-media/media.amp"
#
#
# class video_stream(Thread):
#     def show_frame(self):
#         capture = cv2.VideoCapture(camlink1)
#         while True:
#             if capture.isOpened():
#                 (status, frame) = capture.read()
#                 cv2.imshow('Frame ',frame)
#             time.sleep(.01)
#
#         # Display frames in main program
#         # frame = imutils.resize(self.frame, width=400)
#         # cv2.imshow('Frame ' + self.camname, frame)
#         # key = cv2.waitKey(1)
#         # if key == ord('q'):
#         #     self.capture.release()
#         #     cv2.destroyAllWindows()
#         #     exit(1)
#
#
# class reference(Thread):
#     def ref(self):
#         print("camID:", camlink1)
#         cap = cv2.VideoCapture(camlink1)
#         ret, ref_frame = cap.read()
#         print("campreview function: taking reference frame")
#         cv2.imshow("reference frame", ref_frame)
#
#
# t1 = video_stream()
# # t2 = reference()
#
# t1.start()
# # time.sleep(0.2)
# # t2.start()
#
# t1.join()
# # t2.join()
#
# # print("hello")

import threading
import time
import cv2
import imutils

camlink1 = "rtsp://admin1:admin@123@10.1.89.121:554/axis-media/media.amp"
camlink2 = "rtsp://admin1:admin@123@10.1.89.121:554/axis-media/media.amp"
camname1 = 'cam1'
camname2 = 'cam2'


def ORB_detector(running_frame, reference_image):
    image1 = cv2.cvtColor(running_frame, cv2.COLOR_BGR2GRAY)
    orb = cv2.ORB_create(1000, 1.2)
    (kp1, des1) = orb.detectAndCompute(image1, None)
    (kp2, des2) = orb.detectAndCompute(reference_image, None)
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(des1, des2)
    matches = sorted(matches, key=lambda val: val.distance)
    return len(matches)


def video_stream(link, camname):
    global frame
    capture = cv2.VideoCapture(link)
    while True:
        if capture.isOpened():
            (status, frame) = capture.read()
        time.sleep(.01)
        # frame = imutils.resize(frame, width=400)
        cv2.imshow('Frame ' + camname, frame)
        key = cv2.waitKey(1)
        if key == ord('q'):
            capture.release()
            cv2.destroyAllWindows()
            exit(1)


# def reference(link, camname):
#     global ref_frame
#     print("camID:", camlink2)
#     cap = cv2.VideoCapture(link)
#     while True:
#         if cap.isOpened():
#             ret, ref_frame = cap.read()
#         time.sleep(.01)
#         # ref_frame = imutils.resize(ref_frame, width=400)
#         cv2.imshow('Ref_frame ' + camname, ref_frame)
#         key = cv2.waitKey(1)

        # print("campreview function: taking reference frame")
        # cv2.imshow("reference frame" + camname, ref_frame)
        # cv2.waitKey(1000)
        # cv2.destroyAllWindows()


def camPreview(link,name):
    print("camID:", camlink1)
    cap = cv2.VideoCapture(link)
    ret, ref_frame = cap.read()
    print("campreview function: taking reference frame")
    cv2.imshow("reference frame"+name, ref_frame)

    while True:
        ret, r_frame = cap.read()
        while not ret:
            print("Taking frames")
            cap.release()
            cap = cv2.VideoCapture(link)
            ret, r_frame = cap.read()
        matches = ORB_detector(r_frame, ref_frame)
        output_string = "Matches = " + str(matches)
        cv2.putText(r_frame, output_string, (50, 450), cv2.FONT_HERSHEY_COMPLEX, 2, (250, 0, 250), 2)



        if matches < 800:
            # cv2.rectangle(frame, (top_left_x,top_left_y), (bottom_right_x,bottom_right_y), (0,255,0), 3)
            cv2.putText(r_frame, 'Motion Detected', (50, 50), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 250, 0), 2)

        cv2.imshow('Object Detector using ORB'+name, r_frame)
        if cv2.waitKey(1) == 13:
            break

    cap.release()
    cv2.destroyAllWindows()

st = time.time()
print("st:",st)
x = threading.Thread(target=video_stream, args=(camlink1, camname1))
x.start()

# print("x thread invoked")
y = threading.Thread(target=camPreview, args=(camlink1,camname1))
y.start()
print("y thread invoked")
x1=threading.Thread(target=video_stream,args=(camlink2,camname2))
x1.start()
#
y1 = threading.Thread(target=camPreview, args=(camlink2,camname2))
y1.start()

x.join()
y.join()
x1.join()
y1.join()

et = time.time()
print("et:", et)
diff = st - et
print("diff:", diff)


print(threading.active_count())
print(threading.enumerate())
print(time.perf_counter())
