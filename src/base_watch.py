import rtc
import time
import config


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

    pulse_reading = None
    heart_rate = None

    noise_samples = None

    accel = (0, 0, -9.82)
    gyro = (0, 0, 0)

    top_button = 0
    side_button = 0
    bottom_button = 0

    charge = None


class BaseWatch(object):
    WatchState = BaseWatchState

    def __init__(self, state=None, WatchState=None):
        self._display = None
        self._gps = None
        self._pulse = None
        self._imu = None
        self._mic = None
        self._battery = None
        self._rgb_led = None
        self._top_button = None
        self._side_button = None
        self._vibmo_button = None
        self._rtc = None

        if WatchState is None:
            WatchState = self.WatchState
        if state is None:
            state = WatchState(self)
        self.state = state
        self.run()

    @property
    def display(self):
        if self._display is None:
            from components.display import Display
            self._display = Display()
        return self._display

    @property
    def gps(self):
        if self._gps is None:
            from components.gps import GPS
            self._gps = GPS()
            self._gps.on_lat_update = self.on_lat_update
            self._gps.on_lng_update = self.on_lng_update
            self._gps.on_alt_update = self.on_alt_update
            self._gps.on_time_calibration = self.on_time_calibration
            self._gps.on_time_update = self.on_gps_time_update
        return self._gps

    @property
    def rtc(self):
        return self.gps.rtc

    @property
    def pulse(self):
        if self._pulse is None:
            from components.pulse import Pulse
            self._pulse = Pulse()
            self._pulse.on_value = self.on_pulse_reading
        return self._pulse

    @property
    def imu(self):
        if self._imu is None:
            from components.imu import IMU
            self._imu = IMU()
            self._imu.on_accel_update = self.on_accel_update
            self._imu.on_gyro_update = self.on_gyro_update
        return self._imu

    @property
    def mic(self):
        if self._mic is None:
            from components.mic import Mic
            self._mic = Mic()
            self._mic.on_update = self.on_mic_update
        return self._mic

    @property
    def battery(self):
        if self._battery is None:
            from components.battery import Battery
            self._battery = Battery()
            self._battery.on_update = self.on_charge_update
        return self._battery

    @property
    def rgb_led(self):
        if self._rgb_led is None:
            from components.rgb_led import RGB_LED
            self._rgb_led = RGB_LED()
        return self._rgb_led

    @property
    def top_button(self):
        if self._top_button is None:
            from components.button import Button
            self._top_button = Button(config.TOP_BUTTON)
            self._top_button.push_callback = self.on_top_button_push
            self._top_button.hold_callback = self.on_top_button_hold
            self._top_button.release_callback = self.on_top_button_release
        return self._top_button

    @property
    def side_button(self):
        if self._side_button is None:
            from components.button import Button
            self._side_button = Button(config.SIDE_BUTTON)
            self._side_button.push_callback = self.on_side_button_push
            self._side_button.hold_callback = self.on_side_button_hold
            self._side_button.release_callback = self.on_side_button_release
        return self._side_button

    @property
    def vibmo_button(self):
        if self._vibmo_button is None:
            from components.vibmo_button import VibMoButton
            self._vibmo_button = VibMoButton(config.VIBMO_BUTTON)
            self.bottom_button.push_callback = self.on_bottom_button_push
            self.bottom_button.hold_callback = self.on_bottom_button_hold
            self.bottom_button.release_callback = self.on_bottom_button_release
        return self._vibmo_button


    @property
    def vibmo(self):
        self.vibmo_button.mode = "vibmo"
        return self.vibmo_button.vibmo

    @property
    def bottom_button(self):
        self.vibmo_button.mode = "button"
        return self.vibmo_button.button

    def on_time_calibration(self, ts):
        self.state.last_gps_time = time.mktime(ts)

    def on_gps_time_update(self, ts):
        self.on_time_update()

    def on_time_update(self):
        ts = self.rtc.datetime
        keys = ["year", "month", "day", "hour", "minute", "second", "weekday", "yearday", "is_dst"]
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
        self.state.pulse_reading = value
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

    def on_gyro_update(self, g):
        self.state.gyro = g

    def on_accel_update(self, a):
        self.state.accel = a

    def on_charge_update(self, charge):
        self.state.charge = charge

    def on_mic_update(self, samples):
        pass

    def run(self):
        pass


if __name__ == "__main__":
    bw = BaseWatch()

