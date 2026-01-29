import os
import time
import socket
import json
import threading

class BluetoothReceiver:
    def __init__(self):

        os.system("sudo rfcomm release all")

        self.latest_xr_norm = None
        self.latest_v_norm = None
        self.last_rx_time = 0.0
        self.server_sock = None
        self.client_sock = None
        self.running = True
        
        # 스레드 시작
        self.thread = threading.Thread(target=self.run_server, daemon=True)
        self.thread.start()

    def run_server(self):
        # 1. 소켓 생성 및 포트 재사용 옵션 설정
        self.server_sock = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
        # SOL_SOCKET, SO_REUSEADDR을 통해 프로세스 종료 시 즉시 포트 해제
        self.server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            self.server_sock.bind(("2C:CF:67:6A:DD:87", 1))
            self.server_sock.listen(1)
            print("[BT] RFCOMM 채널 1 대기 중... (Ready)")
        except Exception as e:
            print(f"[BT] 바인딩 에러: {e}")
            return

        while self.running:
            try:
                # 2. 클라이언트 연결 수락
                self.client_sock, info = self.server_sock.accept()
                print(f"\n[BT] 연결됨! 주소: {info}")
                
                # 3. 데이터 수신 루프 실행 (예외 발생 시 종료)
                self.receive_loop()
            except Exception as e:
                print(f"[BT] 연결 유지 오류: {e}")
            finally:
                # 4. 연결이 끊기면 즉시 자원 해제하여 포트 비우기
                if self.client_sock:
                    self.client_sock.close()
                    self.client_sock = None
                print("[BT] 소켓 자원 해제 완료. 다시 연결 대기 중...")

    def receive_loop(self):
        buffer = ""
        # 타임아웃을 설정하여 폰이 꺼지거나 멀어지면 감지하도록 함
        self.client_sock.settimeout(5.0) 
        while self.running:
            try:
                data = self.client_sock.recv(1024)
                if not data: break # 상대방이 연결을 정상적으로 끊음
                
                buffer += data.decode("utf-8")
                while "\n" in buffer:
                    msg, buffer = buffer.split("\n", 1)
                    self.parse(msg)
            except socket.timeout:
                print("[BT] 수신 타임아웃 발생 (연결 확인 중...)")
                continue
            except Exception:
                break # 비정상 종료 시 루프 탈출 -> finally에서 해제
            
    def _parse_value(self, value):
        if isinstance(value, str):
            return None
        if isinstance(value, int):
            if 0 <= value <= 1000:
                return value
            return None
        return None

    def _select_representative(self, a_value, b_value):
        if a_value is not None and b_value is not None:
            return (a_value + b_value) / 2.0
        if a_value is not None:
            return float(a_value)
        if b_value is not None:
            return float(b_value)
        return None

    def parse(self, json_str):
        try:
            data = json.loads(json_str)
        except Exception as e:
            print(f"[Error] 파싱 실패: {e}")
            return

        ex_value = self._parse_value(data.get("ex"))
        sx_value = self._parse_value(data.get("sx"))
        ev_value = self._parse_value(data.get("ev"))
        sv_value = self._parse_value(data.get("sv"))

        xr_1000 = self._select_representative(ex_value, sx_value)
        v_1000 = self._select_representative(ev_value, sv_value)

        self.latest_xr_norm = xr_1000 / 1000.0 if xr_1000 is not None else None
        self.latest_v_norm = v_1000 / 1000.0 if v_1000 is not None else None
        self.last_rx_time = time.monotonic()

    def get_latest_values(self):
        return self.latest_xr_norm, self.latest_v_norm, self.last_rx_time
