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
        
        self.current_pan = 90.0
        self.current_tilt = 90.0
        self.update_servos()

    def update_position(self, target_x, target_y):
        # 1. 목표 각도 변환 (0.0~1.0 -> 0~180)
        raw_pan = (1.0 - target_x) * 180
        
        # ★ [핵심 수정] 물리적 한계 보호 (Safety Margin)
        # 0도와 180도 끝까지 가지 말고, 10도~170도 사이에서만 놀아라!
        # 이렇게 하면 "득득득" 소리가 사라집니다.
        safe_pan = max(10, min(170, raw_pan))
        
        # 2. 미세 떨림 방지 (아까 말한 Deadband)
        if abs(safe_pan - self.current_pan) < 1.0:
            return 

        self.current_pan = safe_pan
        self.update_servos()

    def set_pan_angle(self, angle):
        self.current_pan = angle
        self.update_servos()
            
    def update_servos(self):
        self.pan.angle = self.current_pan
        self.tilt.angle = self.current_tilt

    def cleanup(self):
        self.pca.deinit()
