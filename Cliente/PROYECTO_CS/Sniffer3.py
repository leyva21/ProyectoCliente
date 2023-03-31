from scapy.all import *
import mysql.connector

# Conectar a la base de datos
conn = mysql.connector.connect(
    user='root',
    password='pepedrako123',
    host='localhost',
    database='cliente'
)
cursor = conn.cursor()

# Crear la tabla para almacenar los datos de tráfico
cursor.execute("CREATE TABLE IF NOT EXISTS traffic_data (ip VARCHAR(255), upload_count BIGINT, download_count BIGINT, timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")

# Obtener todas las direcciones IP de la tabla ip_addresses
cursor.execute("SELECT ip FROM cliente.ip_addresses") 
results = cursor.fetchall()

# Iterar sobre los resultados y detectar el tráfico para cada dirección IP
for result in results:
    ip_to_detect = result[0]
    print(f"Detectando el tráfico de la dirección IP {ip_to_detect}.")

    # Inicializar las variables para el conteo de datos y el contador de paquetes
    upload_count = 0
    download_count = 0
    packet_count = 0
    count = 0

    # Configurar el número de veces que se debe imprimir el conteo de datos
    max_print_count = 1
    print_count = 0

    # Configurar el número de veces que se debe detectar el tráfico
    max_packet_count = 1

    # Función para procesar cada paquete
    def process_packet(packet):
        global upload_count, download_count, packet_count, print_count

        # Verificar si el paquete tiene capa IP
        if IP in packet:
            # Obtener la dirección IP origen y destino del paquete
            src_ip = packet[IP].src
            dst_ip = packet[IP].dst

            # Verificar si la dirección IP del paquete coincide con la dirección IP a detectar
            if src_ip == ip_to_detect:
                upload_count += len(packet)
            elif dst_ip == ip_to_detect:
                download_count += len(packet)

            packet_count += 1

        # Insertar los datos en la tabla traffic_data
            query = "INSERT INTO traffic_data (ip, upload_count, download_count) VALUES (%s, %s, %s)"
            values = (ip_to_detect, upload_count, download_count)
            cursor.execute(query, values)
            conn.commit()

        # Imprimir el conteo de datos cada cierto número de paquetes
        if packet_count >= 100:
            print(f"Subida: {upload_count} bytes, Bajada: {download_count} bytes")
            upload_count = 0
            download_count = 0
            packet_count = 0
            print_count += 1

            if print_count >= max_print_count:
                # Detener la captura de paquetes después de imprimir el conteo de datos un número determinado de veces
                raise KeyboardInterrupt
            

        # Detener la captura de paquetes después de un número determinado de paquetes
        if packet_count >= 100 or print_count >= max_print_count or packet_count >= max_packet_count * 100:
            raise KeyboardInterrupt

    # Configurar la captura de paquetes
    try:
        sniff(filter=f"host {ip_to_detect}", prn=process_packet, store=0)
    except KeyboardInterrupt:
        print(f"Deteniendo la detección del tráfico para la dirección IP {ip_to_detect}.")
