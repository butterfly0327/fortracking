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

# 라즈베리파이 팬(회전) 제어 상수
SERVO_MIN_DEG = 10
SERVO_MAX_DEG = 170
SERVO_INIT_DEG = 90

CONTROL_HZ = 50
CONTROL_DT = 1.0 / CONTROL_HZ

RX_TIMEOUT = 0.30

DEAD_BAND_X = 0.02

# 3단 목표 속도(deg/tick)
STEP_TARGET_LOW = 0.16
STEP_TARGET_MID = 0.28
STEP_TARGET_HIGH = 0.44

# 속도 변화 제한(램프)
STEP_RAMP_UP = 0.02
STEP_RAMP_DOWN = 0.03

# 좌표 EMA(저역통과)
XR_EMA_ALPHA = 0.25

# 속도 EMA(저역통과)
V_EMA_ALPHA = 0.30

# 기어 경계(정규화 속도 기준)
V_LOW_MAX = 0.35
V_MID_MAX = 0.75

# 기어 변경 안정화 tick 수
GEAR_STABLE_TICKS = 3

# 방향 반전 게이트
DIR_FLIP_ERR = 0.04

# 방향 반전 시 브레이크 완료 판정
REV_EPS = 0.05
