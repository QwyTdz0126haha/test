import time
import threading
from mcstatus import JavaServer
import socket

SERVER_ADDRESS = "127.0.0.1"  # Địa chỉ server Minecraft
SERVER_PORT = 25565           # Cổng server Minecraft (mặc định là 25565)
PACKET_COUNT = 50000          # Số lượng gói gửi mỗi vòng
INTERVAL = 180                # Thời gian giữa các lần hỏi (3 phút)
TIMEOUT = 5                   # Thời gian chờ trả lời người dùng (5s)

def send_packets():
    try:
        for i in range(PACKET_COUNT):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            try:
                sock.connect((SERVER_ADDRESS, SERVER_PORT))
                # Gửi dữ liệu thô giả lập (không phải packet Minecraft thật)
                sock.sendall(b"\x00\x00")
            except Exception:
                pass  # Bỏ qua lỗi nếu server không trả lời
            finally:
                sock.close()
    except KeyboardInterrupt:
        print("Dừng gửi packet do KeyboardInterrupt.")

def ask_user_continue():
    choice = input("Bạn có muốn tiếp tục gửi packet? (y/n): ").strip().lower()
    return choice != 'n'

def input_with_timeout(prompt, timeout):
    answer = [None]

    def ask():
        answer[0] = input(prompt)

    t = threading.Thread(target=ask)
    t.daemon = True
    t.start()
    t.join(timeout)
    return answer[0]

def main():
    while True:
        print(f"\n🔁 Đang gửi {PACKET_COUNT} packet tới {SERVER_ADDRESS}:{SERVER_PORT}...")
        send_packets()
        print("✅ Gửi xong. Đợi 3 phút...")

        time.sleep(INTERVAL)

        print("\n⏳ Dừng để hỏi người dùng...")
        response = input_with_timeout("❓ Tiếp tục gửi packet? (y/n): ", TIMEOUT)
        if response is not None and response.strip().lower() == 'n':
            print("🛑 Dừng theo yêu cầu người dùng.")
            break
        else:
            print("⏩ Không có phản hồi hoặc người dùng chọn tiếp tục.")

if __name__ == "__main__":
    main()
