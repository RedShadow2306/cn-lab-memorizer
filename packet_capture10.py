import socket
import struct
import sys

def format_mac(bytes_addr):
    return ':'.join(f'{b:02x}' for b in bytes_addr)

def process_packet(raw_data, is_linux=True):
    if is_linux:
        eth_header = raw_data[:14]
        dest_mac, src_mac, eth_proto = struct.unpack("!6s6sH", eth_header)
        print("Ethernet Header:")
        print(f"  Destination MAC: {format_mac(dest_mac)}")
        print(f"  Source MAC:      {format_mac(src_mac)}")
        print(f"  Protocol Type:   {hex(eth_proto)}")

        if eth_proto != 0x0800:
            print("  Non-IPv4 packet.")
            print("---------------------------------------------------")
            return
        ip_data = raw_data[14:]
    else:
        ip_data = raw_data

    ip_header = ip_data[:20]
    iph = struct.unpack("!BBHHHBBH4s4s", ip_header)

    version_ihl = iph[0]
    version = version_ihl >> 4
    ihl = (version_ihl & 0xF) * 4
    ttl = iph[5]
    protocol = iph[6]
    src_addr = socket.inet_ntoa(iph[8])
    dst_addr = socket.inet_ntoa(iph[9])

    protocol_names = {1: "ICMP", 6: "TCP", 17: "UDP"}
    proto_name = protocol_names.get(protocol, f"Unknown ({protocol})")

    print("IP Header:")
    print(f"  Version:         IPv{version}")
    print(f"  Header Length:   {ihl} bytes")
    print(f"  TTL:             {ttl}")
    print(f"  Source IP:       {src_addr}")
    print(f"  Destination IP:  {dst_addr}")
    print(f"  Protocol Number: {protocol} ({proto_name})")
    print("---------------------------------------------------")

def main():
    print("===================================================")
    print("      Packet-Capturing Application (Raw Socket)    ")
    print("===================================================")

    is_linux = hasattr(socket, 'AF_PACKET')

    try:
        if is_linux:
            raw_socket = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0003))
        else:
            host = socket.gethostbyname(socket.gethostname())
            raw_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
            raw_socket.bind((host, 0))
            raw_socket.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
            raw_socket.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
            print(f"Bound to local host IP: {host}")
    except PermissionError:
        print("Error: Administrative / root privileges required to create raw socket.")
        print("Run as Administrator (Windows) or use 'sudo' (Linux).")
        sys.exit(1)
    except Exception as e:
        print(f"Error creating raw socket: {e}")
        sys.exit(1)

    print("Packet Capturing Started... Press Ctrl+C to stop.")
    print("---------------------------------------------------")

    packet_count = 0
    try:
        while True:
            raw_data, _ = raw_socket.recvfrom(65535)
            packet_count += 1
            print(f"\n[Packet #{packet_count} - Length: {len(raw_data)} bytes]")
            process_packet(raw_data, is_linux=is_linux)

    except KeyboardInterrupt:
        print("\nPacket capturing stopped.")
    finally:
        if not is_linux and 'raw_socket' in locals():
            try:
                raw_socket.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
            except Exception:
                pass
        raw_socket.close()
        print("Socket closed. Program terminated.")

if __name__ == "__main__":
    main()
