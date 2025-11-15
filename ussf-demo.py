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


def run_qr_command(qr):
    qr_id = qr[0][0]
    qr_dz = qr[0][1]
    qr_rotation = qr[0][2]

    if int(qr_id) == 1:
        tello.rotate_counter_clockwise(int(qr_rotation))
        tello.move_forward(int(qr_dz) * 100)
    elif int(qr_id) > 1:
        tello.land()


def process_tello_video(drone):
    while True:
        frame = cv2.cvtColor(frame_read.frame, cv2.COLOR_BGR2RGB)

        start = time.perf_counter()

        value, points, qrcode = detector.detectAndDecode(frame)

        frame_center_y = frame.shape[0] // 2
        frame_center_x = frame.shape[1] // 2

        if value != "":
            information = ([list(value.split(","))])

            x1 = points[0][0][0]
            y1 = points[0][0][1]
            x2 = points[0][2][0]
            y2 = points[0][2][1]

            x_center = (x2 - x1) / 2 + x1
            y_center = (y2 - y1) / 2 + y1

            diagonal_length = np.sqrt(((int(x2) - int(x1)) ^ 2) + ((int(y2) - int(y1)) ^ 2))

            # max_distance = 8.00

            calculated_distance = round(-np.log(diagonal_length / 31.568) / 0.126, 3)

            if calculated_distance < 3:
                run_qr_command(information)
                time.sleep(2)
            elif calculated_distance > 3:
                drone.move_forward(20)
                time.sleep(1)

            cv2.putText(frame, str(calculated_distance) + " Ft.", (30, 120), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0))

            cv2.putText(frame, str(value), (30, 170), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0))

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


tello.takeoff()
process_tello_video(tello)
