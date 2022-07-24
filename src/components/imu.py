import board
import time
import math
import digitalio
import busio
from adafruit_lsm6ds.lsm6ds3 import LSM6DS3


class IMU(LSM6DS3):
    def __init__(self, accel_sensitivity=0.2, gyro_sensitivity=0.2):
        dpwr = digitalio.DigitalInOut(board.IMU_PWR)
        dpwr.direction = digitalio.Direction.OUTPUT
        dpwr.value = 1
        time.sleep(1)
        i2c = busio.I2C(board.IMU_SCL, board.IMU_SDA)
        super().__init__(i2c)
        self.accel_sensitivity = accel_sensitivity
        self.last_accel = (0, 0, -9.82)
        self.on_accel_update = None
        self.gyro_sensitivity = gyro_sensitivity
        self.last_gyro = (0, 0, 0)
        self.on_gyro_update = None

    def check(self):
        if self.on_accel_update:
            x, y, z = self.acceleration
            _x, _y, _z = self.last_accel
            s = self.accel_sensitivity
            if abs(x-_x)>s or abs(y-_y)>s or abs(z-_z)>s:
                try:
                    self.on_accel_update((x,y,z))
                finally:
                    self.last_accel = x, y, z
        if self.on_gyro_update:
            x, y, z = self.gyro
            _x, _y, _z = self.last_gyro
            s = self.gyro_sensitivity
            if abs(x - _x) > s or abs(y - _y) > s or abs(z - _z) > s:
                try:
                    self.on_gyro_update((x, y, z))
                finally:
                    self.last_gyro = x, y, z



def print_imu():
    imu = IMU()
    while True:
        print("Acceleration: X:%.2f, Y: %.2f, Z: %.2f m/s^2" % (imu.acceleration))
        print("Gyro X:%.2f, Y: %.2f, Z: %.2f radians/s" % (imu.gyro))
        print("")
        time.sleep(0.5)


def test_imu():
    from components import Display
    display = Display()

    imu = IMU()
    bitmap, tile_grid = display.bitmap(palette=['black','white'])
    x = 120
    y = 120
    c = display.circle(x, y, 5, fill='blue')
    tail = [None]*1000
    tail_ind = 0

    while True:
        for _ in range(10000):
            ax, ay, az = imu.acceleration
            dx = -1 * max([-2, min([ax/5, 2])])
            dy = max([-2, min([ay/5, 2])])
            x = max([20, min([x +dx, 220])])
            y = max([20, min([y + dy, 220])])
            c.x = int(x)
            c.y = int(y)
            t = tail[tail_ind]
            if t is not None:
                bitmap[t[0], t[1]] = 0
            tail[tail_ind] = [c.x + 2, c.y + 2]
            tail_ind = (tail_ind + 1) % len(tail)
            bitmap[c.x + 2, c.y + 2] = 1


if __name__ == "__main__":
    test_imu()