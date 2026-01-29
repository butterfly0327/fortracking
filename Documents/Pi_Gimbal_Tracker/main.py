# main.py
import time
import config
from models.bt_receiver import BluetoothReceiver
from views.servo_view import ServoView

def main():
    print("--- 시스템 초기화 중 ---")
    bt = BluetoothReceiver() # 블루투스 서버 시작
    view = ServoView()       # 모터 초기화
    
    print("--- 준비 완료! 스마트폰에서 연결하세요 ---")
    
    # main.py 루프 부분 수정 제안
    try:
        while True:
            now = time.monotonic()
            xr_norm, v_norm, last_rx_time = bt.get_latest_values()
            view.control_tick(xr_norm, v_norm, last_rx_time, now)
            time.sleep(config.CONTROL_DT)
            
    except KeyboardInterrupt:
        print("종료합니다.")
        view.cleanup()

if __name__ == "__main__":
    main()
