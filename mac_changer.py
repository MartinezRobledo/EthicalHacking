import re #libreria para el uso de expresiones regulares
import subprocess # libreria para ejecutar comandos por consola
import optparse # libreria para tomar argumentos desde consola

def get_arguments():    #funcion para obtener argumentos
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest = "interface", help="Interface para cambiar Direccion MAC")
    parser.add_option("-m", "--mac", dest="new_mac", help="Nueva Direccion MAC")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Por favor indicar una Interfaz, usa --help para mas informacion")
    elif not options.new_mac:
        parser.error("[-] Por favor indicar una direccion MAC, usa --help para mas informacion")
    
    return options

def change_mac(interface, new_mac):
    print("[+] Cambiando direccion MAC para " + interface + " a " + new_mac)

    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])

def main(interface, new_mac):
    ifconfig_initial = subprocess.check_output(["ifconfig", interface])
    ifconfig_initial = str(ifconfig_initial)
    ifconfig_initial = re.search(r'\w\w:\w\w:\w\w:\w\w:\w\w:\w\w', ifconfig_initial).group(0)
    print("Direccion MAC actual " + ifconfig_initial)

    change_mac(interface, new_mac)

    ifconfig_final = subprocess.check_output(["ifconfig", interface])
    ifconfig_final = str(ifconfig_final)
    ifconfig_final = re.search(r'\w\w:\w\w:\w\w:\w\w:\w\w:\w\w', ifconfig_final).group(0)
    
    if ifconfig_initial == ifconfig_final:
        print("[-] No se modifico la direccion MAC") #los resultados se guardan en grupos en caso de haber mas de un resultado por eso se pide el primero
    else:
        print("[+] Se modifico la direccion MAC\nDireccion nueva > " + ifconfig_final)
        


options = get_arguments()

main(options.interface, options.new_mac)