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
    print(scapy_packet.show())
    packet.accept()

queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()