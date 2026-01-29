# main.py
import time
from core.fan_controller import FanController
from models.bt_receiver import BluetoothReceiver
from views.servo_view import ServoView

def main():
    print("--- 시스템 초기화 중 ---")
    bt = BluetoothReceiver() # 블루투스 서버 시작
    view = ServoView()       # 모터 초기화
    controller = FanController()
    
    print("--- 준비 완료! 스마트폰에서 연결하세요 ---")
    
    # main.py 루프 부분 수정 제안
    try:
        
        while True:
            xr_norm, v_norm, last_rx_time = bt.get_latest()
            controller.tick(xr_norm, v_norm, last_rx_time, view.set_pan_angle)

            time.sleep(controller.config.control_dt)
            
    except KeyboardInterrupt:
        print("종료합니다.")
        view.cleanup()

if __name__ == "__main__":
    main()
