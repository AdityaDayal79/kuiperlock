import random
import struct

# CCSDS primary header is 6 bytes
def random_ccsds_primary_header():
    version = random.randint(0, 7)        # 3 bits
    sc_id = random.randint(0, 1023)       # 10 bits
    pkt_type = random.randint(0, 1)       # 1 bit
    sec_header_flag = random.randint(0, 1)# 1 bit
    apid = random.randint(0, 2047)        # 11 bits
    seq_flags = random.randint(0, 3)      # 2 bits
    pkt_seq_count = random.randint(0, 16383)# 14 bits
    pkt_len = random.randint(0, 65535)    # 16 bits

    # Pack fields into 6 bytes (simplified, not bit-exact)
    header = struct.pack(">HHH",
        (version << 13) | (pkt_type << 12) | (sec_header_flag << 11) | apid,
        (seq_flags << 14) | pkt_seq_count,
        pkt_len
    )
    return header

def fuzz_ccsds_packet():
    header = random_ccsds_primary_header()
    payload = bytes([random.randint(0,255) for _ in range(random.randint(1,32))])
    return header + payload

if __name__ == "__main__":
    with open("fuzzed_ccsds_packets.bin", "wb") as f:
        for i in range(1000):
            pkt = fuzz_ccsds_packet()
            # Optionally, write length of packet before each (for easier parsing)
            f.write(len(pkt).to_bytes(2, 'big'))
            f.write(pkt)
    print("Generated 1000 fuzzed CCSDS packets in fuzzed_ccsds_packets.bin")
