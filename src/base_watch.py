import time
import config

from components import Display, GPS, Pulse, VibMoButton, Button, IMU, Mic, Battery, RGB_LED


class BaseWatchState(object):
    def __init__(self, watch):
        pass

    lat = None
    lat_ord = None
    lng = None
    lng_ord = None
    alt = None
    alt_units = None
    last_gps_time = None

    year = None
    day = None
    month = None
    hour = None
    minute = None
    second = None
    weekday = None
    yearday = None
    is_dst = None

    heart_rate = None

    accel = (0, 0, -9.82)
    gyro = (0, 0, 0)

    top_button = 0
    side_button = 0
    bottom_button = 0

    charge = None


class BaseWatch(object):
    WatchState = BaseWatchState

    def __init__(self, state=None, WatchState=None):
        self.display = Display()
        self.gps = GPS()
        self.pulse = Pulse()
        self.imu = IMU()
        self.mic = Mic()
        self.battery = Battery()
        self.rgb_led = RGB_LED()
        self.top_button = Button(config.TOP_BUTTON)
        self.side_button = Button(config.SIDE_BUTTON)
        self.vibmo_button = VibMoButton(config.VIBMO_BUTTON)
        self.rtc = self.gps.position.rtc

        if WatchState is None:
            WatchState = self.WatchState
        if state is None:
            state = WatchState(self)
        self.state = state

        self.mic.on_update = self.on_mic_update
        self.gps.on_update = self.on_gps_update
        self.pulse.on_value = self.on_pulse_reading
        self.imu.on_accel_update = self.on_accel_update
        self.imu.on_gyro_update = self.on_gyro_update
        self.battery.on_update = self.on_charge_update
        self.top_button.push_callback = self.on_top_button_push
        self.top_button.hold_callback = self.on_top_button_hold
        self.top_button.release_callback = self.on_top_button_release
        self.side_button.push_callback = self.on_side_button_push
        self.side_button.hold_callback = self.on_side_button_hold
        self.side_button.release_callback = self.on_side_button_release
        self.bottom_button.push_callback = self.on_bottom_button_push
        self.bottom_button.hold_callback = self.on_bottom_button_hold
        self.bottom_button.release_callback = self.on_bottom_button_release

    @property
    def vibmo(self):
        self.vibmo_button.mode = "vibmo"
        return self.vibmo_button.vibmo

    @property
    def bottom_button(self):
        self.vibmo_button.mode = "button"
        return self.vibmo_button.button

    def on_gps_update(self, **kw):
        for k, v in kw.items():
            if k == "time":
                self.on_gps_time_update(v)
            if k in ["lat", "lng", "alt"]:
                getattr(self, f"on_{k}_update")(*v)

    def on_gps_time_update(self, time_dict):
        self.state.last_gps_time = time.time()

    def on_time_update(self):
        ts = self.rtc.datetime
        keys = ["year", "day", "month", "hour", "minute", "second", "weekday", "yearday", "is_dst"]
        for i, v in enumerate(ts):
            k = keys[i]
            old = getattr(self.state, k)
            if v != old:
                setattr(self.state, k, v)

    def on_lat_update(self, lat, ordinal_str):
        self.state.lat = lat
        self.state.lat_ord = ordinal_str

    def on_lng_update(self, lng, ordinal_str):
        self.state.lng = lng
        self.state.lng_ord = ordinal_str

    def on_alt_update(self, alt, units):
        self.state.alt = alt
        self.state.alt_units = units

    def on_pulse_reading(self, ind, value, dv, phase, new_phase):
        if phase == 1 and new_phase:
            self.on_pulse(self.pulse.rate, value, dv)

    def on_pulse(self, rate, value, dv):
        self.state.heart_rate = rate

    def on_top_button_push(self, config, t, dt):
        self.state.top_button = dt

    def on_top_button_hold(self, config, t, dt):
        self.state.top_button = dt

    def on_top_button_release(self, config, t, dt):
        self.state.top_button = 0

    def on_side_button_push(self, config, t, dt):
        self.state.side_button = dt

    def on_side_button_hold(self, config, t, dt):
        self.state.side_button = dt

    def on_side_button_release(self, config, t, dt):
        self.state.side_button = 0

    def on_bottom_button_push(self, config, t, dt):
        self.state.bottom_button = dt

    def on_bottom_button_hold(self, config, t, dt):
        self.state.bottom_button = dt

    def on_bottom_button_release(self, config, t, dt):
        self.state.bottom_button = 0

    def on_gyro_update(self, gx, gy, gz):
        self.state.gyro = (gx, gy, gz)

    def on_accel_update(self, ax, ay, az):
        self.state.accel = (ax, ay, az)

    def on_charge_update(self, charge):
        self.state.charge = charge

    def on_mic_update(self, samples):
        pass


if __name__ == "__main__":
    bw = BaseWatch()

