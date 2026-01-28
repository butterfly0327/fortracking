# main.py
import time
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
            # 1. 블루투스 객체에서 최신 좌표를 가져오는지 확인
            target_x, target_y = bt.get_coords() 
            
            # 2. 뷰 객체에 이 좌표를 넣어 업데이트하는지 확인
            view.update_position(target_x, target_y)
            
            time.sleep(0.01)
            
    except KeyboardInterrupt:
        print("종료합니다.")
        view.cleanup()

if __name__ == "__main__":
    main()