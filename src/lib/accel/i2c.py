import board
import digitalio
import busio

from .const import *
from .settings import Settings
settings = Settings()


class IMU_I2C(object):
    addr = 0x6A

    MILLI_G_TO_ACCEL = 0.00980665
    TEMPERATURE_SENSITIVITY = 256
    TEMPERATURE_OFFSET = 25.0

    def __init__(self):
        self.pwr = board.IMU_PWR
        self.scl = board.IMU_SCL
        self.sda = board.IMU_SDA
        self.int1 = board.IMU_INT1

        self.dpwr = digitalio.DigitalInOut(self.pwr)
        self.dpwr.direction = digitalio.Direction.OUTPUT
        self.power = True

        self.i2c = busio.I2C(self.scl, self.sda)
        self.i2c.try_lock()

    @property
    def power(self):
        return self.dpwr.value

    @power.setter
    def power(self, power):
        self.dpwr.value = int(bool(power))

    def begin(self):
        # Setup the accelerometer
        data_to_write = 0
        if settings.accelEnabled == 1:
            # Build config reg
            # First patch in filter bandwidth
            data_to_write |= {
                50: LSM6DS3_ACC_GYRO_BW_XL_50Hz,
                100: LSM6DS3_ACC_GYRO_BW_XL_100Hz,
                400: LSM6DS3_ACC_GYRO_BW_XL_400Hz,
            }[settings.accelBandWidth]


            # Next, patch in full scale
            data_to_write |= {
                2: LSM6DS3_ACC_GYRO_FS_XL_2g,
                4: LSM6DS3_ACC_GYRO_FS_XL_4g,
                8: LSM6DS3_ACC_GYRO_FS_XL_8g,
                16: LSM6DS3_ACC_GYRO_FS_XL_16g
            }[settings.accelRange]

            # Lastly, patch in accelerometer ODR
            data_to_write |= {
                13: LSM6DS3_ACC_GYRO_ODR_XL_13Hz,
                26: LSM6DS3_ACC_GYRO_ODR_XL_26Hz,
                52: LSM6DS3_ACC_GYRO_ODR_XL_52Hz,
                104: LSM6DS3_ACC_GYRO_ODR_XL_104Hz,
                208: LSM6DS3_ACC_GYRO_ODR_XL_208Hz,
                416: LSM6DS3_ACC_GYRO_ODR_XL_416Hz,
                833: LSM6DS3_ACC_GYRO_ODR_XL_833Hz,
                1660: LSM6DS3_ACC_GYRO_ODR_XL_1660Hz,
                3330: LSM6DS3_ACC_GYRO_ODR_XL_3330Hz,
                6660: LSM6DS3_ACC_GYRO_ODR_XL_6660Hz,
                13330: LSM6DS3_ACC_GYRO_ODR_XL_13330Hz
            }[settings.accelSampleRate]

        # Now, write the patched together data
        self.write_register(LSM6DS3_ACC_GYRO_CTRL1_XL, data_to_write)

        # Set the ODR bit
        data_to_write = self.read(LSM6DS3_ACC_GYRO_CTRL4_C)
        data_to_write &= ~LSM6DS3_ACC_GYRO_BW_SCAL_ODR_ENABLED
        if settings.accelODROff == 1:
            data_to_write |= LSM6DS3_ACC_GYRO_BW_SCAL_ODR_ENABLE
        self.write_register(LSM6DS3_ACC_GYRO_CTRL4_C, dataToWrite);

// Setup
the
gyroscope ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** **
dataToWrite = 0; // Start
Fresh!
if (settings.gyroEnabled == 1) {
// Build config reg
// First, patch in full scale
switch (settings.gyroRange) {
case
125:
dataToWrite |= LSM6DS3_ACC_GYRO_FS_125_ENABLED;
break;
case
245:
dataToWrite |= LSM6DS3_ACC_GYRO_FS_G_245dps;
break;
case
500:
dataToWrite |= LSM6DS3_ACC_GYRO_FS_G_500dps;
break;
case
1000:
dataToWrite |= LSM6DS3_ACC_GYRO_FS_G_1000dps;
break;
default: // Default
to
full
2000
DPS
range
case
2000:
dataToWrite |= LSM6DS3_ACC_GYRO_FS_G_2000dps;
break;
}
// Lastly, patch in gyro
ODR
switch(settings.gyroSampleRate)
{
case
13:
dataToWrite |= LSM6DS3_ACC_GYRO_ODR_G_13Hz;
break;
case
26:
dataToWrite |= LSM6DS3_ACC_GYRO_ODR_G_26Hz;
break;
case
52:
dataToWrite |= LSM6DS3_ACC_GYRO_ODR_G_52Hz;
break;
default: // Set
default
to
104
case
104:
dataToWrite |= LSM6DS3_ACC_GYRO_ODR_G_104Hz;
break;
case
208:
dataToWrite |= LSM6DS3_ACC_GYRO_ODR_G_208Hz;
break;
case
416:
dataToWrite |= LSM6DS3_ACC_GYRO_ODR_G_416Hz;
break;
case
833:
dataToWrite |= LSM6DS3_ACC_GYRO_ODR_G_833Hz;
break;
case
1660:
dataToWrite |= LSM6DS3_ACC_GYRO_ODR_G_1660Hz;
break;
}
} else {
       // dataToWrite
already = 0(powerdown);
}
// Write
the
byte
writeRegister(LSM6DS3_ACC_GYRO_CTRL2_G, dataToWrite);

// Return
WHO
AM
I
reg // Not
no
mo!
uint8_t
result;
readRegister( & result, LSM6DS3_ACC_GYRO_WHO_AM_I_REG);

// Setup
the
internal
temperature
sensor
if (settings.tempEnabled == 1)
{
if (result == LSM6DS3_ACC_GYRO_WHO_AM_I)
{ // 0x69
LSM6DS3
settings.tempSensitivity = 16; // Sensitivity
to
scale
16
} else if (result == LSM6DS3_C_ACC_GYRO_WHO_AM_I) {// 0x6A LSM6dS3-C
settings.tempSensitivity = 256; // Sensitivity
to
scale
256
}
}

    def read(self, cmd, n=10):
        self.write(cmd)
        print("reading")
        result = bytearray(n)
        self.i2c.readfrom_into(self.addr, result)
        print(result)
        return result

    def write(self, cmd):
        print("writing", cmd)
        self.i2c.writeto(self.addr, bytes([cmd]))

    def write_register(self, offset, cmd):
        self.write(offset)
        self.write(cmd)

    def write_settings(self, offset, settings):
        cmd = 0
        for setting in settings:
            cmd |= cmd
        self.write_settings(offset, cmd)

    def begin(self):
        self.write_settings(0x10, LSM6DS3_ACC_GYRO_BW_XL_400Hz

        i2c = IMU_I2C()
        print("i2c", i2c)
        i2c.i2c.writeto(
        for i in range(4):
            print("A", i2c.read(0X4C))
        print("G", i2c.read(0X4B))
        print("T", i2c.read(0X40), i2c.read(0x41))
