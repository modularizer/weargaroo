import board
import time
import math
import digitalio
import busio
from adafruit_lsm6ds.lsm6ds3 import LSM6DS3


class IMU(LSM6DS3):
    def __init__(self):
        dpwr = digitalio.DigitalInOut(board.IMU_PWR)
        dpwr.direction = digitalio.Direction.OUTPUT
        dpwr.value = 1
        time.sleep(1)
        i2c = busio.I2C(board.IMU_SCL, board.IMU_SDA)
        super().__init__(i2c)


def print_imu():
    imu = IMU()
    while True:
        print("Acceleration: X:%.2f, Y: %.2f, Z: %.2f m/s^2" % (imu.acceleration))
        print("Gyro X:%.2f, Y: %.2f, Z: %.2f radians/s" % (imu.gyro))
        print("")
        time.sleep(0.5)


def test_imu():
    from components.display import Display
    display = Display(native_frames_per_second=60)
    display.clear()

    imu = IMU()
    palette_colors = [0, 0xFFFFFF]

    while True:
        display.clear()
        bitmap = display.init_bitmap(palette_colors)
        x = 120
        y = 120
        for _ in range(10000):
            ax, ay, az = imu.acceleration
            x -= max([-2, min([ax/5, 2])])
            y += max([-2, min([ay/5, 2])])
            x = max([20, min([x, 220])])
            y = max([20, min([y, 220])])
            bitmap[int(x), int(y)] = 1


if __name__ == "__main__":
    test_imu()
