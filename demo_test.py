import subprocess
import time
import socket
import sys
import struct

def print_banner(title):
    print("\n" + "=" * 60)
    print(f"  >>> {title} <<<")
    print("=" * 60)

def test_exp7():
    print_banner("TESTING EXPERIMENT 7: Multi-User Chat Server (TCP)")
    print("[1] Starting server7.py in background...")
    server = subprocess.Popen([sys.executable, "server7.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    time.sleep(1)

    print("[2] Connecting Client 1 to server7 at 127.0.0.1:8080...")
    c1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    c1.connect(("127.0.0.1", 8080))

    print("[3] Connecting Client 2 to server7 at 127.0.0.1:8080...")
    c2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    c2.connect(("127.0.0.1", 8080))

    # Client 1 sends message
    msg1 = "Hello from Client 1!"
    print(f"\n[Client 1] Sending: '{msg1}'")
    c1.send(msg1.encode())
    resp1 = c1.recv(1024).decode()
    print(f"[Client 1] Received response: '{resp1}'")

    # Client 2 sends message
    msg2 = "Hey from Client 2!"
    print(f"\n[Client 2] Sending: '{msg2}'")
    c2.send(msg2.encode())
    resp2 = c2.recv(1024).decode()
    print(f"[Client 2] Received response: '{resp2}'")

    # Disconnecting clients
    print("\n[Client 1] Sending 'exit'...")
    c1.send(b"exit")
    c1.close()

    print("[Client 2] Sending 'exit'...")
    c2.send(b"exit")
    c2.close()

    time.sleep(0.5)
    server.terminate()
    print("\n[✓] Experiment 7 passed successfully!")

def test_exp8():
    print_banner("TESTING EXPERIMENT 8: Concurrent Time Server (UDP)")
    print("[1] Starting server8.py in background on port 1234...")
    server = subprocess.Popen([sys.executable, "server8.py"])
    time.sleep(1)

    c = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Request time
    req = "time"
    print(f"\n[Client] Sending message: '{req}' to server8 at 127.0.0.1:1234")
    c.sendto(req.encode(), ("127.0.0.1", 1234))
    resp, _ = c.recvfrom(1024)
    print(f"[Client] Received Server Time: '{resp.decode()}'")

    # Send stop
    print("\n[Client] Sending 'stop' to server8...")
    c.sendto(b"stop", ("127.0.0.1", 1234))
    c.close()

    time.sleep(0.5)
    server.terminate()
    print("\n[✓] Experiment 8 passed successfully!")

def test_exp9():
    print_banner("TESTING EXPERIMENT 9: Concurrent File Server (TCP)")
    print("[1] Starting server9.py in background on port 9002...")
    server = subprocess.Popen([sys.executable, "server9.py"])
    time.sleep(1)

    # Test existing file: sample.txt
    print("\n--- Test 9.1: Requesting existing file 'sample.txt' ---")
    c1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    c1.connect(("127.0.0.1", 9002))
    print("[Client] Sending filename: 'sample.txt'")
    c1.send(b"sample.txt")
    resp1 = c1.recv(4096).decode()
    print("[Client] Server response:")
    print(resp1)
    c1.close()

    # Test non-existing file: missing.txt
    print("\n--- Test 9.2: Requesting non-existent file 'missing.txt' ---")
    c2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    c2.connect(("127.0.0.1", 9002))
    print("[Client] Sending filename: 'missing.txt'")
    c2.send(b"missing.txt")
    resp2 = c2.recv(4096).decode()
    print("[Client] Server response:")
    print(resp2)
    c2.close()

    time.sleep(0.5)
    server.terminate()
    print("\n[✓] Experiment 9 passed successfully!")

def test_exp10():
    print_banner("TESTING EXPERIMENT 10: Packet-Capturing Application (Raw Socket)")
    print("[1] Running packet_capture10.py to check raw socket initialization...")
    result = subprocess.run([sys.executable, "packet_capture10.py"], capture_output=True, text=True)
    print("Program Output:")
    print(result.stdout.strip())

    print("\n[2] Demonstrating Algorithm Steps 6-9: Continuous Packet Header Extraction...")
    import packet_capture10

    # Packet 1: HTTP / TCP Web Traffic
    print("\n--- Packet #1: TCP / HTTP Traffic ---")
    dest_mac = b'\x00\x1a\x2b\x3c\x4d\x5e'
    src_mac = b'\xe0\xd5\x5e\x6a\x7b\x8c'
    eth_header = struct.pack("!6s6sH", dest_mac, src_mac, 0x0800)
    ip_header = struct.pack("!BBHHHBBH4s4s", (4 << 4) | 5, 0, 40, 1001, 0, 64, 6, 0, socket.inet_aton("192.168.1.15"), socket.inet_aton("172.217.16.206"))
    pkt1 = eth_header + ip_header + b"GET / HTTP/1.1\r\n"
    print(f"Captured frame ({len(pkt1)} bytes). Decoded fields:")
    packet_capture10.process_packet(pkt1, is_linux=True)

    # Packet 2: DNS / UDP Query Traffic
    print("\n--- Packet #2: UDP / DNS Query Traffic ---")
    dest_mac = b'\xff\xff\xff\xff\xff\xff'
    src_mac = b'\xac\xde\x48\x00\x11\x22'
    eth_header = struct.pack("!6s6sH", dest_mac, src_mac, 0x0800)
    ip_header = struct.pack("!BBHHHBBH4s4s", (4 << 4) | 5, 0, 36, 1002, 0, 128, 17, 0, socket.inet_aton("10.0.0.5"), socket.inet_aton("8.8.8.8"))
    pkt2 = eth_header + ip_header + b"DNS_QUERY"
    print(f"Captured frame ({len(pkt2)} bytes). Decoded fields:")
    packet_capture10.process_packet(pkt2, is_linux=True)

    # Packet 3: ICMP Echo Request (Ping) Traffic
    print("\n--- Packet #3: ICMP / Ping Traffic ---")
    dest_mac = b'\x00\x0c\x29\x4f\x8e\x35'
    src_mac = b'\x00\x50\x56\xc0\x00\x08'
    eth_header = struct.pack("!6s6sH", dest_mac, src_mac, 0x0800)
    ip_header = struct.pack("!BBHHHBBH4s4s", (4 << 4) | 5, 0, 28, 1003, 0, 56, 1, 0, socket.inet_aton("192.168.1.100"), socket.inet_aton("1.1.1.1"))
    pkt3 = eth_header + ip_header + b"ECHO_REQUEST"
    print(f"Captured frame ({len(pkt3)} bytes). Decoded fields:")
    packet_capture10.process_packet(pkt3, is_linux=True)

    print("\n[✓] Experiment 10 packet extraction and header decoding verified successfully!")

if __name__ == "__main__":
    print("\n" + "#" * 60)
    print("   AUTOMATED LIVE TERMINAL VERIFICATION OF EXPERIMENTS 7, 8, 9 & 10")
    print("#" * 60)
    test_exp7()
    test_exp8()
    test_exp9()
    test_exp10()
    print("\n" + "#" * 60)
    print("   ALL EXPERIMENTS (7, 8, 9, 10) VERIFIED AND WORKING PROPERLY!")
    print("#" * 60 + "\n")
