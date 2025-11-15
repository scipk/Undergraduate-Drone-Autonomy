import time
import cv2
from threading import Thread
from djitellopy import Tello
import numpy as np

tello = Tello()

tello.connect()

tello.streamon()
frame_read = tello.get_frame_read()

detector = cv2.QRCodeDetector()


def process_tello_video(drone):
    while True:
        frame = cv2.cvtColor(frame_read.frame, cv2.COLOR_BGR2RGB)

        start = time.perf_counter()

        value, points, qrcode = detector.detectAndDecode(frame)

        frame_center_y = frame.shape[0] // 2
        frame_center_x = frame.shape[1] // 2

        if value != "":
            x1 = points[0][0][0]
            y1 = points[0][0][1]
            x2 = points[0][2][0]
            y2 = points[0][2][1]

            x_center = (x2 - x1) / 2 + x1
            y_center = (y2 - y1) / 2 + y1

            diagonal_length = np.sqrt(((int(x2) - int(x1)) ^ 2) + ((int(y2) - int(y1)) ^ 2))

            max_distance = 8.00
            # Use that value to calculate the distance between the drone and the QR Code.

            calculated_distance = round(-np.log(diagonal_length / 31.568) / 0.126, 3)

            cv2.putText(frame, str(calculated_distance) + " Ft.", (30, 120), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0))

            cv2.line(frame, (int(x1), int(y1)), (int(x2), int(y2)), (255, 0, 0), 2)

            if x_center != frame_center_x:
                offset = frame_center_x - x_center

                if offset < 0:
                    cv2.line(frame, (int(x_center), int(y_center)), (int(frame_center_x), int(frame_center_y)), (0, 0, 255),
                             2)
                if offset > 0:
                    cv2.line(frame, (int(x_center), int(y_center)), (int(frame_center_x), int(frame_center_y)), (255, 0, 0),
                             2)

        end = time.perf_counter()
        totalTime = end - start

        fps = 1 / totalTime

        cv2.putText(frame, f'FPS: {int(fps)}', (30, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0))

        cv2.imshow("Tello Camera", frame)
        if cv2.waitKey(1) & 0xFF == 27:   # ESC
            break
    drone.streamoff()
    drone.land()
    cv2.destroyAllWindows()


process_tello_video(tello)
