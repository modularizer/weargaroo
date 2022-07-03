from test_gps import test_gps
from pulse import test_pulse
from watch import Watch

def test_watch():
    w = Watch()
    w.top_button.push_callback

if __name__ == "__main__":
    #test()
    test_pulse()
    # test_gps()

