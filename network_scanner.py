import scapy.all as scapy

def scan(ip):
    #ARP convierte dinámicamente las direcciones de Internet en las 
    # irecciones de hardware exclusivas de las redes de área local.
    arp_request = scapy.ARP(pdst=ip)   #Se obtienen direcciones ip
    #el broadcast es una conexión multipunto, que permite enviar un paquete de datos 
    # desde un punto a todos los usuarios en una red de mensajes
    broadcast = scapy.Ether(dst='ff:ff:ff:ff:ff:ff')    #Se obtienen direcciones mac
    
    arp_request_broadcast = broadcast/arp_request #se concatenan

    answered_list, unanswered_list= scapy.srp(arp_request_broadcast, timeout=1, verbose=False) #se obtienen paquetes de las direcciones dadas, [0] indica que se tienen en cuenta solo los paquetes respondidos y no todos
    #la funcion srp pasa por toda la subnet preguntando a cada ip quien tiene dicha ip
    # devuelve dos objetos answered y unanswered

    clientes_list = []

    for element in answered_list:
        client_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc}
        #psrc contiene la ip, hwsrc contiene la mac
        #agregamos a la lista de clientes el diccionario de cliente
        clientes_list.append(client_dict)

    return clientes_list


def print_result(results_list):
    print("IP\t\t\tMAC adress\n----------------------------------")
    for client in results_list:
        print(client["ip"] + "\t\t" + client["mac"])


scan_result = scan("192.168.0.1/24")    #se envia puerta de enlace y /24 para indicar todas las ip
print_result(scan_result)