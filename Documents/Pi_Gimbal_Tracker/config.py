# config.py
I2C_ADDRESS = 0x60
SERVO_FREQ = 50

# 핀 번호 (PCA9685의 0번, 1번 포트)
PIN_PAN = 15
PIN_TILT = 1

# 트래킹 감도 (값이 클수록 반응이 빠르지만 떨릴 수 있음)
FOV_GAIN = 15 

# 안드로이드와 약속된 UUID (앱에서도 이 값을 써야 함!)
BT_UUID = "94f39d29-7d6d-437d-973b-fba39e49d4ee"