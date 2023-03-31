from scapy.all import ARP, Ether, srp
import mysql.connector

# Definir la dirección IP y la máscara de red
ip = "192.168.88.0/22"

# Crear una solicitud ARP para cada dirección IP en la red
arp = ARP(pdst=ip)

# Crear una trama Ethernet para encapsular las solicitudes ARP
ether = Ether(dst="ff:ff:ff:ff:ff:ff")
x
packet = ether / arp

result = srp(packet, timeout=6, verbose=0)[0]

# Crear una conexión a la base de datos
conexion = mysql.connector.connect(
    host='localhost',
    user='root',
    password='pepedrako123',
    database='cliente'
)

# Crear un cursor para ejecutar las consultas SQL
cursor = conexion.cursor()

clientes = []

for enviado, recibido in result:
    clientes.append({recibido.psrc, recibido.hwsrc})
    
    # Insertar la dirección IP encontrada en la base de datos
    ip_address = recibido.psrc
    insert_query = "INSERT INTO cliente.ip_addresses (ip) VALUES (%s)"
    insert_values = (ip_address,)
    cursor.execute(insert_query, insert_values)
    conexion.commit()

for sent, received in result:
    print(f"IP: {received.psrc} - MAC: {received.hwsrc}")
    
# Cerrar la conexión a la base de datos
conexion.close()
