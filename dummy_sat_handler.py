def parse_ccsds_header(packet: bytes):
    if len(packet) < 6:
        return False, "Too short for CCSDS header"
    try:
        word1 = int.from_bytes(packet[0:2], 'big')
        word2 = int.from_bytes(packet[2:4], 'big')
        pkt_len = int.from_bytes(packet[4:6], 'big')
    except Exception as e:
        return False, f"Header unpack error: {e}"
    version = (word1 >> 13) & 0x7
    apid = word1 & 0x7FF
    seq_flags = (word2 >> 14) & 0x3
    pkt_seq_count = word2 & 0x3FFF
    if version > 7:
        return False, "Invalid CCSDS version"
    if apid > 2047:
        return False, "Invalid APID"
    if pkt_len > 1024:  # Arbitrary cutoff
        return False, "Packet length too large"
    return True, "OK"

def read_packets_from_binary(filename):
    packets = []
    with open(filename, "rb") as f:
        while True:
            len_bytes = f.read(2)
            if not len_bytes or len(len_bytes) < 2:
                break
            pkt_len = int.from_bytes(len_bytes, 'big')
            pkt = f.read(pkt_len)
            if len(pkt) < pkt_len:
                break
            packets.append(pkt)
    return packets

def handle_packet(packet: bytes):
    valid, reason = parse_ccsds_header(packet)
    if valid:
        print("Accepted:", packet.hex(), "-", reason)
    else:
        print("Rejected:", packet.hex(), "-", reason)

if __name__ == "__main__":
    packets = read_packets_from_binary("fuzzed_ccsds_packets.bin")
    for pkt in packets:
        handle_packet(pkt)
