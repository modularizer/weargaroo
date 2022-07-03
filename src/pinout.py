import board

TOP_BUTTON = board.A2
MIDDLE_BUTTON = board.A1
BOTTOM_BUTTON = board.A0
VIBMO = board.A0
PULSE = board.A3
TFT_RST = board.D4
TFT_DC = board.D5
TFT_CS = board.NFC2 # unused

if __name__ == "__main__":
    print([v for v in dir(board) if not v.startswith('_')])