# views/servo_view.py
from adafruit_pca9685 import PCA9685
from adafruit_motor import servo
import board
import busio
import config

class ServoView:
    def __init__(self):
        i2c = busio.I2C(board.SCL, board.SDA)
        self.pca = PCA9685(i2c, address=0x60)
        self.pca.frequency = config.SERVO_FREQ
        
        # 펄스 폭 설정 (이것도 모터마다 다를 수 있어 기본값 사용)
        self.pan = servo.Servo(self.pca.channels[config.PIN_PAN], min_pulse=500, max_pulse=2500)
        self.tilt = servo.Servo(self.pca.channels[config.PIN_TILT], min_pulse=500, max_pulse=2500)
        
        self.current_pan = float(config.SERVO_INIT_DEG)
        self.current_tilt = float(config.SERVO_INIT_DEG)

        self.step_actual = 0.0
        self.gear_state = "LOW"
        self.gear_change_count = 0
        self.xr_filt = None
        self.v_filt = None
        self.dir_state = 0
        self.flip_pending = False
        self.flip_target_sign = 0

        self.update_servos()

    def _clamp_angle(self, angle):
        return max(config.SERVO_MIN_DEG, min(config.SERVO_MAX_DEG, angle))

    def _update_gear(self, v_norm):
        if v_norm is not None:
            if self.v_filt is None:
                self.v_filt = v_norm
            else:
                self.v_filt = self.v_filt + config.V_EMA_ALPHA * (v_norm - self.v_filt)

        if self.v_filt is None:
            desired_gear = self.gear_state
        elif self.v_filt <= config.V_LOW_MAX:
            desired_gear = "LOW"
        elif self.v_filt < config.V_MID_MAX:
            desired_gear = "MID"
        else:
            desired_gear = "HIGH"

        if desired_gear != self.gear_state:
            self.gear_change_count += 1
        else:
            self.gear_change_count = 0

        if self.gear_change_count >= config.GEAR_STABLE_TICKS:
            self.gear_state = desired_gear
            self.gear_change_count = 0

        if self.gear_state == "LOW":
            return config.STEP_TARGET_LOW
        if self.gear_state == "MID":
            return config.STEP_TARGET_MID
        return config.STEP_TARGET_HIGH

    def control_tick(self, xr_norm, v_norm, last_rx_time, now):
        if now - last_rx_time > config.RX_TIMEOUT:
            self.step_actual = 0.0
            self.flip_pending = False
            self.update_servos()
            return

        if xr_norm is None:
            self.step_actual = 0.0
            self.flip_pending = False
            self.update_servos()
            return

        if self.xr_filt is None:
            self.xr_filt = xr_norm
        else:
            self.xr_filt = self.xr_filt + config.XR_EMA_ALPHA * (xr_norm - self.xr_filt)

        err = self.xr_filt - 0.5

        if abs(err) < config.DEAD_BAND_X:
            self.step_actual = 0.0
            self.flip_pending = False
            self.update_servos()
            return

        desired_sign = 1 if err > 0 else -1
        if self.dir_state == 0:
            self.dir_state = desired_sign

        if desired_sign != self.dir_state:
            if abs(err) < config.DIR_FLIP_ERR:
                desired_sign = self.dir_state
            else:
                self.flip_pending = True
                self.flip_target_sign = desired_sign

        if self.flip_pending:
            step_target = 0.0
            self.step_actual = max(self.step_actual - config.STEP_RAMP_DOWN, 0.0)
            if self.step_actual <= config.REV_EPS:
                self.dir_state = self.flip_target_sign
                self.flip_pending = False
        else:
            step_target = self._update_gear(v_norm)

        if self.step_actual < step_target:
            self.step_actual = min(self.step_actual + config.STEP_RAMP_UP, step_target)
        elif self.step_actual > step_target:
            self.step_actual = max(self.step_actual - config.STEP_RAMP_DOWN, step_target)

        new_angle = self.current_pan + self.dir_state * self.step_actual
        new_angle = self._clamp_angle(new_angle)

        if new_angle == self.current_pan:
            self.update_servos()
            return

        self.current_pan = new_angle
        self.update_servos()
            
    def update_servos(self):
        self.pan.angle = self.current_pan
        self.tilt.angle = self.current_tilt

    def cleanup(self):
        self.pca.deinit()
