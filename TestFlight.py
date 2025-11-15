from djitellopy import tello
from time import sleep
import cv2
import math

a10 = tello.Tello()

a10.connect()
print("Battery:", a10.get_battery())
# a10.takeoff()
# sleep(2)

# Flip Maneuver


# Square Maneuver
# a10.send_rc_control(0, 20, 0, 0)
# sleep(5)
# a10.send_rc_control(20, 0, 0, 0)
# sleep(5)
# a10.send_rc_control(0, -20, 0, 0)
# sleep(5)
# a10.send_rc_control(-20, 0, 0, 0)
# sleep(5)
# a10.send_rc_control(0, 0, 0, 0)

# Circle Maneuver
# a10.send_rc_control(0, 0, 20, 0)
# sleep(2)
# a10.send_rc_control(0, 0, 0, 0)
# multiplier = 10
# for i in range(157):
#     a10.send_rc_control((math.floor(math.cos(i * 4) - multiplier) * multiplier), math.floor((math.sin(i * 4) - multiplier) * multiplier), 0, 0)
#     sleep(2)
# a10.send_rc_control(0, 0, 0, 0)

# Take a video
# a10.streamon()
# frame = a10.get_frame_read()

# sleep(10)
# a10.streamoff()
#
# a10.land()
