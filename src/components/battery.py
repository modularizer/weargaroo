import board
import analogio
import digitalio

# TODO find out how exactly to use these
vbatt = analogio.AnalogIn(board.VBATT)
vbatt_en = digitalio.DigitalInOut(board.READ_BATT_ENABLE)
vbatt_en.direction = digitalio.Direction.INPUT
charge_status = digitalio.DigitalInOut(board.CHARGE_STATUS)
charge_status.direction = digitalio.Direction.INPUT

if __name__ == "__main__":
    import time
    while True:
        print(vbatt.value)
        time.sleep(0.5)