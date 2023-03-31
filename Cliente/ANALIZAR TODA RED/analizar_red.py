from scapy.all import ARP, Ether, srp

# Definir la dirección IP y la máscara de red
ip = "192.168.100.4/24"

# Crear una solicitud ARP para cada dirección IP en la red
arp = ARP(pdst=ip)

# Crear una trama Ethernet para encapsular las solicitudes ARP
ether = Ether(dst="ff:ff:ff:ff:ff:ff")

packet = ether / arp

result = srp(packet, timeout=6, verbose=0)[0]

clientes = []

for enviado, recibido in result:
    clientes.append({recibido.psrc, recibido.hwsrc})

for sent, received in result:
    print(f"IP: {received.psrc} - MAC: {received.hwsrc}")

