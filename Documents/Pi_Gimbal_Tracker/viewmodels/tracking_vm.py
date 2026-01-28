from core.observable import Observable
import config

class TrackingViewModel:
    def __init__(self):
        self.pan_angle = Observable(90)
        self.tilt_angle = Observable(90)
    
    def update(self, x, y):
        if x is None or y is None: return
        
        # P 제어 로직 (config.FOV_GAIN 활용)
        # ... (이전 답변의 로직이 들어감)
        
        # 계산된 값을 Observable에 업데이트 -> View가 자동으로 반응
        self.pan_angle.value = new_pan
        self.tilt_angle.value = new_tilt