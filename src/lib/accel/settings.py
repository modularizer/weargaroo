class Settings(object):
    gyroEnabled = 1  # Can be 0 or 1
    gyroRange = 2000   # Max deg/s.  Can be: 125, 245, 500, 1000, 2000
    gyroSampleRate = 416   # Hz.  Can be: 13, 26, 52, 104, 208, 416, 833, 1666
    gyroBandWidth = 400  # Hz.  Can be: 50, 100, 200, 400;
    gyroFifoEnabled = 1  # Set to include gyro in FIFO
    gyroFifoDecimation = 1  # set 1 for on /1

    accelEnabled = 1
    accelODROff = 1
    accelRange = 16      # Max G force readable.  Can be: 2, 4, 8, 16
    accelSampleRate = 416  # Hz.  Can be: 13, 26, 52, 104, 208, 416, 833, 1666, 3332, 6664, 13330
    accelBandWidth = 100  # Hz.  Can be: 50, 100, 200, 400;
    accelFifoEnabled = 1  # Set to include accelerometer in the FIFO
    accelFifoDecimation = 1  # set 1 for on /1

    tempEnabled = 1

    # Select interface mode
    commMode = 1  # Can be modes 1, 2 or 3

    # FIFO control data
    fifoThreshold = 3000  # Can be 0 to 4096 (16 bit bytes)
    fifoSampleRate = 10  # default 10Hz
    fifoModeWord = 0  # Default off
